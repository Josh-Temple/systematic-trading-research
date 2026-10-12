"""A-authored recreations of D's R01-R14 specifications, plus new A cases.

These are NOT D's original unpublished test bytes and NOT an independent audit.
All data, requests, identities and sinks are fabricated entirely offline.
"""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from hashlib import sha256
import copy
from threading import Barrier, Event
import unittest

from safe_boundary import ApprovedDocument, Boundary, BoundaryStopped, DeliverySink, Policy, ReceiptSink
from test_safe_boundary import (BASE, EXCERPT, HEAD, MARKER, PATH, REPO, SAFE_BYTES,
                                document, fixture, metadata, page, paths, request)


class FailAfterPublish(DeliverySink):
    def __init__(self):
        super().__init__()
        self.calls = 0
    def publish(self, content):
        super().publish(content)
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError(MARKER)


class FailBeforePublish(DeliverySink):
    def publish(self, content):
        raise RuntimeError(MARKER)


class FailReleaseAudit(ReceiptSink):
    def append(self, *, state, reason, policy_id, operation):
        if state == "RELEASED":
            raise BoundaryStopped("AUDIT_UNAVAILABLE")
        return super().append(state=state, reason=reason, policy_id=policy_id, operation=operation)


def new_policy(**kw):
    return replace(fixture()[0].policy, **kw)


class RemediationAdversarialSyntheticTests(unittest.TestCase):
    def test_R01_race_same_sink_same_op(self):
        b, sink, receipt = fixture()
        start = Barrier(2)
        def job():
            start.wait(timeout=5)
            return b.run(request(), metadata())
        with ThreadPoolExecutor(max_workers=2) as pool:
            outs = list(pool.map(lambda _: job(), range(2)))
        self.assertEqual(len(sink.delivered), 1)
        self.assertEqual(sum(o is not None for o in outs), 1)
        self.assertEqual(sum(x["state"] == "RELEASED" for x in receipt.receipts), 1)

    def test_R02_partial_publish_unknown_no_retry(self):
        p = new_policy()
        sink = FailAfterPublish(); receipts = ReceiptSink()
        b = Boundary(p, sink, receipts)
        self.assertIsNone(b.run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)
        self.assertIsNone(b.run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)
        self.assertEqual([x["state"] for x in receipts.receipts], ["RESERVED", "UNKNOWN"])

    def test_R03_pre_publish_error_no_false_released(self):
        p = new_policy()
        sink = FailBeforePublish(); receipts = ReceiptSink()
        self.assertIsNone(Boundary(p, sink, receipts).run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 0)
        self.assertNotIn("RELEASED", [x["state"] for x in receipts.receipts])

    def test_R04_approval_mapping_mutation_rejected(self):
        b, sink, _ = fixture()
        with self.assertRaises(TypeError):
            b.policy.approved_documents[PATH] = b.policy.approved_documents[PATH]
        self.assertIn(b"approved_excerpt", b.run(request("SAFE_DOCUMENT"), document()))
        self.assertNotIn(MARKER.encode(), sink.delivered[0])

    def test_R05_new_boundary_same_sink_cannot_duplicate(self):
        b, sink, receipt = fixture()
        self.assertIsNotNone(b.run(request(), metadata()))
        self.assertIsNone(Boundary(b.policy, sink, receipt).run(request(), metadata()))
        self.assertEqual(len(sink.delivered), 1)

    def test_R06_unapproved_request_id(self):
        b, sink, _ = fixture()
        q = request(); q["request_id"] = MARKER
        self.assertIsNone(b.run(q, metadata()))
        self.assertEqual(sink.delivered, [])

    def test_R07_nested_state_type(self):
        b, sink, _ = fixture()
        x = metadata(); x["pages"][0]["items"][0]["draft"] = {"raw": MARKER}
        self.assertIsNone(b.run(request(), x)); self.assertEqual(sink.delivered, [])

    def test_R08_late_page_unapproved(self):
        b, sink, _ = fixture()
        x = paths(); x["pages"] = [page([{"path": PATH, "blob_oid": "c"*40}], next_cursor="x"),
                                  page([{"path": MARKER, "blob_oid": "c"*40}], cursor="x")]
        self.assertIsNone(b.run(request("FILE_PATHS"), x)); self.assertEqual(sink.delivered, [])

    def test_R09_cursor_loop(self):
        b, sink, _ = fixture()
        x = paths(); x["pages"] = [page([{"path":PATH,"blob_oid":"c"*40}], next_cursor="x"),
                                  page([{"path":PATH,"blob_oid":"c"*40}], cursor="x",next_cursor="x"),
                                  page([{"path":PATH,"blob_oid":"c"*40}], cursor="x")]
        self.assertIsNone(b.run(request("FILE_PATHS"), x)); self.assertFalse(sink.delivered)

    def test_R10_large_fictional_document(self):
        b, sink, _ = fixture()
        self.assertIsNone(b.run(request("SAFE_DOCUMENT"), document(b"X"*100000)))
        self.assertFalse(sink.delivered)

    def test_R11_trusted_approval_input_required(self):
        with self.assertRaises(BoundaryStopped):
            ApprovedDocument(PATH, sha256(SAFE_BYTES).hexdigest(), MARKER)
        with self.assertRaises(BoundaryStopped):
            ApprovedDocument(PATH, sha256(SAFE_BYTES).hexdigest(), MARKER,
                             approval_id="SYNTH-APPROVAL-001",
                             excerpt_sha256=sha256(EXCERPT.encode()).hexdigest())
        # A syntactically matching *fabricated* approval is still an external
        # custody and independent-content-review gap, NOT an operational pass.

    def test_R12_policy_id_reject_free_text(self):
        with self.assertRaises(BoundaryStopped):
            new_policy(policy_id="bad-"+MARKER)

    def test_R13_logical_metadata_contradiction(self):
        b, sink, _ = fixture()
        x = metadata(); x["pages"][0]["items"][0].update({"state":"OPEN", "merged":True, "draft":True})
        self.assertIsNone(b.run(request(), x)); self.assertFalse(sink.delivered)

    def test_R14_expected_blob_pair_mismatch(self):
        b, sink, _ = fixture()
        x = paths(); x["pages"][0]["items"][0]["blob_oid"] = "d"*40
        self.assertIsNone(b.run(request("FILE_PATHS"), x)); self.assertFalse(sink.delivered)

    def test_A01_three_concurrent(self):
        b, sink, _ = fixture()
        start = Barrier(3)
        def job():
            start.wait(timeout=5)
            return b.run(request(), metadata())
        with ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(lambda _: job(), range(3)))
        self.assertEqual(sum(v is not None for v in results), 1)
        self.assertEqual(len(sink.delivered), 1)

    def test_A02_same_request_different_operation(self):
        b, sink, _ = fixture()
        q1=request(); q1["approved_request_id"]="SYN-001"
        q2=request("FILE_PATHS"); q2["approved_request_id"]="SYN-001"
        self.assertIsNotNone(b.run(q1,metadata()))
        self.assertIsNotNone(b.run(q2,paths()))
        self.assertEqual(len(sink.delivered),2)

    def test_A03_different_document_same_operation(self):
        b, sink, receipt=fixture()
        new_path="approved/fictional-two.txt"
        new_body=b"FICTIONAL TWO"
        new_excerpt="Fictional second approved schema."
        approval=ApprovedDocument(new_path,sha256(new_body).hexdigest(),new_excerpt,
                                  approval_id="SYNTH-APPROVAL-002",
                                  excerpt_sha256=sha256(new_excerpt.encode()).hexdigest())
        docs=dict(b.policy.approved_documents);docs[new_path]=approval
        pol=replace(b.policy,approved_documents=docs,allowed_paths=frozenset({PATH,new_path}))
        new_b=Boundary(pol,sink,receipt)
        self.assertIsNotNone(new_b.run(request("SAFE_DOCUMENT"),document()))
        d=document(new_body); d["path"]=new_path
        self.assertIsNotNone(new_b.run(request("SAFE_DOCUMENT"),d))
        self.assertEqual(len(sink.delivered),2)

    def test_A04_distinct_trusted_request_ids(self):
        b,sink,_=fixture()
        q=request();q["approved_request_id"]="SYN-001"
        q2=request();q2["approved_request_id"]="SYN-002"
        self.assertIsNotNone(b.run(q,metadata()))
        self.assertIsNotNone(b.run(q2,metadata()))
        self.assertEqual(len(sink.delivered),2)

    def test_A05_delayed_ack_no_concurrent_duplicate(self):
        class SlowSink(DeliverySink):
            def __init__(self):
                super().__init__(); self.inside=Event(); self.release=Event()
            def publish(self, content):
                self.inside.set()
                if not self.release.wait(3):
                    raise RuntimeError("synthetic timeout")
                return super().publish(content)
        b,_,r=fixture(); sink=SlowSink();b=Boundary(b.policy,sink,r)
        with ThreadPoolExecutor(max_workers=2) as pool:
            one=pool.submit(b.run,request(),metadata())
            self.assertTrue(sink.inside.wait(2))
            two=pool.submit(b.run,request(),metadata())
            sink.release.set()
            self.assertIsNotNone(one.result(timeout=5))
            self.assertIsNone(two.result(timeout=5))
        self.assertEqual(len(sink.delivered),1)

    def test_A06_before_publish_failure(self):
        b,_,r=fixture(); sink=FailBeforePublish();b=Boundary(b.policy,sink,r)
        self.assertIsNone(b.run(request(),metadata()))
        self.assertEqual(sink._operations[next(iter(sink._operations))],"UNKNOWN")
        self.assertNotIn("RELEASED",[e["state"] for e in r.receipts])

    def test_A07_after_publish_failure_and_retry(self):
        self.test_R02_partial_publish_unknown_no_retry()

    def test_A08_audit_failure_after_publish(self):
        b,_,_=fixture(); sink=DeliverySink();r=FailReleaseAudit();b=Boundary(b.policy,sink,r)
        self.assertIsNone(b.run(request(),metadata()))
        self.assertEqual(len(sink.delivered),1)
        self.assertIsNone(b.run(request(),metadata()))
        self.assertEqual(len(sink.delivered),1)
        self.assertEqual(sink._operations[next(iter(sink._operations))],"UNKNOWN")

    def test_A09_registry_unknown_disclosed_no_global_guarantee(self):
        b,sink,r=fixture()
        self.assertIsNotNone(b.run(request(),metadata()))
        self.assertIsNone(Boundary(b.policy,sink,r).run(request(),metadata()))
        self.assertEqual(list(sink._operations.values()),["RELEASED"])
        # A newly constructed unrelated sink is NOT known to share state:
        # this is a declared non-guarantee; no real host adapter is supplied.

    def test_A10_deep_mutable_policy_reference(self):
        docs={PATH:fixture()[0].policy.approved_documents[PATH]}
        p=new_policy(approved_documents=docs)
        docs.clear()
        self.assertIn(PATH,p.approved_documents)
        with self.assertRaises(TypeError):
            p.approved_documents[PATH]=None

    def test_A11_path_blob_and_extra_mode_tree(self):
        b,sink,_=fixture()
        x=paths();x["pages"][0]["items"][0]["mode"]="100644"
        self.assertIsNone(b.run(request("FILE_PATHS"),x))
        y=paths();y["pages"][0]["items"][0]["tree_oid"]="d"*40
        self.assertIsNone(b.run(request("FILE_PATHS"),y))
        self.assertFalse(sink.delivered)

    def test_A12_large_partial_stream_type_mix(self):
        b,sink,_=fixture();x=paths();x["pages"] = [page([{"path":PATH,"blob_oid":"c"*40}],next_cursor="missing")]
        self.assertIsNone(b.run(request("FILE_PATHS"),x))
        y=metadata();y["stream_chunks"]=["partial",MARKER]
        self.assertIsNone(b.run(request(),y))
        z=metadata();z["pages"][0]["items"][0]["draft"]=1
        self.assertIsNone(b.run(request(),z))
        self.assertFalse(sink.delivered)

if __name__ == "__main__":
    unittest.main(verbosity=2)
