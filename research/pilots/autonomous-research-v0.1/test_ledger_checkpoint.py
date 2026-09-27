import copy
import tempfile
import unittest
from pathlib import Path

import evaluator


KEY = b"phase-a-checkpoint-key-32-bytes!!"


class LedgerCheckpointTests(unittest.TestCase):
    def _ledger(self, path: Path) -> None:
        evaluator.append_ledger(path, {"kind": "evaluation", "n": 1})
        evaluator.append_ledger(path, {"kind": "evaluation", "n": 2})

    def test_checkpoint_verifies_exact_ledger_state(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            self._ledger(path)
            checkpoint = evaluator.create_ledger_checkpoint(path, KEY)
            state = evaluator.verify_ledger_checkpoint(path, checkpoint, KEY)
            self.assertEqual(state["events"], 2)
            self.assertEqual(state["last_event_hash"], checkpoint["last_event_hash"])
            self.assertNotIn("key", checkpoint)

    def test_checkpoint_detects_suffix_truncation(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            self._ledger(path)
            checkpoint = evaluator.create_ledger_checkpoint(path, KEY)

            first = path.read_text(encoding="utf-8").splitlines()[0]
            path.write_text(first + "\n", encoding="utf-8")

            # The remaining chain is locally valid...
            self.assertEqual(evaluator.verify_ledger(path)["events"], 1)
            # ...but it no longer matches the externally protected checkpoint.
            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger_checkpoint(path, checkpoint, KEY)

    def test_checkpoint_detects_appended_tail(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            self._ledger(path)
            checkpoint = evaluator.create_ledger_checkpoint(path, KEY)
            evaluator.append_ledger(path, {"kind": "evaluation", "n": 3})

            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger_checkpoint(path, checkpoint, KEY)

    def test_wrong_key_and_checkpoint_tampering_fail(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            self._ledger(path)
            checkpoint = evaluator.create_ledger_checkpoint(path, KEY)

            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger_checkpoint(
                    path,
                    checkpoint,
                    b"different-checkpoint-key-32-bytes",
                )

            changed = copy.deepcopy(checkpoint)
            changed["events"] = 999
            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.verify_ledger_checkpoint(path, changed, KEY)

    def test_short_checkpoint_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.jsonl"
            evaluator.append_ledger(path, {"kind": "evaluation", "n": 1})
            with self.assertRaises(evaluator.EvaluatorFailure):
                evaluator.create_ledger_checkpoint(path, b"short")


if __name__ == "__main__":
    unittest.main()
