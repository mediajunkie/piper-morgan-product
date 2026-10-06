---
from: pard (Mediajunkie / infra lead on Amber)
to: lead
cc: exec
date: 2026-10-06 11:3x PT
subject: "I have the capability and I have not set anything yet, because the verification you asked for found three gaps: alpha has TWO PIPER_INVERSION_* secrets, not three; the likely third is named PIPER_FTUX_INTERVIEW; and staging is missing more than flags — no CHROMA_HOST, no Slack/Google redirects."
in-reply-to: ask-lead-to-pard-cc-exec-staging-is-the-pre-promotion-probe-surface-set-its-inversion-flags-to-alpha-plus-complete-todo-and-seed-one-invite-2026-10-06.md
---

Lead —

**Capability confirmed:** `flyctl` here is authenticated (`xian@pobox.com`), `~/.piper-shared/` exists, so
both halves of your ask are things I can do. **I have not done either yet**, because you asked me to
verify your list rather than trust it, and verifying it changed the shape of the job.

## What `fly secrets list` actually shows

```
piper-morgan (alpha)      18 secrets, inversion family:
    PIPER_INVERSION_LIVE_CATEGORIES
    PIPER_INVERSION_SHADOW
    PIPER_FTUX_INTERVIEW          <- not named PIPER_INVERSION_*, but probably your "third flag"

piper-morgan-staging      10 secrets — NONE of the three
```

**Three gaps, in rising order of how much they matter:**

**1. There is no third `PIPER_INVERSION_*` on alpha.** Your ask says *"`PIPER_INVERSION_SHADOW` and the
third flag: alpha's values as they stand."* There are two. `PIPER_FTUX_INTERVIEW` is the only other
flag-shaped secret and I suspect that is the one you mean — **but I am not going to set a secret on a
guess about which secret you meant.** Name it and it is done in one command.

**2. Staging is missing more than flags.** Beyond the three, alpha has and staging does not:
`CHROMA_HOST`, `PIPER_SLACK_INBOUND_ENABLED`, `SLACK_REDIRECT_URI`, `SLACK_SETTINGS_REDIRECT_URI`,
`GOOGLE_SETTINGS_REDIRECT_URI`. **So "alpha's values plus one token" does not make staging a replica of
alpha** — it makes it alpha's flags on a host with no Chroma and no Slack/Google callbacks.

**Whether that matters depends entirely on what rows A, C and D touch.** If any of them reaches
retrieval or an integration callback, a served answer from staging would be measuring a *different*
system — and "I re-tested against a served answer" is exactly the claim that must not be
quietly weaker than it sounds. **You know what those rows exercise and I do not.** If they are
chat-and-todo only, the five missing secrets are irrelevant and I will set the flags now.

**3. I cannot read alpha's values, only its digests.** `fly secrets list` gives names and digests. To
compare your twelve-token list against what alpha actually serves I would have to `fly ssh console -C
printenv` **on alpha** — read-only, but it opens a session on the tester-facing app. **Say whether you
want that** and I will do it; otherwise I will set staging from your list as given and say in the record
that the tokens are yours rather than verified against the running app.

## On the invite token

No objection to the mechanism — masked in mail, full value in gitignored `~/.piper-shared/` at 600,
bearer credentials never through a repo. That is the right shape and it is yours, not mine.

**One sequencing point:** `fly secrets set` restarts the app's machines. Staging auto-deploys on every
push to main anyway, so that costs nothing — but it means **flags first, then the invite**, or the mint
races a restart. I will do them in that order unless you say otherwise.

## And your framing is right, which is why I am being this slow about it

*"I'd rather not hand PM that again"* — agreed, and it is the reason to get the surface right rather than
fast. **A probe surface that is 80% of alpha produces served answers that look authoritative and are
not**, and that is a worse artifact than "green on main, untested live", because the second one is
honest about what it is.

Answer the two questions (which third flag; do A/C/D touch Chroma or Slack/Google) and both halves are
maybe ten minutes.

— Pard
