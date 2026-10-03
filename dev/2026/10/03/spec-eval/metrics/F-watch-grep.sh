#!/bin/bash
# F-watch-grep.sh — count files (session logs dev/2026/0[6-9]|10, mailboxes) mentioning watcher outcomes. Read-only.
cd /home/user/piper-morgan-product
for pat in "false positive|false-positive|false alarm|false-alarm|alerting on compliance" "genuine(ly)? (stall|frozen|stale)|real stall|caught a real|true positive|actually frozen|confirmed frozen|confirmed dead" "merge-keeper.*(stranded|caught|found)" "ci.liveness.*(caught|flag|red)" "false.clean|false clear|all-clear.*(wrong|false)"; do
  L=$(grep -rliE "$pat" dev/2026/0[6-9] dev/2026/10 --include=*.md 2>/dev/null | wc -l)
  M=$(grep -rliE "$pat" mailboxes 2>/dev/null | wc -l)
  echo "[$pat] session-log/dev files=$L mailbox files=$M"
done
