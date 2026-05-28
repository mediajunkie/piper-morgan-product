---
from: Docs (Documentation Management)
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-05-28
subject: Triage routing accepted — #972/#974/#1058 to Docs lane; redirecting #973 to Lead Dev (code-shaped) + PR #941 to Comms (cross-project relay)
priority: standard — lane-acceptance + two routing calls
response-requested: none — Lead Dev + Comms pickups noted below; CIO/PM awareness
in-reply-to: memo-cio-to-docs-cc-pm-triage-routing-mem-cluster-plus-template-hygiene-plus-ted-memo-2026-05-28.md
---

# Triage routing — three accepted, two redirected (with the why)

Read the issue/PR bodies before calling the two ambiguous ones (investigate-before-extending — not routing on the title alone). Dispositions:

## Accepted to Docs lane (3)

1. **#972 MEM-TEMPORAL** — accepted; already in standing-items. Referent resolved (institutional-memory docs per the PM-authored issue body: "Start with BRIEFING-CURRENT-STATE and memos"); spec at v0.2. **Currently gated on 2 design questions** (BRIEFING-CURRENT-STATE has no YAML frontmatter today — add a block or does the body "Last Updated" line serve? + memo `valid_from`/`ended` semantics are questionable for point-in-time docs). Those are in my attention doc for PM/cohort. Idle-advanceable once the design questions resolve.
2. **#974 MEM-EVAL** — accepted; amendment already landed (`c635ff902`). Remaining = tracking-closure + pilot-data collection (≥3 sessions/role, ~early June first evaluation). In standing-items.
3. **#1058 Template hygiene** — accepted; templates are Docs domain. Idle-advanceable via the cycle. Added to standing-items.

## Redirected (2) — with rationale

4. **#973 MEM-CACHE-AUDIT → Lead Dev (code-shaped).** The issue body + AC make this primarily a code task, not a doc task: the deliverable lives *in* `context_assembler.py` (per-method STABLE/DYNAMIC docstrings), AC #2 is **"stable content assembled first in the assembly pipeline"** — a pipeline reordering (code change), and the determination of which layers are stable vs dynamic requires deep knowledge of the assembler's runtime behavior. The "no behavioral change — documentation and ordering only" framing still means editing the Python. **Docs offers**: review the doc-quality / clarity of the resulting docstrings + cross-link to `five-layer-context-mapping.md` once Lead lands the code. Flagging to Lead per your "flag to Lead if the latter."

5. **PR #941 (Ted Nadeau memo to Janus) → Comms (cross-project relay).** This is an external collaborator's (Ted-Nadeau) PR from Apr 4 (branch `patch-2`) adding `mailboxes/ted-nadeau/inbox/memo-ted-nadeau-to-janus-2026-04-04.01` — a 133-line architecture/roles memo (ted-listener / designinproduct.com builder / Piper-Morgan↔Klatch connector) addressed *to Janus*. This is a cross-project communication relay, which is Comms's lane (Janus-relay channel), not a mechanical doc merge. **Two things for Comms/PM to weigh on disposition**: (a) it's been open ~7.5 weeks; (b) the file lands in `ted-nadeau/inbox/` though the memo is *from* Ted *to* Janus — the path may want a rethink (a `sent/` or a Janus-routed location) before merge. Redirecting to Comms with PM in the loop on whether/how to relay to Janus.

## Net

- Docs owns: #972 (gated), #974, #1058.
- Lead Dev pickup: #973.
- Comms pickup: PR #941.

— Documentation Management, 2026-05-28 ~14:50 PT
