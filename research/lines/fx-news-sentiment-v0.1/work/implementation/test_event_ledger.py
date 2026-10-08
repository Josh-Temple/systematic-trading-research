"""Synthetic-only negative and boundary fixtures; no news/quote/model requests."""
import copy
import json
import tempfile
import unittest
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

from event_ledger import (EventBlocked, SyntheticSourceEvidence, associate_market_outcome,
                          build_synthetic_event, issue_formal_event, verify_synthetic_event,
                          write_synthetic_event, write_blocked_receipt)
from fxns import event_schedule, canonical_json_bytes, canonical_sha256


class SyntheticEventLedgerTest(unittest.TestCase):
    def setUp(self):
        self.day = date(2026, 10, 8)  # Thursday -> Friday, both synthetic.
        c, e, x = event_schedule(self.day)
        self.cutoff, self.entry, self.exit = c, e, x
        self.records = [dict(record_id="synthetic-1", gdelt_seen_at=(c-timedelta(seconds=1)).isoformat(),
                             title="SYNTHETIC: Policy headline", url="https://news.invalid/1",
                             source_domain="news.invalid")]
        self.outputs = [json.dumps(dict(record_id="synthetic-1", EUR="APPRECIATION",
                                        JPY="DEPRECIATION", reason_code_EUR="POLICY",
                                        reason_code_JPY="POLICY"))]
        self.source = SyntheticSourceEvidence(source_status="PASS", acquisition_status="PASS",
            independent_review_ref="synthetic://review", independent_review_sha256="a"*64,
            raw_ref="synthetic://raw", raw_sha256="b"*64,
            metadata_ref="synthetic://meta", metadata_sha256="c"*64,
            query_version="synthetic-query", retrieved_at=(c-timedelta(seconds=1)).isoformat())
        self.kw = dict(event_date=self.day, issued_at=(c+timedelta(minutes=10)).isoformat(),
                       raw_records=self.records, raw_count=1, raw_outputs=self.outputs,
                       source=self.source, expected_model="synthetic-visible-model",
                       visible_model="synthetic-visible-model", expected_config="synthetic-fixed-config",
                       visible_config="synthetic-fixed-config")

    def build(self, **changes):
        kwargs = dict(self.kw); kwargs.update(changes)
        return build_synthetic_event(**kwargs)

    def blocked(self, message=None, **changes):
        with self.assertRaises(EventBlocked) as ctx: self.build(**changes)
        if message: self.assertIn(message, str(ctx.exception))

    def test_thursday_friday_and_synthetic_only(self):
        event = self.build()
        self.assertEqual((event["entry_target"], event["exit_target"]),
                         (self.entry.isoformat(), self.exit.isoformat()))
        self.assertEqual(self.exit-self.entry, timedelta(days=1))
        self.assertEqual(event["decision"], "LONG_EURJPY")
        self.assertEqual(event["formal_cohort_status"], "CLOSED")
        self.assertEqual(event["market_outcome"], "UNAVAILABLE_NOT_REQUESTED")

    def test_friday_issuance_refused(self): self.blocked("INELIGIBLE", event_date=date(2026,10,9))
    def test_known_friday_closure_refused(self): self.blocked("UNAVAILABLE", unavailable_dates=(date(2026,10,9),))
    def test_after_cutoff_acquisition_refused(self):
        self.blocked("POST_CUTOFF", source=replace(self.source,retrieved_at=(self.cutoff+timedelta(seconds=1)).isoformat()))
    def test_timestamp_unaware_or_unknown_refused(self):
        self.blocked("INVALID_ISSUED_AT", issued_at="2026-10-08T08:10:00")
        self.blocked("INVALID_RETRIEVED_AT", source=replace(self.source,retrieved_at="unknown"))
    def test_post_cutoff_and_equality_news_refused(self):
        for seen in (self.cutoff, self.cutoff+timedelta(seconds=1), self.cutoff-timedelta(days=1)):
            bad=[dict(self.records[0], gdelt_seen_at=seen.isoformat())]
            with self.subTest(seen=seen): self.blocked(raw_records=bad)
    def test_raw_count_250_pre_dedupe_refused(self):
        records=[dict(self.records[0], record_id=f"synthetic-{i}") for i in range(250)]
        self.blocked("COMPLETENESS",raw_records=records,raw_count=250)
    def test_raw_count_mismatch_refused(self): self.blocked("RAW_COUNT_MISMATCH", raw_count=2)
    def test_empty_source_blocked(self): self.blocked("EMPTY_INPUT",raw_records=[],raw_count=0,raw_outputs=[])
    def test_news_after_retrieval_rejected(self):
        self.blocked("NEWS_AFTER_PIPELINE_RETRIEVAL", source=replace(self.source,retrieved_at=(self.cutoff-timedelta(seconds=3)).isoformat()))
    def test_unapproved_source_never_inferred_from_count(self):
        for source in (replace(self.source,source_status="PARTIAL_WITH_GAPS"),
                       replace(self.source,acquisition_status="UNVERIFIED")):
            with self.subTest(source=source): self.blocked("SOURCE_QUALIFICATION_BLOCKED",source=source)
    def test_source_receipt_or_hash_missing(self):
        self.blocked("SHA256",source=replace(self.source,independent_review_sha256=""))
        self.blocked("REAL_SOURCE",source=replace(self.source,raw_ref="https://example.com/real"))
    def test_model_identity_config_missing_or_changed(self):
        self.blocked("MISSING_VISIBLE_MODEL",visible_model="")
        self.blocked("model identity changed",visible_model="different-model")
        self.blocked("MODEL_CONFIG_CHANGED",visible_config="changed-config")
    def test_version_mismatch(self): self.blocked("VERSION_MISMATCH",version="SPEC-FXNS-001-v02")
    def test_prompt_hash_mismatch_blocks_before_scoring(self):
        with patch("event_ledger._candidate_hashes", side_effect=EventBlocked("PROMPT_SCHEMA_HASH_MISMATCH")), \
             patch("event_ledger.daily_scores") as scores:
            self.blocked("PROMPT_SCHEMA_HASH_MISMATCH")
            scores.assert_not_called()
    def test_duplicate_raw_record_id(self):
        r=[self.records[0],dict(self.records[0])]
        self.blocked("DUPLICATE_RAW_RECORD_ID",raw_records=r,raw_count=2)
    def test_duplicate_title_dedupe_precedes_output_parse(self):
        r=[self.records[0], dict(self.records[0],record_id="synthetic-2",url="https://news.invalid/2")]
        event=self.build(raw_records=r,raw_count=2)
        self.assertEqual(event["input_record_ids"],["synthetic-1"])
    def test_missing_or_duplicate_output_refused(self):
        self.blocked("OUTPUT_PARSE_OR_SCORE_BLOCKED",raw_outputs=[])
        self.blocked("OUTPUT_PARSE_OR_SCORE_BLOCKED",raw_outputs=self.outputs*2)
        raw=self.outputs[0].replace('"EUR": "APPRECIATION"','"EUR": "APPRECIATION", "EUR": "DEPRECIATION"')
        self.blocked("OUTPUT_PARSE_OR_SCORE_BLOCKED",raw_outputs=[raw])
    def test_real_headline_and_real_url_refused(self):
        self.blocked("REAL_HEADLINE",raw_records=[dict(self.records[0],title="actual news")])
        self.blocked("REAL_URL",raw_records=[dict(self.records[0],url="https://example.com/headline")])
    def test_empty_model_field_refused(self): self.blocked("MISSING_EXPECTED_MODEL",expected_model="")
    def test_late_issuance_refused(self): self.blocked("late issuance",issued_at=self.entry.isoformat())
    def test_no_trade_is_immutable_even_after_freeze(self):
        out=[json.dumps(dict(record_id="synthetic-1",EUR="UNCHANGED",JPY="UNCHANGED",
                             reason_code_EUR="NONE",reason_code_JPY="NONE"))]
        event=self.build(raw_outputs=out)
        self.assertTrue(event["is_no_trade"])
        with tempfile.TemporaryDirectory() as tmp:
            file,_=write_synthetic_event(event,Path(tmp))
            replacement=copy.deepcopy(event);replacement["decision"]="LONG_EURJPY"
            with self.assertRaises(FileExistsError): write_synthetic_event(replacement,Path(tmp))
            self.assertEqual(verify_synthetic_event(file)["decision"],"NO_TRADE")
            changed=json.loads(file.read_text());changed["record"]["decision"]="SHORT_EURJPY"
            file.write_text(json.dumps(changed)+"\n")
            with self.assertRaisesRegex(EventBlocked,"TAMPER"): verify_synthetic_event(file)
    def test_blocked_receipt_does_not_become_no_trade(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=write_blocked_receipt(event_id="SYNTHETIC-FXNS-20261008",
                reason="SOURCE_QUALIFICATION_BLOCKED",directory=Path(tmp))
            receipt=verify_synthetic_event(file)
            self.assertIsNone(receipt["decision"])
            self.assertIsNone(receipt["is_no_trade"])
            self.assertEqual(receipt["blocked_reason"],"SOURCE_QUALIFICATION_BLOCKED")
            with self.assertRaises(FileExistsError):
                write_blocked_receipt(event_id=receipt["event_id"],reason="NO_TRADE",directory=Path(tmp))

    def test_duplicate_event_id_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            event=self.build(); write_synthetic_event(event,Path(tmp))
            with self.assertRaises(FileExistsError):write_synthetic_event(event,Path(tmp))
    def test_closed_formal_issuance_and_outcome_join_even_with_fake_gates(self):
        with self.assertRaisesRegex(EventBlocked,"FORMAL_COHORT_CLOSED_NO_ISSUANCE"):
            issue_formal_event(**self.kw, human_freeze=True, source_qualified=True, xm_qualified=True,
                               model_response="synthetic", market_quote="synthetic")
        with self.assertRaisesRegex(EventBlocked,"FORMAL_COHORT_CLOSED_NO_OUTCOME_JOIN"):
            associate_market_outcome(event_id="SYNTHETIC-FXNS-20261008", price=123.45,
                                     decision="NO_TRADE", source_status="PASS")
    def test_missing_market_price_not_translated_into_no_trade(self):
        event=self.build();self.assertEqual(event["market_outcome"],"UNAVAILABLE_NOT_REQUESTED")
        self.assertNotEqual(event["decision"],"NO_TRADE")


    def test_direct_writer_cannot_label_external_fields_as_synthetic(self):
        event = self.build()
        with tempfile.TemporaryDirectory() as tmp:
            for patch_record, rejected in (
                ({"market_outcome": "synthetic-fabricated-outcome"}, "SYNTHETIC_MARKET_OUTCOME_FORBIDDEN"),
                ({"extra_price_field": "synthetic-not-a-price"}, "INVALID_SYNTHETIC_EVENT_SHAPE"),
                ({"version": "SPEC-FXNS-001-v02"}, "SYNTHETIC_VERSION_OR_COHORT_MISMATCH"),
            ):
                forged = copy.deepcopy(event)
                forged.update(patch_record)
                with self.subTest(patch_record=patch_record), self.assertRaisesRegex(EventBlocked, rejected):
                    write_synthetic_event(forged, Path(tmp))
            for field, replacement in (
                ("raw_ref", "https://example.com/real"),
                ("independent_review_ref", "https://example.com/real"),
                ("synthetic_fixture_only", False),
            ):
                forged = copy.deepcopy(event)
                forged["source"][field] = replacement
                with self.subTest(field=field), self.assertRaises(EventBlocked):
                    write_synthetic_event(forged, Path(tmp))
            forged = copy.deepcopy(event)
            forged["model"]["observed_visible_identity"] = "real-model"
            with self.assertRaisesRegex(EventBlocked, "REAL_MODEL_IDENTITY"):
                write_synthetic_event(forged, Path(tmp))
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_verifier_rejects_rehashed_synthetic_label_bypass(self):
        event = self.build()
        with tempfile.TemporaryDirectory() as tmp:
            file, _ = write_synthetic_event(event, Path(tmp))
            for change in ("market_outcome", "raw_ref", "extra_field"):
                forged = copy.deepcopy(event)
                if change == "market_outcome":
                    forged["market_outcome"] = "synthetic-forged-outcome"
                elif change == "raw_ref":
                    forged["source"]["raw_ref"] = "https://example.com/not-synthetic"
                else:
                    forged["extra_field"] = "synthetic-only"
                payload = {"record": forged, "record_sha256": canonical_sha256(forged)}
                file.write_bytes(canonical_json_bytes(payload) + b"\n")
                with self.subTest(change=change), self.assertRaises(EventBlocked):
                    verify_synthetic_event(file)
            blocked = write_blocked_receipt(event_id="SYNTHETIC-FXNS-20261008",
                reason="SOURCE_QUALIFICATION_BLOCKED", directory=Path(tmp))
            receipt = verify_synthetic_event(blocked)
            forged = copy.deepcopy(receipt)
            forged["decision"] = "NO_TRADE"
            blocked.write_bytes(canonical_json_bytes({"record": forged,
                "record_sha256": canonical_sha256(forged)}) + b"\n")
            with self.assertRaisesRegex(EventBlocked, "BLOCKED_RECEIPT_CANNOT_BE_A_DECISION"):
                verify_synthetic_event(blocked)

if __name__ == "__main__": unittest.main()
