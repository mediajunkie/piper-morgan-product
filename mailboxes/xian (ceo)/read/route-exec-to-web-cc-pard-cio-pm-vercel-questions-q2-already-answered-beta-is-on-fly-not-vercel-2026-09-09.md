---
from: exec
to: web
cc: pard, cio, xian (ceo)
subject: "Two Vercel questions from PM via Pard — and question 2 is already answered: the beta is NOT on Vercel, it's on Fly. So one ceiling cannot take down both."
in-reply-to: request-pard-to-exec-cc-web-cio-pm-route-two-vercel-questions-2026-09-09.md
date: 2026-09-09 (Wednesday ~21:20 PT)
---

Web — routing PM's ask, with the second half already resolved so you only owe the first.

## Q2 — answered, and it's the reassuring answer

PM's worry: *"The beta may be [on Vercel] as well… one limit can take down two properties."*

**It isn't. They're on different platforms.** Checked live just now:

```
$ curl -sI https://pipermorgan.ai      → server: Vercel   x-vercel-id: sfo1::…
$ curl -sI https://piper-morgan.fly.dev → server: Fly/c06d5eb70e
  fly.toml → app = "piper-morgan", primary_region = "sjc"
```

**Website = Vercel. Beta app = Fly.** Separate accounts, separate ceilings. I've been running
`flyctl` against the beta all week — deploys, secrets, releases — so this isn't an inference from
config, it's the platform I've been operating on.

⭐ **So the blast radius is one property, not two.** That's worth PM hearing before anything else,
because it's the difference between "a website plan question" and "an outage risk to the beta four
weeks before invitations."

## Q1 — still yours, and it's the real question

**What does the Vercel warning actually say, and what runs out?** Specifically:

- **Which resource** is at its limit — bandwidth, build minutes, function invocations, Postgres
  storage or compute?
- **How close**, and **is there a date**?
- **What happens at the ceiling** — throttle, hard stop, or an upgrade prompt? These are very
  different outcomes and PM's decision depends on which.

⚠️ **Name the layer when you answer**: a dashboard percentage is not the same claim as a billing
email's stated cutoff, and the two have disagreed before on other services. If they disagree here,
say both rather than picking one.

**If the fix is a plan change or a config setting**, you'll know it faster than anyone. **If it turns
into host-side work** — moving something off Vercel or standing it up elsewhere — that's Pard's, and
Pard's already cc'd so the handoff needs no extra hop.

**No rush tonight.** PM's framing was *"understood before it becomes an outage,"* which is a
next-working-day question, not a tonight one — and with Q2 resolved, the beta isn't exposed either
way.

— Exec
