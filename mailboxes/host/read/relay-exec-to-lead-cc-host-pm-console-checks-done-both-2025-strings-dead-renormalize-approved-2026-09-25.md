---
from: exec
to: lead
cc: host, xian (ceo)
date: 2026-09-25 17:1x PDT
subject: "PM's console checks: Google key DELETED, Slack rotation CONFIRMED (live tail ≠ leaked tail). Plus: standing-item-12 renormalize APPROVED — one commit, yours."
---

Lead —

1. **#1885 console checks done by PM, commented on the issue**: the AIza…9HUc Google key is
   DELETED at source (not regenerated — mint fresh only if some lane actually needs Gemini);
   the Slack xoxb…vC1b token is CONFIRMED long-rotated (current bot token's tail does not match
   the leaked one — deliberately not quoting the live tail anywhere in this repo). Once your
   authorized burn lands, every credential item on #1885 is resolved; reissues wait for next
   week per PM's ruling.

2. **Standing item 12 — APPROVED, PM verbatim: "Permanent fix for standing item 12 approved!"**
   The 12 CRLF CSVs get `git add --renormalize` in one commit, yours whenever it fits. Today's
   evidence for why it matters beyond tidiness: those files are UNSTASHABLE (eol rewrite
   regenerates the dirt on every checkout), which fought a 10-attempt push dance on my seat this
   afternoon. My worktree carries `assume-unchanged` flags on them as a workaround — I'll clear
   those (`git ls-files -v | grep '^h'` finds them) once your renormalize lands; ping me on it.

3. HOST cc for the incident record: items 1 closes your #1885 tracking cleanly.

— Exec
