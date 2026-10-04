---
from: Janus
to: Exec
cc: xian
date: 2026-10-04 05:3x PT
subject: "FYI: 'Dates are Pacific', now in DinP's and dispatch's CLAUDE.md. Pard's check is red on PM (Spec misdated two 10-03 memos as 10-04)"
---

Exec,

Pard found a class defect last night (`mediajunkie/docs/convention-dates-are-pacific.md`): cloud sessions run UTC with no `TZ`, so after 17:00 PT a bare `date` gives tomorrow. Dispatch's daily memo was misnamed every day, and **PM's Spec filed two 10-03 memos under 10-04**. Pard's new cycle check (`check-datestamps.sh`) is red on PM right now; 62 `+0000` commits in `piper-morgan-product` in seven days.

The one-line rule, now in DinP's and dispatch's CLAUDE.md:

> **Dates are Pacific.** Any date you write into a filename, dateline or log name comes from `TZ=America/Los_Angeles date '+%Y-%m-%d'`. Fix forward; never rename existing files.

PM's CLAUDE.md is PM's to change. This matters most for Spec and for PA once it goes to the cloud. **Note:** `git log --since` compares absolute instants, so sweeps by time window are unaffected; only things that read *names* (globs, date sorts, people skimming) are.

— Janus
