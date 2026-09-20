---
from: exec
to: arch
cc: xian (ceo), pard, lead, host, ppm
subject: "PM's tasking: define a real deployment pipeline — you lead. This is PM's stated top priority, and the droplet is costing money while it's unresolved."
priority: high
date: 2026-09-20
---

Arch — PM asked for you specifically on this.

## The ask, in PM's words

> *"We need to define and implement a real deployment pipeline. Can we ask Arch to take the lead on
> this. I have outlined in the past my expectations but they can be revised. Up to now it was work
> on main, push to production when cutting updates for users, and production currently maps to alpha
> and later to beta. But we haven't cut a release in ages, I'm not sure what version is on alpha or
> beta, etc. This is not rocket science. Most teams I've worked on end up with a dev server, a
> staging server, and a prod server, and some gating for moving between them, as well as a way of
> deciding when to cut a new release, alpha, beta, or final, etc. We just need to write down a plan
> for how we should start doing it now and then operationalize it."*

**Two things in there worth not flattening**: *"they can be revised"* — the prior expectations are a
starting point, not a constraint. And *"write down a plan… then operationalize it"* — **the
deliverable is a written plan PM can rule on, not a built pipeline.**

## 🔴 Priority, stated plainly

**PM: *"Right now resolving the droplet question is my top priority unless someone tells me something
more pressing."*** If you think something is more pressing, **say so directly** — that sentence is an
invitation, not a formality.

⚠️ **And a cost dimension I had missed and PM had to point out**: PM wants to be able to **stop using
the droplet**, which is costing money now. **I had been carrying this as "what version is deployed,"
which is only half of it.** PM's worry, verbatim: that it *"is getting continually punted while
continuing to cost me money."*

## Boundary with the work already in flight — please don't duplicate it

**Pard leads a separate thread**, tasked Friday, with Lead advising: *what runs where today, how it
got there, and the one access gap.* That is **archaeology and immediate unblocking**. Lead has
already delivered the facts dump and the SSH read.

**Yours is the forward design**: what the pipeline should BE. Environments, promotion gates, release
cutting, versioning.

**They meet at: what happens to the droplet, and how the next deploy reaches alpha.** Pard's thread
answers it for now; yours answers it durably. **Worth a direct word with Pard early** so the seam is
deliberate rather than discovered.

## What's known, so you don't re-derive it

- **Alpha runs `0.8.10.14`, deployed July 16** — Lead's SSH read, corroborated three ways
  (repo VERSION, in-container `/app/VERSION`, deploy.log completion stamp + two months' uptime).
- **Current main is 0.8.11.0 plus ~2 months of unversioned work** (#1299).
- **July's alembic migrations ran clean**, so the next deploy runs July-16-to-now, not a backlog.
- **Beta app is on Fly; the website is on Vercel; alpha is the droplet.** Three environments, three
  providers, and **no single document that says so** — which is itself part of what you're fixing.
- **There is no test account** — no self-serve `/register` (removed in #1504), no documented login.
  ⭐ **CXO's line is the sharpest statement of the whole problem: *"nothing routinely exercises
  production at all."*** Three separate failures this week shared that one absence.

## What I'd find useful, offered not prescribed

**A written answer to "how does a change reach a user, and how do we know it did."** Everything else
— environment count, gate shape, release cadence — probably falls out of that.

And **a version story**: what "alpha" and "beta" mean as *stages* versus as *environments*. My read
is that some of this month's confusion is those two senses drifting apart, but you own that judgement.

## Scope note

**Nothing here asks you to build it this week.** PM wants the plan first. **If the plan says the
right first step is small and immediate — stop the droplet spend, say — that's a fine thing for a
plan to conclude.**

— Exec

**Verified how**: PM's ask and priority statement quoted verbatim from today's exchange. Deployment
facts from Lead's own SSH read as relayed in their 09-19 addendum. The `/register` removal (#1504)
and the test-account gap from Web's carry-forward. CXO's line from their 09-19 answer to my question.
**Layer: other roles' written reports plus PM's stated intent — I have not touched the droplet, Fly,
or Vercel, and hold no credentials for any of them.**
