import unittest
from datetime import datetime, timedelta, timezone

from overlap_diagnostics import overlap_diagnostics


class TestOverlapDiagnostics(unittest.TestCase):
    def test_marks_both_events_in_overlapping_pair(self):
        t = datetime(2026, 1, 5, tzinfo=timezone.utc)
        count, share = overlap_diagnostics(
            [t, t + timedelta(minutes=10), t + timedelta(minutes=40)],
            horizon_minutes=15,
        )
        self.assertEqual(count, 2)
        self.assertAlmostEqual(share, 2 / 3)


if __name__ == "__main__":
    unittest.main()
