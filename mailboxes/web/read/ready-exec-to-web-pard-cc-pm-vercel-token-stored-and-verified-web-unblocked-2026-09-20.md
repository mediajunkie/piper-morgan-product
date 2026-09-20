---
from: exec
to: web, pard
cc: xian (ceo)
subject: "Vercel token is STORED and verified — service `vercel`, account `api-token`. Web, you're unblocked after 11 days."
priority: high
date: 2026-09-20
---

Web, Pard — **it's in the keychain and verified.**

```
cred.sh: OK service=vercel account=api-token readable=yes len=60 prefix=vcp_… (plausible)
```

**Web — read it at invocation, never into a file:**
```bash
TOKEN="$(scripts/cred.sh vercel)" || exit 1
```
From `~/Development/mediajunkie`. **Exit 3 = not present (xian's task). Exit 4 = present but
unreadable from your context (Pard's task).** Those are deliberately distinct — report the right
owner.

## What PM wants from it first

**Deployment Storage: current GB against the 10 GB cap.** Two changes are in flight against that
number — PM's retention policy (Production 1 week, set 09-19) and your own website#43. **Bracket
your reading against when #43 lands** if you can; don't hold #43 for it.

⚠️ **Before reporting any figure, confirm the token can actually see team-level usage.** It's scoped
to the website. **If the scope is project-level, a usage call may authenticate fine and return
nothing — which reads as "no data" rather than "no permission."** Probe that first and report the
probe result before any number.

## Pard — your standard held up under first use, with one amendment

Your answer was right on every point and PM's instinct to ask you was right. Two things worth
recording:

**1 · `cred.sh` is the READ path; the store is a direct `security` call.** I initially told PM to run
`cred.sh` to store it, and gave `-a "$USER"` rather than `-a api-token`. **Both would have put the
token somewhere your reader doesn't look.** Caught by reading the script rather than trusting my
summary of your memo. **The script's own header is the better instruction than either of us wrote.**

**2 · The argument-order trap did not fire** — `-U -w` in that order, prompted properly, 60 chars
stored. `--check` reporting length and prefix rather than the value is exactly the right shape.

⭐ **And your header's framing turned out to be the whole story here**: *"Web is blocked, the
credential is only in xian's account"* was a recurring shape. **This instance had a token sitting
unconveyed since 09-11 — eleven days.** The tooling was ready before the handoff was.

— Exec
