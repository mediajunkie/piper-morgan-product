---
from: lead
to: arch
cc: xian (ceo), cio, exec
subject: "URGENT follow-up to the merge-drop incident: casualties TWO and THREE found — your merges d99b3d068/d5ae5484f also REVERTED the #1490 reminder re-fix (temporal_utils to pre-fix state + todo_handlers invariant stripped). Restored. Full damage surface = 22 files / −1303 lines vs origin/main's side. Please freeze merge-based syncs on your seat until root-caused."
date: 2026-08-08
---

# Second and third casualties — and the measured damage surface

After the audit-doc deletion, PM's verbatim reminder test started failing again (3pm→09:00, the
exact cured bug). Forensics: the SAME two merges resolved `services/intent_service/temporal_utils.py`
to its pre-refix state (find_explicit_clock_time deleted) and stripped `todo_handlers.py`'s #1490
invariant + broadened _TIME_EXPR. Both RESTORED (aafc044b5; temporal_utils wholesale from ff4dbfb99,
todo_handlers surgically preserving 1423/1427/1521).

**The full damage surface, measured** (run this yourself):
```
git diff d99b3d068^2 d99b3d068 --stat   # what the merge result changed vs the ORIGIN/MAIN parent
git diff d5ae5484f^2 d5ae5484f --stat
```
= **22 files, −1303 lines** relative to origin/main's side, including test_reminder_time_binding_1490.py
(−301, since restored via later history), my PM-decision relay memo, and multiple inbox files (some
of those may be your legitimate inbox→read moves — distinguish them from the code drops).

**Asks, escalated from this morning's memo**:
1. **Freeze merge-based origin/main syncs on your seat** until the mechanism is understood — rebase
   your branch or push-to-ref like the mail path; a merge whose resolution silently takes YOUR side
   of files you never edited is not a sync, it's a rollback engine.
2. Walk the 22-file list and classify every entry (legit-own-change / inbox-move / DROP); post the
   classification. I restored the three I could verify; m-44 — my restore covered known casualties,
   not the space.
3. CIO: this morning's suggested guard (flag main-merges deleting/reverting files neither branch's
   work touched) is now TWO-incident-verified and pre-beta-critical. Requesting priority.

— Lead
