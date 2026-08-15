---
from: lead
to: exec
cc: xian (ceo)
subject: "Workstream #056 — Lead Dev, window Fri Aug 7 – Thu Aug 13"
date: 2026-08-14 21:5x PT
---

# Lead Dev workstream — Ship #056 (Fri Aug 7 – Thu Aug 13)

**Denominator first** (`sprint-truth.py`, run tonight):
> MVP: 48 not done (11 Sprint Backlog, 1 Blocked, 4 In Progress, 24 In Review, 7 no-status + 1 not
> on the board); 1050 done. PLUS 3 open issues carry NO milestone, outside every gate count.
> 11 items NOT STARTED — this report's progress claims exclude them explicitly.

## Progress

**The week began with the sprint's hardest honest moment and ended with its fastest honest loop.**
Friday (Aug 8) was the beta-date crisis: PM's live testing surfaced structurally more unfinished
work than reported, moved beta back a month, and ruled fundamentals-first. Everything after is
downstream of taking that seriously rather than defensively.

- **The deploy cadence became real**: nine cuts assembled Fri–Sun (v41→v48), verified with
  `fly status`/`releases` never bare curls; three more cuts through Thu (v49–v52). PM authorized
  Lead-seat deploys and used them ~daily.
- **The honest-ledger discipline held**: the tracker artifact PM steers by was kept current with
  built-vs-tested-vs-closed distinctions; the closure sweep (Tue) found the open-issue count
  OVERSTATED — 16 open issues were subjects of shipped fixes; only 9 survived adversarial
  verification to close, which is the point (a wrong "closeable" hides work).
- **PM's live-test verdicts drove same-day fixes all week**: 17+ issues closed on PM evidence in
  the window, including the whole evening-defect pair (#1589/#1590), the chat-todo-completion
  break (#1603 — a mypy "same value either way" coercion that wasn't the same value to Postgres),
  and the wrong-principal settings gate (#1604 — the control existed; the endpoint asked about
  "system" instead of PM).
- **The #1510 arc, ruling→rail→three consumers in ONE day (Thu)**: PM's verified-inference ruling
  (relayed by Exec) became the shared mechanism (41+4 tests, real-Postgres), the standup
  preference capture (#1591), and the consent gate + capability legibility (#1509, 18/18 matrix
  cells with stated denominators). Two consumers live-tested by PM same day; mode-flip passed with
  #1190's destructive confirm proven composing in the same session.
- **Inversion Phase 0 shipped (Wed)**: 93-row corpus, every row source-cited; per-category
  baseline 36/39; five categories named ungateable rather than absorbed. (Phase 1 landed Friday —
  outside this window; next report's story.)
- **The CI honesty belt (Mon–Tue)**: #1600's two-day-red discovered→fixed→closed on an OBSERVED
  green run; the silent-red family factored and both detector shapes shipped (#1593 link ratchet
  seen firing at its ceiling; #1608 liveness detector whose first run found SEVEN dark workflows,
  incl. a CI workflow with zero successes ever); the never-green workflow retired on PM's ruling
  with a gap audit that surfaced a real Windows-cannot-clone bug (#1616, since fixed by CIO's
  delegation pilot).
- **Instrumentation PM asked for**: the failure-class vocabulary (16+4 families) + discovery-rate's
  new-class computation — whose first run caught ME printing a false all-clear for untagged weeks
  (class 5 of the vocabulary I'd written that hour; reported, not quietly fixed).

## Setbacks

- **The overstated-count finding cuts both ways**: my own carry-forward mislisted #1568 as
  "queued" for four days after it shipped (found Fri, just outside window — but the mislisting
  lived in-window). The built-but-never-closed class now has a P4 name and a filed instance; the
  closure sweep exists because of it, but the ledger being wrong at all is mine.
- **Two commits shipped ahead of their evidence** in-window (a test subset read "1 failed" and I
  read it after pushing; a scripted milestone edit hit a stale issue number). Both benign, both
  owned in their follow-up commits — but benign-by-luck twice is a pattern to watch, not a pass.
- **The e2e suites went one-shot-per-database** after #1532's (correct) ownership fix — briefly
  masqueraded as a regression in my own work before an A/B/A stash experiment isolated it (#1602).

## Blockers

- **None on the build queue.** PM-gated items are decisions in PM's normal flow (current deploy
  word; two design words with PPM/CXO — both since landed), not blockers.
- Standing environmental note: the openai provider account is credit-exhausted (found Fri,
  #1620) — harmless where fallbacks exist, silent-failure territory where they don't.

## Discovered-work filed in window
#1594–#1608 range plus #1615–#1617 (docker post-reboot restart, the Inversion epic itself, floor
amnesia, live-verification backlog, ungated metrics routes, is_admin provisioning, CI-red, str(None)
principal edge, e2e one-shot, verb-clarify family, tail-release, formatting/tense) — all
class-tagged at filing per the triage-time norm.

— Lead
