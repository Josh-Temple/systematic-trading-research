import math
import unittest
from datetime import datetime, timezone, timedelta

from fxns import (
    Action, Quote, Sentiment, canonical_sha256, currency_score, daily_scores,
    dedupe_exact_url, executable_return_bps, midpoint_return_bps, pair_action,
    select_quote_at_or_after, validate_classification, validate_headline_record,
    validate_model_identity, validate_signal_timing,
)

UTC = timezone.utc


class FXNSTest(unittest.TestCase):
    def test_currency_score(self):
        v = [Sentiment.APPRECIATION, Sentiment.APPRECIATION, Sentiment.DEPRECIATION]
        self.assertAlmostEqual(currency_score(v), math.log(3) - math.log(2))

    def test_neutral_labels_do_not_count(self):
        v = [Sentiment.UNCHANGED, Sentiment.NOT_MENTIONED, Sentiment.INSUFFICIENT]
        self.assertEqual(currency_score(v), 0.0)

    def test_daily_scores_reject_duplicate_ids(self):
        rows = [{"record_id":"x","EUR":"APPRECIATION","JPY":"DEPRECIATION"}] * 2
        with self.assertRaises(ValueError):
            daily_scores(rows)

    def test_long_action(self):
        self.assertEqual(pair_action(0.5, -0.2), Action.LONG)

    def test_short_action(self):
        self.assertEqual(pair_action(-0.1, 0.4), Action.SHORT)

    def test_same_sign_no_trade(self):
        self.assertEqual(pair_action(0.5, 0.1), Action.NO_TRADE)
        self.assertEqual(pair_action(-0.5, -0.1), Action.NO_TRADE)

    def test_zero_vs_positive_has_action(self):
        self.assertEqual(pair_action(0.0, 0.2), Action.SHORT)
        self.assertEqual(pair_action(0.2, 0.0), Action.LONG)

    def test_invalid_sentiment_rejected(self):
        with self.assertRaises(ValueError):
            validate_classification({"record_id":"x","EUR":"BULLISH","JPY":"UNCHANGED"})

    def test_post_cutoff_headline_rejected(self):
        cutoff = datetime(2026, 10, 7, 0, 0, tzinfo=UTC)
        r={"record_id":"1","gdelt_seen_at":"2026-10-07T00:00:01+00:00","source_domain":"x","title":"t","url":"u"}
        with self.assertRaises(ValueError):
            validate_headline_record(r, cutoff)

    def test_cutoff_headline_allowed(self):
        cutoff = datetime(2026, 10, 7, 0, 0, tzinfo=UTC)
        r={"record_id":"1","gdelt_seen_at":"2026-10-07T00:00:00+00:00","source_domain":"x","title":"t","url":"u"}
        validate_headline_record(r, cutoff)

    def test_exact_url_dedupe_preserves_first(self):
        rows=[{"url":"u","x":1},{"url":"u","x":2},{"url":"v","x":3}]
        out=dedupe_exact_url(rows)
        self.assertEqual([r["x"] for r in out],[1,3])

    def test_late_issuance_rejected(self):
        cutoff=datetime(2026,10,7,0,0,tzinfo=UTC)
        entry=cutoff+timedelta(minutes=15)
        with self.assertRaises(ValueError):
            validate_signal_timing(cutoff, entry, entry)

    def test_on_time_issuance(self):
        cutoff=datetime(2026,10,7,0,0,tzinfo=UTC)
        entry=cutoff+timedelta(minutes=15)
        validate_signal_timing(cutoff, cutoff+timedelta(minutes=14), entry)

    def test_quote_boundary_exact(self):
        target=datetime(2026,10,7,0,15,tzinfo=UTC)
        q=Quote(target, 170.00,170.02)
        self.assertEqual(select_quote_at_or_after([q],target),q)

    def test_quote_boundary_within_tolerance(self):
        target=datetime(2026,10,7,0,15,tzinfo=UTC)
        q=Quote(target+timedelta(seconds=60),170.00,170.02)
        self.assertEqual(select_quote_at_or_after([q],target),q)

    def test_quote_boundary_outside_tolerance(self):
        target=datetime(2026,10,7,0,15,tzinfo=UTC)
        q=Quote(target+timedelta(seconds=61),170.00,170.02)
        with self.assertRaises(ValueError):
            select_quote_at_or_after([q],target)

    def test_invalid_quote_rejected(self):
        with self.assertRaises(ValueError):
            Quote(datetime.now(UTC), 170.02,170.00)

    def test_long_executable_uses_ask_bid(self):
        e=Quote(datetime(2026,10,7,0,15,tzinfo=UTC),170.00,170.02)
        x=Quote(datetime(2026,10,8,0,15,tzinfo=UTC),171.00,171.02)
        got=executable_return_bps(Action.LONG,e,x)
        exp=10000*math.log(171.00/170.02)
        self.assertAlmostEqual(got,exp)

    def test_short_executable_uses_bid_ask(self):
        e=Quote(datetime(2026,10,7,0,15,tzinfo=UTC),170.00,170.02)
        x=Quote(datetime(2026,10,8,0,15,tzinfo=UTC),169.00,169.02)
        got=executable_return_bps(Action.SHORT,e,x)
        exp=10000*math.log(170.00/169.02)
        self.assertAlmostEqual(got,exp)

    def test_no_trade_requires_no_quotes(self):
        self.assertEqual(executable_return_bps(Action.NO_TRADE,None,None),0.0)
        self.assertEqual(midpoint_return_bps(Action.NO_TRADE,None,None),0.0)

    def test_midpoint_gross_is_directional(self):
        e=Quote(datetime(2026,10,7,0,15,tzinfo=UTC),170.00,170.02)
        x=Quote(datetime(2026,10,8,0,15,tzinfo=UTC),171.00,171.02)
        self.assertGreater(midpoint_return_bps(Action.LONG,e,x),0)
        self.assertLess(midpoint_return_bps(Action.SHORT,e,x),0)

    def test_model_change_rejected(self):
        with self.assertRaises(ValueError):
            validate_model_identity("GPT-5.6 Sol","GPT-6")

    def test_model_same_allowed(self):
        validate_model_identity("GPT-5.6 Sol","GPT-5.6 Sol")

    def test_canonical_hash_order_independent(self):
        self.assertEqual(canonical_sha256({"b":2,"a":1}),canonical_sha256({"a":1,"b":2}))


if __name__ == "__main__":
    unittest.main()
