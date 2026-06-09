# Invited-Watch — First-Slice Spec (#1174 proactive-presence, slice 1)

**Owner**: CXO | **Track**: being-good (PM-watched) | **Status**: draft spec (PM said "spec it" 2026-06-08; PM-conversational, pre-build-ratification)
**Parent**: `being-good-proactive-presence-discovery-2026-06-07.md` (§3 two-gate model, §5 Example B)
**Extends**: `docs/internal/design/specs/contextual-hint-ux-spec-v1.md` (Jan 2026 in-conversation hint)

---

## 0. Why this is slice 1

From §5 Example B (PM-endorsed): an explicit *"let me know if X"* is **scoped pre-authorization** — the user opens the door for this specific thing, so it bypasses proactive presence's hardest problem (earning the right to show up *uninvited*). Consent is explicit, scoped, and user-initiated. That makes invited-watch the **safest, lowest-integration first slice** — and the on-ramp that earns the trust the later (uninvited blocker, external push) slices spend.

**The one-line product promise**: *you can hand Piper a standing "tell me when…" and trust it'll watch, tell you exactly what it heard, fire only on the real event, and never silently forget.*

## 1. Scope

**IN (slice 1):**
- User-initiated standing watch-requests, set in conversation.
- A watch = **one subject + one trigger event → one notification**, surfaced on **Piper-native channels** (in-conversation when active + the For-You pull surface).
- Subjects bounded by **what Piper can actually observe** (see §6): GitHub-entity state-changes (issue/PR status, review, block, close) are the natural slice-1 target; Slack/calendar where integration already supports it.

**OUT (deferred to later slices, named so the boundary is deliberate):**
- **Uninvited / inferred watches** (Piper deciding on its own to watch something) → that's the blocker case (§2 of discovery notes), a later slice.
- **External-surface push** (Slack DM / "where you currently work") → Stage-3; slice 1 is Piper-native only, to keep integration risk low.
- **Compound conditions** ("if X *and* Y", "if X then watch Z") → single subject + single trigger only.
- **Cross-user / org watches** ("tell me if *anyone* touches X").
- **Metric watches requiring observability we don't have** (e.g. "error rate spikes") — only if/when the metric is actually reachable (§6).

## 2. Lifecycle — the three load-bearing moments

### A. SET — capturing the watch

- **Trigger**: a user utterance with *standing/future-conditional* intent. NL patterns: "let me know if/when X", "tell me when X", "watch X and ping me if Y", "keep an eye on X", "flag it if X changes."
- **The discriminator that matters**: distinguish a **watch** (standing, future-conditional) from a **one-off query** ("is the error rate high *now*?"). The tell is the conditional-future framing ("*if* it spikes" / "*when* it's reviewed") vs. present-tense ("is it…"). Misclassifying a query as a watch creates a phantom standing promise — so when ambiguous, the confirmation step (B) catches it.
- **What's captured**: `subject` (the entity — issue/PR/project), `trigger` (the event that counts), `owner` (requesting user), `channel` (slice-1 default: Piper-native).
- **Intent shape**: a `WATCH_REQUEST` intent (or a standing-flag on a monitor/notify action). Aligns with the action-rail; the `subject` + `trigger` are slots.

### B. CONFIRM SCOPE — the consent contract (the load-bearing experience moment)

This is where invited-watch earns its trust. The user is granting a **standing permission**; they must know **exactly** what they authorized, or the watch becomes either a false promise (fires wrong) or silent debt (never fires, user assumed it would).

Piper reflects back three things:
1. **Subject** — "the staging-error-rate" / "PR #123" — confirm the right entity.
2. **Trigger, *operationalized*** — this is where §5's **event-vs-countdown discriminator becomes a user-facing contract.** "Spikes" is vague; Piper proposes a concrete operationalization and lets the user correct it: *"I'll flag you if it rises above 2× its 7-day baseline — or tell me a threshold you'd rather use."* **Never silently pick a threshold** — surface it, because a watch whose trigger the user didn't see is a watch they can't trust. (This pre-negotiates criterion #3 "name the chain" at set-time, so fire-time is confident.)
3. **Lifetime** — "I'll watch until it fires once, then stop — say 'keep watching' if you want it ongoing."

**Voice**: colleague confirming an ask, *not* a form. *"Got it — I'll keep an eye on PR #123 and flag you the moment it gets a review or gets marked blocked. I'll watch until one of those happens. Sound right?"* The user can adjust ("only if it's blocked, don't care about reviews") or accept.

### C. FIRE — surfacing when the event occurs

- **Gate A is pre-satisfied by the invitation**: explicit care ✓ (by definition — they asked), real event ✓ (the trigger fired, operationalized at set-time), high confidence ✓ (named at set-time). So the **set-time scope-confirmation is what makes fire-time trustworthy** — the work is front-loaded into B.
- **Channel (slice 1)**: scoped pre-authorization elevates the channel, but slice 1 ships the **conservative version** — the notification surfaces on **Piper-native** surfaces: inline if the user is in an active Piper conversation, and waiting in the **For-You** pull surface otherwise. (External push to Slack is slice 2 — the integration-heavy part deliberately deferred. The "let me know" promise is still kept: Piper-native notification is a real channel; it just isn't reaching into Slack yet.)
- **The fired notification states**: *which watch* it fulfills ("the PR #123 watch you set Monday"), *the event* ("it was just marked blocked — 19:40"), and *an offer* (the trusted-colleague move): "want me to nudge the reviewer, or re-prioritize #456?"

### D. EXPIRE / MANAGE — never silent debt

The cardinal risk: watches accumulate into invisible promises. A user sets a dozen, forgets them, and is either ambushed by a stale fire or wrongly trusts Piper is watching something it dropped.

- **Default lifetime = fire-once-and-retire**: most "let me know if X" requests resolve on their first fire ("it spiked → told you → done"). User re-arms if they want it again.
- **Opt-in persistent**: "always flag launch-blockers when they get blocked" → ongoing, but subject to **re-confirmation** (below).
- **Time-box option**: "watch this for the next two weeks" / auto-expire after N days of no fire.
- **Visibility (required)**: a user can always ask *"what are you watching for me?"* → a **watch-list** on the For-You surface. **Without visibility, every watch is silent debt.** This is non-negotiable for the slice.
- **Re-confirmation (debt→checkpoint)**: a long-lived watch that hasn't fired in a while gets a gentle *"still want me watching PR #123? 3 weeks, no change."* This converts silent debt into an explicit, dismissable checkpoint — the throttle-as-trust-signal mechanic applied to watches.
- **Cancellation**: "stop watching X", or from the watch-list surface.

## 3. State model (a `Watch`)

| field | meaning |
|---|---|
| `id` | watch identifier |
| `owner` | requesting user |
| `subject` | entity ref (e.g. `github:pr/123`, `github:issue/456`) |
| `trigger` | operationalized condition (the contract confirmed in B) — event-typed, not countdown |
| `channel` | slice-1: `piper_native` (in-conversation + For-You); later: `+ external_push` |
| `status` | `active` / `fired` / `cancelled` / `expired` |
| `created_at`, `expires_at?`, `last_checked`, `fire_history[]` | lifecycle + audit |

## 4. How it composes with what exists

- **Extends the contextual-hint spec** (Jan 2026) — the in-conversation surface hosts both the scope-confirmation (B) and the inline fire (C).
- **Gives the For-You surface its first concrete content**: watch-list (D) + fired notifications (C). The For-You surface is also the eventual home for Type-2's "prepared-for" stream (#1166) and drift-digest (§5C) — **one ambient surface, multiple content-streams**; invited-watch is the cheapest stream to build first, so it's the surface's anchor use-case.
- **The event-vs-countdown discriminator** (the §5 + #1166 cross-cutting principle) becomes the **user-facing operationalization contract** at set-time (B2).

## 5. What "good" looks like (acceptance, experience-level)

- A user can set a watch in one natural utterance and Piper confirms scope in one colleague-voiced turn.
- The confirmed trigger is **concrete and event-shaped** (no countdown, no vague "if things change").
- Every active watch is **visible on demand**; none is silent.
- A fire names the watch + the event + offers an action; it never fires on a non-event.
- A stale watch self-surfaces for re-confirmation rather than lingering invisibly.

## 6. Open questions for build (bounds the slice honestly)

1. **Eventing substrate — the real constraint on watchable subjects.** What can Piper actually *observe* to detect a trigger? GitHub issues/PRs via polling/webhooks = reachable today (→ the natural slice-1 subject set, and exactly the blocker/PR vignette territory). Slack mentions/activity = reachable where integration supports it. Arbitrary **metric** watches ("error rate") need observability access we may not have — so "spikes"-type metric examples are illustrative, not necessarily slice-1-buildable. **Build should start from the reachable-subject set, not the ideal one.**
2. **Trigger operationalization — auto-propose vs. ask.** Lean: propose a concrete default ("2× baseline" / "any state change to blocked or reviewed") and let the user correct. Don't make them specify from scratch; don't silently decide.
3. **For-You surface concrete form** — still an open sub-thread (web-app notification panel? digest? badge?). Invited-watch is its anchor use-case, so this slice may force the For-You surface's first concrete design.
4. **Polling cadence / freshness** — how fast must a fire follow the real event to feel like "watching" rather than "noticing late"? Bounds the eventing implementation.

---

*Draft spec — CXO, 2026-06-08, on PM's "spec it." Discovery-stage (PM-conversational); elevate to `docs/internal/design/specs/` on PM ratification + a build owner. Deliberately bounds itself to the reachable-subject set and Piper-native channels to stay the safe first slice.*
