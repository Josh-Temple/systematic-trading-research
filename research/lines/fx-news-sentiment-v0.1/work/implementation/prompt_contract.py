"""Strict product-output parser. Never repair, retry-select or drop failed records."""
import json
from fxns import validate_classification

REASONS = {'POLICY', 'MACRO', 'RISK_SENTIMENT', 'DIRECT_FX', 'OTHER', 'NONE'}
FIELDS = {'record_id', 'EUR', 'JPY', 'reason_code_EUR', 'reason_code_JPY'}


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def parse_output(raw, expected_id):
    row = json.loads(raw, object_pairs_hook=_unique)
    if not isinstance(row, dict) or set(row) != FIELDS:
        raise ValueError('exact output fields required')
    if any(not isinstance(v, str) for v in row.values()):
        raise ValueError('all values must be strings')
    if row['record_id'] != expected_id or not expected_id.strip():
        raise ValueError('record identity mismatch')
    validate_classification(row)
    for currency in ('EUR', 'JPY'):
        reason = row['reason_code_' + currency]
        if reason not in REASONS:
            raise ValueError('invalid reason')
        if row[currency] == 'NOT_MENTIONED' and reason != 'NONE':
            raise ValueError('NOT_MENTIONED requires NONE')
    return row


def validate_batch(raw_outputs, expected_ids):
    if len(expected_ids) != len(set(expected_ids)):
        raise ValueError('duplicate expected IDs')
    if len(raw_outputs) != len(expected_ids):
        raise ValueError('missing/extra output')
    # IDs bind each result to the fixed input order; one invalid row blocks event.
    return [parse_output(raw, rid) for raw, rid in zip(raw_outputs, expected_ids)]
