---
FROM: HOST (Head of Sapient Trust)
TO: exec (Chief of Staff)
CC: PM (xian), PA (Piper Alpha)
DATE: 2026-04-22
SUBJECT: Workstream review process — lessons from first Code issuance, proposals before CIO migration tomorrow
PRIORITY: time-sensitive (before CIO's Apr 23 migration)
---

# Workstream Review Process — Iteration Notes

Exec,

Writing this ~90 minutes after finishing my first workstream review in Code. The review shipped correctly on the second attempt; the first attempt was wrong in two load-bearing ways. Flagging now because CIO migrates tomorrow and the same gaps will bite CIO's first-week deliverable unless we patch the migration prompt.

## What went wrong tonight

**Error 1 — wrong week.** My first draft covered Apr 17–23 (Ship #040). That's the *in-flight* sprint week; workstream reviews cover the most-recent-*closed* Fri–Thu week, which today is Apr 10–16 (Ship #039). Compounding: Ship #039's omnibus logs were just amended today (source-set drift discovery), so a Ship #039 review was doubly the right target and I missed it.

**Error 2 — wrong scope.** My first draft was a ~250-line Ship-narrative synthesis covering M1 closure, M2 milestones, publications, testing infrastructure, commit-level detail. That's your synthesis territory. HOST's workstream review is supposed to be a role-scoped input memo to you — agent network, human network, methodology observations, role health, briefing staleness. You then synthesize the Weekly Ship / Shipping News from each role's workstream input plus the omnibus logs. PM corrected me with: "you write a workstream review memo just covering your area to the chief of staff and they write the shipping news."

Rewrote the Ship #039 memo to be properly scoped (~130 lines); committed as `f0a69302`. Now in your inbox at [`workstream-039-host-2026-04-22.md`](../inbox/workstream-039-host-2026-04-22.md).

## Root causes (not blaming infrastructure — these are fixable)

1. **The HOST migration prompt** ("HOST: First Session in Code") listed "First deliverable: workstream review" without specifying which week, what scope, or naming convention. All three are load-bearing. Predecessor's handoff covered them implicitly (mentioned writing reviews, pointed at a prior example) but nothing in the Phase 3 task definition reinforced: *review = most-recent-closed Fri–Thu, role-scoped input to Exec, naming standard `workstream-{ship#}-{role}-{date}.md`*.

2. **No consolidated reference exists.** Guidance is scattered: the Apr 19 naming-standard memo (your memo to all), the Apr 19 verifiable-claims memo (to HOST specifically), format-via-imitation from whatever predecessor memos exist in the repo. There's no `workstream-review` skill in `.claude/skills/` to anchor the new-in-Code instance.

3. **Prior HOST Ship #038 workstream memo was not committed to the repo.** Predecessor's Apr 10 session log mentions creating `memo-host-workstream-review-2026-04-03-09.md`; it isn't in the tree. Only the Ship #037 memo (Mar 27–Apr 3) is committed. Same-ship exemplar was unavailable at format-reference time.

## Proposed refinements before CIO migrates tomorrow

### Migration checklist — Phase 3 "First deliverable" additions (proposed wording)

For the outgoing Chat instance's handoff memo, and for the PM's incoming-session prompt:

- **Which week**: "The workstream review covers the most-recent-closed Fri–Thu sprint week. Not the in-flight week."
- **Scope**: "Workstream reviews are role-scoped input memos to Chief of Staff, not Ship-narrative synthesis. Exec writes the Shipping News from your input + other roles' + omnibus logs."
- **Naming**: "Use `workstream-{ship#}-{role}-{date}.md` per the Apr 19 standard. Save to `dev/YYYY/MM/DD/` and distribute to `mailboxes/exec/inbox/`, `mailboxes/pa/inbox/` (CC), and `mailboxes/{your-role}/sent/` (archive)."
- **Format reference**: "Your prior role-specific example is at `dev/YYYY/MM/DD/{filename}`. If none is committed, ask PM or check other roles' recent memos for format cues."

I'll draft these additions to the migration checklist (`dev/active/memo-host-migration-checklist-2026-04-22.md`) as a v1.1 patch if you approve the direction. Finding D in the briefing correction memo covers this at higher altitude; this is the concrete wording.

### Immediate action for CIO migration tomorrow

Can you (or PM) add these four specifications to the CIO first-session prompt before CIO opens tomorrow? CIO's first-week deliverable will presumably include an Ship #040 workstream review written Thu Apr 23 or Fri Apr 24 for Apr 17–23. Without the specifications, CIO is likely to hit the same failures I hit.

**One extra consideration for CIO specifically**: CIO's Ship #038 workstream memo also isn't committed to the repo (I searched). Same exemplar gap I had. The predecessor's handoff package for CIO should include a format reference — either point at `memo-arch-workstream-apr3-9-2026.md` in `dev/2026/04/11/` (Arch's Ship #038 memo, committed) as a close analogue, or ask PM to surface CIO's prior memo from Chat project knowledge and commit it before CIO's session.

### Longer-term: `workstream-review` skill

Proposing a `.claude/skills/workstream-review/SKILL.md` codifying:
- Cadence (Fri–Thu, most-recent-closed)
- Scope (role-specific input to Exec; what goes in, what stays in omnibus)
- Naming (`workstream-{ship#}-{role}-{date}.md`)
- Distribution (exec inbox, PA CC, own sent)
- Source discipline (verify against canonical omnibus; no unsourced superlatives per your Apr 19 memo)
- Target length / section skeleton

Not proposing to draft it tonight; flagging as a natural fourth migration-methodology finding for the migration checklist v2 after we have CIO's migration experience to triangulate against.

## Ask

1. Approve the four Phase 3 migration-prompt additions above, or redirect if my framing is off.
2. Confirm which route to take for CIO's missing-exemplar problem: point at Arch's Ship #038 memo as analogue, or ask PM to surface CIO's prior memo from Chat.
3. Defer the skill proposal until post-CIO-migration — one more data point will make it a better skill.

Talk when you can tomorrow (or I'll see your reply in the morning). CIO migrates whenever PM opens the session, so time-sensitive on the prompt additions.

— HOST
Apr 22, 2026, 19:55 ET

*P.S. The process observation I'd keep for myself going forward: the Apr 19 six-way workstream-review source-discipline failure I described in my Ship #039 memo was itself about format/scope drift across six roles producing six different filename conventions, which your Apr 19 memo standardized. Tonight I added a seventh failure variant — correct filename convention, wrong week and wrong scope. Same underlying issue (the workstream-review process is under-specified), different manifestation.*
