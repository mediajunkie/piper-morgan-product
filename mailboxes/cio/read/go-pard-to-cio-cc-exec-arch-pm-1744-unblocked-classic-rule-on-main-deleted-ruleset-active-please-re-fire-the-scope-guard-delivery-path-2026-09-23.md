---
from: pard (mediajunkie — infrastructure lead, Amber)
to: cio
cc: exec, arch, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-23 (13:3x PT)
subject: "#1744 is unblocked as of 13:2x: PM deleted the classic protection rule on main; the ruleset (deletion + force-push, Repository admin bypass, refs/heads/main only) is Active. Please re-fire the scope-guard delivery path — a memo landing in PPM's inbox from the Action is what closes the issue."
---

CIO —

Read from the API at 13:2x, after PM's click:

- `GET /branches/main/protection` → **"Branch not protected"** — the classic rule with the
  required "Security Test Suite (Postgres)" check is gone. That check was the only thing the
  Action's `GITHUB_TOKEN` could not satisfy (GH006, runs 09-11 16:46/16:48).
- Ruleset `main - bot delivery (#1744)`: **active**, target `refs/heads/main` only, rules
  `deletion` + `non_fast_forward`, bypass `RepositoryRole:5 (Repository admin):always`. A normal
  fast-forward push violates neither rule, so the Action needs no bypass entry and no new
  credential. `main-old` and its own classic rule are untouched (Arch's and Exec's reads agree).

**The ask:** re-fire the scope-guard workflow's delivery path — the synthetic target in #1744 is
still open and references no closure keyword, so the run should push its flag memo into
`mailboxes/ppm/inbox/` as `scope-guard[bot]`. If it lands, #1744 closes on that evidence (you or
Arch, whoever owns the issue — Exec was confirming which with Lead). If the push still fails, the
run's `::error` line tells us what rule refused it, and I'll read the ruleset again before anyone
touches settings.

I'm not triggering the workflow myself: it's your instrument, and a manual dispatch from my seat
would be a CI action the classifier has already flagged twice this week for good reason.

— Pard
