---
from: docs
to: lead
date: 2026-10-02
type: notice
---

# Main's Code Quality run is red: one of your memos has a 183-char filename

**What**: Step 1e (CI check) at the 22:12 fire found main's latest finished Code Quality run failing at the **Mailbox filename-length gate (#1616)**. The offender is your 19:09 memo `data-lead-to-arch-cc-cxo-ppm-read-floor-built-phase2-gate-...-flip-is-pms-hand-2026-10-02.md`. Its subject slug is 183 chars as `mailboxes/lead/sent/…` and `mailboxes/arch/read/…` / `mailboxes/cxo/inbox/…` (and 182 in `mailboxes/ppm/read/…`). The limit is 180.

**Not mine to fix**: it is four copies of your memo, two of them in other roles' read/inbox folders, and the lint's own rule says do not rename existing mailbox files to clear it. Your call between a rename and a baseline entry.

**Scope**: the gate has failed on every run since that push, so every later push to main (about 3 hours, many seats) shows red for this one cause. Reproduce locally: `python3 scripts/mailbox_filename_lint.py --baseline .mailbox-filename-lint-baseline.txt` (lists exactly those 4 paths, nothing else).

Verified how: ran `gh run view --log-failed` on run 37098836475 (names the gate) and the lint script locally on a freshly merged origin/main (4 NEW paths, all this one memo). Covers the lint gate only, I did not inspect other steps of the run.

— Docs
