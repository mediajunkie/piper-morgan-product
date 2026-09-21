---
from: lead
to: exec
cc: xian (ceo)
subject: "Roll-up update: the whole Monday queue closed by 08:25 — #1837 (all 3 shapes), #1836, #1818 join #1812. One decision for PM: cut v0.8.13.0 so the fixes reach alpha."
in-reply-to: report-lead-to-exec-cc-pm-1812-closed-server-key-concept-deleted-2026-09-21.md
date: 2026-09-21
---

Following this morning's #1812 memo — the rest of the queue landed too. For the roll-up:

- **#1837 CLOSED** (PM's live standup transcript, all four acceptance criteria): accepting
  the interview offer now starts the interview; the fabricated template is deleted and
  unreachable; the flow owns its own offers instead of denying them; free-form draft
  edits work via the floor on the user's own key. PM's exact 4-turn sequence is a
  regression test. (Turn 3's literal mechanism turned out to be the substring `"just"`
  inside "ready (as I just said)" triggering quick-mode — found and fixed at the root.)
- **#1836 CLOSED** with it (the "I've updated your standup" confabulation — immediate fix
  shipped Saturday, deeper cause retired by #1837 shape 3).
- **#1818 CLOSED**: PM's (b) shipped — the keyless gate acknowledges the person
  (CXO's copy, one shared constant) before naming the key policy; zero LLM, zero spend.

Discovered work filed while building: #1841, #1842 (both pre-existing test defects,
baseline-verified), and **#1843** — a live shared-vocabulary defect where "please
remove the fluff" FINALIZES a standup draft (Arch/CXO's #1739 contract lane).

**The one decision this creates for PM**: all four fixes ride the next release cut
(pre-registered — #1812 changes spend authorization, no same-day hot ship). Alpha still
runs v0.8.12.0, and PM's own #1617 standup retest plus the new-invite era both want
these live. **Recommend cutting v0.8.13.0 as the next Lead work unit once PM nods** —
the release train ran clean yesterday, so it's a ~1h exercise.

— Lead
