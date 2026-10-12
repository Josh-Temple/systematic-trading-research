"""New A-authored, fully fictional regression cases reconstructed from Wave D01-D21 descriptions.

Not the earlier unpublished D fixture and not an independent D acceptance.
"""
import copy
from dataclasses import replace
from hashlib import sha256
import unittest

from safe_boundary import Boundary, BoundaryStopped, DeliverySink, ReceiptSink, DeliveryAck, Policy, ApprovedDocument
from test_safe_boundary import (BASE, EXCERPT, HEAD, PATH, REPO, SAFE_BYTES,
                                fixture, request, metadata, page, paths, document, item)


class EightFindingsSynthetic(unittest.TestCase):
    def blocked(self, operation, payload, sink=None, receipts=None, q=None, policy=None):
        b, default_sink, default_receipts = fixture()
        sink = sink if sink is not None else default_sink
        receipts = receipts if receipts is not None else default_receipts
        b = Boundary(policy if policy is not None else b.policy, sink, receipts)
        self.assertIsNone(b.run(q if q is not None else request(operation), payload))
        return b, sink, receipts

    def test_D01_duplicate_file_identity_across_pages(self):
        x = paths()
        x["pages"] = [page([{"path": PATH, "blob_oid": "c"*40}], next_cursor="p2"),
                      page([{"path": PATH, "blob_oid": "c"*40}], cursor="p2")]
        _, sink, _ = self.blocked("FILE_PATHS", x)
        self.assertEqual(sink.delivered, [])

    def test_D02_duplicate_file_identity_same_page(self):
        x = paths()
        x["pages"][0]["items"].append(dict(x["pages"][0]["items"][0]))
        _, sink, _ = self.blocked("FILE_PATHS", x)
        self.assertFalse(sink.delivered)

    def test_D03_duplicate_metadata_identity(self):
        x = metadata()
        x["pages"][0]["items"].append(dict(x["pages"][0]["items"][0]))
        _, sink, _ = self.blocked("PR_METADATA", x)
        self.assertFalse(sink.delivered)

    def test_D04_noop_publish_no_ack(self):
        class Noop(DeliverySink):
            def publish(self, content):
                return None
        sink = Noop()
        b, sink, receipt = self.blocked("PR_METADATA", metadata(), sink=sink)
        self.assertFalse(sink.delivered)
        self.assertEqual(list(sink._operations.values()), ["UNKNOWN"])
        self.assertNotIn("RELEASED", [e["state"] for e in receipt.receipts])
        self.assertIsNone(b.run(request(), metadata()))

    def test_D05_noop_audit_return(self):
        class Noop(ReceiptSink):
            def append(self, *, state, reason, policy_id, operation):
                return None
        _, sink, receipt = self.blocked("PR_METADATA", metadata(), receipts=Noop())
        self.assertFalse(sink.delivered)
        self.assertFalse(receipt.receipts)

    def test_D06_equal_but_nonstring_head_repo(self):
        class Equal:
            def __eq__(self, x): return True
        x = metadata()
        x["pages"][0]["items"][0]["head_repo"] = Equal()
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D07_equal_but_nonstring_base_repo(self):
        class Equal:
            def __eq__(self, x): return True
        x = metadata()
        x["pages"][0]["items"][0]["base_repo"] = Equal()
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D08_equal_but_nonstring_post_head(self):
        class Equal:
            def __eq__(self, x): return True
        x = metadata()
        x["post_head_oid"] = Equal()
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D09_cursor_object_rejected(self):
        x = paths()
        x["pages"][0]["next_cursor"] = object()
        self.assertFalse(self.blocked("FILE_PATHS", x)[1].delivered)

    def test_D10_boolean_pr_number_rejected(self):
        x = metadata()
        x["pr_number"] = True
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D11_bool_or_nonstring_blob_rejected(self):
        x = paths()
        x["pages"][0]["items"][0]["blob_oid"] = True
        self.assertFalse(self.blocked("FILE_PATHS", x)[1].delivered)

    def test_D12_mutating_input_mapping_does_not_rewrite_approval(self):
        b, _, _ = fixture()
        docs = dict(b.policy.approved_documents)
        p = replace(b.policy, approved_documents=docs)
        docs.clear()
        self.assertIn(PATH, p.approved_documents)

    def test_D13_bytearray_body_rejected(self):
        x = document()
        x["body"] = bytearray(SAFE_BYTES)
        self.assertFalse(self.blocked("SAFE_DOCUMENT", x)[1].delivered)

    def test_D14_unsafe_request_id_rejected(self):
        q = request()
        q["approved_request_id"] = "SYN-" + "A"*40
        self.assertFalse(self.blocked("PR_METADATA", metadata(), q=q)[1].delivered)

    def test_D15_audit_failure_no_retry_after_publish(self):
        class ReleaseError(ReceiptSink):
            def append(self, *, state, reason, policy_id, operation):
                if state == "RELEASED": raise RuntimeError("synthetic")
                return super().append(state=state, reason=reason, policy_id=policy_id, operation=operation)
        receipts = ReleaseError()
        b, sink, _ = self.blocked("PR_METADATA", metadata(), receipts=receipts)
        self.assertEqual(len(sink.delivered), 1)
        self.assertIsNone(b.run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)
        self.assertEqual(list(sink._operations.values()), ["UNKNOWN"])

    def test_D16_valid_closed_unmerged_metadata(self):
        b, sink, _ = fixture()
        x = metadata()
        x["pages"][0]["items"][0].update(state="CLOSED", merged=False, draft=False)
        self.assertIsNotNone(b.run(request(), x))
        self.assertEqual(len(sink.delivered), 1)

    def test_D17_merged_and_draft_inconsistent(self):
        x = metadata()
        x["pages"][0]["items"][0].update(state="CLOSED", merged=True, draft=True)
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D18_unknown_nested_field_rejected(self):
        x = metadata()
        x["pages"][0]["items"][0]["body"] = "fictional"
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_D19_shared_registry_no_duplicate(self):
        b, sink, receipts = fixture()
        self.assertIsNotNone(b.run(request(), metadata()))
        self.assertIsNone(Boundary(b.policy, sink, receipts).run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)

    def test_D20_fabricated_approval_not_independent_custody(self):
        # Demonstrates a LIMITATION, not proof of an independent signer.
        fake = ApprovedDocument(PATH, sha256(SAFE_BYTES).hexdigest(), EXCERPT,
                                approval_id="SYNTH-FABRICATED",
                                excerpt_sha256=sha256(EXCERPT.encode()).hexdigest())
        self.assertEqual(fake.approval_id, "SYNTH-FABRICATED")

    def test_D21_separate_sinks_not_exactly_once(self):
        # Demonstrates a LIMITATION across sink/registry scopes.
        b1, sink1, _ = fixture()
        b2, sink2, _ = fixture()
        self.assertIsNotNone(b1.run(request(), metadata()))
        self.assertIsNotNone(b2.run(request(), metadata()))
        self.assertEqual((len(sink1.delivered), len(sink2.delivered)), (1, 1))

    def test_A13_distinct_approved_file_paths(self):
        b, sink, receipts = fixture()
        other = "approved/second.txt"
        p = replace(b.policy, allowed_paths=frozenset({PATH, other}),
                    expected_blob_oids={PATH: "c"*40, other: "d"*40})
        x = paths()
        x["pages"][0]["items"].append({"path": other, "blob_oid": "d"*40})
        out = Boundary(p, sink, receipts).run(request("FILE_PATHS"), x)
        self.assertIsNotNone(out)
        self.assertEqual(len(sink.delivered), 1)

    def test_A14_unduplicated_single_metadata(self):
        b, sink, _ = fixture()
        self.assertIsNotNone(b.run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)

    def test_A15_valid_sink_ack_exact(self):
        sink = DeliverySink()
        ack = sink.publish(b"synthetic")
        self.assertEqual(type(ack), DeliveryAck)
        self.assertEqual(ack.index, 0)
        self.assertEqual(ack.content_sha256, sha256(b"synthetic").hexdigest())

    def test_A16_delivery_recorded_ack_missing(self):
        class LostAck(DeliverySink):
            def publish(self, content):
                super().publish(content)
                return None
        sink = LostAck()
        b, _, _ = self.blocked("PR_METADATA", metadata(), sink=sink)
        self.assertEqual(len(sink.delivered), 1)
        self.assertEqual(list(sink._operations.values()), ["UNKNOWN"])
        self.assertIsNone(b.run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)

    def test_A17_release_audit_noop_after_publish(self):
        class LostReceipt(ReceiptSink):
            def append(self, *, state, reason, policy_id, operation):
                if state == "RELEASED": return None
                return super().append(state=state, reason=reason, policy_id=policy_id, operation=operation)
        r = LostReceipt()
        b, sink, receipts = self.blocked("PR_METADATA", metadata(), receipts=r)
        self.assertEqual(len(sink.delivered), 1)
        self.assertEqual(list(sink._operations.values()), ["UNKNOWN"])
        self.assertNotIn("RELEASED", [e["state"] for e in receipts.receipts])
        self.assertIsNone(b.run(request(), metadata()))

    def test_A18_unicode_path_policy_rejected(self):
        b, _, _ = fixture()
        with self.assertRaises(BoundaryStopped):
            replace(b.policy, allowed_paths=frozenset({"approved/ｆake.txt"}))

    def test_A19_foreign_object_envelope_repo_rejected(self):
        class Equal:
            def __eq__(self, x): return True
        x = metadata()
        x["repository"] = Equal()
        self.assertFalse(self.blocked("PR_METADATA", x)[1].delivered)

    def test_A20_noop_publish_explicit_fake_ack(self):
        class Forged(DeliverySink):
            def publish(self, content):
                return DeliveryAck(0, sha256(content).hexdigest())
        sink = Forged()
        b, sink, _ = self.blocked("PR_METADATA", metadata(), sink=sink)
        self.assertFalse(sink.delivered)
        self.assertEqual(list(sink._operations.values()), ["UNKNOWN"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
