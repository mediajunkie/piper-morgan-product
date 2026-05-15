# Pattern-071: Audit Logs as Attack Surface

## Status

**Emerging** — Filed 2026-05-15 by Lead Developer per CIO disposition (May 15) following Architect's observation during #1017 Phase 1 ratification + Lead Dev's methodology memo to CIO. Slot 071 allocated after 12l pre-filing slot-availability check. Sibling-of-Pattern-064 framing co-signed by CIO ("dark twin of Alive Scaffolding" — same skeletal shape covering a different load-bearing problem; distinct slots tracking filing chronology rather than taxonomic adjacency). Promotion to Proven contingent on **no exceptions surfacing in 4-6 weeks of cohort exposure** — i.e., does the hash-only-as-only-allowed-shape discipline hold up under all audit-log uses, or do compliance-required surfaces emerge where raw-content is externally mandated and an explicit exception path is needed.

## Product Relevance

**Architecture / Security** — Reusable discipline for audit-log infrastructure across content-governance surfaces. Users will not encounter this pattern directly; engineers building or extending audit envelopes will reach for it. Failure to apply produces real user-facing harm: audit logs intended to record content-filtering decisions can themselves become a curated dataset of the very content the filter was meant to remove from circulation.

## Context

Two parent observations frame the pattern:

1. **Pattern-064 (Extension Without Integration)** names the failure mode where *infrastructure that looks present doesn't actually do what it claims* (alive scaffolding). The same skeletal shape — false signal of safety — covers a different load-bearing problem: **infrastructure that looks like compliance but actively makes the underlying problem worse**. Compliance label, leak amplification mechanism.

2. **ADR-061's four-element principle** (LLM-touch boundary enforcement) specifies that every LLM-touch surface needs an *audit envelope* (element 4). The envelope is the operator-legible record of what the filter did. Without explicit discipline on *what the envelope stores*, the envelope's "operator legible" property makes it the highest-density compliance-shaped surface in the system — and therefore the highest-density leak amplification surface if it stores raw content.

The pattern was sharpened during the #1017 Phase 1 design ratification (2026-05-15). The original `OutputFilterDecision` schema design candidate included `filtered_content` and `original_content` as raw strings for "forensic visibility." Architect named the failure mode during ratification: *"audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only."* The schema was revised to store sha256 hashes only; the discipline was named.

### Why this is sibling, not refinement, of Pattern-064

Pattern-064 covers extension-into-new-context where the component doesn't handle the new input shape (a *passive* failure — the component does nothing useful but appears wired). This pattern covers infrastructure that explicitly performs the action it claims, but the action turns a safety mechanism into a hazard (an *active* failure — the component does something, but that something is dangerous).

| | Pattern-064 (parent / sibling) | Pattern-071 (this) |
|---|---|---|
| **Failure shape** | Alive scaffolding that does nothing | Compliance-shaped scaffolding that does the opposite |
| **Detection class** | Passive (no effect when expected) | Active (effect amplifies the problem it was supposed to solve) |
| **Reference instance** | BoundaryEnforcer substring-recall on naturally-phrased input | OutputFilterDecision schema candidate storing raw filtered content |
| **Mitigation shape** | Verify behavior against realistic input shape | Restrict the schema to non-reversible identifiers only |

Same skeletal class (false signal of safety); different load-bearing mechanism. Distinct slots reflect filing chronology rather than refinement hierarchy.

## Problem

### The Failure Mode

```
Content-governance audit log records every filter decision
  → schema includes the filtered content as raw text
  → audit log becomes searchable index of every PII/secret/violation the filter caught
  → audit log access (operator, BI tool, ML pipeline, compliance export) becomes leak surface
  → the *more* effective the filter, the *higher-density* the leak surface
```

The compounding asymmetry: **the audit log's value to operators grows linearly with filter activity, but its risk grows quadratically** because (a) more events = more rows = more PII in one place, and (b) audit-log access is by definition broader than user data access (operators, compliance reviewers, ML feedback loops, retention sweeps all reach in).

A complete content-governance pipeline can ship with PII redaction working perfectly at the user-facing surface, BoundaryEnforcer catching every violation, and the audit log faithfully recording all of it — and have a worse PII posture than no filter at all, because the audit log concentrates what was previously scattered.

### Where this surfaced

#1017 OUTPUT-CONTENT-FILTER Phase 1 design (2026-05-15). The Phase 1 design memo proposed an `OutputFilterDecision` schema that included `filtered_content` and `original_content` as raw strings for forensic visibility. Architect's Q4 ratification observation:

> *"Critical: hashes only — never store raw PII even in the audit log; otherwise the audit becomes a PII honeypot."*

The schema was revised to store `original_content_hash` (sha256) and `filtered_content_hash` (sha256) only. Forensic verification works via hash comparison: an operator with two events can confirm same-content-or-not without seeing either.

### Where this *could* surface (cohort exposure question)

The 4-6-week promotion-to-Proven window is to surface whether other audit-log use cases hit external constraints that would require raw content (e.g., regulatory compliance requiring full content retention with separately-managed access). If those cases surface, the pattern needs an explicit exception path — a "compliance-required raw-content audit" annotation with operator-discoverable acceptance of the amplification risk. If no such cases surface in the window, hash-only stays the unconditional rule.

## Solution

### The discipline

**Audit envelopes for content-governance decisions store non-reversible identifiers only:**

1. **Hashes of the content** — sha256 hex is sufficient for forensic match-confirmation without exposing content. Two events with the same `original_content_hash` are confirmable as the same input without either being readable.
2. **Rule IDs** — semantic-level non-sensitive identifiers (`pii:email`, `secret:openai_key`, `boundary:harassment`). These describe *what* fired without exposing *the content that triggered it*.
3. **Counts** — redaction counts, multi-match counts. Numeric, non-reversible, useful for telemetry.
4. **Action taken + severity** — decision-level metadata. Non-content.
5. **Decision-flow metadata** — `attempt_number`, `prior_attempt_decision_id`, `surface`, `profile_applied`, `user_id`, `session_id`. All identifiers, none content.

Forensic operator workflows:
- *"Did this user have a PII redaction event in the last hour?"* → query by `user_id` + `event_type` + `timestamp`. No content read.
- *"Are these two events the same content?"* → compare `original_content_hash` strings. No content read.
- *"What rule fired most frequently this week?"* → group by `matched_rules`. No content read.
- *"What was the actual content that fired rule X?"* → **not answerable from audit log alone.** This is by design; if needed, the operator must reproduce the input through a non-audit-log path (e.g., reproduce the user's query and observe the live filter output).

### Two-layer enforcement

The pattern requires enforcement at both the schema definition and the write site:

**Schema layer** — the audit record's typed shape has fields for hashes and identifiers only, never raw content. A future developer adding a raw-content field would need to consciously edit the schema.

**Write-time guard** — even with a constrained schema, an extension point like `audit_metadata: Dict[str, Any]` can be abused by a future caller passing raw content. The write site truncates any audit-metadata string longer than a threshold (e.g., 256 chars) and flags `invariant_violations[]` so the audit-log layer catches drift. This is belt-and-braces: the schema is the primary fence; the runtime guard is the breach detector.

## Architectural reasoning

Three asymmetries make this pattern load-bearing rather than nice-to-have:

1. **Audit-log access is structurally broader than user-data access.** User data access is gated by user authentication and request scoping. Audit-log access typically reaches operators, compliance reviewers, BI tools, retention sweeps, and (often) automated ML feedback loops. The principal set who can read audit data is a superset of the principal set who can read user data.

2. **Audit-log density grows with filter activity.** A successful PII filter catching 1,000 events/day produces 1,000 rows of content-bearing audit data/day if raw content is stored. A *more successful* filter = *more concentrated* leak surface. The metric of filter quality (catch rate) co-varies with the metric of leak surface size (audit-row count).

3. **Audit-log retention is typically longer than per-event content retention.** A user message exists for the duration of a session (or a deletion period); an audit record retains for compliance periods (months to years). Storing raw content in audit logs extends content lifetime past the user's expected window.

Hash-only forensic capability covers the operationally-required workflows (event correlation, frequency analysis, user-event lookup, rule-fire telemetry) without paying any of these three asymmetric costs.

## Forces / when to apply

**Apply when**:
- Building or extending an audit log for content-governance decisions (PII filters, content moderation, boundary enforcement, output filtering)
- Adding a new field to an existing content-governance audit envelope
- Reviewing audit-log access patterns (who reads, how often, retained how long)

**Tension to resolve**:
- **Forensic visibility** (operator wants to debug filter behavior) vs. **leak amplification risk**. The pattern resolves this by routing forensic debugging through *reproduction* (re-run the input through the filter in a controlled environment) rather than *retention* (store the input forever in the audit log). Reproduction is operationally heavier but eliminates the persistent risk.

**Exception path** (if surfaced during 4-6 week promotion window):
- External compliance requirement mandating raw-content retention. Should be opt-in at the schema level with an explicit `requires_raw_content_acceptance: True` flag + operator sign-off, not implicit in field definition.

## Code references (canonical reference implementation)

`services/ethics/output_filter.py:OutputFilterDecision` (lines ~150-220):
```python
@dataclass
class OutputFilterDecision:
    decision_id: str
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    surface: str
    profile_applied: str
    matched_rules: List[str]
    severity: str
    redactions_count: int
    action_taken: str

    # Content references (hashes only — never raw)
    original_content_hash: str
    filtered_content_hash: str

    # Regenerate-trigger chain
    attempt_number: int
    prior_attempt_decision_id: Optional[str]

    # Extension point
    audit_metadata: Dict[str, Any]
```

`services/ethics/audit_transparency.py:log_output_filter_decision`:
- Sibling of `log_ethics_decision`; writes through per-call `session_scope` to `ethics_audit_log` table
- Belt-and-braces guard at the write site: any `audit_metadata` string >256 chars is truncated + flagged via `invariant_violations[]`

`tests/ethics/test_output_filter_audit.py:test_hash_only_invariant_no_raw_content_in_entry`:
- Round-trip assertion that the entry's `details` dict contains hashes but NOT the original `filtered_content` / `raw_content` keys
- Validates the invariant at test-time so future regressions surface as test failures

`tests/integration/services/test_output_filter_audit_integration.py:test_llm_client_end_to_end_writes_audit_row`:
- Real-Postgres integration test exercising the full path: LLM emits PII → OutputFilter redacts → audit envelope persists → audit row queryable → raw PII (`alice@example.com`) NEVER appears in serialized `entry.details`

ADR-061 v1.1 amendment (2026-05-15) memorializes the discipline in the architectural decision record:

> *"Storing the content an audit log is intended to govern as raw text turns the audit log into the leak amplification surface — same skeletal shape as Pattern-064 ('alive scaffolding'), different failure mode (compliance-shaped infrastructure that actively makes the underlying problem worse)."*

## Anti-pattern recognition

Code-review signals that this pattern is being violated or worth applying:

- An audit-log dataclass with a `content: str` or `original_text: str` or `raw_input: str` field for "forensic visibility"
- A `metadata: Dict[str, Any]` field on an audit record with no length cap or content validation
- An audit-log table column typed `TEXT` or `JSONB` with no schema-level restriction on what gets stored
- Audit-log retrieval endpoints that expose raw content fields to operators ("show me what was filtered")
- A test that asserts raw content survives the audit round-trip (i.e., tests *for* the leak)

Healthy signals:
- Audit schemas with `*_hash` fields and no corresponding `*_content` fields
- Write-time guards that bound or hash extension-point values
- Tests that *assert absence* of raw content in audit serialization (the invariant test)
- Audit retrieval endpoints that return rule IDs + counts + hashes but not content

## Relationship to other patterns

- **Pattern-064 (Extension Without Integration)** — parent skeletal shape (false signal of safety). Pattern-064 covers the passive variant (alive scaffolding doing nothing); Pattern-071 covers the active variant (compliance-shaped scaffolding doing the opposite). Sibling shape, distinct mechanism.
- **Pattern-062 (Assembly Assumption)** — grandparent. Both Pattern-064 and Pattern-071 are specific compositions where the seam between components produces a false-safety outcome.
- **Pattern-045 (Beads Completion Discipline / "Green Tests, Red User")** — adjacent at the test layer. The presence of audit-log tests asserting roundtrip-of-raw-content is exactly Pattern-045 at the infrastructure layer: tests pass, audit log "works," and the user (and operator) is worse off than with no audit log at all.
- **ADR-061 (LLM-Touch Boundary Enforcement)** — v1.1 amendment (2026-05-15) memorializes the discipline alongside the broader four-element principle.

## Promotion criteria

**To Proven**:
- 4-6 weeks of cohort exposure (~2026-06-12 to ~2026-06-26 window) with no surfaced exception path required
- At least one additional audit-log review or new audit-shaped surface trial-applies the hash-only discipline without rediscovery
- No new audit-log additions ship with raw-content fields after this pattern is filed

**Promotion-blocking signals**:
- A legitimate compliance-required raw-content audit surface emerges that needs the discipline relaxed
- The hash-only forensic workflow proves operationally insufficient (operators repeatedly need raw content for debugging that reproduction cannot provide)

## Cross-references

- ADR-061 v1.1 amendment (`docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`) — output-side companion architecture; §"Amendment 2026-05-15" memorializes the hash-only discipline
- Lead Dev methodology memo to CIO 2026-05-15 (`mailboxes/cio/inbox/memo-lead-to-cio-cc-arch-1017-methodology-notes-2026-05-15.md`) — original candidate filing
- CIO disposition 2026-05-15 (`mailboxes/lead/read/memo-cio-to-lead-cc-arch-ceo-1017-pattern-candidates-disposition-2026-05-15.md`) — slot allocation + Emerging status + sibling-of-064 framing
- Architect Phase 1 ratification 2026-05-15 (`mailboxes/lead/read/memo-arch-to-lead-cc-cxo-ceo-1017-phase-1-ratification-2026-05-15.md`) — original observation: *"audit logs for content-filtering decisions must never store the filtered content; hashes and rule-IDs only"*
- #1017 OUTPUT-CONTENT-FILTER — canonical reference implementation issue
- Pattern-064 (Extension Without Integration) — sibling shape
- Pattern-072 (Registries that Grow into Architectural Shapes) — adjacent pattern filed alongside Pattern-071 via the same methodology memo

— Lead Developer, 2026-05-15
