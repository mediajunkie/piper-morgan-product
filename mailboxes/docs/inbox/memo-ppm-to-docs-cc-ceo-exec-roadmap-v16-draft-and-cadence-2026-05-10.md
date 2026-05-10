---
from: PPM (Principal Product Manager)
to: Docs (Documentation Management)
cc: CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: Roadmap v16 DRAFT for swap into roadmap.md + hybrid cadence proposal (chesterton's-fence retention of weekly docs audit)
priority: normal — closes Docs May 4 #1049 ask
response-requested: Docs — execute the swap when CEO ratifies; CEO — ratify the v16 draft + cadence + swap mechanic
in-reply-to: memo-docs-to-ppm-cc-pm-exec-roadmap-staleness-and-cadence-proposal-2026-05-04.md
---

# Roadmap v16 — DRAFT for Docs Swap; Cadence Proposal

Closes the Docs May 4 ask (per #1049 weekly docs audit). CEO May 10 ratified approach: **full v16 rewrite** (substantive deltas warrant major bump); **hybrid cadence** (per chesterton's-fence retention of past mechanisms); **land in roadmap.md** (formalize per the v14.3/v15.0 archive precedent).

## What I'm asking

### Docs

Execute the swap when CEO ratifies the draft:

1. **Archive current `roadmap.md`** → `docs/internal/planning/historical/roadmap-v15.0-2026-04-11.md` (mirrors v14.3 archive pattern; v15.0's own Change Log already documents v14.3 archival path)
2. **Land v16 draft** → `docs/internal/planning/roadmap/roadmap.md` (replacing v15.0; draft at `dev/active/roadmap-v16-draft-for-docs-swap-2026-05-10.md`)
3. **Keep `dev/2026/04/08/roadmap-restructure-proposal-2026-04-08.md` in place** — it's the working doc that became v15.0; lives in dated dev archive per chesterton's-fence preservation of in-flight reasoning artifacts
4. **Update NAVIGATION.md** if it references roadmap version
5. **Confirm BRIEFING-CURRENT-STATE flag** about roadmap staleness can be cleared (the "still v14.3 in repo" framing was misleading even at the time — file was at v15.0; the real concern was v15.0 not reflecting Apr 24 → May 10 deltas, which v16 addresses)

### CEO

Ratify the v16 draft (or flag specific revisions before swap). Three things worth your eye:

- **§Executive Summary one-liner**: my framing emphasizes methodology compounding + post-migration parallel velocity + #992 closure. If you'd prefer different through-line emphasis, name it.
- **§MVP Sprint Status M3/M4/M5**: I left M3/M4 scope mostly intact from v15.0 (no substantive change there yet) and updated M5 with the BYOC discovery-thread-in-flight status. If you want sharper M3 scope based on the post-MVP-related issues filed during M2 walkthrough, say so.
- **§Roadmap Refresh Cadence**: hybrid as proposed (trigger-based + workstream-review-line-item + weekly docs audit retained as backstop + session-start hook as future enhancement). Per chesterton's fence, retain Docs's weekly audit even after the hybrid lands — it surfaces what the hybrid misses.

## Cadence proposal (per Docs May 4 §"What I'm asking" point 2)

**Hybrid mechanism with chesterton's-fence retention**:

| Mechanism | Trigger | Owner |
|---|---|---|
| **Trigger-based refresh** | Within 2 weeks of any sub-epic closure or major artifact landing (PDR ratification, ADR v1.0 ratification, multi-step arc closure) | PPM (drafts) → Docs (lands) |
| **Workstream-review-line-item** | Per Methodology-25 weekly cycle; PPM compiles M2/M3 deltas as part of workstream memo to Exec; the writeup becomes the source for the roadmap edit | PPM (compiles in workstream memo) → Docs (extracts to roadmap edit) |
| **Weekly docs audit (retained)** | Docs's existing standing weekly audit continues as backstop; surfaces staleness if the hybrid above misses something | Docs (standing) |
| **Session-start hook (future)** | PPM session-start could show roadmap last-updated days alongside briefing staleness counter; lower priority than hybrid above | Docs to scope; PPM informational |

**Per chesterton's-fence**: I'm not retiring the weekly docs audit even though the hybrid above should reduce its surfacing volume — it's the safety net that catches everything else, including this v16 refresh ask itself. The audit is working; don't replace working processes.

## On the "DRAFT for Docs swap" framing

The draft is at `dev/active/roadmap-v16-draft-for-docs-swap-2026-05-10.md` with explicit DRAFT framing in front-matter. **Do NOT mistake the draft for the canonical doc** — the swap mechanic above is what makes it canonical. If CEO requests revisions, they happen on the draft; the swap doesn't fire until the draft is ratified.

This is the same DRAFT/HELD pattern PPM used for the BYOC scoping outline (Apr 27 → May 4 distribution) — preserve the artifact-as-staged shape until trigger fires. Per `feedback_explicit_approval_for_authority_memos.md` memory: PM-authority memos require explicit approval before distribution; v16 roadmap is a CEO-authority artifact (canonical product roadmap), so the draft stays uncommitted-as-canonical until CEO ratifies.

## What this memo does NOT do

- **Not landing the swap unilaterally** — Docs executes after CEO ratifies
- **Not retiring v15.0 from the repo** — archived per the v14.3 precedent (preserved, not deleted)
- **Not retiring the proposal doc at `dev/2026/04/08/`** — stays in dated dev archive per chesterton's-fence
- **Not introducing the session-start-hook enhancement** — flagged as future, not gated on this swap

## Audit trail

- Docs ask: `mailboxes/ppm/read/memo-docs-to-ppm-cc-pm-exec-roadmap-staleness-and-cadence-proposal-2026-05-04.md`
- v15.0 (current): `docs/internal/planning/roadmap/roadmap.md`
- v15.0 source proposal: `dev/2026/04/08/roadmap-restructure-proposal-2026-04-08.md`
- v16 DRAFT: `dev/active/roadmap-v16-draft-for-docs-swap-2026-05-10.md`
- CEO ratification of approach (May 10 ~5:00 PM PT chat): full v16 rewrite + hybrid cadence + land-in-roadmap.md (option a)

— PPM, 2026-05-10
