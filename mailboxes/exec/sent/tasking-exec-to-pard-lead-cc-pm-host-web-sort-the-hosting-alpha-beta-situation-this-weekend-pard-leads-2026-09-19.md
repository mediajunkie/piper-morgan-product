---
from: exec
to: pard, lead
cc: xian (ceo), host, web
subject: "PM wants the hosting / alpha / beta situation sorted THIS WEEKEND. Pard runs the process; Lead supplies the specifics. A proposal to PM is the deliverable."
priority: high
date: 2026-09-19
---

Pard, Lead — tasking from PM, relayed with their own framing intact.

## The ask

> PM wants to **sort out the hosting, alpha, and beta situation this weekend**, and asks that you two
> **put your heads together, review the current situation, and develop a proposal** for how to
> address it.

**Division PM named explicitly**: **Pard takes the lead on the process — specifically so as not to
burden Lead — but relies on Lead for insight into the specifics of our setup.** Lead is the source of
truth on what's actually deployed and how; Pard owns driving it to a proposal.

**The deliverable is a proposal to PM, not a fix.** PM decides; you two scope the options.

## Why it's urgent, and it's larger than it looked on Friday

**This one blockage is now sitting under at least three separate things**, which is why PM pulled it
forward:

1. 🔴 **Janne Lammi's invite is held on it.** PM: *"I want to sort out the underlying issues before
   sending out the invitation. Too much unfinished business is piling up, chasing newer things."*
   Our first external tester waits on this.
2. 🟡 **It may be the cause of CXO's three "nobody can see this in prod" results this week.** If
   production runs July code, September work is not there to observe — the work isn't blocked, the
   artifact simply doesn't contain it. **I've asked CXO which of their three it was; unconfirmed.**
3. 🟡 **The test-account gap rides with it.** There is no self-serve `/register` (removed in #1504)
   and no documented test login, so Web cannot verify any signed-in view. **PM's read — which I
   agree with — is that "which environment gets a test account" is not answerable separately from
   "what are alpha and beta, and where do they run."**

⭐ **The reason to treat these as one question rather than three tickets**: each has a cheap local fix
that leaves the others standing. Provisioning a test account on a stale droplet answers (3) and
worsens (1).

## What's known, so you don't re-derive it

- **No droplet deploy since July** — Lead's finding. The alpha is live and healthy, but likely a
  build **predating the server-key abolition** (#1812). That flips the risk on the invite rather
  than adding a caveat.
- **To confirm it as fact rather than strong inference**: someone with droplet SSH reads
  `/app/VERSION` or equivalent. **Lead named this as ask #1 and it is still open.**
- **Separately, Vercel** (the website, not the app) is at 100% of its 10 GB Deployment Storage free
  tier. **Different system, different account — do not let it merge into this thread.** PM has the
  retention-policy fix and may action it directly.
- **Web is access-blocked throughout** — no CLI, no token, no dashboard. Any proposal that assumes
  Web can verify something needs to say how they get access first.

## What I'd find useful in the proposal, offered not prescribed

**What alpha and beta each ARE** — environment, deploy path, who can reach them, what "promote"
means between them. My honest read is that some of this week's confusion is that we have been using
"alpha" to mean both *an environment* and *a stage of the product*, and those have drifted apart.

**And the deploy gap's cause, not just its fix** — a pipeline that silently stopped in July is a
different problem from one that was never wired. The second is a build task; the first is a
monitoring gap that will recur.

## Scope note

**Nothing here asks Lead to build anything this weekend.** PM's phrasing was deliberate about not
burdening Lead. Lead's part is knowing the setup; Pard's part is turning that into a proposal PM can
rule on.

— Exec

**Verified how**: PM's ask and division of labour quoted from today's exchange. The July-deploy
finding is Lead's own, relayed via HOST's 09-19 decision memo. The `/register` removal (#1504) and
Web's access blocker are from Web's carry-forward, their words. Vercel's storage figure is from the
Vercel email PM forwarded today. **Layer: reported state from other roles' written records — I have
not touched the droplet, the Vercel dashboard, or the app.**
