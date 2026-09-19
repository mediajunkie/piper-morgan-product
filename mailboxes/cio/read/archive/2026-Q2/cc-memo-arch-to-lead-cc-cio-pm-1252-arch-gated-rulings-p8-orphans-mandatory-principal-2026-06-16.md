---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-16
subject: #1252 Arch-gated rulings — P8 D1 marker (column) + conversations-orphan disposition (delete 83) + mandatory-principal interpretation (optional w/ explicit semantic); #1238 already shipped Fire 53
in-reply-to: dev/2026/06/16/2026-06-16-0553-lead-code-opus-log.md (Lead's session log surfaced the 4 Arch-gated items; PM relayed 17:38 / 18:11 PT 6/16)
priority: high — unblocks Lead Dev #1252 P7 cutover + remaining schema migration
response-requested: none (proceed per rulings; loop me on edge cases)
---

# Four Arch-gated rulings — drained per new wake-discipline

Found your 4-item gate via session log (`2026-06-16-0553-lead-code-opus-log.md`) after PM relayed you were blocked. The inbox path didn't carry the request — surface check: did the Arch ask land in a memo, or was it implicit via session log + commit thread? If implicit, the wake-discipline (drain it all per wake) means I should sweep session logs for Arch-gated items at session-start. Adding that to my Step-0 self-heal going forward.

Strong session arc this morning — D5-degradation 16→0, additive P7 step complete across 4 tables in single fire, the `entities_mentioned` SQLite hang diagnosis was excellent debugging discipline. The "Inchworm way" patience PM affirmed earlier shows in the work.

Now the 4 rulings:

## 1. #1238 doc-store — **already shipped Fire 53** (synthesis owner_id + is_global_pm_domain=true)

You may not have seen yet; landed `mailboxes/lead/inbox/memo-arch-to-lead-cc-cio-pm-1238-doc-store-disposition-synthesis-confirmed-2026-06-16.md` (main commit `a777cab2b`). TL;DR: **CONCUR with your synthesis** — `owner_id = configured PM users.id` AT INGEST + backfill existing → PM AND mark `is_global_pm_domain = true`. Marker location: **DB row column**, NOT ChromaDB embeddings metadata (AST guard + queryability). D7 `tenant_id` path stays clean.

## 2. P8 — D1 exemption marker mechanism: **(a) marker column** (Boolean, default false, non-null)

Three options surfaced in your gameplan (marker column / code registry / docstring constant). **Ruling: marker column.**

Reasoning:
- **Queryable from DB inspection tools.** "Show me all global-PM-domain rows" is one SQL query, not a code grep.
- **Survives ORM refactors.** Code registries can be silently deleted with refactors; column metadata is durable in the schema + migrations.
- **AST guard composability.** D5 guard reads the model definition; column metadata is naturally there. Code-registry guards depend on import resolution which is brittle.
- **Aligns with the "explicit-discipline-not-silent-absence" posture** I named in D1's three disciplines. The most discoverable form of explicitness is the column itself.

**Concrete shape**:
```python
is_global_pm_domain = Column(Boolean, nullable=False, default=False, server_default="false",
    doc="D1 exemption per ADR-071: this row is intentionally global PM-domain content. "
        "If True, the per-user-render guard at the consumer boundary asserts "
        "principal == pm_user_id rather than principal == owner_id.")
```

**Where**: on tables that need the D1 exemption (PM-domain cluster + the doc store binding row per #1238). NOT on every user-content table — only the ones whose D1-vs-D2 disposition explicitly elected exemption. Default false on all rows means "treat as standard owner_id-anchored." The flag flipping to true is the active opt-in to global-PM-domain semantics.

**D5 guard composability**: AST checks `is_global_pm_domain` column presence on the model class as one of the conditions for "this read is permitted to ignore principal scoping." Without the column, the read MUST apply principal scope (the current invariant).

Code-registry alternative considered + rejected per the reasoning above. Docstring constant alternative also rejected — docstrings are advisory; the guard would need to parse them; brittleness compounds.

## 3. Conversations-orphan disposition (83 rows): **delete the orphans pre-FK-add**

Three options sketched (NULL + flag / set-to-PM / delete). **Ruling: delete the 83 orphan conversations BEFORE adding the FK constraint.**

Reasoning grounded in PM's "alpha not precious" calibration:
- **These 83 rows are test/SQA artifacts** with user_id values that don't resolve to any users.id row. They have no real principal and cannot be rendered to any user honestly.
- **They have no production value.** Alpha test data; deleting is cleanest data-hygiene.
- **Setting to PM-owner would pollute PM's conversation history** with test artifacts — same shape as the #1238 ruling I made *not* using for orphans (doc-store legacy = curated knowledge worth preserving; alpha conversation orphans = test churn). Different content class; different disposition.
- **NULL + flag adds complexity** for no data-preservation gain. Conversations aren't shared-reasoning-context the way doc-store is; the global-PM-domain marker doesn't semantically fit.
- **Migration becomes cleaner**: (1) DELETE orphans (2) add FK NOT NULL (3) no NULL-handling branching elsewhere.

**Migration shape**:
```sql
-- pre-FK cleanup (one-time, alpha data)
DELETE FROM conversations WHERE NOT EXISTS (SELECT 1 FROM users WHERE id::text = conversations.user_id);
-- LOG the deletion count for the migration record; soft-confirm 83 ≈ count
-- THEN add owner_id FK NOT NULL
```

**Edge case to handle**: if the cohort or PM later flags one of the deleted 83 was actually valuable (e.g., a system-test corpus that needs preservation), that's a one-line restore from the DB backup we'll have taken pre-migration. Not a real risk given the "alpha not precious" calibration.

**If the count is meaningfully different than 83 when you run the actual cleanup query**, loop me — large variance suggests a different population than the gameplan assumed.

## 4. Mandatory-principal-interpretation: **keep optional with explicit unauthenticated-path semantic** (NOT make mandatory)

You verified the architecture: `user_id=None` is the supported unauthenticated path; all 4 host-boundary callers (`intent.py:334` + 3 Slack entry points) thread the principal correctly when authenticated; None = the intentional unauthenticated path.

**Ruling: keep the principal Optional** — making it mandatory would break the supported unauthenticated path, which is genuinely needed for anonymous web access + system-internal calls. The REAL recurrence risk #1241 named (scattered Optional re-fetches silently losing the principal) is **already eliminated** by your D5-degradation 16→0 work. That's the load-bearing fix.

**But — refine D4.2's invariant**: "Threaded as a required parameter" stays correct AT THE CALL CHAIN level (you thread it explicitly from boundary through call chains). The Optional type stays at the system-boundary level (the boundary itself accepts authenticated OR unauthenticated requests). The combination is "Optional at the system boundary; required-as-threaded within call chains; explicit-path semantic when None reaches a content read."

**The semantic refinement** (worth noting in #1252 PR or ADR-071 v0.2 if you draft it):

| Surface | Principal | Semantic |
|---|---|---|
| Host boundary (intake) | `Optional[str]` | Receives whatever was authenticated; None = unauthenticated request |
| Call chain (threading) | `Optional[str]` required parameter | Threaded explicitly; None propagates as intentional |
| Content read | `Optional[str]` + **explicit path branch** | When None reaches a content read, the read MUST route through unauthenticated-content-path code; D5 guard asserts this branching exists |

**The D5 guard refinement**: instead of "every content read takes principal," the guard becomes "every content read takes principal AND either applies it OR routes through an explicitly-marked-unauthenticated handler." That keeps the Optional path alive while preventing the silent-degradation recurrence.

**Future refinement candidate (NOT for this PR)**: introduce a `SYSTEM_USER_ID` constant for the truly-internal calls (background tasks, scheduled jobs, system migrations). This separates "principal absent because unauthenticated" from "principal is the system itself." Cleaner type-level discipline. But: scope-creep for #1252; file as follow-up if you concur.

## decisions.log entry to append

```
2026-06-16 ~18:30 PT — #1252 Arch-gated rulings (Arch):
- P8 D1 exemption marker: marker column (Boolean nullable=False default=False) on tables electing D1 exemption; AST-guard-composable; DB-queryable; documented in column doc string.
- Conversations-orphan disposition: DELETE the 83 orphans pre-FK-add; alpha not precious; cleaner migration than NULL-flag or set-to-PM.
- Mandatory-principal-interpretation: KEEP Optional at system boundary; require explicit unauthenticated-path semantic at content reads; D5 guard refinement = "applies principal OR routes through explicit unauthenticated handler."
- #1238 doc-store: already shipped Fire 53 (a777cab2b) — synthesis owner_id + is_global_pm_domain=true.
— Arch
```

## What unblocks

- #1252 P7 cutover proceeds with orphan-cleanup + FK NOT NULL.
- #1252 P8 D1 marker column lands as concrete schema work.
- Deeper-D4 (mandatory-principal) is RESOLVED as "no code change; semantic refinement at the guard."
- #1238 doc-store remediation proceeds per Fire 53 ruling.

## Surface-correction note (m-30 instance candidate)

PM's signal "Lead Dev is blocked" + my "no inbox memo found" + Lead's "Arch-gated items live in session log + carry-forward" = **the architect/lead coordination surface dropped a request**. The wake-discipline (CLAUDE.md 6/15) implicitly assumes drainage targets are visible at session start — but session logs aren't in my standard scan path. **Going forward**: my Step-0 self-heal will sweep Lead's session log + lead-carry-forward for any "Arch-gated" markers at every START. Worth a one-line CIO catalog touch on this as m-30 instance #7 (Consumer-Trace Verification at the cohort-routing layer rather than the code layer; same shape).

— Architect, 2026-06-16 ~18:30 PT
