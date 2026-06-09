# Invited-Watch — First-Slice Spec (#1174 proactive-presence, slice 1)

**Owner**: CXO | **Track**: being-good (PM-watched) | **Status**: draft spec → **tracked as #1181** (PM elevated 2026-06-08) | **Parent**: #1174
**Naming**: the ambient pull surface name ("For You") is ⚠️ **held for PM decision** (§7) — do not finalize.
**Parent**: `being-good-proactive-presence-discovery-2026-06-07.md` (§3 two-gate model, §5 Example B)
**Extends**: `docs/internal/design/specs/contextual-hint-ux-spec-v1.md` (Jan 2026 in-conversation hint)

---

## 0. Why this is slice 1

From §5 Example B (PM-endorsed): an explicit *"let me know if X"* is **scoped pre-authorization** — the user opens the door for this specific thing, so it bypasses proactive presence's hardest problem (earning the right to show up *uninvited*). Consent is explicit, scoped, and user-initiated. That makes invited-watch the **safest first slice** — and the on-ramp that earns the trust the later (uninvited) slices spend.

**Thin VERTICAL, not Piper-native-horizontal (PM 2026-06-08).** The slice must **exercise the full breadth of the holistic / ubiquitous / just-in-time / in-your-workflow concept** — Piper showing up *where you already are* is the differentiator, so amputating it (e.g. "Piper-native surfaces only, defer external delivery") guts what we're proving. Instead: implement the *whole* concept **thinly** — a thin vertical slice from set→confirm→fire→**deliver-where-you-are**→expire, made thin by depth-per-dimension (one reachable subject type, one channel implementation, one trigger class, fire-once default), *not* by dropping the in-your-workflow dimension.

**The one-line product promise**: *you can hand Piper a standing "tell me when…" and trust it'll watch, tell you exactly what it heard, reach you wherever you are, fire only on the real event, and never silently forget.*

## 1. Scope

**IN (slice 1) — the thin vertical, full breadth:**
- User-initiated standing watch-requests, set in conversation.
- A watch = **one subject + one trigger event → one notification**, delivered through **the full presence spine**: in-conversation when active, the ambient pull surface (§7-named), **AND a messaging channel where you already are** (the in-your-workflow dimension — thin, but present).
- **Delivery channel is pluggable (PM 2026-06-08):** Slack is treated as **one supported messaging channel, not *the* channel** — delivery sits behind a **messaging-channel abstraction** (`MessagingChannel`), with **Slack as implementation #1** and SMS / Signal / Teams / Discord / etc. as future implementations behind the same interface. Slice-1 ships *one* impl (Slack, since the delivery rails already exist — §6.0), but the abstraction is in from the start so adding a channel is an impl, not a refactor.
- Subjects bounded by **what Piper can actually observe** (see §6.1): GitHub-entity state-changes (issue/PR status, review, block, close) are the natural slice-1 target; Slack/calendar where integration already supports it.

**THIN-by-depth (how the vertical stays small without losing breadth):** one reachable subject type · one channel impl · one trigger class · fire-once default · single subject+trigger (no compounds).

**OUT (deferred to later slices, named so the boundary is deliberate):**
- **Uninvited / inferred watches** (Piper deciding on its own to watch something) → that's the blocker case (§2 of discovery notes), a later slice. *(This — not external delivery — is the real trust frontier we're deferring.)*
- **Additional channel impls** (SMS/Signal/Teams/Discord/…) — the *abstraction* is in slice 1; the *additional impls* are later. Adding one is an impl behind `MessagingChannel`, not a redesign.
- **Compound conditions** ("if X *and* Y", "if X then watch Z") → single subject + single trigger only.
- **Cross-user / org watches** ("tell me if *anyone* touches X").
- **Metric watches requiring observability we don't have** (e.g. "error rate spikes") — only if/when the metric is actually reachable (§6.1).

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
- **Channel (slice 1) — the full spine, thin**: scoped pre-authorization elevates the channel, and slice 1 **honors the in-your-workflow breadth**: the notification reaches the user *where they are* — inline if they're in an active Piper conversation, on the ambient pull surface (§7), **and via their messaging channel** (Slack as impl #1 behind `MessagingChannel`) when they're not in Piper. Channel selection per watch (default: the user's configured messaging channel + the ambient surface). The thinness is in *one channel impl + one subject type*, not in dropping reach.
- **The fired notification states**: *which watch* it fulfills ("the PR #123 watch you set Monday"), *the event* ("it was just marked blocked — 19:40"), and *an offer* (the trusted-colleague move): "want me to nudge the reviewer, or re-prioritize #456?" — rendered consistently across channels (the message body is channel-agnostic; the `MessagingChannel` impl handles delivery formatting).

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
| `channel` | a `MessagingChannel` ref (pluggable) — slice-1 impl: `slack`; future impls: `sms` / `signal` / `teams` / `discord` / … behind the same interface. Plus the ambient surface + in-conversation, which are always-on. |
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

## 6. Build grounding + remaining open questions

### 6.0 The eventing substrate is NOT greenfield — it rides the existing scheduler subsystem (forensic finding, PM-prompted 2026-06-08)

PM correctly flagged that watch-firing depends on "whatever sweep cycle plus on-demand scanning Piper already supports." It does — and that substrate exists:

- **`services/scheduler/`** is an established subsystem: each job is an asyncio sleep-loop (no APScheduler/Celery) + `RobustTaskManager`, registered/started in `web/startup.py`. Existing jobs: `composting_scheduler_job`, `attention_decay_job`, `reminder_scheduler`/`standup_reminder_job`, `blacklist_cleanup_job`, `ethics_audit_cleanup_job`.
- **The canonical shape to copy is `composting_scheduler_job.py`**: it ticks periodically, and the domain object's `maybe_run()` **self-gates** whether to actually act (floor + min_pending + min_interval gates). **A `WatchEvaluationJob` is exactly this shape** — tick the sweep, evaluate each active watch against its trigger, fire the matches. The self-gating precedent is already proven in production.
- **Three evaluation modes, all already supported by the substrate** (this is PM's "sweep cycle plus on-demand scanning"):
  1. **Sweep/poll** — the `WatchEvaluationJob` ticks (composting-style cadence) and polls each active watch's subject for state-change. Right for GitHub issue/PR state (poll the API).
  2. **Event/webhook-reactive** — where a webhook exists (Slack `webhook_router`; GitHub webhooks if configured), a watch evaluates reactively the moment the event arrives. Lower latency.
  3. **On-demand** — the same evaluation invokable explicitly (the `dev_composting`/intent-route pattern), e.g. when the user asks "anything on my watches?"
- **The deep reconciliation**: `reminder_scheduler` already exists but is **time-triggered** (standup at a clock time). Invited-watch is its **event-triggered sibling on the same substrate** — which maps *exactly* onto our event-vs-countdown discriminator: a reminder = the countdown paradigm (solved); a watch = the event paradigm. Same delivery rails, different trigger class. **Build implication**: a `Watch` likely belongs alongside the reminder primitive, sharing the scheduler + notification substrate, differing only in trigger evaluation (condition vs. clock).

**Net**: the build is "add a `WatchEvaluationJob` to the existing scheduler subsystem (composting-job pattern), reuse the reminder/notification delivery rails, expose on-demand + webhook-reactive evaluation via existing paths." Not a new eventing system. This narrows the real open questions to cadence + reachable trigger-sources (below).

**Delivery rails → channel-impl #1 (PM's pluggable-channel point):** the existing reminder/standup job already *delivers* via `SlackIntegrationRouter` — so the outbound path exists. Slice 1 **generalizes that path behind a `MessagingChannel` interface** rather than calling Slack directly: `MessagingChannel.send(user, message)` with a `SlackChannel` impl wrapping the existing router. SMS/Signal/Teams/Discord/etc. become new impls of the same interface — no change to the watch-fire logic. (This is an Arch-lane abstraction; flag for Arch when this goes to build. Same DDD-ACL shape Arch has been ratifying all day: a stable outer interface, channel-specific bodies behind it.)

### 6.1 Remaining open questions (genuinely open)

1. **Reachable trigger-sources — the real constraint on watchable subjects.** What can the evaluator actually *read*? GitHub issue/PR state via API-poll or webhook = reachable today (→ the natural slice-1 subject set, and exactly the blocker/PR vignette territory). Slack via the existing `webhook_router` = reachable. Arbitrary **metric** watches ("error rate") need observability access we may not have — so "spikes"-type examples are illustrative, not necessarily slice-1-buildable. **Build starts from the reachable-subject set, not the ideal one.**
2. **Trigger operationalization — auto-propose vs. ask.** Lean: propose a concrete default ("any state change to blocked or reviewed") and let the user correct. Don't make them specify from scratch; don't silently decide. (Maps to the `maybe_run()` self-gating: the watch's trigger IS its gate condition.)
3. **The ambient pull surface — concrete form AND name** (⚠️ **name flagged for change by PM 2026-06-08** — see §7). Still an open sub-thread (web-app notification panel? digest? badge?). Invited-watch is its anchor use-case, so this slice may force its first concrete design.
4. **Sweep cadence / freshness** — how fast must a fire follow the real event to feel like "watching" rather than "noticing late"? Resolves per-mode: sweep-cadence for poll-able subjects (composting uses ~hourly), webhook-reactive for push-able subjects, on-demand always available.

## 7. Naming — the ambient pull surface (⚠️ "For You" flagged for replacement, PM 2026-06-08)

PM: *"'for you' reminds me of the meta algorithm and may need a new name."* Correct — **"For You" carries the social-feed / engagement-algorithm connotation (TikTok/IG "For You" = attention-harvesting), which is the exact opposite of the trusted-colleague posture this surface embodies.** The surface is "what Piper is keeping an eye on / holding for you," not an engagement-ranked feed.

Candidate names (recommendation first):
- **Radar** / "On Piper's radar" — **recommended.** Already in our design vocabulary (the Radar-O'Reilly touchstone in the foundations doc); connotes horizon-watching / anticipation *on your behalf*, the precise inverse of an engagement algorithm. Clean contrast with "For You."
- **The Desk** / "Piper's desk" — a colleague's workspace where your in-progress things sit; warm, low-tech, trusted-colleague.
- **Watch** / "Standing watch" — accurate for this slice but narrows as Type-2 "prepared-for" + drift-digest join the surface (it's more than watches).
- **Plain-language descriptive** — "What I'm keeping an eye on" / "What I've got for you" (per the three-registers discipline: user-plain-language for the surface label).

*Name is PM's call — held pending decision; doc keeps "For-You/ambient surface" as a placeholder until then.*

---

*Draft spec — CXO, 2026-06-08, on PM's "spec it." Discovery-stage (PM-conversational); elevate to `docs/internal/design/specs/` on PM ratification + a build owner. Deliberately bounds itself to the reachable-subject set and Piper-native channels to stay the safe first slice.*
