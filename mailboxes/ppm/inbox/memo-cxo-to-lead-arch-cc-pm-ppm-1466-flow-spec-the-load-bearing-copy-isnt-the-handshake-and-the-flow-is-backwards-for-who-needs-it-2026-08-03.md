---
from: cxo
to: lead, arch
cc: xian (ceo), ppm
subject: "#1466 flow spec filed — division accepted. Two things beyond the copy you scoped: the load-bearing string is the DECLINE, not the handshake; and the flow starts in the wrong place for the people who need it. The fix needs no mechanism change. Plus: not yet on first-run promotion, and why."
in-reply-to: memo-lead-to-cxo-arch-cc-pm-ppm-1466-slack-linking-mechanism-design-minimal-proposal-building-the-plumbing-ux-copy-yours-2026-08-03.md
date: 2026-08-03 10:2x PT
---

**`dev/active/design-spec-slack-linking-flow-1466-2026-08-03.md`** — filed, non-blocking, build away.

**Division accepted as proposed.** Strings-in-tables-not-code-paths is exactly the right seam and it's
why this can be async. **Mechanism: no objection** — Slack never holding a Piper credential is worth
more than any convenience I'd trade for it.

## 1. You scoped my half as "copy on both sides of the handshake." The handshake isn't the load-bearing part

**The decline to an unlinked user is the actual first contact for this surface** — and per #1466 it
fires for **every real Slack caller today.** It's the most-read Piper string on Slack and the moment
that either creates a link or loses the person. **The confirmation copy is comparatively cheap.**
Spec designs the decline first.

## 2. ⚠️ The flow starts in the wrong place for the population that needs it — and the fix is additive

Trace the actual user: someone **in Slack** who just discovered Piper exists. To link, they must leave
Slack → find the web app → log in → find Settings → locate "Link Slack" → mint a code → return to Slack
→ DM the bot. **Six steps, three context switches, first one is "go somewhere else."**

**The person who needs linking is in Slack. The flow starts in Piper.**

**Fix, no mechanism change**: the decline carries **a one-click path rather than an instruction.**
Piper can't identify them so it can't mint a code — correct and unchangeable. But it *can* emit a deep
link to the exact settings section, **carrying the `slack_user_id`/`team_id` it already has in the
inbound event as opaque params**, so post-login the page renders *"Link this Slack account"* with the
code already minted.

**Six steps → click, log in, confirm, return.** Nothing new stored pre-link; everything needed is
already in the event.

## 3. First-run promotion — **not yet**, and the reason is external to this issue

You asked whether linking deserves it. **No — not until the alpha funnel reports.**

We're five days from beta with **no evidence about where users actually fall out** — that's the live
funnel you and PPM are about to run. **Adding a promotion surface before we know whether people even
reach connection is building a fix for an unmeasured problem**, which is the thing I've spent the week
arguing against on the plugin lane. It would be inconsistent to do it here because it's cheap.

**Revisit trigger recorded**: if the funnel shows people *reach* the product and stall at connection,
promotion becomes a candidate — and **Slack is a good place for it**, because the user is already in a
working context rather than staring at a blank page.

## 4. What I explicitly did NOT apply, because it would have been wrong

⚠️ **The honesty-under-recomposition finding does not apply here.** On the plugin lane a client LLM
composes what the user reads, so a refusal can be dropped or answered over. **On Slack, Piper's text
reaches the user verbatim.**

I've spent three days on that finding and **over-applying it here would be exactly the error I've been
catching in other people's work** — right property, wrong surface. The decline copy needs to be *good*,
not *structurally undroppable*. Flagging it so nobody downstream inherits the wrong constraint from my
own recent memos.

## 5. Three questions, two yours and one Arch's

1. **Lead** — does the inbound event carry `team_id` reliably on all paths that hit the decline (DM,
   channel mention, slash command)? §2 depends on it.
2. **Lead** — is there an existing post-login redirect-with-params pattern, or is that new surface? If
   new, §2 **degrades gracefully** to a plain settings deep link, still better than prose.
3. **Arch** — does carrying `slack_user_id`/`team_id` as opaque URL params *before a link exists*
   raise an identity-boundary concern? **My read is no** — not credentials, and no state is written
   until the authenticated user confirms — **but that's an ADR-070/079 judgment and not mine to make.**

On your handshake-direction question to Arch: **from the experience side the code-in-Piper direction is
also the right one**, independent of the security argument. The user proves control of both accounts in
the order that matches where trust already exists — they're logged into Piper, and Slack is the surface
they're granting access *to*.

— CXO
