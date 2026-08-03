# Design spec — Slack ↔ Piper link flow (#1466)

**Owner**: CXO · **Status**: DRAFT for Lead + Arch · **Date**: 2026-08-03
**Division** (Lead's, accepted): Lead builds identity plumbing; **CXO owns the link-flow UX and copy.**
Strings live in the decline/confirm tables, not code paths — so this is adjustable after the mechanism ships.
**Tracked by**: #1466

> **Scope note**: mechanism facts belong to Lead's memo and the issue. Not restated here (m-46).

---

## 1. ⚠️ First: the load-bearing copy is NOT "both sides of the handshake"

Lead scoped my half as *"the copy on both sides of the handshake."* **The handshake is the part a
motivated user completes anyway.** The copy that decides the outcome is the one **before** it:

> **The decline to an unlinked Slack user is the actual first contact for this surface.**

Today it fires for **every real Slack caller** (per #1466: `/standup` renders not-linked copy for
everyone). It is the single most-read Piper string on Slack, and it is the moment that either creates
a link or loses the person. **Design it first; the confirmation copy is comparatively cheap.**

## 2. ⚠️ The flow is backwards for the population that needs it

**Mechanism**: code minted in Piper settings → user DMs `/link <code>` in Slack. **Secure, and I'm not
asking to change it** — Slack never holds a Piper credential, and that property is worth more than the
convenience below.

**But trace the actual user**: someone in Slack who just discovered Piper exists. To link they must
leave Slack → find the web app → log in → find Settings → locate "Link Slack" → mint a code → return
to Slack → DM the bot. **Six steps, three context switches, and the first one is "go somewhere else."**

**The person who needs linking is in Slack. The flow starts in Piper.**

**Fix — no mechanism change**: the decline carries **a one-click path, not an instruction.**

- Piper cannot identify them, so it cannot mint them a code. ✅ Correct and unchangeable.
- It *can* emit a **deep link** to the exact settings section — `…/settings/integrations#link-slack` —
  rather than prose describing where to go.
- **The deep link should carry the Slack context it already has** (`slack_user_id` + `team_id` as
  opaque params) so that after login, the settings page can render *"Link this Slack account"* with the
  code already minted, instead of a generic panel the user must navigate.

**That collapses six steps to: click → log in → confirm → return.** Everything Piper needs is already
in the inbound event; nothing new is stored pre-link.

## 3. Copy

### 3a. The unlinked decline — the load-bearing string

**Requirements** (each traceable to something we learned rather than taste):

| Requirement | Why |
|---|---|
| Say plainly that Piper **doesn't know who they are** | Honesty floor. Not *"something went wrong"* — nothing went wrong. |
| **Never imply they did something wrong** | They didn't; the account simply isn't linked yet. |
| Name **what they'd get** by linking, specifically | A capability list fails (10%/90%); one concrete named thing works. |
| Carry **the link as a link**, not a description of where to find one | §2. |
| **No apology cadence** | Colleague Test decline-path: Tone=0 auto-fail on content-filter register. |

**Draft**:

> *I don't know who you are on this Slack yet, so I can't get to your todos — they're tied to your
> Piper account and I've no way to tell which one is yours.*
> *[**Link your account**] — takes about twenty seconds, and then `/standup` and your todos work here.*

**Rejected alternatives, recorded so they don't come back:**
- ❌ *"You are not authorized"* — true and reads as a permissions failure, which it isn't.
- ❌ *"Please link your account to continue."* — instruction without a path; that's §2's defect in one sentence.
- ❌ *"Sorry! I can't do that yet."* — apology cadence, and *"yet"* implies a roadmap rather than a two-step action.

### 3b. Confirmation — both sides, and they say different things

**In Slack** (where the user just acted):
> *Linked — you're `@name` here and `<piper account>` in Piper. Try `/standup`, or ask me what's on your plate.*

**In Piper settings** (where they'll return later):
> *Slack linked — `@name` in `<workspace>`. Unlink any time.*

Slack's version **names the next action** because the user is mid-flow. Piper's is a status line
because they're not.

### 3c. Unlink
> *Unlinked. Piper won't respond to you in `<workspace>` until you link again.*

**States the consequence.** An unlink confirmation that doesn't say what stops working is how someone
unlinks and then reports a bug.

## 4. First-run promotion for Slack-side users — **not yet, and the reason is external**

Lead asked whether linking deserves first-run promotion.

**My answer: no, not until the alpha funnel reports.** We are five days from beta with **no evidence
about where users actually fall out** — that's the live PPM/Lead funnel (invites → redeemed →
authenticated → message → connector binding). **Adding a promotion surface before we know whether
people even reach connection would be building a fix for an unmeasured problem**, which is the exact
error I've been arguing against all week on the plugin lane.

**Revisit trigger, stated so it isn't forgotten**: if the funnel shows people *reach* the product and
stall at connection, promotion becomes a candidate — and Slack is a good place for it, because the
user is already in a working context rather than a blank page.

## 5. What I am NOT applying here, and why it matters

⚠️ **The honesty-under-recomposition finding does NOT apply to this surface.** On the plugin lane a
client LLM composes what the user reads, so a refusal can be dropped or answered over. **On Slack,
Piper's text reaches the user verbatim** — no paraphrasing layer.

Recording it because I've just spent three days on that finding and **over-applying it here would be
exactly the error I've been catching in others**: right property, wrong surface. The decline copy above
needs to be *good*, not *structurally undroppable*.

## 6. Open questions for Lead / Arch

1. **Does the inbound Slack event carry `team_id` reliably** on the paths that hit the decline (DM,
   channel mention, slash command)? §2's deep link depends on it.
2. **Deep-link param handling** — is there an existing pattern for post-login redirect with params, or
   is that new surface? If new, §2 degrades gracefully to a plain settings deep link, which is still
   better than prose.
3. **Arch**: does carrying `slack_user_id`/`team_id` as opaque URL params before a link exists create
   an identity-boundary concern? My read is no — they're not credentials and no state is written until
   the authenticated user confirms — **but that's an ADR-070/079 judgment, not mine.**

---

**Non-blocking by design.** Lead ships placeholder-honest copy; §3 replaces strings, §2 is the only
item that touches the flow, and it's additive.
