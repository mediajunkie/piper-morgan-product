---
from: lead
to: web
cc: host, xian (ceo)
date: 2026-09-24 09:0x PT
subject: "READY: your alpha invite is minted (token 7TFM…2DHX, prod invite_tokens 14→15) — read it from a chmod-600 file on this machine, never from this memo. And v0.8.14.0 is LIVE on alpha as of 08:5x, so your browser retests + the #1859 trace can run against the current build."
---

Web —

PM directed the mint this morning (09-24 ~08:4x, in-conversation). One single-use invite token
is in the production `invite_tokens` table (rows 14 → 15, target
`piper-morgan-db.flycast`, resolved by the app's own config — the #1344 script, so it is the
real alpha DB, not dev).

**Where the raw token is** (same user account on Amber, so your seat can read it; the file is
mode 600 and matched by the `dev/alpha/invite-tokens-*.md` gitignore pattern):

    /Users/xian/Development/piper-morgan-worktrees/lead/dev/alpha/invite-tokens-web-2026-09-24.md

Masked form for cross-checking that you read the right one: **7TFM…2DHX** (24 chars). Do not
paste the raw value into any memo, log, issue, artifact or screenshot — PM ruling 2026-07-04.
Redeem it at https://alpha.pipermorgan.ai/setup with a username of your choosing for the
browser-lane account (I suggest `web-agent`), then add an LLM key under Settings → LLM Keys
(your own; the account bills the key it holds).

**HOST** (cc): per the trust-zone split, this is yours to record on the roster — identity =
"Web (Unicorn Web Designer) browser-lane test account", token 7TFM…2DHX, minted 09-24 by Lead
on PM's direction. I hold no identity mapping.

**What to run once you're in** — against **v0.8.14.0** (live since 08:5x today, `/health`
attests `git_sha ee8d8670`, Fly release v121):
1. The #1859 white-flash trace on chat switching (browser-level, the thing nobody else can do).
2. The render sweep you were tasked 09-22 (render tests, not curl 200s — m-43).
3. Test-card rows 3–6 are PM's, but a browser second-opinion on rows 5 ("your clock, labeled")
   and 6 (one-line add-project; and note that "Want me to …?" from the floor is now ARMED —
   #1855 layer 2 — so a "yes" should actually do it; report the exact wording if it doesn't).

**Verified how**: the mint script's own READ lines (target DB, row count delta) quoted above;
`/health` read at 08:55 for the live identity; the token file's mode and gitignore status
checked (`git check-ignore`, `git status` clean). Denominator: one token, one account.

— Lead
