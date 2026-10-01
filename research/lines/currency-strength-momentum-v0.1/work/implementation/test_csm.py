"""Synthetic-only tests. No exchange-rate history or strategy outcomes are read."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import io
import json
import os
import random
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

import csm


HERE = Path(__file__).parent
FIXTURE = json.loads((HERE / "fixtures" / "toy_cases.json").read_text(encoding="utf-8"))
VALID_STATUS = {"valid": ["A"], "missing": ["M"]}
UNIT_BY_CURRENCY = {currency: "units_per_EUR" for currency in csm.NON_EUR_CURRENCIES}


def vector(values: dict[str, str] | None = None) -> dict[str, Decimal]:
    result = {currency: Decimal("1") for currency in csm.CURRENCIES}
    for currency, value in (values or {}).items():
        result[currency] = Decimal(value)
    return result


def valid_rows(day: str = "2020-01-31") -> list[dict[str, str]]:
    return [
        {"date": day, "currency": currency, "obs_value": str(Decimal("1") + Decimal(i) / 100),
         "unit": UNIT_BY_CURRENCY[currency], "status": "A", "available_at": "UNKNOWN"}
        for i, currency in enumerate(csm.NON_EUR_CURRENCIES, start=1)
    ]


def table_from_vectors(by_date: dict[str, dict[str, Decimal]]) -> csm.QuoteTable:
    parsed_dates = {date.fromisoformat(key): value for key, value in by_date.items()}
    return csm.QuoteTable(values=parsed_dates, statuses={}, row_dates=frozenset(parsed_dates))


def generated_vector(index: int) -> dict[str, Decimal]:
    result: dict[str, Decimal] = {}
    for position, currency in enumerate(csm.CURRENCIES):
        if currency == "EUR":
            result[currency] = Decimal("1")
        else:
            result[currency] = Decimal("1") + Decimal(index * (position + 1)) / Decimal("1000")
    return result


def synthetic_table(month_ends: dict[str, str], *, omit: set[str] | None = None,
                    remove_currency: tuple[str, str] | None = None,
                    add_neighbor: tuple[str, dict[str, Decimal]] | None = None) -> csm.QuoteTable:
    omit = omit or set()
    values: dict[str, dict[str, Decimal]] = {}
    for index, month in enumerate(sorted(month_ends)):
        day = month_ends[month]
        if day in omit:
            continue
        prices = generated_vector(index + 1)
        if remove_currency and remove_currency[0] == day:
            prices.pop(remove_currency[1])
        values[day] = prices
    if add_neighbor:
        values[add_neighbor[0]] = add_neighbor[1]
    return table_from_vectors(values)


def dates_for_small_grid() -> dict[str, str]:
    # All values below are synthetic; the production calendar comes from C's
    # official calendar artifact and is intentionally not reproduced here.
    return {
        "2019-11": "2019-11-29",
        "2019-12": "2019-12-31",
        "2020-01": "2020-01-31",
        "2020-02": "2020-02-28",
        "2020-03": "2020-03-31",
    }


class ParseAndIdentityTests(unittest.TestCase):
    def test_parse_decimal_and_quote_rows(self) -> None:
        self.assertEqual(csm.parse_decimal("1.234"), Decimal("1.234"))
        table = csm.parse_quote_rows(valid_rows(), status_policy=VALID_STATUS,
                                     unit_by_currency=UNIT_BY_CURRENCY)
        self.assertEqual(len(table.values[date(2020, 1, 31)]), 7)
        self.assertEqual(csm.price_vector(table, date(2020, 1, 31))["EUR"], Decimal(1))

    def test_rejects_nonfinite_nonpositive_and_bad_decimal(self) -> None:
        for value in ("NaN", "Infinity", "0", "-0.1", "not-a-number"):
            with self.subTest(value=value), self.assertRaises(csm.DataError):
                csm.parse_decimal(value)
        with self.assertRaisesRegex(csm.DataError, "decimal text"):
            csm.parse_decimal(0.1)

    def test_rejects_duplicate_date_currency_and_unordered_dates(self) -> None:
        rows = valid_rows()
        with self.assertRaisesRegex(csm.DataError, "duplicate"):
            csm.parse_quote_rows(rows + [rows[0]], status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)
        out_of_order = valid_rows("2020-01-31") + valid_rows("2020-01-30")
        with self.assertRaisesRegex(csm.DataError, "ordered"):
            csm.parse_quote_rows(out_of_order, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)

    def test_rejects_wrong_unit_unknown_status_and_missing_value_conflict(self) -> None:
        rows = valid_rows()
        rows[0]["unit"] = "wrong-unit"
        with self.assertRaisesRegex(csm.DataError, "unit"):
            csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)
        rows = valid_rows()
        rows[0]["status"] = "?"
        with self.assertRaisesRegex(csm.DataError, "status"):
            csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)
        rows = valid_rows()
        rows[0]["status"] = "M"
        with self.assertRaisesRegex(csm.DataError, "unexpectedly contains"):
            csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)

    def test_rejects_external_eur_quote_and_fake_available_at(self) -> None:
        rows = valid_rows()
        rows[0]["available_at"] = "2020-01-31T16:00:00+01:00"
        with self.assertRaisesRegex(csm.DataError, "AVAILABLE_AT"):
            csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)
        rows = valid_rows()
        rows.append({"date": "2020-01-31", "currency": "EUR", "obs_value": "1",
                     "unit": "units_per_EUR", "status": "A"})
        with self.assertRaisesRegex(csm.DataError, "EUR is synthetic"):
            csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                 unit_by_currency=UNIT_BY_CURRENCY)

    def test_missing_status_is_preserved_as_missing(self) -> None:
        rows = valid_rows()
        rows[0]["status"] = "M"
        rows[0]["obs_value"] = ""
        table = csm.parse_quote_rows(rows, status_policy=VALID_STATUS,
                                     unit_by_currency=UNIT_BY_CURRENCY)
        self.assertNotIn("AUD", table.values[date(2020, 1, 31)])
        self.assertEqual(table.statuses[date(2020, 1, 31)]["AUD"], "M")

    def test_rejects_snapshot_rows_outside_the_fixed_source_range(self) -> None:
        table = csm.parse_quote_rows(valid_rows("2026-10-01"), status_policy=VALID_STATUS,
                                     unit_by_currency=UNIT_BY_CURRENCY)
        with self.assertRaisesRegex(csm.DataError, "outside the fixed contract range"):
            csm.validate_observed_date_bounds(table)

    def test_source_lock_requires_exact_series_identity(self) -> None:
        lock = synthetic_source_lock()
        csm.validate_series_identity(lock)
        lock["series_by_currency"]["USD"] = "D.USD.EUR.BAD.A"
        with self.assertRaisesRegex(csm.GateError, "series identity"):
            csm.validate_series_identity(lock)

    def test_csv_adapter_uses_only_source_lock_column_and_series_mapping(self) -> None:
        lock = synthetic_source_lock()
        lines = ["TIME_PERIOD,SERIES_KEY,OBS_VALUE,UNIT,OBS_STATUS"]
        for index, currency in enumerate(csm.NON_EUR_CURRENCIES, start=1):
            lines.append(
                f"2020-01-31,{lock['series_by_currency'][currency]},{1 + index / 100},units_per_EUR,A"
            )
        table = csm.parse_source_csv("\n".join(lines).encode(), lock)
        vector_at_date = csm.price_vector(table, date(2020, 1, 31))
        self.assertEqual(vector_at_date["EUR"], Decimal(1))
        self.assertIn("USD", vector_at_date)


class FormulaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old = {k: Decimal(v) for k, v in FIXTURE["old"].items()}
        self.formation = {k: Decimal(v) for k, v in FIXTURE["formation_end"].items()}
        self.target = {k: Decimal(v) for k, v in FIXTURE["target_end"].items()}

    def test_eur_constant_usd_included_and_exact_extrema(self) -> None:
        selected = csm.select_extrema(self.old, self.formation)
        self.assertEqual(selected.status, "UNIQUE_EXTREMA")
        self.assertEqual(selected.winner, FIXTURE["expected_winner"])
        self.assertEqual(selected.loser, FIXTURE["expected_loser"])
        self.assertIn("USD", selected.exact_growth_ratios)
        self.assertEqual(selected.exact_growth_ratios["EUR"], 1)

    def test_all_56_directed_max_matches_unique_raw_max_minus_min(self) -> None:
        selected = csm.select_extrema(self.old, self.formation)
        maximum, pairs = csm.max_directed_pair(self.old, self.formation)
        self.assertEqual(pairs, ((selected.winner, selected.loser),))
        self.assertEqual(maximum, selected.exact_growth_ratios[selected.winner]
                         / selected.exact_growth_ratios[selected.loser])

    def test_numeraire_invariance(self) -> None:
        original = csm.select_extrema(self.old, self.formation)
        old_cross = csm.cross_quote_vector(self.old, "CAD")
        formation_cross = csm.cross_quote_vector(self.formation, "CAD")
        changed = csm.select_extrema(old_cross, formation_cross)
        self.assertEqual((changed.winner, changed.loser), (original.winner, original.loser))
        transformed_ratios = csm.exact_growth_ratios(old_cross, formation_cross)
        common = original.exact_growth_ratios["CAD"]
        for currency in csm.CURRENCIES:
            self.assertEqual(transformed_ratios[currency], original.exact_growth_ratios[currency] / common)

    def test_eur_can_be_winner_or_loser(self) -> None:
        eur_wins = vector({"AUD": "1.4", "CAD": "1.1", "CHF": "1.12", "GBP": "1.15",
                           "JPY": "1.18", "NZD": "1.2", "USD": "1.25"})
        eur_loses = vector({"AUD": "0.9", "CAD": "0.92", "CHF": "0.94", "GBP": "0.96",
                            "JPY": "0.98", "NZD": "0.97", "USD": "0.5"})
        self.assertEqual(csm.select_extrema(self.old, eur_wins).winner, "EUR")
        self.assertEqual(csm.select_extrema(self.old, eur_loses).loser, "EUR")

    def test_usd_can_be_winner_or_loser(self) -> None:
        usd_wins = vector({"AUD": "1.2", "CAD": "1.1", "CHF": "1.08", "GBP": "1.04",
                           "JPY": "1.03", "NZD": "1.02", "USD": "0.5"})
        usd_loses = vector({"AUD": "0.5", "CAD": "0.8", "CHF": "0.85", "GBP": "0.9",
                            "JPY": "0.95", "NZD": "0.92", "USD": "1.5"})
        self.assertEqual(csm.select_extrema(self.old, usd_wins).winner, "USD")
        self.assertEqual(csm.select_extrema(self.old, usd_loses).loser, "USD")

    def test_exact_decimal_ratio_tie_is_not_broken_by_float_rounding(self) -> None:
        tied = vector({"USD": "0.8", "GBP": "0.80", "AUD": "1.2"})
        selected = csm.select_extrema(self.old, tied)
        self.assertEqual(selected.status, "TIED_EXTREME")
        self.assertIsNone(selected.winner)
        self.assertIsNone(selected.loser)
        self.assertEqual(selected.exact_growth_ratios["USD"], selected.exact_growth_ratios["GBP"])

    def test_quote_direction_and_simple_return_difference_bug(self) -> None:
        target = vector({"USD": "0.9", "AUD": "1.1"})
        log_return = csm.pair_log_return("USD", "AUD", self.old, target)
        expected_pair = (target["AUD"] / target["USD"]) / (self.old["AUD"] / self.old["USD"])
        self.assertAlmostEqual(float(log_return.exp() - 1), float(expected_pair - 1), places=12)
        r_usd = self.old["USD"] / target["USD"] - 1
        r_aud = self.old["AUD"] / target["AUD"] - 1
        wrong_difference = r_usd - r_aud
        correct_pair_simple = log_return.exp() - 1
        self.assertNotEqual(wrong_difference, correct_pair_simple)

    def test_28_canonical_long_directions_need_not_contain_56_way_winner(self) -> None:
        selected = csm.select_extrema(self.old, self.formation)
        order = {currency: index for index, currency in enumerate(csm.CURRENCIES)}
        long_only_directions = {
            (left, right) for left in csm.CURRENCIES for right in csm.CURRENCIES
            if left != right and order[left] < order[right]
        }
        self.assertEqual(len(long_only_directions), 28)
        self.assertNotIn((selected.winner, selected.loser), long_only_directions)

    def test_equal_pair_average_preserves_complete_network_rank(self) -> None:
        selected = csm.select_extrema(self.old, self.formation)
        average_scores = csm.equal_pair_average_log_strength(self.old, self.formation)
        ratio_order = sorted(csm.CURRENCIES, key=selected.exact_growth_ratios.get)
        average_order = sorted(csm.CURRENCIES, key=average_scores.get)
        self.assertEqual(ratio_order, average_order)


class CalendarAndLeakageTests(unittest.TestCase):
    def test_year_boundary_and_expected_calendar_endpoints_are_used(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(
            calendar,
            add_neighbor=("2020-02-29", vector({"USD": "0.01", "AUD": "25"})),
        )
        events = csm.build_signal_events(("2020-01",), calendar, table)
        event = events[0]
        self.assertEqual(event.formation_start_date, "2019-11-29")
        self.assertEqual(event.formation_end_date, "2019-12-31")
        self.assertEqual(event.target_end_date, "2020-01-31")
        february = csm.build_signal_events(("2020-02",), calendar, table)[0]
        self.assertEqual(february.target_end_date, "2020-02-28")

    def test_whole_missing_month_is_recorded_without_compressing_grid(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar, omit={calendar["2019-11"]})
        months = ("2020-01", "2020-02", "2020-03")
        events = csm.build_signal_events(months, calendar, table)
        self.assertEqual(len(events), 3)
        self.assertEqual([e.target_month for e in events], list(months))
        self.assertIn("WHOLE_MISSING_MONTH:2019-11", events[0].skip_reason or "")

    def test_one_currency_missing_at_endpoint_is_skip_not_rollback(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar, remove_currency=(calendar["2020-01"], "USD"))
        event = csm.build_signal_events(("2020-01",), calendar, table)[0]
        self.assertEqual(event.status, "SKIP")
        self.assertIn("MISSING_CURRENCY:USD@2020-01", event.skip_reason or "")

    def test_missing_expected_target_endpoint_does_not_use_prior_day_or_shift(self) -> None:
        calendar = dates_for_small_grid()
        prior = vector({"USD": "0.997", "AUD": "1.003"})
        table = synthetic_table(calendar, omit={calendar["2020-02"]},
                                add_neighbor=("2020-02-27", prior))
        months = ("2020-01", "2020-02", "2020-03")
        events = csm.build_signal_events(months, calendar, table)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[1].target_month, "2020-02")
        self.assertIn("MISSING_EXPECTED_ENDPOINT:2020-02@2020-02-28", events[1].skip_reason or "")
        self.assertEqual(events[2].target_month, "2020-03")
        self.assertIn("MISSING_EXPECTED_ENDPOINT:2020-02@2020-02-28", events[2].skip_reason or "")

    def test_missing_calendar_endpoint_is_not_inferred_from_prices(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar)
        incomplete = dict(calendar)
        del incomplete["2020-01"]
        event = csm.build_signal_events(("2020-01",), incomplete, table)[0]
        self.assertEqual(event.status, "SKIP")
        self.assertIn("NO_EXPECTED_ENDPOINT:2020-01", event.skip_reason or "")

    def test_prefix_truncation_and_future_perturbation_preserve_past_signal(self) -> None:
        calendar = dates_for_small_grid()
        full_table = synthetic_table(calendar)
        full_events = csm.build_signal_events(("2020-01", "2020-02", "2020-03"), calendar, full_table)
        truncated_calendar = dict(calendar)
        truncated_table = synthetic_table(calendar, omit={calendar["2020-01"]})
        truncated = csm.build_signal_events(("2020-01",), truncated_calendar, truncated_table)[0]
        self.assertEqual((full_events[0].winner, full_events[0].loser),
                         (truncated.winner, truncated.loser))

        perturbed_vectors = {
            day: dict(prices) for day, prices in full_table.values.items()
        }
        future_date = date.fromisoformat(calendar["2020-03"])
        perturbed_vectors[future_date] = vector({"USD": "0.01", "EUR": "1", "AUD": "25"})
        perturbed = csm.build_signal_events(
            ("2020-01", "2020-02", "2020-03"), calendar,
            csm.QuoteTable(perturbed_vectors, {}, full_table.row_dates),
        )
        for index in (0, 1):
            self.assertEqual((full_events[index].winner, full_events[index].loser),
                             (perturbed[index].winner, perturbed[index].loser))

    def test_shared_boundary_is_reference_association_not_entry_claim(self) -> None:
        receipt = {"temporal_claim": "REFERENCE_ASSOCIATION_ONLY", "available_at": "UNKNOWN",
                   "reference_timestamp": "2020-01-31T00:00:00Z", "executable_claim": False}
        csm.validate_temporal_receipt(receipt)
        with self.assertRaisesRegex(csm.GateError, "AVAILABLE_AT"):
            csm.validate_temporal_receipt({**receipt, "available_at": "2020-01-31T00:00:00Z"})
        with self.assertRaisesRegex(csm.GateError, "executable"):
            csm.validate_temporal_receipt({**receipt, "executable_claim": True})

    def test_fixed_full_grid_has_partial_final_year_and_no_shift(self) -> None:
        months = csm.month_range(csm.TARGET_START, csm.TARGET_END)
        self.assertEqual(months[0], "2010-01")
        self.assertEqual(months[-1], "2026-09")
        self.assertEqual(len(months), 201)
        self.assertEqual(sum(month.startswith("2026-") for month in months), 9)
        self.assertEqual(csm.month_shift("2020-01", -1), "2019-12")


class MetricsAndBootstrapTests(unittest.TestCase):
    def test_type7_percentile_linear_interpolation(self) -> None:
        sample = [Decimal(1), Decimal(2), Decimal(4), Decimal(8)]
        self.assertEqual(csm.percentile_type7(sample, Decimal("0.5")), Decimal(3))
        self.assertEqual(csm.percentile_type7(sample, Decimal("0.25")), Decimal("1.75"))

    def test_circular_resample_keeps_calendar_length_and_missing_slot(self) -> None:
        grid = (Decimal(1), None)
        sample = csm.circular_resample_grid(grid, random.Random(0))
        self.assertEqual(len(sample), len(grid))
        self.assertEqual(sample.count(None), 1)

    def test_fixed_seed_bootstrap_is_reproducible_with_missing_slots(self) -> None:
        grid = tuple(Decimal(i - 10) / Decimal(10) if i not in (4, 17) else None
                     for i in range(24))
        first = csm.moving_block_bootstrap(grid)
        second = csm.moving_block_bootstrap(grid)
        self.assertEqual(first, second)
        self.assertEqual(first.valid_replicates, 10_000)
        self.assertEqual(first.block_length, 12)
        self.assertEqual(first.seed, 20_261_001)

    def test_any_zero_valid_replicate_fails_closed(self) -> None:
        with self.assertRaisesRegex(csm.DataError, "zero valid"):
            csm.moving_block_bootstrap((None,) * 24)

    def test_sufficiency_and_decision_boundaries(self) -> None:
        insufficient_n = csm.classify_result(mean_bps=Decimal(10), lower_95_bps=Decimal(5),
                                              eligible_count=119, scheduled_count=150)
        insufficient_coverage = csm.classify_result(mean_bps=Decimal(10), lower_95_bps=Decimal(5),
                                                     eligible_count=120, scheduled_count=151)
        supported = csm.classify_result(mean_bps=Decimal(10), lower_95_bps=Decimal("0.01"),
                                        eligible_count=120, scheduled_count=150)
        nonpositive = csm.classify_result(mean_bps=Decimal(0), lower_95_bps=Decimal(-1),
                                          eligible_count=120, scheduled_count=150)
        interval_includes_zero = csm.classify_result(mean_bps=Decimal(1), lower_95_bps=Decimal(0),
                                                      eligible_count=120, scheduled_count=150)
        self.assertEqual(insufficient_n, ("INSUFFICIENT_EVIDENCE", "HOLD"))
        self.assertEqual(insufficient_coverage, ("INSUFFICIENT_EVIDENCE", "HOLD"))
        self.assertEqual(supported, ("PROMISING_EXPLORATORY",
                                    "ADVANCE_TO_SEPARATE_ECONOMIC_SCREEN_DESIGN"))
        self.assertEqual(nonpositive, ("NOT_SUPPORTED", "DEPRIORITIZE"))
        self.assertEqual(interval_includes_zero, ("INCONCLUSIVE", "HOLD"))

    def test_metrics_keep_schedule_count_and_skip_reasons(self) -> None:
        events = (
            csm.SignalEvent("2020-01", "2019-11", "2019-12", "2020-01", None, None,
                            None, None, None, "SKIP", "WHOLE_MISSING_MONTH:2019-11"),
            csm.SignalEvent("2020-02", "2019-12", "2020-01", "2020-02", None, None,
                            None, "USD", "AUD", "READY", None),
        )
        metrics = csm.summarize_metrics((None, Decimal("0.001")), events)
        self.assertEqual(metrics.scheduled_count, 2)
        self.assertEqual(metrics.eligible_count, 1)
        self.assertEqual(metrics.skip_reasons["WHOLE_MISSING_MONTH:2019-11"], 1)
        self.assertEqual(metrics.mean_bps, Decimal(10))


class GateAndReceiptTests(unittest.TestCase):
    def test_config_is_single_proposed_spec_and_rejects_drift(self) -> None:
        config = json.loads(csm.CONFIG_PATH.read_text(encoding="utf-8"))
        csm.validate_config(config)
        changed = dict(config)
        changed["target_end"] = "2026-10"
        with self.assertRaisesRegex(csm.GateError, "target_end"):
            csm.validate_config(changed)

    def test_gate_closed_and_no_access_cli_does_not_read_outcome_file_or_emit_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lock_path = root / "source-lock.json"
            metadata_path = root / "probe-metadata.json"
            gate_path = root / "gate.json"
            csv_path = root / "input.csv"
            calendar_path = root / "calendar.json"
            manifest_path = root / "manifest.json"
            output_path = root / "output"
            lock = synthetic_source_lock()
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            metadata_path.write_text("{}", encoding="utf-8")
            gate_path.write_text(json.dumps({"gate_status": "CLOSED"}), encoding="utf-8")
            csv_path.write_text("VERY_DISTINCT_SYNTHETIC_VALUE_987654321", encoding="utf-8")
            calendar_path.write_text("{}", encoding="utf-8")
            manifest_path.write_text("{}", encoding="utf-8")
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                status = csm.cli(["run", "--source-csv", str(csv_path), "--source-lock", str(lock_path),
                                  "--probe-metadata", str(metadata_path),
                                  "--expected-calendar", str(calendar_path), "--capture-manifest", str(manifest_path),
                                  "--gate-receipt", str(gate_path), "--output-dir", str(output_path)])
            self.assertEqual(status, 2)
            self.assertIn("GateError", stderr.getvalue())
            self.assertNotIn("987654321", stdout.getvalue() + stderr.getvalue())
            self.assertFalse(output_path.exists())

    def test_capture_preflight_hash_and_identity(self) -> None:
        lock = synthetic_source_lock()
        raw = b"synthetic bytes only"
        manifest = {
            "capture_status": "CAPTURED",
            "source_lock_id": lock["id"],
            "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(lock)),
            "spec_id": csm.SPEC_ID,
            "data_role": "EXPLORATORY_DISCOVERY",
            "requested_start": "2009-11-01",
            "requested_end": "2026-09-30",
            "raw_snapshot_sha256": csm.sha256_bytes(raw),
            "source_series_keys": list(csm.EXPECTED_SERIES_BY_CURRENCY.values()),
            "access_ledger_id": "SYNTHETIC-LEDGER",
            "retrieval_timestamp": "2020-01-01T00:00:00Z",
            "snapshot_uri": "SYNTHETIC",
            "identity_check": "PASS",
        }
        csm.validate_capture_manifest(manifest, raw, lock)
        manifest["raw_snapshot_sha256"] = "0" * 64
        with self.assertRaisesRegex(csm.GateError, "hash mismatch"):
            csm.validate_capture_manifest(manifest, raw, lock)
        manifest["raw_snapshot_sha256"] = csm.sha256_bytes(raw)
        manifest["source_lock_id"] = "DIFFERENT-LOCK"
        with self.assertRaisesRegex(csm.GateError, "identity mismatch"):
            csm.validate_capture_manifest(manifest, raw, lock)

    def test_partial_or_unfrozen_gate_receipt_cannot_authorize(self) -> None:
        with self.assertRaisesRegex(csm.GateError, "human has not frozen"):
            csm.validate_gate_receipt({"gate_status": "PASS"}, synthetic_source_lock())

    def test_gate_rejects_source_lock_content_mutation(self) -> None:
        lock = synthetic_source_lock()
        gate = synthetic_gate_receipt(lock)
        gate["source_lock_sha256"] = "0" * 64
        with self.assertRaisesRegex(csm.GateError, "source-lock content identity"):
            csm.validate_gate_receipt(gate, lock)

    def test_network_audit_hook_rejects_connect(self) -> None:
        with self.assertRaisesRegex(PermissionError, "disabled"):
            csm._block_network_audit("socket.connect", ("example.invalid", 443))

    def test_event_ledger_must_be_persisted_and_hashed_before_outcomes(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar)
        events = csm.build_signal_events(("2020-01",), calendar, table)
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "event-ledger.json"
            with self.assertRaisesRegex(csm.GateError, "before outcome"):
                csm.calculate_outcomes_after_ledger(events, table, ledger_path=ledger,
                                                    expected_ledger_sha256="0" * 64)
            digest = csm.persist_event_ledger(events, ledger)
            outcomes = csm.calculate_outcomes_after_ledger(events, table, ledger_path=ledger,
                                                           expected_ledger_sha256=digest)
            self.assertEqual(len(outcomes), 1)
            self.assertIsNotNone(outcomes[0])
            self.assertEqual(csm.sha256_bytes(ledger.read_bytes()), digest)

    def test_event_ledger_mutation_fails_identity_check(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar)
        events = csm.build_signal_events(("2020-01",), calendar, table)
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "event-ledger.json"
            digest = csm.persist_event_ledger(events, ledger)
            ledger.write_bytes(ledger.read_bytes() + b" ")
            with self.assertRaisesRegex(csm.GateError, "identity mismatch"):
                csm.calculate_outcomes_after_ledger(events, table, ledger_path=ledger,
                                                    expected_ledger_sha256=digest)

    def test_hashing_and_decimal_json_snapshot_are_stable(self) -> None:
        self.assertEqual(csm.sha256_bytes(b"abc"),
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        self.assertEqual(csm.canonical_json_bytes({"x": Decimal("1.20")}), b'{"x":"1.20"}')


class PacketCIntegrationTests(unittest.TestCase):
    def test_exact_packet_c_artifacts_with_synthetic_csv_rows(self) -> None:
        source_lock_path = os.environ.get("CSM_PACKET_C_SOURCE_LOCK")
        metadata_path = os.environ.get("CSM_PACKET_C_PROBE_METADATA")
        calendar_path = os.environ.get("CSM_PACKET_C_EXPECTED_CALENDAR")
        if not all((source_lock_path, metadata_path, calendar_path)):
            self.skipTest("exact Packet C artifacts were not supplied to this test run")

        paths = {
            "source-lock": (Path(source_lock_path), "81bd315cd8301142e5e8ffcbfcb43bf89f99e5bf"),
            "probe-metadata": (Path(metadata_path), "21aa9149b7b7db9b07f1aa3f4bf0312675a166bd"),
            "expected-calendar": (Path(calendar_path), "6ed720353472ba6f35391936c536d46fb6ae8c66"),
        }
        payloads: dict[str, bytes] = {}
        for name, (path, expected_blob) in paths.items():
            raw = path.read_bytes()
            actual_blob = hashlib.sha1(
                f"blob {len(raw)}\0".encode("ascii") + raw
            ).hexdigest()
            self.assertEqual(actual_blob, expected_blob, f"Packet C {name} blob identity")
            payloads[name] = raw

        source_lock = json.loads(payloads["source-lock"].decode("utf-8"))
        metadata = json.loads(payloads["probe-metadata"].decode("utf-8"))
        calendar_doc = json.loads(payloads["expected-calendar"].decode("utf-8"))
        csm.validate_packet_c_source_lock(source_lock)
        schema = csm.validate_packet_c_probe_metadata(source_lock, metadata)
        month_ends = csm.validate_calendar_document(
            calendar_doc, source_lock=source_lock,
            raw_bytes=payloads["expected-calendar"],
        )
        self.assertEqual(len(schema), 32)
        self.assertEqual(len(month_ends), 203)
        self.assertEqual(month_ends["2009-11"], "2009-11-30")
        self.assertEqual(month_ends["2026-09"], "2026-09-30")

        synthetic_csv = packet_c_synthetic_csv(schema, source_lock)
        table = csm.parse_source_csv(synthetic_csv, source_lock, source_metadata=metadata)
        observed = table.values[date(2009, 11, 2)]
        self.assertEqual(set(observed), set(csm.NON_EUR_CURRENCIES))
        self.assertEqual(csm.price_vector(table, date(2009, 11, 2))["EUR"], Decimal(1))

        metadata_hash = csm.sha256_bytes(payloads["probe-metadata"])
        synthetic_gate = synthetic_gate_receipt(source_lock)
        synthetic_gate["expected_calendar_sha256"] = source_lock["calendar"]["sha256"]
        synthetic_gate["probe_metadata_sha256"] = metadata_hash
        csm.validate_gate_receipt(
            synthetic_gate, source_lock,
            expected_probe_metadata_sha256=metadata_hash,
        )
        capture_manifest = {
            "capture_status": "CAPTURED",
            "source_lock_id": csm.source_lock_id(source_lock),
            "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(source_lock)),
            "spec_id": csm.SPEC_ID,
            "data_role": "EXPLORATORY_DISCOVERY",
            "requested_start": "2009-11-01",
            "requested_end": "2026-09-30",
            "raw_snapshot_sha256": csm.sha256_bytes(synthetic_csv),
            "source_series_keys": list(csm.EXPECTED_SERIES_BY_CURRENCY.values()),
            "access_ledger_id": "SYNTHETIC-LEDGER",
            "retrieval_timestamp": "2020-01-01T00:00:00Z",
            "snapshot_uri": "SYNTHETIC",
            "identity_check": "PASS",
            "probe_metadata_sha256": metadata_hash,
        }
        csm.validate_capture_manifest(
            capture_manifest, synthetic_csv, source_lock,
            expected_metadata_sha256=metadata_hash,
        )

        reordered = list(schema)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        bad_header_csv = packet_c_synthetic_csv(tuple(reordered), source_lock)
        with self.assertRaisesRegex(csm.DataError, "exact Packet C schema"):
            csm.parse_source_csv(bad_header_csv, source_lock, source_metadata=metadata)

        bad_dimension_csv = synthetic_csv.replace(b",EUR,SP00,", b",USD,SP00,", 1)
        with self.assertRaisesRegex(csm.DataError, "dimensions or units"):
            csm.parse_source_csv(bad_dimension_csv, source_lock, source_metadata=metadata)


def packet_c_synthetic_csv(
    schema: tuple[str, ...] | list[str], source_lock: dict[str, object]
) -> bytes:
    """Create metadata-shaped test rows; all OBS_VALUE text here is synthetic."""
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(schema), lineterminator="\n")
    writer.writeheader()
    for index, series in enumerate(source_lock["series"], start=1):
        row = {field: "" for field in schema}
        row.update({
            "KEY": series["key"],
            "FREQ": series["frequency"],
            "CURRENCY": series["currency"],
            "CURRENCY_DENOM": series["currency_denom"],
            "EXR_TYPE": series["exr_type"],
            "EXR_SUFFIX": series["exr_suffix"],
            "TIME_PERIOD": "2009-11-02",
            "OBS_VALUE": f"{index}.25",
            "OBS_STATUS": "A",
            "SOURCE_AGENCY": series["source_agency"],
            "UNIT": series["unit"],
            "UNIT_MULT": str(series["unit_mult"]),
            "DECIMALS": str(series["decimals"]),
        })
        writer.writerow(row)
    return stream.getvalue().encode("utf-8")

def synthetic_source_lock() -> dict[str, object]:
    return {
        "id": "SYNTHETIC-LOCK-ONLY",
        "spec_id": csm.SPEC_ID,
        "source_transport": "SYNTHETIC_FIXTURE_ONLY",
        "series_by_currency": dict(csm.EXPECTED_SERIES_BY_CURRENCY),
        "csv_field_map": {"date": "TIME_PERIOD", "series": "SERIES_KEY", "value": "OBS_VALUE",
                          "unit": "UNIT", "status": "OBS_STATUS"},
        "unit_by_currency": dict(UNIT_BY_CURRENCY),
        "status_policy": {"valid": ["A"], "missing": ["M"]},
        "fixture_status": "SYNTHETIC",
    }


def synthetic_gate_receipt(source_lock: dict[str, object]) -> dict[str, object]:
    unit_status = csm.source_unit_status_map(source_lock)
    return {
        "gate_status": "PASS",
        "human_freeze_status": "FROZEN",
        "market_outcome_access_authorized": True,
        "data_role": "EXPLORATORY_DISCOVERY",
        "spec_id": csm.SPEC_ID,
        "spec_git_blob_sha1": csm.SPEC_GIT_BLOB_SHA1,
        "spec_sha256": csm.SPEC_SHA256,
        "hypothesis_id": csm.HYPOTHESIS_ID,
        "source_lock_id": csm.source_lock_id(source_lock),
        "human_contract_decision_id": "SYNTHETIC_FIXTURE_ONLY",
        "source_transport": csm.source_transport(source_lock),
        "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(source_lock)),
        "unit_status_map_sha256": csm.sha256_bytes(csm.canonical_json_bytes(unit_status)),
        "expected_calendar_sha256": "a" * 64,
        "raw_capture_process_id": "SYNTHETIC_FIXTURE_ONLY",
        "access_ledger_id": "SYNTHETIC_FIXTURE_ONLY",
        "code_commit": "SYNTHETIC_FIXTURE_ONLY",
        "synthetic_test_log_sha256": "b" * 64,
        "environment_identity_sha256": "c" * 64,
        "independent_audit_id": "SYNTHETIC_FIXTURE_ONLY",
        "integrator_gate_id": "SYNTHETIC_FIXTURE_ONLY",
        "run_id": "SYNTHETIC_FIXTURE_ONLY",
        "outcome_access_owner": "SYNTHETIC_FIXTURE_ONLY",
        "source_series_keys": list(csm.EXPECTED_SERIES_BY_CURRENCY.values()),
        "time_range": {"source_start": csm.SOURCE_START, "source_end": csm.SOURCE_END,
                       "target_start": csm.TARGET_START, "target_end": csm.TARGET_END},
        "full_history_run_authorized": True,
    }


if __name__ == "__main__":
    unittest.main()
