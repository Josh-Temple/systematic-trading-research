"""Synthetic-only tests. No exchange-rate history or strategy outcomes are read."""
from __future__ import annotations

import contextlib
import base64
import csv
import hashlib
import io
import json
import os
import random
import tempfile
import unittest
from datetime import date, datetime
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
        self.assertEqual(event.status, "READY")
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "event-ledger.json"
            digest = csm.persist_event_ledger((event,), ledger)
            outcomes = csm.calculate_outcomes_after_ledger(
                (event,), table, ledger_path=ledger, expected_ledger_sha256=digest
            )
        self.assertEqual(outcomes, (None,))
        metrics = csm.summarize_metrics(outcomes, (event,))
        self.assertIn("TARGET_ENDPOINT_UNAVAILABLE:2020-01", metrics.skip_reasons)

    def test_missing_expected_target_endpoint_does_not_use_prior_day_or_shift(self) -> None:
        calendar = dates_for_small_grid()
        prior = vector({"USD": "0.997", "AUD": "1.003"})
        table = synthetic_table(calendar, omit={calendar["2020-02"]},
                                add_neighbor=("2020-02-27", prior))
        months = ("2020-01", "2020-02", "2020-03")
        events = csm.build_signal_events(months, calendar, table)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[1].target_month, "2020-02")
        self.assertEqual(events[1].status, "READY")
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "event-ledger.json"
            digest = csm.persist_event_ledger((events[1],), ledger)
            outcomes = csm.calculate_outcomes_after_ledger(
                (events[1],), table, ledger_path=ledger, expected_ledger_sha256=digest
            )
        self.assertEqual(outcomes, (None,))
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
        self.assertEqual(set(event.score_identities), set(csm.CURRENCIES))
        self.assertTrue(all(len(score["identity_sha256"]) == 64
                            and len(score["input_identity_sha256"]) == 64
                            for score in event.score_identities.values()))

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

    def test_pre_outcome_ledger_records_a_b_and_all_score_identities(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar)
        event = csm.build_signal_events(("2020-01",), calendar, table)[0]
        row = csm.event_ledger_payload((event,))["events"][0]
        self.assertEqual(row["a"], event.winner)
        self.assertEqual(row["b"], event.loser)
        self.assertEqual(row["formation_start_date"], calendar["2019-11"])
        self.assertEqual(row["formation_end_date"], calendar["2019-12"])
        self.assertEqual(set(row["score_identities"]), set(csm.CURRENCIES))
        for currency, score in event.score_identities.items():
            self.assertEqual(score["status"], "AVAILABLE")
            self.assertEqual(score["score_spec"], csm.SCORE_IDENTITY_SPEC)
            self.assertEqual(len(score["identity_sha256"]), 64)
            self.assertEqual(len(score["input_identity_sha256"]), 64)
        repeated = csm.build_signal_events(("2020-01",), calendar, table)[0]
        self.assertEqual(event.score_identities, repeated.score_identities)

    def test_score_ledger_is_independent_of_target_values_and_target_availability(self) -> None:
        calendar = dates_for_small_grid()
        table = synthetic_table(calendar)
        baseline = csm.build_signal_events(("2020-01",), calendar, table)
        changed_values = {day: dict(values) for day, values in table.values.items()}
        target_day = date.fromisoformat(calendar["2020-01"])
        changed_values[target_day].update({"AUD": Decimal("9000"), "USD": Decimal("0.0001")})
        changed = csm.QuoteTable(changed_values, table.statuses, table.row_dates)
        changed_event = csm.build_signal_events(("2020-01",), calendar, changed)
        self.assertEqual(
            csm.canonical_json_bytes(csm.event_ledger_payload(baseline)),
            csm.canonical_json_bytes(csm.event_ledger_payload(changed_event)),
        )
        target_missing = csm.QuoteTable(
            {day: values for day, values in table.values.items() if day != target_day},
            table.statuses,
            frozenset(day for day in table.row_dates if day != target_day),
        )
        missing_event = csm.build_signal_events(("2020-01",), calendar, target_missing)
        self.assertEqual(
            csm.canonical_json_bytes(csm.event_ledger_payload(baseline)),
            csm.canonical_json_bytes(csm.event_ledger_payload(missing_event)),
        )

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
    def test_config_is_single_frozen_spec_and_rejects_drift(self) -> None:
        config = json.loads(csm.CONFIG_PATH.read_text(encoding="utf-8"))
        csm.validate_config(config)
        self.assertEqual(csm.SPEC_GIT_BLOB_SHA1, "7fe114e2fcfa33b0565b51c717455abd8837d5d9")
        self.assertEqual(csm.SPEC_SHA256, "a1ba23f0b2c6ff25201779f18779e75f013ba8af84cdf8b531ce650f35a9c6a2")
        self.assertEqual(config["accepted_pre_freeze_spec_sha256"], "e39569e9e238e3b869ff302d4f67002252eb4f970cd83592bdeed632fe9eed90")
        self.assertEqual(config["human_decision_id"], "HDEC-CSM-002-20261001")
        self.assertEqual(config["freeze_status"], "FROZEN")
        self.assertEqual(
            config["market_outcome_access"],
            "CLOSED_UNTIL_INTEGRATOR_GATE_PASS_AND_SEPARATE_X_INSTRUCTION",
        )
        changed = dict(config)
        changed["target_end"] = "2026-10"
        with self.assertRaisesRegex(csm.GateError, "target_end"):
            csm.validate_config(changed)
        changed = dict(config)
        changed["freeze_status"] = "PROPOSED_NOT_FROZEN"
        with self.assertRaisesRegex(csm.GateError, "freeze_status"):
            csm.validate_config(changed)
        changed = dict(config)
        changed["market_outcome_access"] = "OPEN"
        with self.assertRaisesRegex(csm.GateError, "market_outcome_access"):
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
        source_lock_raw = csm.canonical_json_bytes(lock)
        raw = b"synthetic bytes only"
        manifest = {
            "capture_status": "CAPTURED",
            "source_lock_id": lock["id"],
            "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(lock)),
            "source_lock_raw_sha256": csm.sha256_bytes(source_lock_raw),
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
        csm.validate_capture_manifest(manifest, raw, lock, source_lock_raw_bytes=source_lock_raw)
        manifest["raw_snapshot_sha256"] = "0" * 64
        with self.assertRaisesRegex(csm.GateError, "hash mismatch"):
            csm.validate_capture_manifest(manifest, raw, lock, source_lock_raw_bytes=source_lock_raw)
        manifest["raw_snapshot_sha256"] = csm.sha256_bytes(raw)
        manifest["source_lock_id"] = "DIFFERENT-LOCK"
        with self.assertRaisesRegex(csm.GateError, "identity mismatch"):
            csm.validate_capture_manifest(manifest, raw, lock, source_lock_raw_bytes=source_lock_raw)

    def test_partial_or_unfrozen_gate_receipt_cannot_authorize(self) -> None:
        with self.assertRaisesRegex(csm.GateError, "human has not frozen"):
            receipt, trusted, raw = synthetic_gate_receipt(
                synthetic_source_lock(), gate_overrides={"human_freeze_status": "NOT_FROZEN"}
            )
            csm.validate_gate_receipt(
                receipt, synthetic_source_lock(), source_lock_raw_bytes=raw,
                trusted_keys=trusted, expected_file_hashes=TEST_FILE_HASHES,
                expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
                expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
                now=TEST_NOW, expected_current_i2_gate=TEST_CURRENT_I2_GATE,
                expected_e_audit=TEST_E_AUDIT, allow_synthetic_test_fixtures=True,
            )

    def test_signed_gate_receipt_accepts_only_trusted_e_and_i2_signatures(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        accepted = csm.validate_gate_receipt(
            gate, lock, source_lock_raw_bytes=raw, trusted_keys=keys,
            expected_file_hashes=TEST_FILE_HASHES,
            expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
            expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
            now=TEST_NOW, expected_current_i2_gate=TEST_CURRENT_I2_GATE,
            expected_e_audit=TEST_E_AUDIT, allow_synthetic_test_fixtures=True,
        )
        self.assertEqual(accepted["gate_status"], "PASS")


    def test_signed_e_and_i_fixture_keys_are_independent(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        self.assertNotEqual(keys["auditor-test-key-001"]["principal_id"],
                            keys["integrator-test-key-001"]["principal_id"])
        self.assertNotEqual(int(keys["auditor-test-key-001"]["n_hex"], 16),
                            int(keys["integrator-test-key-001"]["n_hex"], 16))
        self.assertEqual(validate_test_gate(gate, lock, raw, keys)["gate_status"], "PASS")

    def test_signed_gate_rejects_same_e_i_principal_despite_valid_signatures(self) -> None:
        lock = synthetic_source_lock()
        gate, original_keys, raw = synthetic_gate_receipt(lock)
        keys = json.loads(json.dumps(original_keys))
        keys["auditor-test-key-001"]["principal_id"] = "integrator-principal-001"
        e_payload = gate["payload"]["independent_audit_attestation"]["payload"]
        e_payload["signer_principal_id"] = "integrator-principal-001"
        e_signed = sign_envelope(e_payload, "auditor-test-key-001")
        gate["payload"]["independent_audit_attestation"] = e_signed
        gate["payload"]["independent_audit_envelope_sha256"] = csm.sha256_bytes(
            csm.canonical_json_bytes(e_signed))
        gate = sign_gate_payload(gate["payload"])
        # Both role-specific signatures verify; separation must still fail.
        csm._verify_signed_envelope(
            e_signed, keys, required_role="independent_auditor", now=TEST_NOW)
        csm._verify_signed_envelope(
            gate, keys, required_role="integrator", now=TEST_NOW)
        with self.assertRaisesRegex(csm.GateError, "share signing principal"):
            validate_test_gate(gate, lock, raw, keys)

    def test_signed_gate_rejects_same_public_key_behind_distinct_key_ids(self) -> None:
        lock = synthetic_source_lock()
        gate, original_keys, raw = synthetic_gate_receipt(lock)
        keys = json.loads(json.dumps(original_keys))
        # Deliberately alias the RSA modulus under a different key ID and principal,
        # with a valid signature from the matching synthetic E private exponent.
        keys["integrator-test-key-001"]["n_hex"] = (
            "000" + keys["auditor-test-key-001"]["n_hex"])
        gate = sign_envelope(gate["payload"], "integrator-test-key-001",
                             rsa_signer_key_id="auditor-test-key-001")
        csm._verify_signed_envelope(
            gate["payload"]["independent_audit_attestation"], keys,
            required_role="independent_auditor", now=TEST_NOW)
        csm._verify_signed_envelope(
            gate, keys, required_role="integrator", now=TEST_NOW)
        with self.assertRaisesRegex(csm.GateError, "share RSA modulus/public key"):
            validate_test_gate(gate, lock, raw, keys)

    def test_signed_gate_rejects_role_swap_revocation_and_future_validity(self) -> None:
        lock = synthetic_source_lock()
        gate, original_keys, raw = synthetic_gate_receipt(lock)
        for label, target, change, expected in (
            ("role swap", "auditor-test-key-001", {"role": "integrator"}, "role is not trusted"),
            ("revoked", "integrator-test-key-001", {"revoked": True}, "role is not trusted"),
            ("future", "auditor-test-key-001",
             {"valid_from": "2026-10-02T08:00:00+09:00"}, "exceeds signing key validity"),
        ):
            with self.subTest(case=label):
                keys = json.loads(json.dumps(original_keys))
                keys[target].update(change)
                with self.assertRaisesRegex(csm.GateError, expected):
                    validate_test_gate(gate, lock, raw, keys)

    def test_signed_gate_rejects_stale_i2_and_e_expected_identities(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        stale_i2 = dict(TEST_CURRENT_I2_GATE)
        stale_i2["head_sha"] = "f" * 40
        with self.assertRaisesRegex(csm.GateError, "expected I2 gate"):
            validate_test_gate(gate, lock, raw, keys, expected_current_i2_gate=stale_i2)
        stale_e = dict(TEST_E_AUDIT)
        stale_e["head_sha"] = "e" * 40
        with self.assertRaisesRegex(csm.GateError, "expected E audit"):
            validate_test_gate(gate, lock, raw, keys, expected_e_audit=stale_e)

    def test_signed_gate_rejects_mutated_e_signature(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        gate["payload"]["independent_audit_attestation"]["signature"]["signature_b64"] = (
            base64.b64encode(b"\x00" * 256).decode("ascii"))
        with self.assertRaisesRegex(csm.GateError, "signature verification failed"):
            validate_test_gate(gate, lock, raw, keys)

    def test_gate_rejects_arbitrary_signing_key_and_bad_signature(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        unknown = json.loads(json.dumps(gate))
        unknown["signature"]["key_id"] = "attacker-key-0001"
        with self.assertRaisesRegex(csm.GateError, "not in the trusted key store"):
            validate_test_gate(unknown, lock, raw, keys)
        bad_signature = json.loads(json.dumps(gate))
        bad_signature["signature"]["signature_b64"] = base64.b64encode(b"\x00" * 256).decode()
        with self.assertRaisesRegex(csm.GateError, "signature verification failed"):
            validate_test_gate(bad_signature, lock, raw, keys)

    def test_gate_rejects_placeholder_missing_and_expired_receipts(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock, gate_overrides={"gate_id": "PLACEHOLDER"})
        with self.assertRaisesRegex(csm.GateError, "placeholder gate_id"):
            validate_test_gate(gate, lock, raw, keys)
        missing, keys, raw = synthetic_gate_receipt(lock)
        del missing["signature"]
        with self.assertRaisesRegex(csm.GateError, "not a signed envelope"):
            validate_test_gate(missing, lock, raw, keys)
        expired, keys, raw = synthetic_gate_receipt(
            lock,
            gate_issued_at="2026-10-01T00:00:00+00:00",
            gate_expires_at="2026-10-01T12:00:00+00:00",
        )
        with self.assertRaisesRegex(csm.GateError, "expired"):
            validate_test_gate(expired, lock, raw, keys)

    def test_source_lock_raw_byte_identity_rejects_semantically_equal_json(self) -> None:
        lock = synthetic_source_lock()
        receipt, keys, raw = synthetic_gate_receipt(lock)
        different_bytes = json.dumps(lock, indent=2, sort_keys=True).encode("utf-8")
        self.assertEqual(json.loads(different_bytes.decode("utf-8")), lock)
        with self.assertRaisesRegex(csm.GateError, "raw-byte identity mismatch"):
            validate_test_gate(receipt, lock, different_bytes, keys)
        changed = json.loads(json.dumps(receipt))
        changed["payload"]["source_lock_raw_sha256"] = csm.sha256_bytes(different_bytes)
        changed = sign_gate_payload(changed["payload"])
        with self.assertRaisesRegex(csm.GateError, "raw-byte identity mismatch"):
            validate_test_gate(changed, lock, raw, keys)

    def test_closed_i2_identity_is_not_authorizing(self) -> None:
        lock = synthetic_source_lock()
        closed = dict(TEST_CURRENT_I2_GATE)
        closed["gate_status"] = "CLOSED"
        closed["market_outcome_access"] = False
        receipt, keys, raw = synthetic_gate_receipt(lock, current_i2_gate=closed)
        with self.assertRaisesRegex(csm.GateError, "current I2 gate is not PASS"):
            csm.validate_gate_receipt(
                receipt, lock, source_lock_raw_bytes=raw,
                trusted_keys=keys, expected_file_hashes=TEST_FILE_HASHES,
                expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
                expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
                now=TEST_NOW, allow_synthetic_test_fixtures=True,
            )

    def test_partial_e_recommendation_blocks_even_a_valid_signature(self) -> None:
        lock = synthetic_source_lock()
        partial = dict(TEST_E_AUDIT)
        partial["status"] = "PARTIAL_WITH_GAPS"
        partial["recommendation"] = "BLOCKED"
        receipt, keys, raw = synthetic_gate_receipt(
            lock, current_i2_gate=TEST_CURRENT_I2_GATE, e_audit=partial,
        )
        with self.assertRaisesRegex(csm.GateError, "current E audit status is not PASS"):
            csm.validate_gate_receipt(
                receipt, lock, source_lock_raw_bytes=raw,
                trusted_keys=keys, expected_file_hashes=TEST_FILE_HASHES,
                expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
                expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
                now=TEST_NOW, allow_synthetic_test_fixtures=True,
            )

    def test_signed_e_attestation_must_bind_current_d_hashes(self) -> None:
        lock = synthetic_source_lock()
        gate, keys, raw = synthetic_gate_receipt(lock)
        tampered = json.loads(json.dumps(gate))
        e_payload = tampered["payload"]["independent_audit_attestation"]["payload"]
        e_payload["audited_d_file_hashes"]["csm.py"] = "0" * 64
        tampered["payload"]["independent_audit_attestation"] = sign_envelope(
            e_payload, "auditor-test-key-001"
        )
        tampered["payload"]["independent_audit_envelope_sha256"] = csm.sha256_bytes(
            csm.canonical_json_bytes(tampered["payload"]["independent_audit_attestation"])
        )
        tampered = sign_gate_payload(tampered["payload"])
        with self.assertRaisesRegex(csm.GateError, "does not bind the current D file hashes"):
            csm.validate_gate_receipt(
                tampered, lock, source_lock_raw_bytes=raw,
                trusted_keys=keys, expected_file_hashes=TEST_FILE_HASHES,
                expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
                expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
                now=TEST_NOW, allow_synthetic_test_fixtures=True,
            )

    def test_dynamic_signed_i_and_e_identities_do_not_require_code_pin_update(self) -> None:
        lock = synthetic_source_lock()
        i2 = dict(TEST_CURRENT_I2_GATE)
        i2["head_sha"] = "c" * 40
        i2["gate_blob_sha1"] = "d" * 40
        i2["gate_sha256"] = "e" * 64
        audit = dict(TEST_E_AUDIT)
        audit["audit_id"] = "AUDIT-CSM-E-SYNTH-ROTATED"
        audit["head_sha"] = "f" * 40
        gate, keys, raw = synthetic_gate_receipt(lock, current_i2_gate=i2, e_audit=audit)
        accepted = csm.validate_gate_receipt(
            gate, lock, source_lock_raw_bytes=raw,
            trusted_keys=keys, expected_file_hashes=TEST_FILE_HASHES,
            expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
            expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
            now=TEST_NOW, allow_synthetic_test_fixtures=True,
        )
        self.assertEqual(accepted["current_i2_gate_identity"]["head_sha"], "c" * 40)

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


class AtomicPersistenceTests(unittest.TestCase):
    def fail_at(self, target: str):
        def inject(point: str) -> None:
            if point == target:
                raise OSError(f"injected {target} failure")
        return inject

    def build_stage(self, root: Path, name: str) -> Path:
        stage = root / f".{name}.stage"
        stage.mkdir()
        files = {
            "attempt-start.json": b'{"execution_status":"IN_PROGRESS"}',
            "event-ledger.json": b'{"record_type":"PRE_OUTCOME_EVENT_LEDGER"}',
            "primary-metrics.json": b'{"synthetic":true}',
            "inference.json": b'{"scientific_status":"NOT_APPLICABLE"}',
        }
        for filename, payload in files.items():
            (stage / filename).write_bytes(payload)
        success = {
            "execution_status": "SUCCESS",
            "output_file_sha256": {
                filename: hashlib.sha256(payload).hexdigest()
                for filename, payload in files.items()
            },
        }
        (stage / "_completion-pending.json").write_bytes(csm.canonical_json_bytes({
            "promotion_status": "READY_TO_PROMOTE",
            "success_receipt": success,
        }))
        return stage

    def test_capture_write_flush_fsync_and_promotion_failures_never_publish_partial_bytes(self) -> None:
        for point in ("write", "flush", "file_fsync", "promotion", "parent_fsync"):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                destination = root / "capture.bin"
                payload = b"synthetic capture bytes only"
                with self.assertRaisesRegex(csm.GateError, "failed"):
                    csm.atomic_capture_bytes(
                        payload, destination,
                        expected_sha256=csm.sha256_bytes(payload),
                        validator=lambda raw: self.assertEqual(raw, payload),
                        fault_injector=self.fail_at(point),
                    )
                self.assertFalse(destination.exists())
                self.assertEqual(list(root.glob(".capture.bin.stage-*")), [])

    def test_capture_hash_mismatch_is_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "capture.bin"
            with self.assertRaisesRegex(csm.GateError, "hash mismatch"):
                csm.atomic_capture_bytes(
                    b"synthetic bytes", destination, expected_sha256="0" * 64,
                    validator=lambda raw: None,
                )
            self.assertFalse(destination.exists())

    def test_output_rename_and_promotion_failures_never_leave_success_receipt(self) -> None:
        for point in ("rename", "parent_fsync", "success_receipt", "success_file_fsync",
                      "success_promotion", "success_parent_fsync"):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                destination = root / "published-run"
                stage = self.build_stage(root, destination.name)
                with self.assertRaisesRegex(csm.GateError, "failed|injected"):
                    csm.promote_output_directory(
                        stage, destination, fault_injector=self.fail_at(point)
                    )
                self.assertFalse((destination / "run-receipt.json").exists())
                self.assertFalse(destination.exists())
                if stage.exists():
                    self.assertTrue((stage / "_completion-pending.json").exists())

    def test_compound_final_fsync_and_rollback_delete_failure_never_leaves_success_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / "published-run"
            stage = self.build_stage(root, destination.name)
            original_fsync = csm._fsync_directory
            original_rmtree = csm.shutil.rmtree
            count = {"destination": 0}

            def fail_second_destination_fsync(path: Path) -> None:
                if path == destination:
                    count["destination"] += 1
                    if count["destination"] == 2:
                        raise OSError("synthetic final directory fsync fault")
                original_fsync(path)

            def fail_cleanup(path: object, *args: object, **kwargs: object) -> object:
                if Path(path) == destination:
                    raise OSError("synthetic rollback deletion fault")
                return original_rmtree(path, *args, **kwargs)

            csm._fsync_directory = fail_second_destination_fsync
            csm.shutil.rmtree = fail_cleanup
            try:
                with self.assertRaisesRegex(csm.GateError, "failed"):
                    csm.promote_output_directory(stage, destination)
                self.assertFalse(
                    (destination / "run-receipt.json").exists(),
                    "failed promotion must never leave a SUCCESS receipt",
                )
            finally:
                csm._fsync_directory = original_fsync
                csm.shutil.rmtree = original_rmtree
                if destination.exists():
                    original_rmtree(destination)


    def test_output_promotion_validates_all_bytes_before_final_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            destination = root / "published-run"
            stage = self.build_stage(root, destination.name)
            (stage / "event-ledger.json").write_bytes(b"mutated synthetic bytes")
            with self.assertRaisesRegex(csm.GateError, "hash mismatch"):
                csm.promote_output_directory(stage, destination)
            self.assertFalse(destination.exists())
            self.assertFalse((stage / "run-receipt.json").exists())


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
        synthetic_gate, trusted_keys, _ = synthetic_gate_receipt(
            source_lock,
            source_lock_raw_bytes=payloads["source-lock"],
            expected_calendar_sha256=source_lock["calendar"]["sha256"],
            probe_metadata_sha256=metadata_hash,
        )
        csm.validate_gate_receipt(
            synthetic_gate, source_lock, source_lock_raw_bytes=payloads["source-lock"],
            trusted_keys=trusted_keys,
            expected_file_hashes=TEST_FILE_HASHES,
            expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
            expected_probe_metadata_sha256=metadata_hash,
            expected_calendar_sha256=source_lock["calendar"]["sha256"],
            now=TEST_NOW, expected_current_i2_gate=TEST_CURRENT_I2_GATE,
            expected_e_audit=TEST_E_AUDIT, allow_synthetic_test_fixtures=True,
        )
        capture_manifest = {
            "capture_status": "CAPTURED",
            "source_lock_id": csm.source_lock_id(source_lock),
            "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(source_lock)),
            "source_lock_raw_sha256": csm.sha256_bytes(payloads["source-lock"]),
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
            source_lock_raw_bytes=payloads["source-lock"],
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


TEST_RSA_N = int(
    "f12c454cafaa2a3cc5d755f9db98ca193944475b5ed676efb0facd2a0ebcce35272e6721d8ac76a15a136b01e41fd481b3926cdc95f48f27680cd57a2fe9ae13f0bc79d31d616b1cbb5b028c86f69aecf93ad84efc426ff3b77245d9e38ed6868069f84adddb175a1eddb99983da0a8ba8975d047e8fb50390f6a09c723bd84b855d65995738c247bddc199af39ae49324305be07cc587ba074bbe6f72af3cb516734036a8e20998589cb37256cc32ccd5275d0a3dedb3ef320d334ae9dd8e6d78391021f0f58288a74a625c32e66f4023710a378c068ddcd1bd59976ef2722bb662cd4a4241ac21a47f134568a5157eeee81d4b3ccbf39e8a4ded3def126833",
    16,
)
TEST_RSA_D = int(
    "4bf6a04b53c75aef72776d96ba22e9814166eebcea65cde7988c9ec3c1099a3fe6bbf873123edc4cdd44e17f227e1e1ece53702398be03bb2b4c638f4d7922c218211d94301c67b310964d7abae6010d64413331c9c61962202587b7e633af0185801b5b657ee55f96fa4ac3fe6256d0ff84d1a121461d83668d3030a6d08fc3394dc7a94ed00c9bfaecd94c8ce147c3c154d534b7163f36b2ca8f929ff20ca69ace7d6197c527a4cb5fc773ae19668945df5a1436cea37b561c560566d360737f660c73921e06c46a5bfed26936be53dc751dbfe2a911f88eeb1bc1847754e759899e84280df1cfa055a555e60c20dab7d60dd25b662790b50443f017946a7d",
    16,
)
# Test-only RSA identity, generated independently of TEST_RSA_N. Never provision
# either toy private exponent as a production credential.
TEST_INTEGRATOR_RSA_N = int("e3f8587d9958561bcdf7d45ab93d08c4dd3e44be1ea0beedc9eb17d20f55d6b30c8ce0ff0b8df7f7bd1ce0d523fc9b3fd90ab007dcfce615becd47f1870df6b21208f662f03c32f7bf9537bfe5d89d4d2cad7086f70994143c06ef24b49499976d23b00bf840d02066220d99cf6773e32fba2f58e103f73854a5526f82243a0f767072afec3c3755ace9c7d4a8fb44152dbc074bf6e8293a544c80bb091fbf7a5f5b4d3aa599786eec6f5ee55075dc0db237816d6da5ac0f7a2488a5cd8cfe91f23bf8e334dd95627356e48f9bb41562e72cc49fff6e0cd7b046fbf05b66486de24525c9bf09c4c35d1a11350a6007cf3cbb791c264d0bdab44bdaed55ca9cbf", 16)
TEST_INTEGRATOR_RSA_D = int("3bf574a8cc2d3cb0a1729e6aa22fd85f96e52ac56a5ed2f8cdd3c4771e4b7065b55654532061dda74e190b5563daaba6965a46443b2e5501c12652d6c6b3b87fcb588a1d299c5bb767af4273796b88abe4a555645a132ddc489176528c204d69536e407e55740e8986f34bea796f773e78ae1a87e0dedf25f4b56ac223538de5462483723791fc3877512cb7959a2bd1d61d432db5a0134dec419538f84d8fb83b931822d2d36eb7d9c1c2fc335de4f6d84833127c1f76440139a08b578a03bcb0e393ec7db9a532a28be9ace1f75c824ec01863ae5bbe04d610b18934b3b5a5805628bb9b8541817e722e6a07aa504549364670513498ef47ecaef6ba5136a9", 16)

TEST_NOW = datetime.fromisoformat("2026-10-02T07:00:00+09:00")
TEST_CURRENT_I2_GATE = {
    "pr_number": 37,
    "head_sha": "a" * 40,
    "gate_blob_sha1": "1" * 40,
    "gate_sha256": "2" * 64,
    "gate_markdown_blob_sha1": "3" * 40,
    "gate_markdown_sha256": "4" * 64,
    "gate_status": "PASS",
    "market_outcome_access": True,
}
TEST_E_AUDIT = {
    "audit_id": "AUDIT-CSM-E-SYNTH-001",
    "pr_number": 38,
    "head_sha": "b" * 40,
    "result_blob_sha1": "5" * 40,
    "result_sha256": "6" * 64,
    "matrix_blob_sha1": "7" * 40,
    "matrix_sha256": "8" * 64,
    "status": "PASS",
    "recommendation": "ALLOW_I2",
}
TEST_FILE_HASHES = {
    "csm.py": "1" * 64,
    "test_csm.py": "2" * 64,
    "config.json": "3" * 64,
    "RUNBOOK.md": "4" * 64,
    "ENVIRONMENT.md": "5" * 64,
    "RESULT.md": "6" * 64,
    "TEST_MATRIX.md": "7" * 64,
    "TEST_LOG.txt": "8" * 64,
    "fixtures/toy_cases.json": "9" * 64,
}
TEST_ENVIRONMENT_SHA256 = "c" * 64
TEST_TRUSTED_KEYS = {
    "auditor-test-key-001": {
        "role": "independent_auditor", "principal_id": "auditor-principal-001",
        "n_hex": format(TEST_RSA_N, "x"), "e": 65537, "revoked": False,
        "valid_from": "2026-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z",
    },
    "integrator-test-key-001": {
        "role": "integrator", "principal_id": "integrator-principal-001",
        "n_hex": format(TEST_INTEGRATOR_RSA_N, "x"), "e": 65537, "revoked": False,
        "valid_from": "2026-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z",
    },
}


def sign_envelope(
    payload: dict[str, object], key_id: str, *,
    issued_at: str = "2026-10-02T06:00:00+09:00",
    expires_at: str = "2026-10-02T18:00:00+09:00",
    rsa_signer_key_id: str | None = None,
) -> dict[str, object]:
    signature_doc = {
        "key_id": key_id,
        "algorithm": "RSASSA-PKCS1-v1_5-SHA256",
        "issued_at": issued_at,
        "expires_at": expires_at,
    }
    message = csm.canonical_json_bytes({"payload": payload, **signature_doc})
    digest_info = csm.RSA_SHA256_DIGEST_INFO_PREFIX + hashlib.sha256(message).digest()
    signer_id = rsa_signer_key_id or key_id
    if signer_id == "auditor-test-key-001":
        rsa_n, rsa_d = TEST_RSA_N, TEST_RSA_D
    elif signer_id == "integrator-test-key-001":
        rsa_n, rsa_d = TEST_INTEGRATOR_RSA_N, TEST_INTEGRATOR_RSA_D
    else:
        raise ValueError("unknown synthetic signing key")
    size = (rsa_n.bit_length() + 7) // 8
    padding_len = size - len(digest_info) - 3
    encoded = b"\x00\x01" + b"\xff" * padding_len + b"\x00" + digest_info
    signature = pow(int.from_bytes(encoded, "big"), rsa_d, rsa_n).to_bytes(size, "big")
    return {"payload": payload, "signature": {
        **signature_doc,
        "signature_b64": base64.b64encode(signature).decode("ascii"),
    }}


def sign_gate_payload(payload: dict[str, object], **kwargs: object) -> dict[str, object]:
    return sign_envelope(payload, "integrator-test-key-001", **kwargs)


def synthetic_gate_receipt(
    source_lock: dict[str, object], *, source_lock_raw_bytes: bytes | None = None,
    expected_calendar_sha256: str = "a" * 64,
    probe_metadata_sha256: str | None = None,
    current_i2_gate: dict[str, object] | None = None,
    e_audit: dict[str, object] | None = None,
    gate_overrides: dict[str, object] | None = None,
    gate_issued_at: str = "2026-10-02T06:00:00+09:00",
    gate_expires_at: str = "2026-10-02T18:00:00+09:00",
) -> tuple[dict[str, object], dict[str, dict[str, object]], bytes]:
    raw_lock = source_lock_raw_bytes or csm.canonical_json_bytes(source_lock)
    audit_identity = dict(e_audit or TEST_E_AUDIT)
    file_hashes = TEST_FILE_HASHES
    audit_payload = {
        **audit_identity,
        "signer_principal_id": "auditor-principal-001",
        "audited_d_file_hashes": dict(file_hashes),
        "audited_environment_identity_sha256": TEST_ENVIRONMENT_SHA256,
        "audited_spec_sha256": csm.SPEC_SHA256,
        "audited_source_lock_raw_sha256": csm.sha256_bytes(raw_lock),
        "audited_calendar_sha256": expected_calendar_sha256,
    }
    e_envelope = sign_envelope(audit_payload, "auditor-test-key-001")
    payload: dict[str, object] = {
        "gate_id": "I2-CSM-002-20261002-TEST-001",
        "integrator_principal_id": "integrator-principal-001",
        "signer_principal_id": "integrator-principal-001",
        "gate_status": "PASS",
        "human_freeze_status": "FROZEN",
        "market_outcome_access_authorized": True,
        "data_role": "EXPLORATORY_DISCOVERY",
        "spec_id": csm.SPEC_ID,
        "spec_git_blob_sha1": csm.SPEC_GIT_BLOB_SHA1,
        "spec_sha256": csm.SPEC_SHA256,
        "hypothesis_id": csm.HYPOTHESIS_ID,
        "human_contract_decision_id": csm.HUMAN_DECISION_ID,
        "source_lock_id": csm.source_lock_id(source_lock),
        "source_transport": csm.source_transport(source_lock),
        "source_lock_sha256": csm.sha256_bytes(csm.canonical_json_bytes(source_lock)),
        "source_lock_raw_sha256": csm.sha256_bytes(raw_lock),
        "unit_status_map_sha256": csm.sha256_bytes(
            csm.canonical_json_bytes(csm.source_unit_status_map(source_lock))
        ),
        "expected_calendar_sha256": expected_calendar_sha256,
        "probe_metadata_sha256": probe_metadata_sha256,
        "source_series_keys": list(csm.EXPECTED_SERIES_BY_CURRENCY.values()),
        "time_range": {"source_start": csm.SOURCE_START, "source_end": csm.SOURCE_END,
                       "target_start": csm.TARGET_START, "target_end": csm.TARGET_END},
        "raw_capture_process_id": "capture-process-20261002-001",
        "access_ledger_id": "access-ledger-20261002-001",
        "run_id": "csm-run-20261002-001",
        "outcome_access_operator_id": "operator-account-20261002-001",
        "outcome_access_operator_name": "Jordan Rivera",
        "code_file_hashes": dict(file_hashes),
        "synthetic_test_log_sha256": file_hashes["TEST_LOG.txt"],
        "environment_identity_sha256": TEST_ENVIRONMENT_SHA256,
        "current_i2_gate_identity": dict(current_i2_gate or TEST_CURRENT_I2_GATE),
        "independent_audit_identity": audit_identity,
        "independent_audit_attestation": e_envelope,
        "independent_audit_envelope_sha256": csm.sha256_bytes(csm.canonical_json_bytes(e_envelope)),
        "full_history_run_authorized": True,
    }
    payload.update(gate_overrides or {})
    return (sign_gate_payload(payload, issued_at=gate_issued_at, expires_at=gate_expires_at),
            TEST_TRUSTED_KEYS, raw_lock)


def validate_test_gate(
    receipt: dict[str, object], source_lock: dict[str, object], source_lock_raw_bytes: bytes,
    trusted_keys: dict[str, dict[str, object]], *,
    expected_current_i2_gate: dict[str, object] | None = TEST_CURRENT_I2_GATE,
    expected_e_audit: dict[str, object] | None = TEST_E_AUDIT,
) -> dict[str, object]:
    return csm.validate_gate_receipt(
        receipt, source_lock, source_lock_raw_bytes=source_lock_raw_bytes,
        trusted_keys=trusted_keys, expected_file_hashes=TEST_FILE_HASHES,
        expected_environment_sha256=TEST_ENVIRONMENT_SHA256,
        expected_probe_metadata_sha256=None, expected_calendar_sha256="a" * 64,
        now=TEST_NOW, expected_current_i2_gate=expected_current_i2_gate,
        expected_e_audit=expected_e_audit, allow_synthetic_test_fixtures=True,
    )


if __name__ == "__main__":
    unittest.main()
