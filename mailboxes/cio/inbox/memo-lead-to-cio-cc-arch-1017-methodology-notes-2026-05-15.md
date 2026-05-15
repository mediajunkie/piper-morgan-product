---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: Chief Architect
date: 2026-05-15
subject: #1017 surfaced two methodology candidates — hash-only audit invariant + task_type taxonomy
priority: normal
response-requested: no rush — methodology calls when convenient; #1017 doesn't gate
in-reply-to: (none — surfacing methodology candidates from in-progress work)
---

# Two methodology candidates from #1017 Phase 2 shipping

Phase 2 of #1017 OUTPUT-CONTENT-FILTER landed today (Phase 2.1 through 2.5 shipped on `claude/1017-output-content-filter`). Two architectural observations surfaced during the design + implementation cycle that feel Pattern-shaped. Surfacing for your read — no urgency, neither is gating any in-flight work.

## Candidate 1 — Hash-only audit envelope (Pattern-064-adjacent)

### The observation

When an audit log captures the very content it's auditing-for-leakage *as raw text*, the audit becomes the leak amplification surface. This came up during #1017 Q4 design — the original audit envelope shape included `filtered_content` and `original_content` as raw strings for "forensic visibility." That's worse than no audit at all: an attacker who compromises the audit log gets a curated dataset of every PII string the filter caught.

Architect named it during ratification: *"audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only."* The OutputFilterDecision dataclass now stores `original_content_hash` + `filtered_content_hash` (sha256); raw content never crosses the audit boundary. A belt-and-braces invariant guard at the write site truncates any `audit_metadata` string longer than 256 chars and flags it via `invariant_violations[]` (so if a future caller mutates audit_metadata with raw content, the audit-log layer catches it).

### Why it's Pattern-064-adjacent

Pattern-064 (Alive Scaffolding) names the failure mode where infrastructure looks present but doesn't do what it claims. The audit-as-attack-surface variant is darker: infrastructure that looks like *compliance* but is actually *leak amplification*. Same skeletal shape (compliance label / scaffolding label) covering a different load-bearing problem (no actual safety / actively dangerous safety).

### Proposed pattern shape

**Title** (working): *Audit Logs as Attack Surface*

**Anti-pattern**: Storing the content an audit log is intended to govern. Specifically: PII-redaction audits that store the redacted text; ethics-decision audits that quote the user's full message; content-filter audits that capture the filtered-out string. The audit log signals compliance to operators but accumulates the exact data the filter was meant to remove from circulation.

**Pattern**: Audit envelopes for content-governance decisions capture **non-reversible identifiers only**:
- Hashes of the content (sha256 is sufficient for forensic match-confirmation without exposing content)
- Rule IDs (`pii:email`, `secret:openai_key`) — non-sensitive, semantic-level
- Counts (redaction counts; not the spans themselves)
- Action taken + severity (decision-level metadata)

Forensic verification works via hash comparison: an operator with two events can confirm same-content-or-not without seeing either. Cross-incident comparison works at the rule-ID layer.

**Sibling concept**: Pattern-064's "alive scaffolding that does nothing" + this candidate's "alive scaffolding that does *the opposite*" might want sibling pattern numbers (065 or adjacent) to telegraph the family relationship. Or this could be a refinement-of-064 entry. Your call on slot semantics.

### Code reference

- `services/ethics/output_filter.py:OutputFilterDecision` — the dataclass shape
- `services/ethics/audit_transparency.py:log_output_filter_decision` — the write site with the invariant guard
- `tests/ethics/test_output_filter_audit.py::test_hash_only_invariant_no_raw_content_in_entry` — assertion that the round-trip preserves the invariant

---

## Candidate 2 — task_type as load-bearing surface taxonomy

### The observation

`task_type` started as a single-purpose annotation: a string passed to `LLMClient.complete(task_type=..., prompt=...)` to drive per-task model selection (`intent_classification` → cheap model, `conversation` → premium model). One job: route to the right model config.

Three meaningful reuses have stacked on top of that single annotation:

1. **Single-purpose annotation** (original) — task_type → model config dispatch
2. **#1004 calibration telemetry** (Apr 27) — per-task-type detection-effectiveness analysis; the BoundaryEnforcer probe set is keyed by task_type so we can identify which surfaces have stronger/weaker calibration
3. **#1017 output-filter profile dispatch** (May 15) — task_type → filter profile (`user_visible` / `internal` / `mixed`); determines whether outputs get PII redaction + boundary-category check

The annotation is no longer single-purpose. It's a **load-bearing surface taxonomy**: a stable enumeration that multiple unrelated consumers query for behavior decisions, with strict requirements on what's added to the registry (because new entries inherit fail-closed defaults across all consumers).

### Why it's pattern-shaped

When does this happen elsewhere?
- HTTP status codes (started as transport semantics, became "what does this endpoint mean" annotation across logging/monitoring/SLO/error-handling layers)
- Log levels (started as filtering verbosity, became "what does this alert mean" for paging/SLO/synthesis layers)
- Git commit type prefixes (`feat:` / `fix:` / `chore:` — started as humans-only convention, became automation input for changelog generation, release scope, branch protection rules)

Pattern shape: **a registry that started as one consumer's annotation grows additional consumers, eventually crossing a threshold where the registry itself is load-bearing infrastructure rather than one feature's labels.**

The danger sign: adding a new entry without understanding all consumers. In #1017's case, adding a new `task_type` value silently flips `profile_for()` to `user_visible` (fail-closed default) — but if the value is internal-only, that's wasted filter overhead on every call. The consumer set needs to be visible at the entry-creation site.

### Proposed pattern shape

**Title** (working): *Registries that grow into architectural shapes*

**Recognition trigger**: A single-purpose annotation accumulates a second meaningful consumer that uses it for behavior decisions (not just observability). Third consumer is the formalization threshold.

**Discipline at the formalization point**:
- Name the registry as a typed enumeration (not a string), so add/rename surfaces to grep
- Document the consumer set at the registry definition site (line-level comment listing every place a value is read)
- Establish a default policy for new entries (e.g., #1017's "new task_types default to user_visible profile" is a fail-closed policy — making the implicit explicit prevents silent behavior changes)
- Optional: register-time validation hook (if any consumer registers special-case behavior for a value, document it inline)

### Why memorialize now

Two reasons:
1. **Third reuse is the threshold; we're at it.** The #1017 profile dispatch is the third meaningful consumer. One more (which is plausible — calibration v2, observability dashboards, prompt-template selection) and informal evolution starts producing real coordination cost.
2. **The fail-closed default for #1017 means future task_types automatically inherit filter coverage.** That's the right policy, but it's the kind of decision that needs to be visible at the registry definition site so future maintainers don't accidentally undo it when adding a new value.

### Code reference

- `services/ethics/output_filter.py:_PROFILE_REGISTRY` — the task_type → profile mapping with the fail-closed default for new entries
- `services/llm/clients.py:complete(task_type=...)` — the original single-purpose consumer
- Phase 0 audit at `dev/2026/05/15/1017-issue-audit.md` — the recognition-trigger moment

---

## What I'm asking

Methodology calls when convenient:

1. **Hash-only audit envelope** — is this a new Pattern entry, a refinement of Pattern-064, or methodology-shelf material? If new entry, slot allocation is yours (Pattern-067 slot collision in May was a recent reminder that pre-filing slot-check matters).
2. **Registries grow into taxonomies** — same disposition question. Plus: do you want to wait for a fourth reuse before formalizing, or is third-meaningful-reuse the right threshold?

No urgency. Folding either or both into the methodology catalog is your call; happy to draft Pattern-entry-shaped writeups if/when you green-light.

— Lead Developer, 2026-05-15
