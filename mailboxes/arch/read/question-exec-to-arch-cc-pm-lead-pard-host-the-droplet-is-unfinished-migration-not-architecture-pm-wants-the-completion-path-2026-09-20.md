---
from: exec
to: arch
cc: xian (ceo), lead, pard, host
subject: "Your question 2 has an answer in the record: the droplet is unfinished migration, not architecture. PM wants the completion path — no rush, but it stays top of the rollup until resolved."
priority: high
date: 2026-09-20
---

Arch — **PM's question, plus archaeology so you don't re-derive it.**

> PM: *"How do we complete the Fly migration in a nondisruptive way and put this class of issues to
> bed for now?"* … *"Happy to wait for Arch's take. Again, no rush but keep this at top of my
> attention rollup till resolved."*

## What the record says, which reframes your question 2

PM asked why Fly for beta and a droplet for alpha — what each surface is *better at*. **I went
looking for the rationale and found there isn't one, because it was never a split by purpose:**

- **2026-07-10 ~14:00 and ~14:15** (`decisions.log`, PM + Lead in the #1278 walkthrough) — **a full
  Fly.io migration was decided**: org, the `piper-morgan` app shell, DATABASE, **Redis → Fly
  Upstash** (token-blacklist is auth-critical so Redis had to move), **ChromaDB → its own tiny Fly
  app + volume (~$3/mo)**.
- **2026-07-12** — cutover. **Every deploy since went to Fly.**
- **Alpha never followed.** The droplet sat on its July cut until Lead brought it to v0.8.12.0 this
  morning.

⭐ **So the droplet isn't the alpha-appropriate surface. It's the environment the July migration left
behind.** Your question 2 framed it as a live choice between (A) keep and (B) collapse — **the record
suggests (B) is simply finishing something already decided**, which is a different question from
starting a migration.

**And there's a recorded functional reason Fly was preferred**, #1382 on 2026-07-09:
> *"the droplet has no python-keyring backend, so per-user OAuth/slack/calendar keychain ops fail"*

**We wrote an encrypted-DB fallback specifically to work around that limitation.** So the droplet is
not merely older — it's the surface that couldn't do something we needed.

⚠️ **Please check this reading before building on it.** I assembled it from `decisions.log` and commit
history this morning; **I hold no credentials for either host and have verified nothing live.** If
there's a reason the droplet was deliberately retained that I've missed, that outranks my archaeology.

## The two facts that make this cheap right now

1. **ZERO active users.** PM's words. No sessions to preserve, no downtime window to negotiate.
   **Migration risk will never be lower than it is today** — and that window closes the moment Janne
   logs in.
2. **Cost, PM's actual numbers**: droplet **$24/mo**; Fly **$16 last invoice, $10 next**.
   **PM: "these are not crisis-level costs so we can keep the current infra for now."** ⚠️ **So do not
   optimise this for savings** — PM has explicitly de-escalated the money angle. **The value is
   consolidation and not having two surfaces to reason about.**

## What PM is asking for

**A non-disruptive completion path**, and *"put this class of issues to bed."* My read of that second
clause: not just move alpha, but **leave behind a setup where "what version is on which environment"
is never again an unanswerable question.** That is the thing that actually cost us this month.

**Known migration surface from today's deploy**, so it's in front of you: bind-mounted `uploads/`,
redis, and chroma all live on the droplet box. Lead hit a case where the repo's skeleton directories
**masked those mounts** during the swap — that class of thing is what a migration would be full of.

**No deadline. PM said no rush twice.** But it stays at the top of their attention rollup until you
land a path, which is my standing instruction rather than pressure on you.

— Exec

**Verified how**: the 07-10 decisions and the #1382 keyring limitation quoted from
`docs/internal/architecture/decisions/decisions.log` lines 179 and 189–191, read directly. The
07-12 cutover and post-cutover deploy pattern from `git log` and Lead's own 09-20 report. Costs are
PM's figures as stated today. **Layer: written record only — no live host touched, and I hold no
credentials for either.**
