"""Purely fictional, offline model-input surrogate; NOT GitHub/Work enforcement.

Guarantees in scope: one in-process registry attached to one DeliverySink,
serial reservation/release, refusal to retry after uncertain publish/audit.
No cross-process durability, no actual downstream idempotency/ACK, no source-side
selection, no safe-excerpt reviewer authentication or real model-input control.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
import re
from threading import RLock
from types import MappingProxyType
from typing import Any, Mapping

_HEX40 = re.compile(r"[0-9a-f]{40}\Z")
_POLICY = re.compile(r"SYNTHETIC-[A-Z0-9-]{1,48}\Z")
_APPROVAL = re.compile(r"SYNTH-[A-Z0-9-]{1,48}\Z")
_REQUEST_ID = re.compile(r"SYN-[A-Za-z0-9_-]{1,32}\Z")
_METADATA_FIELDS = frozenset({"number", "state", "draft", "merged", "head_oid", "base_oid", "head_repo", "base_repo"})
_PATH_FIELDS = frozenset({"path", "blob_oid"})
_ENVELOPE_FIELDS = frozenset({"operation", "repository", "pr_number", "head_oid", "post_head_oid", "requested_fields", "pages", "complete", "errors", "content_type"})
_PAGE_FIELDS = frozenset({"items", "complete", "next_cursor", "cursor"})
_DOC_FIELDS = frozenset({"operation", "repository", "pr_number", "head_oid", "post_head_oid", "path", "body", "content_type", "complete", "errors"})
_OPS = frozenset({"PR_METADATA", "FILE_PATHS", "SAFE_DOCUMENT"})
_REASONS = frozenset({"OK", "BAD_TARGET", "BAD_STRUCTURE", "UNAPPROVED_FIELD", "UNAPPROVED_CONTENT", "INCOMPLETE", "VERSION_DRIFT", "EXTERNAL_ACCESS", "UPSTREAM_FAILURE", "AUDIT_UNAVAILABLE", "ALREADY_DELIVERED", "DELIVERY_UNKNOWN"})
_STATES = frozenset({"BLOCKED", "RESERVED", "RELEASED", "UNKNOWN", "EXPOSURE_REPORTED"})


class BoundaryStopped(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def _valid_string(value: Any, pattern: re.Pattern[str]) -> bool:
    return type(value) is str and pattern.fullmatch(value) is not None


@dataclass(frozen=True)
class ApprovedDocument:
    path: str
    sha256: str
    safe_excerpt: str
    media_type: str = "text/plain"
    # These are *trusted synthetic inputs*. Neither signature nor independent
    # review of the excerpt's actual meaning is performed by this prototype.
    approval_id: str = ""
    excerpt_sha256: str = ""

    def __post_init__(self):
        if not (_valid_string(self.approval_id, _APPROVAL)
                and _valid_string(self.sha256, re.compile(r"[0-9a-f]{64}\Z"))
                and type(self.safe_excerpt) is str
                and _valid_string(self.excerpt_sha256, re.compile(r"[0-9a-f]{64}\Z"))
                and sha256(self.safe_excerpt.encode("utf-8")).hexdigest() == self.excerpt_sha256
                and type(self.path) is str and self.path
                and self.media_type == "text/plain"):
            raise BoundaryStopped("UNAPPROVED_CONTENT")


@dataclass(frozen=True)
class Policy:
    repository: str
    pr_number: int
    head_oid: str
    base_oid: str
    allowed_paths: frozenset[str]
    approved_documents: Mapping[str, ApprovedDocument] = field(default_factory=dict)
    max_pages: int = 3
    max_items: int = 10
    max_bytes: int = 4096
    policy_id: str = "SYNTHETIC-POLICY-V01"
    expected_blob_oids: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not (_valid_string(self.policy_id, _POLICY)
                and type(self.repository) is str and 0 < len(self.repository) <= 128
                and type(self.pr_number) is int and self.pr_number > 0
                and _valid_string(self.head_oid, _HEX40)
                and _valid_string(self.base_oid, _HEX40)
                and type(self.allowed_paths) is frozenset
                and all(type(p) is str and p and len(p) <= 256 for p in self.allowed_paths)
                and all(type(x) is int and 0 < x <= 100000 for x in (self.max_pages, self.max_items, self.max_bytes))):
            raise BoundaryStopped("BAD_STRUCTURE")
        docs = dict(self.approved_documents)
        blobs = dict(self.expected_blob_oids)
        if (any(type(k) is not str or k not in self.allowed_paths or
                type(v) is not ApprovedDocument or v.path != k for k, v in docs.items())
            or any(type(k) is not str or k not in self.allowed_paths or
                   not _valid_string(v, _HEX40) for k, v in blobs.items())):
            raise BoundaryStopped("BAD_STRUCTURE")
        object.__setattr__(self, "approved_documents", MappingProxyType(docs))
        object.__setattr__(self, "expected_blob_oids", MappingProxyType(blobs))


@dataclass
class DeliverySink:
    """Synthetic in-memory surrogate. A shared sink is the SAME registry scope."""
    delivered: list[bytes] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock, repr=False)
    _operations: dict[tuple[str, ...], str] = field(default_factory=dict, repr=False)

    def publish(self, content: bytes) -> None:
        self.delivered.append(content)
        # A normal return emulates an ACK ONLY in this fictional test sink.


@dataclass
class ReceiptSink:
    available: bool = True
    receipts: list[dict[str, str]] = field(default_factory=list)

    def append(self, *, state: str, reason: str, policy_id: str, operation: str) -> None:
        if not self.available:
            raise BoundaryStopped("AUDIT_UNAVAILABLE")
        if state not in _STATES or reason not in _REASONS:
            raise BoundaryStopped("INVALID_AUDIT_STATE")
        if not (_valid_string(policy_id, _POLICY) and operation in _OPS | {"DELIVERY_TRACE", "UNSUPPORTED"}):
            raise BoundaryStopped("BAD_STRUCTURE")
        self.receipts.append({"state": state, "reason": reason, "policy_id": policy_id, "operation": operation})


class Boundary:
    def __init__(self, policy: Policy, deliveries: DeliverySink, receipts: ReceiptSink):
        if not isinstance(policy, Policy) or not isinstance(deliveries, DeliverySink) or not isinstance(receipts, ReceiptSink):
            raise BoundaryStopped("BAD_STRUCTURE")
        self.policy, self.deliveries, self.receipts = policy, deliveries, receipts

    @staticmethod
    def _check(ok: bool, reason: str = "BAD_STRUCTURE") -> None:
        if not ok:
            raise BoundaryStopped(reason)

    def _start(self, operation: str, request: Any) -> str:
        self._check(operation in _OPS, "EXTERNAL_ACCESS")
        self._check(type(request) is dict and set(request) in ({"operation", "repository", "pr_number", "head_oid"},
                         {"operation", "repository", "pr_number", "head_oid", "approved_request_id"}), "BAD_STRUCTURE")
        self._check(request["operation"] == operation and type(request["repository"]) is str
                    and request["repository"] == self.policy.repository
                    and type(request["pr_number"]) is int and request["pr_number"] == self.policy.pr_number
                    and type(request["head_oid"]) is str and request["head_oid"] == self.policy.head_oid,
                    "BAD_TARGET")
        rid = request.get("approved_request_id", "SYN-LEGACY")
        self._check(_valid_string(rid, _REQUEST_ID), "BAD_TARGET")
        return rid

    @staticmethod
    def _receipt_reason(reason: str) -> str:
        return reason if reason in _REASONS else "BAD_STRUCTURE"

    def _audit(self, state: str, reason: str, operation: str) -> bool:
        try:
            self.receipts.append(state=state, reason=reason, policy_id=self.policy.policy_id, operation=operation)
            return True
        except Exception:
            return False

    def run(self, request: Mapping[str, Any], response: Any) -> bytes | None:
        """Fail-closed within *one process and shared sink* only.

        Policy instances with a different sink/registry, any process crash, and
        real network/model delivery are explicitly OUTSIDE the guarantee.
        """
        try:
            operation = request.get("operation", "UNKNOWN") if type(request) is dict else "UNKNOWN"
        except Exception:
            operation = "UNKNOWN"
        if type(operation) is not str or operation not in _OPS:
            operation = "UNSUPPORTED"
        try:
            rid = self._start(operation, request)
            self._check(type(response) is dict, "UPSTREAM_FAILURE")
            if operation == "SAFE_DOCUMENT":
                content = self._document(response)
                path_key = response["path"]
            else:
                content = self._paged(operation, response)
                path_key = ""
            self._check(len(content) <= self.policy.max_bytes, "INCOMPLETE")
            key = (self.policy.policy_id, self.policy.repository, str(self.policy.pr_number),
                   self.policy.head_oid, rid, operation, path_key)
            # One shared in-process sink provides atomic reserve AND release.
            # UNKNOWN and RESERVED must NEVER be retried in this scope.
            with self.deliveries._lock:
                self._check(key not in self.deliveries._operations, "ALREADY_DELIVERED")
                if not self._audit("RESERVED", "OK", operation):
                    return None
                self.deliveries._operations[key] = "RESERVED"
                try:
                    self.deliveries.publish(content)
                except Exception:
                    self.deliveries._operations[key] = "UNKNOWN"
                    self._audit("UNKNOWN", "DELIVERY_UNKNOWN", operation)
                    return None
                self.deliveries._operations[key] = "UNKNOWN"  # until audit-confirmation
                if not self._audit("RELEASED", "OK", operation):
                    return None   # delivery might have occurred; irreversible
                self.deliveries._operations[key] = "RELEASED"
                return content
        except BoundaryStopped as failure:
            # No blocking audit is written for a duplicate after release, so
            # earlier RELEASED receipts retain their precise meaning.
            if failure.reason != "ALREADY_DELIVERED":
                self._audit("BLOCKED", self._receipt_reason(failure.reason), operation)
            return None
        except Exception:
            self._audit("BLOCKED", "UPSTREAM_FAILURE", operation)
            return None

    def _shared(self, data: dict[str, Any], fields: frozenset[str]) -> None:
        self._check(set(data) == fields, "UNAPPROVED_FIELD")
        self._check(data["repository"] == self.policy.repository and
                    type(data["pr_number"]) is int and data["pr_number"] == self.policy.pr_number and
                    data["head_oid"] == self.policy.head_oid, "BAD_TARGET")
        self._check(data["post_head_oid"] == self.policy.head_oid, "VERSION_DRIFT")
        self._check(type(data["complete"]) is bool and data["complete"], "INCOMPLETE")
        self._check(type(data["errors"]) is list and not data["errors"], "UPSTREAM_FAILURE")
        self._check(data["content_type"] == ("application/json" if "pages" in data else "text/plain"), "BAD_STRUCTURE")

    def _paged(self, operation: str, data: dict[str, Any]) -> bytes:
        self._shared(data, _ENVELOPE_FIELDS)
        self._check(data["operation"] == operation, "BAD_TARGET")
        expected = _METADATA_FIELDS if operation == "PR_METADATA" else _PATH_FIELDS
        fields = data["requested_fields"]
        self._check(type(fields) is list and len(fields) == len(expected)
                    and all(type(k) is str for k in fields) and set(fields) == expected, "UNAPPROVED_FIELD")
        pages = data["pages"]
        self._check(type(pages) is list and 1 <= len(pages) <= self.policy.max_pages, "INCOMPLETE")
        outputs: list[dict[str, Any]] = []
        seen: set[str] = set()
        for ix, page in enumerate(pages):
            self._check(type(page) is dict and set(page) == _PAGE_FIELDS, "UNAPPROVED_FIELD")
            self._check(type(page["complete"]) is bool and page["complete"], "INCOMPLETE")
            self._check(type(page["items"]) is list, "BAD_STRUCTURE")
            cursor, nxt = page["cursor"], page["next_cursor"]
            self._check(cursor is None or type(cursor) is str and 0 < len(cursor) <= 32, "BAD_STRUCTURE")
            self._check(nxt is None or type(nxt) is str and 0 < len(nxt) <= 32, "BAD_STRUCTURE")
            self._check((ix == 0 and cursor is None) or (ix > 0 and cursor == pages[ix-1]["next_cursor"]), "INCOMPLETE")
            if cursor is not None:
                self._check(cursor not in seen, "INCOMPLETE")
                seen.add(cursor)
            self._check((ix == len(pages)-1 and nxt is None) or (ix < len(pages)-1 and nxt is not None), "INCOMPLETE")
            for item in page["items"]:
                self._check(len(outputs) < self.policy.max_items, "INCOMPLETE")
                self._check(type(item) is dict and set(item) == expected, "UNAPPROVED_FIELD")
                if operation == "PR_METADATA":
                    # Membership check deliberately preserves old T07 behavior:
                    # hostile objects throwing in __hash__ are caught as UPSTREAM_FAILURE.
                    self._check(type(item["number"]) is int and item["number"] == self.policy.pr_number
                                and type(item["draft"]) is bool and type(item["merged"]) is bool
                                and item["state"] in {"OPEN", "CLOSED"} and type(item["state"]) is str
                                and not (item["state"] == "OPEN" and item["merged"])
                                and not (item["merged"] and item["draft"])
                                and item["head_oid"] == self.policy.head_oid
                                and item["base_oid"] == self.policy.base_oid
                                and item["head_repo"] == self.policy.repository
                                and item["base_repo"] == self.policy.repository, "BAD_TARGET")
                    outputs.append({"number": self.policy.pr_number, "state": item["state"], "draft": item["draft"],
                                    "merged": item["merged"], "head_oid": self.policy.head_oid, "base_oid": self.policy.base_oid})
                else:
                    self._check(type(item["path"]) is str and item["path"] in self.policy.allowed_paths
                                and item["path"] in self.policy.expected_blob_oids
                                and _valid_string(item["blob_oid"], _HEX40)
                                and item["blob_oid"] == self.policy.expected_blob_oids[item["path"]], "BAD_TARGET")
                    outputs.append({"approved_path": item["path"], "blob_oid": self.policy.expected_blob_oids[item["path"]]})
        self._check(len(outputs) > 0, "INCOMPLETE")
        return json.dumps({"operation": operation, "items": outputs}, sort_keys=True, separators=(",", ":")).encode()

    def _document(self, data: dict[str, Any]) -> bytes:
        self._shared(data, _DOC_FIELDS)
        self._check(data["operation"] == "SAFE_DOCUMENT", "BAD_TARGET")
        path = data["path"]
        self._check(type(path) is str and path in self.policy.allowed_paths and path in self.policy.approved_documents, "BAD_TARGET")
        approved = self.policy.approved_documents[path]
        self._check(data["content_type"] == approved.media_type, "BAD_STRUCTURE")
        self._check(type(data["body"]) is bytes and len(data["body"]) <= self.policy.max_bytes, "INCOMPLETE")
        self._check(sha256(data["body"]).hexdigest() == approved.sha256, "UNAPPROVED_CONTENT")
        # Only a TRUSTED synthetic approval object is released, not raw body.
        return json.dumps({"operation": "SAFE_DOCUMENT", "approved_path": path,
                           "content_hash": approved.sha256, "approved_excerpt": approved.safe_excerpt},
                          sort_keys=True, separators=(",", ":")).encode()

    def check_prior_delivery(self, *, was_delivered: bool, rendered_masked: bool) -> bool:
        if was_delivered:
            self._audit("EXPOSURE_REPORTED", "ALREADY_DELIVERED", "DELIVERY_TRACE")
            return False
        return True
