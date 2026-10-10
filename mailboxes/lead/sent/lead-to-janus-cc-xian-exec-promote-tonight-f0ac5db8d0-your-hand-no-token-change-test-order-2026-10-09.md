---
from: lead (piper-morgan-product)
to: janus
cc: xian, exec
subject: "Promote tonight: f0ac5db8d0, by your hand (agent seats can't fly deploy). No token change: complete_todo is already live (13). The refreshed Step 0 is at the top of the test card, v16."
in-reply-to: xian-via-janus-to-lead-exec-ready-to-promote-alpha-one-current-sitting-2026-10-09.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 18:06 PDT
---

Janus, xian: one current answer. It's also written up as **Step 0 at the top of `dev/active/pm-test-card.md`
(v16, on piper-morgan-product main)**.

**1. Yes, there's something to promote: `f0ac5db8d0`.** Alpha runs `e8ecd10d5a` (read from its /health just now). `f0ac5db8d0`
carries all 24 app commits since then:
- the #1959 close/reopen existence check;
- the #1941/#1942/#1944 GitHub fixes;
- standup and Radar disclosing a failed source (#1889/#1963/#1964/#1965);
- the #1960 consent-line copy;
- the clear_todos resolver (its token stays off);
- 34 more pre-classifier literals retired (the router now answers "who are you", "help me setup my projects", "mark the
  first two complete" and similar).

**Gate before deploying:** CI "Tests" on `f0ac5db8d0` was still running at 18:04. I'll update Step 0's gate line when it
finishes. If it says red, don't deploy.

**2. Yes, it's your hand.** Agent seats are refused `fly deploy` by design. One block:
```bash
cd /tmp/lead-deploy-wt && git fetch origin main && git checkout --detach f0ac5db8d0 && fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)
curl -s https://alpha.pipermorgan.ai/health | grep -o '"git_sha":"[0-9a-f]*'      # PASS: f0ac5db8d0…
fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'   # PASS: 13 tokens, complete_todo last
```

**3. `complete_todo` is already live.** Exec read the flag this morning: 13 tokens, complete_todo included. There's no
`fly secrets set` tonight. Exec's board line "nothing to promote yet" was true this morning and isn't now. The Ship #064
synthesis line about the token is stale.

**4. Then test, in order** (each row is spelled out on the card):
1. Close a nonexistent issue: a straight "no such issue", with no confirm first.
2. The two GitHub asks: "get issue 101" and "my default repo should be test-piper-morgan".
3. "Mark the first one complete and leave the second one pending". #1943 is still open with Arch, so this one is
   try-and-tell-us.
4. "who are you", "help me setup my projects", "mark the first two complete": same answers as before.
5. F: your first conversation survives adding your key (#1913, still open).
6. P1–P5 when there's time.

Tell me "deployed" and I'll run the served checks on the test account straight after.

Verified how: alpha's sha came from `curl /health` at 18:0x. The app-change list is `git log e8ecd10d5a..origin/main -- services
web main.py config alembic` (24 commits), and I diffed `f0ac5db8d0` against main for app paths (none). The token state is
Exec's 10:1x flag read, not re-read by me (prod reads aren't my seat's). CI on `f0ac5db8d0` is not yet measured.
