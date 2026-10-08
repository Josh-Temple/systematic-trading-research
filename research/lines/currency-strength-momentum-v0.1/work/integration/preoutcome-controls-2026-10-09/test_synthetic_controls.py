"""Offline I2 *model* tests. No real keys, rates, source fetch, OS sandbox or authorization.

These tests independently model the CSM D signed I/E identity contract; they do not
import/replace the actual Packet D verifier or confer permission to access outcomes.
The RSA key below was already published as a synthetic test fixture in Packet D #34.
"""
import base64
import copy
import hashlib
import hmac
import json
import re
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Deliberately public TEST-ONLY key, not a production trust root.
N = int("f12c454cafaa2a3cc5d755f9db98ca193944475b5ed676efb0facd2a0ebcce35272e6721d8ac76a15a136b01e41fd481b3926cdc95f48f27680cd57a2fe9ae13f0bc79d31d616b1cbb5b028c86f69aecf93ad84efc426ff3b77245d9e38ed6868069f84adddb175a1eddb99983da0a8ba8975d047e8fb50390f6a09c723bd84b855d65995738c247bddc199af39ae49324305be07cc587ba074bbe6f72af3cb516734036a8e20998589cb37256cc32ccd5275d0a3dedb3ef320d334ae9dd8e6d78391021f0f58288a74a625c32e66f4023710a378c068ddcd1bd59976ef2722bb662cd4a4241ac21a47f134568a5157eeee81d4b3ccbf39e8a4ded3def126833", 16)
D = int("4bf6a04b53c75aef72776d96ba22e9814166eebcea65cde7988c9ec3c1099a3fe6bbf873123edc4cdd44e17f227e1e1ece53702398be03bb2b4c638f4d7922c218211d94301c67b310964d7abae6010d64413331c9c61962202587b7e633af0185801b5b657ee55f96fa4ac3fe6256d0ff84d1a121461d83668d3030a6d08fc3394dc7a94ed00c9bfaecd94c8ce147c3c154d534b7163f36b2ca8f929ff20ca69ace7d6197c527a4cb5fc773ae19668945df5a1436cea37b561c560566d360737f660c73921e06c46a5bfed26936be53dc751dbfe2a911f88eeb1bc1847754e759899e84280df1cfa055a555e60c20dab7d60dd25b662790b50443f017946a7d", 16)
ALG = "RSASSA-PKCS1-v1_5-SHA256"
PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")
NOW = datetime(2026, 10, 9, 0, 0, tzinfo=timezone.utc)
I_CURRENT = "a" * 40   # deliberately fictional identities, NOT GitHub head hashes
E_CURRENT = "b" * 40
D_CURRENT = "c" * 64
ISSUED = "2026-10-08T22:00:00+00:00"
EXPIRES = "2026-10-09T10:00:00+00:00"


class Denied(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sign(payload, key_id):
    meta = dict(key_id=key_id, algorithm=ALG, issued_at=ISSUED, expires_at=EXPIRES)
    msg = canonical({"payload": payload, **meta})
    length = (N.bit_length() + 7) // 8
    info = PREFIX + hashlib.sha256(msg).digest()
    padded = b"\x00\x01" + b"\xff" * (length - 3 - len(info)) + b"\x00" + info
    raw = pow(int.from_bytes(padded, "big"), D, N).to_bytes(length, "big")
    return {"payload": payload, "signature": {**meta, "signature_b64": base64.b64encode(raw).decode()}}


def keys():
    return {
        "test-I": {"principal_id": "synthetic-integrator", "role": "integrator", "revoked": False,
                   "valid_until": "2026-12-31T00:00:00+00:00", "n_hex": format(N, "x"), "e": 65537},
        "test-E": {"principal_id": "synthetic-auditor", "role": "independent_auditor", "revoked": False,
                   "valid_until": "2026-12-31T00:00:00+00:00", "n_hex": format(N, "x"), "e": 65537},
    }


def verify_envelope(env, trust, role):
    if not isinstance(env, dict) or not isinstance(env.get("signature"), dict):
        raise Denied("unsigned")
    meta = env["signature"]
    key = trust.get(meta.get("key_id"))
    if not key or key.get("revoked") or key.get("role") != role:
        raise Denied("untrusted-role-or-revoked")
    if not isinstance(env.get("payload"), dict) or env["payload"].get("signer_principal_id") != key["principal_id"]:
        raise Denied("principal")
    if meta.get("algorithm") != ALG:
        raise Denied("algorithm")
    try:
        issued = datetime.fromisoformat(meta["issued_at"])
        expires = datetime.fromisoformat(meta["expires_at"])
        key_end = datetime.fromisoformat(key["valid_until"])
        if any(t.tzinfo is None for t in (issued, expires, key_end)):
            raise ValueError("naive time")
    except (KeyError, TypeError, ValueError) as exc:
        raise Denied("time-format") from exc
    if not (issued <= NOW < expires <= key_end) or (expires - issued).total_seconds() > 86400:
        raise Denied("expired-or-invalid")
    try:
        raw = base64.b64decode(meta["signature_b64"], validate=True)
    except (KeyError, ValueError) as exc:
        raise Denied("signature-format") from exc
    modulus, exponent = int(key["n_hex"], 16), key["e"]
    length = (modulus.bit_length() + 7) // 8
    if modulus.bit_length() < 2048 or len(raw) != length or int.from_bytes(raw, "big") >= modulus:
        raise Denied("signature-length-or-key")
    signed = {"payload": env["payload"], **{k: meta[k] for k in ("key_id", "algorithm", "issued_at", "expires_at")}}
    info = PREFIX + hashlib.sha256(canonical(signed)).digest()
    expected = b"\x00\x01" + b"\xff" * (length - 3 - len(info)) + b"\x00" + info
    got = pow(int.from_bytes(raw, "big"), exponent, modulus).to_bytes(length, "big")
    if not hmac.compare_digest(got, expected):
        raise Denied("bad-signature")
    return env["payload"]


def fixture():
    e = {"signer_principal_id": "synthetic-auditor", "head_sha": E_CURRENT,
         "status": "PASS", "recommendation": "ALLOW_I2", "audited_d_sha256": D_CURRENT}
    signed_e = sign(e, "test-E")
    gate = {"signer_principal_id": "synthetic-integrator", "head_sha": I_CURRENT,
            "gate_status": "PASS", "market_outcome_access": True,
            "human_final_approval": True, "exposure_human_disposition": True,
            "outcome_access_operator_id": "synthetic-operator-001", "auditor": signed_e,
            "auditor_envelope_sha256": digest(canonical(signed_e))}
    return sign(gate, "test-I"), keys()


def check_gate(gate, trust, *, current_i=I_CURRENT, current_e=E_CURRENT, current_d=D_CURRENT):
    """Toy independent oracle; no integration with production CSM or real HEAD APIs."""
    i = verify_envelope(gate, trust, "integrator")
    if not (re.fullmatch(r"[0-9a-f]{40}", i.get("head_sha", "")) and i["head_sha"] == current_i):
        raise Denied("stale-i-head")
    if i.get("gate_status") != "PASS" or i.get("market_outcome_access") is not True:
        raise Denied("closed-gate")
    if i.get("human_final_approval") is not True or i.get("exposure_human_disposition") is not True:
        raise Denied("human-approval")
    if not i.get("outcome_access_operator_id"):
        raise Denied("unnamed-operator")
    e_env = i.get("auditor")
    if not isinstance(e_env, dict) or i.get("auditor_envelope_sha256") != digest(canonical(e_env)):
        raise Denied("auditor-envelope-binding")
    e = verify_envelope(e_env, trust, "independent_auditor")
    if e["signer_principal_id"] == i["signer_principal_id"]:
        raise Denied("not-independent")
    if e.get("head_sha") != current_e:
        raise Denied("stale-e-head")
    if e.get("status") != "PASS" or e.get("recommendation") != "ALLOW_I2":
        raise Denied("e-not-authorizing")
    if e.get("audited_d_sha256") != current_d:
        raise Denied("stale-d-hash")
    return True


def resign_gate(gate, **updates):
    payload = copy.deepcopy(gate["payload"])
    payload.update(updates)
    return sign(payload, "test-I")


class AttemptLedger:
    """Temporary hash-chain proof only; anchor has no OS/enclave protection."""
    def __init__(self, path):
        self.path = Path(path)

    def append(self, event, result, *, fail=False):
        if fail:
            raise OSError("injected-write-failure")
        prev = "0" * 64
        if self.path.exists() and self.path.read_text():
            prev = json.loads(self.path.read_text().splitlines()[-1])["hash"]
        value = {"event": event, "result": result, "prev": prev}
        value["hash"] = digest(canonical(value))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(value, sort_keys=True) + "\n")
            f.flush()
            import os
            os.fsync(f.fileno())
        return value["hash"]

    def verify(self, external_anchor):
        prev = "0" * 64
        for line in self.path.read_text().splitlines():
            item = json.loads(line)
            h = item.pop("hash")
            if item["prev"] != prev or digest(canonical(item)) != h:
                raise Denied("ledger-tampered")
            prev = h
        if prev != external_anchor:
            raise Denied("anchor-mismatch")
        return True


def simulated_access(event, target, allowed_root, ledger):
    """Policy simulation (NOT a real open/connect/spawn system-call denial)."""
    root = Path(allowed_root).resolve()
    destination = Path(target).resolve()
    allow = event in ("read", "write") and (destination == root or root in destination.parents)
    ledger.append(f"{event}:{destination}", "ALLOWED" if allow else "DENIED")
    if not allow:
        raise PermissionError("synthetic-denial")
    return True


class SignedHeadAndRoleTests(unittest.TestCase):
    def setUp(self):
        self.gate, self.trust = fixture()

    def test_baseline_toy_envelope_accepts(self):
        self.assertTrue(check_gate(self.gate, self.trust))

    def test_current_i_head_mismatch_is_denied(self):
        with self.assertRaisesRegex(Denied, "stale-i-head"):
            check_gate(self.gate, self.trust, current_i="d" * 40)

    def test_old_e_head_is_denied(self):
        with self.assertRaisesRegex(Denied, "stale-e-head"):
            check_gate(self.gate, self.trust, current_e="e" * 40)

    def test_old_d_hash_is_denied(self):
        with self.assertRaisesRegex(Denied, "stale-d-hash"):
            check_gate(self.gate, self.trust, current_d="f" * 64)

    def test_same_signer_and_auditor_is_denied(self):
        self.trust["test-E"]["principal_id"] = "synthetic-integrator"
        e = self.gate["payload"]["auditor"]["payload"].copy()
        e["signer_principal_id"] = "synthetic-integrator"
        signed_e = sign(e, "test-E")
        forged = resign_gate(self.gate, auditor=signed_e, auditor_envelope_sha256=digest(canonical(signed_e)))
        with self.assertRaisesRegex(Denied, "not-independent"):
            check_gate(forged, self.trust)

    def test_wrong_role(self):
        self.trust["test-E"]["role"] = "integrator"
        with self.assertRaisesRegex(Denied, "untrusted-role"):
            check_gate(self.gate, self.trust)

    def test_revoked_key(self):
        self.trust["test-I"]["revoked"] = True
        with self.assertRaisesRegex(Denied, "untrusted-role"):
            check_gate(self.gate, self.trust)

    def test_expired_key(self):
        self.trust["test-I"]["valid_until"] = "2026-10-09T00:00:00+00:00"
        with self.assertRaisesRegex(Denied, "expired"):
            check_gate(self.gate, self.trust)

    def test_expired_signed_receipt(self):
        bad = copy.deepcopy(self.gate)
        bad["signature"]["expires_at"] = "2026-10-08T23:00:00+00:00"
        with self.assertRaisesRegex(Denied, "expired"):
            check_gate(bad, self.trust)

    def test_forged_signature(self):
        bad = copy.deepcopy(self.gate)
        bad["payload"]["gate_status"] = "CLOSED"
        with self.assertRaisesRegex(Denied, "bad-signature"):
            check_gate(bad, self.trust)

    def test_unsigned_pass_is_denied(self):
        with self.assertRaisesRegex(Denied, "unsigned"):
            check_gate({"payload": self.gate["payload"]}, self.trust)

    def test_closed_gate(self):
        with self.assertRaisesRegex(Denied, "closed-gate"):
            check_gate(resign_gate(self.gate, gate_status="CLOSED"), self.trust)

    def test_access_false(self):
        with self.assertRaisesRegex(Denied, "closed-gate"):
            check_gate(resign_gate(self.gate, market_outcome_access=False), self.trust)

    def test_unapproved_pass(self):
        with self.assertRaisesRegex(Denied, "human-approval"):
            check_gate(resign_gate(self.gate, human_final_approval=False), self.trust)

    def test_unresolved_exposure(self):
        with self.assertRaisesRegex(Denied, "human-approval"):
            check_gate(resign_gate(self.gate, exposure_human_disposition=False), self.trust)

    def test_unnamed_operator(self):
        with self.assertRaisesRegex(Denied, "unnamed-operator"):
            check_gate(resign_gate(self.gate, outcome_access_operator_id=""), self.trust)

    def test_auditor_negative_recommendation(self):
        e = self.gate["payload"]["auditor"]["payload"].copy()
        e["recommendation"] = "BLOCKED"
        s = sign(e, "test-E")
        g = resign_gate(self.gate, auditor=s, auditor_envelope_sha256=digest(canonical(s)))
        with self.assertRaisesRegex(Denied, "e-not-authorizing"):
            check_gate(g, self.trust)

    def test_auditor_envelope_mutation(self):
        g = copy.deepcopy(self.gate)
        g["payload"]["auditor"]["payload"]["status"] = "BLOCKED"
        with self.assertRaisesRegex(Denied, "bad-signature"):
            check_gate(g, self.trust)

    def test_untrusted_signer(self):
        self.trust.pop("test-I")
        with self.assertRaisesRegex(Denied, "untrusted-role"):
            check_gate(self.gate, self.trust)


class StorageAndDenialSimulationTests(unittest.TestCase):
    def test_simulated_file_read_write_and_event_denials_recorded(self):
        with tempfile.TemporaryDirectory(prefix="csm-synthetic-") as tmp:
            base = Path(tmp) / "allowed"
            base.mkdir()
            log = AttemptLedger(Path(tmp) / "attempts.jsonl")
            self.assertTrue(simulated_access("read", base / "toy.txt", base, log))
            for event, target in (("read", Path(tmp) / "forbidden.txt"),
                                  ("write", Path(tmp) / "forbidden-write.txt"),
                                  ("connect", base / "no-socket"),
                                  ("spawn", base / "no-subprocess")):
                with self.assertRaises(PermissionError):
                    simulated_access(event, target, base, log)
            records = [json.loads(s) for s in log.path.read_text().splitlines()]
            self.assertEqual([r["result"] for r in records], ["ALLOWED", "DENIED", "DENIED", "DENIED", "DENIED"])
            self.assertTrue(log.verify(records[-1]["hash"]))

    def test_local_readback_new_instance_and_tamper_detection(self):
        with tempfile.TemporaryDirectory(prefix="csm-synthetic-") as tmp:
            p = Path(tmp) / "attempts.jsonl"
            log = AttemptLedger(p)
            log.append("read:fictional-path", "DENIED")
            anchor = log.append("spawn:fictional-process", "DENIED")
            self.assertTrue(AttemptLedger(p).verify(anchor))  # new object, NOT OS restart
            data = p.read_text().replace("spawn:fictional-process", "spawn:changed")
            p.write_text(data)
            with self.assertRaisesRegex(Denied, "ledger-tampered"):
                AttemptLedger(p).verify(anchor)

    def test_complete_chain_rewrite_detected_by_saved_anchor(self):
        with tempfile.TemporaryDirectory(prefix="csm-synthetic-") as tmp:
            p = Path(tmp) / "attempts.jsonl"
            log = AttemptLedger(p)
            original = log.append("read:fictional-path", "DENIED")
            p.unlink()  # the experiment has full write access; this is not an append-only system
            new = log.append("read:fictional-path", "ALLOWED")
            self.assertNotEqual(original, new)
            with self.assertRaisesRegex(Denied, "anchor-mismatch"):
                AttemptLedger(p).verify(original)

    def test_failed_append_cannot_claim_success(self):
        with tempfile.TemporaryDirectory(prefix="csm-synthetic-") as tmp:
            log = AttemptLedger(Path(tmp) / "attempts.jsonl")
            with self.assertRaises(OSError):
                log.append("unrecorded", "ALLOWED", fail=True)
            self.assertFalse(log.path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
