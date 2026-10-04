"""No holdout file is opened until a durable, bound advancement receipt validates."""
import hashlib
import json
from pathlib import Path
from jp225_ema_screen import select_discovery_candidate

def load_holdout(path, decision_path, expected_decision_sha256, expected_binding, reader):
    receipt_bytes=Path(decision_path).read_bytes()
    if hashlib.sha256(receipt_bytes).hexdigest()!=expected_decision_sha256:
        raise PermissionError('DISCOVERY_DECISION_IDENTITY_FAILURE')
    d=json.loads(receipt_bytes)
    if (d.get('discovery_advancement') is not True or d.get('sample')!='2025_DISCOVERY' or
        d.get('packet_a')!='PASS' or d.get('independent_audit')!='PASS' or
        d.get('binding')!=expected_binding or not expected_binding or
        set(expected_binding)!={'spec_sha256','code_sha256','source_sha256','result_sha256'} or
        any(not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v)
            for v in expected_binding.values()) or
        d.get('candidate')!=select_discovery_candidate(d.get('metrics',{})) or
        d.get('candidate') is None):
        raise PermissionError('HOLDOUT_LOCKED')
    # reader must enforce 2026-01-01 <= UTC time < 2026-10-01 and selected candidate only.
    # Deliberately no concrete holdout parser until qualified holdout schema exists.
    return reader(path,d['candidate'])
