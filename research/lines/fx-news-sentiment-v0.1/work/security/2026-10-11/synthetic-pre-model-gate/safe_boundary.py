"""Offline-only prototype of a fail-closed, pre-model release boundary.

All adapters and tests are synthetic. This module has NO network/connector interface,
no filesystem read of source data, and no integration with ChatGPT Work.
It cannot enforce that a host model uses this boundary exclusively.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
import re
from typing import Any, Mapping

_HEX40 = re.compile(r"^[a-f0-9]{40}$")
_METADATA_FIELDS = frozenset({
    "number", "state", "draft", "merged", "head_oid", "base_oid",
    "head_repo", "base_repo",
})
_PATH_FIELDS = frozenset({"path", "blob_oid"})
_ENVELOPE_FIELDS = frozenset({
    "operation", "repository", "pr_number", "head_oid", "post_head_oid",
    "requested_fields", "pages", "complete", "errors", "content_type",
})
_PAGE_FIELDS = frozenset({"items", "complete", "next_cursor", "cursor"})
_DOC_FIELDS = frozenset({"operation", "repository", "pr_number", "head_oid", "post_head_oid", "path", "body", "content_type", "complete", "errors"})


class BoundaryStopped(Exception):
    """Reason is a fixed code; untrusted contents are never included."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class ApprovedDocument:
    path: str
    sha256: str
    safe_excerpt: str
    media_type: str = "text/plain"


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


@dataclass
class DeliverySink:
    """Synthetic model-input surrogate, NOT a real model connector."""

    delivered: list[bytes] = field(default_factory=list)

    def publish(self, content: bytes) -> None:
        self.delivered.append(content)


@dataclass
class ReceiptSink:
    """Synthetic independent-audit surrogate; can fail before publication."""

    available: bool = True
    receipts: list[dict[str, str]] = field(default_factory=list)

    def append(self, *, state: str, reason: str, policy_id: str, operation: str) -> None:
        if not self.available:
            raise BoundaryStopped("AUDIT_UNAVAILABLE")
        if state not in {"BLOCKED", "RELEASED", "EXPOSURE_REPORTED"}:
            raise BoundaryStopped("INVALID_AUDIT_STATE")
        if reason not in {"OK", "BAD_TARGET", "BAD_STRUCTURE", "UNAPPROVED_FIELD",
                          "UNAPPROVED_CONTENT", "INCOMPLETE", "VERSION_DRIFT",
                          "EXTERNAL_ACCESS", "UPSTREAM_FAILURE", "AUDIT_UNAVAILABLE",
                          "ALREADY_DELIVERED"}:
            raise BoundaryStopped("INVALID_AUDIT_REASON")
        self.receipts.append({
            "state": state, "reason": reason, "policy_id": policy_id,
            "operation": operation,
        })


class Boundary:
    def __init__(self, policy: Policy, deliveries: DeliverySink, receipts: ReceiptSink):
        self.policy, self.deliveries, self.receipts = policy, deliveries, receipts
        self._released_operations: set[str] = set()

    def _check(self, ok: bool, reason: str = "BAD_STRUCTURE") -> None:
        if not ok:
            raise BoundaryStopped(reason)

    def _start(self, operation: str, request: Mapping[str, Any]) -> None:
        self._check(operation in {"PR_METADATA", "FILE_PATHS", "SAFE_DOCUMENT"}, "EXTERNAL_ACCESS")
        self._check(type(request) is dict and set(request) == {"operation", "repository", "pr_number", "head_oid"}, "BAD_STRUCTURE")
        self._check(request["operation"] == operation, "BAD_TARGET")
        self._check(request["repository"] == self.policy.repository and
                    type(request["pr_number"]) is int and request["pr_number"] == self.policy.pr_number and
                    request["head_oid"] == self.policy.head_oid and
                    bool(_HEX40.fullmatch(self.policy.head_oid)) and bool(_HEX40.fullmatch(self.policy.base_oid)), "BAD_TARGET")

    def run(self, request: Mapping[str, Any], response: Any) -> bytes | None:
        """Returns only released bytes. Caller MUST NOT give source response to model.

        The caller must be an isolated orchestrator; the research model must not
        have alternate connector/browser/shell access. Not enforced here.
        """
        op = request.get("operation", "UNKNOWN") if type(request) is dict else "UNKNOWN"
        if op not in {"PR_METADATA", "FILE_PATHS", "SAFE_DOCUMENT"}:
            op = "UNSUPPORTED"
        try:
            self._start(op, request)
            self._check(op not in self._released_operations, "ALREADY_DELIVERED")
            if type(response) is not dict:
                raise BoundaryStopped("UPSTREAM_FAILURE")
            if op == "SAFE_DOCUMENT":
                result = self._document(response)
            else:
                result = self._paged(op, response)
            self._check(len(result) <= self.policy.max_bytes, "INCOMPLETE")
            # Audit BEFORE delivery: if audit is unavailable, no release.
            self.receipts.append(state="RELEASED", reason="OK", policy_id=self.policy.policy_id, operation=op)
            self.deliveries.publish(result)
            self._released_operations.add(op)
            return result
        except BoundaryStopped as failure:
            try:
                self.receipts.append(state="BLOCKED", reason=self._receipt_reason(failure.reason),
                                     policy_id=self.policy.policy_id, operation=op)
            except BoundaryStopped:
                # Fail closed with no receipt; cannot claim audited rejection.
                pass
            return None
        except Exception:
            # No exception text / repr / traceback flows to public output.
            try:
                self.receipts.append(state="BLOCKED", reason="UPSTREAM_FAILURE",
                                     policy_id=self.policy.policy_id, operation=op)
            except BoundaryStopped:
                pass
            return None

    @staticmethod
    def _receipt_reason(reason: str) -> str:
        allowed = {"BAD_TARGET", "BAD_STRUCTURE", "UNAPPROVED_FIELD", "UNAPPROVED_CONTENT",
                   "INCOMPLETE", "VERSION_DRIFT", "EXTERNAL_ACCESS", "UPSTREAM_FAILURE", "AUDIT_UNAVAILABLE", "ALREADY_DELIVERED"}
        return reason if reason in allowed else "BAD_STRUCTURE"

    def _shared(self, data: dict[str, Any], allowed: frozenset[str]) -> None:
        self._check(set(data) == allowed, "UNAPPROVED_FIELD")
        self._check(data["repository"] == self.policy.repository and
                    type(data["pr_number"]) is int and data["pr_number"] == self.policy.pr_number and
                    data["head_oid"] == self.policy.head_oid, "BAD_TARGET")
        self._check(data["post_head_oid"] == self.policy.head_oid, "VERSION_DRIFT")
        self._check(type(data["complete"]) is bool and data["complete"], "INCOMPLETE")
        self._check(type(data["errors"]) is list and not data["errors"], "UPSTREAM_FAILURE")
        self._check(data["content_type"] == "application/json" if "pages" in data else
                    data["content_type"] == "text/plain", "BAD_STRUCTURE")

    def _paged(self, operation: str, data: dict[str, Any]) -> bytes:
        self._shared(data, _ENVELOPE_FIELDS)
        self._check(data["operation"] == operation, "BAD_TARGET")
        expected = _METADATA_FIELDS if operation == "PR_METADATA" else _PATH_FIELDS
        self._check(type(data["requested_fields"]) is list and
                    len(data["requested_fields"]) == len(expected) and
                    all(type(k) is str for k in data["requested_fields"]) and
                    set(data["requested_fields"]) == expected, "UNAPPROVED_FIELD")
        pages = data["pages"]
        self._check(type(pages) is list and 1 <= len(pages) <= self.policy.max_pages, "INCOMPLETE")
        count = 0
        outputs: list[dict[str, Any]] = []
        seen_cursors: set[str] = set()
        for ix, page in enumerate(pages):
            self._check(type(page) is dict and set(page) == _PAGE_FIELDS, "UNAPPROVED_FIELD")
            self._check(type(page["complete"]) is bool and page["complete"], "INCOMPLETE")
            self._check(type(page["items"]) is list, "BAD_STRUCTURE")
            cursor = page["cursor"]
            nxt = page["next_cursor"]
            self._check(cursor is None or (type(cursor) is str and 0 < len(cursor) <= 32), "BAD_STRUCTURE")
            self._check(nxt is None or (type(nxt) is str and 0 < len(nxt) <= 32), "BAD_STRUCTURE")
            self._check(ix == 0 and cursor is None or
                        ix > 0 and cursor == pages[ix-1]["next_cursor"], "INCOMPLETE")
            if cursor is not None:
                self._check(cursor not in seen_cursors, "INCOMPLETE")
                seen_cursors.add(cursor)
            self._check((ix == len(pages)-1 and nxt is None) or
                        (ix < len(pages)-1 and nxt is not None), "INCOMPLETE")
            for item in page["items"]:
                count += 1
                self._check(count <= self.policy.max_items, "INCOMPLETE")
                self._check(type(item) is dict and set(item) == expected, "UNAPPROVED_FIELD")
                if operation == "PR_METADATA":
                    self._check(type(item["number"]) is int and item["number"] == self.policy.pr_number and
                                type(item["draft"]) is bool and type(item["merged"]) is bool and
                                item["state"] in {"OPEN", "CLOSED"} and type(item["state"]) is str and
                                item["head_oid"] == self.policy.head_oid and
                                item["base_oid"] == self.policy.base_oid and
                                item["head_repo"] == self.policy.repository and
                                item["base_repo"] == self.policy.repository, "BAD_TARGET")
                    # No opaque response field is released; only fixed enums/IDs.
                    outputs.append({"number": self.policy.pr_number, "state": item["state"],
                                    "draft": item["draft"], "merged": item["merged"],
                                    "head_oid": self.policy.head_oid, "base_oid": self.policy.base_oid})
                else:
                    self._check(type(item["path"]) is str and item["path"] in self.policy.allowed_paths and
                                type(item["blob_oid"]) is str and bool(_HEX40.fullmatch(item["blob_oid"])), "BAD_TARGET")
                    outputs.append({"approved_path": item["path"], "blob_oid": item["blob_oid"]})
        # Fail closed if incomplete pages or a partial response; release only once after all checks.
        self._check(count > 0, "INCOMPLETE")
        return json.dumps({"operation": operation, "items": outputs},
                          sort_keys=True, separators=(",", ":")).encode("utf-8")

    def _document(self, data: dict[str, Any]) -> bytes:
        self._shared(data, _DOC_FIELDS)
        self._check(data["operation"] == "SAFE_DOCUMENT", "BAD_TARGET")
        path = data["path"]
        self._check(type(path) is str and path in self.policy.allowed_paths and
                    path in self.policy.approved_documents, "BAD_TARGET")
        approved = self.policy.approved_documents[path]
        self._check(data["content_type"] == approved.media_type, "BAD_STRUCTURE")
        self._check(type(data["body"]) is bytes and len(data["body"]) <= self.policy.max_bytes, "INCOMPLETE")
        self._check(sha256(data["body"]).hexdigest() == approved.sha256, "UNAPPROVED_CONTENT")
        # Never publish the incoming raw body, even when it matches an approved digest.
        return json.dumps({"operation": "SAFE_DOCUMENT", "approved_path": path,
                           "content_hash": approved.sha256, "approved_excerpt": approved.safe_excerpt},
                          sort_keys=True, separators=(",", ":")).encode("utf-8")

    def check_prior_delivery(self, *, was_delivered: bool, rendered_masked: bool) -> bool:
        """A post-delivery mask cannot retroactively satisfy pre-model non-exposure."""
        if was_delivered:
            try:
                self.receipts.append(state="EXPOSURE_REPORTED", reason="ALREADY_DELIVERED",
                                     policy_id=self.policy.policy_id, operation="DELIVERY_TRACE")
            except BoundaryStopped:
                pass
            return False
        return True
