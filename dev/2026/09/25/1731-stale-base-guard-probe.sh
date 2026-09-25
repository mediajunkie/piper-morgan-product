#!/bin/bash
# #1731 sandbox probe (Lead, 2026-09-25). Builds nothing against the real origin: run it from a
# scratch dir holding remote.git (bare) + seed/ + agent/ clones as described on the issue.
cd "$(dirname "$0")/agent"; export PIPER_MAIL_REMOTE=origin PIPER_MAIL_BRANCH=main
ms() { bash scripts/mail-send.sh "$@" 2>&1 | grep -E "pushed|REFUSING|nothing to send" | head -1; }
ox() { git fetch -q origin; git cat-file -p origin/main:mailboxes/a/inbox/X.md 2>/dev/null | tr '\n' '|'; }
git fetch -q origin; git reset -q --hard origin/main; git clean -qfd -e scripts/; mkdir -p mailboxes/a/read; cp /Users/xian/Development/piper-morgan-worktrees/lead/scripts/mail-send.sh scripts/; grep -c "STALE-BASE GUARD" scripts/mail-send.sh
printf 'local\n' > local.txt; git add local.txt; git commit -qm "local commit (branch diverges, as every role branch does)"
echo "--- Case A with guard: send v1+L2, then append L3 on the reconciled (stale) copy, send again"
printf 'v1\nline2\n' > mailboxes/a/inbox/X.md; ms s1 mailboxes/a/inbox/X.md; echo "origin X: $(ox)  worktree X: $(tr '\n' '|' < mailboxes/a/inbox/X.md)"
printf 'line3\n' >> mailboxes/a/inbox/X.md; ms s2 mailboxes/a/inbox/X.md; echo "origin X after s2: $(ox)   (must still hold line2)"
echo "--- PPM shape: plain re-pass of the reconciled path"; git checkout -q HEAD -- mailboxes/a/inbox/X.md; ms s3 mailboxes/a/inbox/X.md; echo "origin X after s3: $(ox)"
echo "--- the prescribed recovery: merge, re-apply, send"; git merge -q origin/main --no-edit && printf 'line3\n' >> mailboxes/a/inbox/X.md && ms s4 mailboxes/a/inbox/X.md; echo "origin X after s4: $(ox)"
echo "--- normal flows still pass: new memo; move inbox->read; MANIFEST regen"
git merge -q origin/main --no-edit; printf 'memo\n' > mailboxes/a/inbox/M.md; ms s5 mailboxes/a/inbox/M.md
git merge -q origin/main --no-edit; mv mailboxes/a/inbox/M.md mailboxes/a/read/M.md; printf 'm2\n' > mailboxes/a/inbox/MANIFEST.md; ms s6 mailboxes/a/inbox/M.md mailboxes/a/read/M.md mailboxes/a/inbox/MANIFEST.md
git fetch -q origin; echo "origin: inbox/M=$(git cat-file -e origin/main:mailboxes/a/inbox/M.md 2>/dev/null && echo present || echo absent) read/M=$(git cat-file -e origin/main:mailboxes/a/read/M.md 2>/dev/null && echo present || echo ABSENT) MANIFEST=$(git cat-file -p origin/main:mailboxes/a/inbox/MANIFEST.md)"
echo "--- cross-agent: another clone pushes X; this clone (unmerged) edits X and sends"
(cd ../seed && git pull -q origin main && printf 'other agent line\n' >> mailboxes/a/inbox/X.md && git commit -qam other && git push -q origin main)
printf 'mine\n' >> mailboxes/a/inbox/X.md; ms s7 mailboxes/a/inbox/X.md; echo "origin X after s7: $(ox)   (must keep 'other agent line')"
