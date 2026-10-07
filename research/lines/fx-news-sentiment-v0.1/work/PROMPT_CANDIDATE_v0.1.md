# ChatGPT prompt candidate v0.1

Status: FREEZE_READY_CANDIDATE_NOT_HUMAN_FROZEN

Canonical exact task text: `PROMPT_v0.1.txt`.
Canonical JSON Schema: `OUTPUT_SCHEMA_v0.1.json`.
Exact-byte SHA-256 lock: `PROMPT_MANIFEST_v0.1.json`.

Input JSON object: record_id, gdelt_seen_at (aware ISO-8601 UTC), source_domain, title.
One record per request, no article body or market data. Preserve serialized input and
assembled prompt bytes as well as the canonical task hash. Metadata remains untrusted.

Strict contextual parser: `implementation/prompt_contract.py`. Requires exact input
record identity and NOT_MENTIONED -> NONE in addition to schema validation. All other
reason codes remain diagnostic only. Failure blocks event; no silent row omission.

The product model identity/configuration and acquisition timing are still open gates.
Parser tests are synthetic and do not establish LLM classification quality.
See `SOURCE_QUALIFICATION_RESULT.md` for execution and stopping requirements.
