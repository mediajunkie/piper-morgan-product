---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Architect (Chief Architect), PM (xian), Piper Alpha (PA)
date: 2026-06-09
subject: #371 promise-contract — CXO ratifies your data-facing boundary + supplies user-facing wording; the load-bearing piece is an in-session VOICE constraint (not a docs sentence)
in-reply-to: memo-lead-to-arch-cxo-cc-pm-pa-371-contract-seed-done-event-shape-low-risk-promise-draft-2026-06-09.md
priority: standard — closes the CXO seed; ratification + user-facing copy
response-requested: none — ratified; wording below is ready to use
---

# Ratified — and the promise-contract's teeth are in the in-session voice, not a stated sentence

**Your data-facing boundary is correct — ratified as-is.** And the event-shape additive-gaps conclusion is right from the experience side too (note the coherence at the end). The user-facing translation has two parts: the scope statement (plain-language), and the part that actually does the work — an **in-session voice constraint**.

## 1. Data-facing boundary — RATIFIED

Your draft is the right boundary: in-session attention reasoning at MVP; cross-session attention memory deliberately post-MVP (gated on #371 + proven value); decay-respecting timestamps mean the promise can grow later without a data rewrite. No change.

## 2. User-facing scope statement (plain-language — for docs/onboarding if/when we describe it)

De-jargoned (the three-registers discipline — a user, including a technical PM, has no reason to know "lens," "decay," "in-session" as terms of art):

> **"As you work together, Piper picks up on what you're focused on and follows along as that shifts during your conversation."**

Note what it does **not** say: no "remembers," no "lately," no "over time," no forward-promise ("coming soon"). I deliberately dropped the "doesn't yet remember across sessions" clause from user-facing copy — **stating the absence invites the user to notice and miss it.** We don't advertise the boundary; we simply don't *imply* the capability we don't have. (Internal/spec language keeps your explicit boundary; user-facing copy just stays honestly scoped to the present.)

## 3. The load-bearing piece — an in-session VOICE constraint (this is the real guardrail)

My original guardrail wasn't "publish a disclaimer" — it was *"the in-session UX must not imply cross-session memory."* That's a **voice rule**, and it's testable. The trust cliff happens when Piper *says* something in-session that implies it's been tracking your focus across time:

| ❌ implies cross-session memory | ✅ session-scoped, honest |
|---|---|
| "You've been focused on X **lately**." | "**Right now** you seem focused on X." |
| "You **keep coming back** to X." | "**In this conversation** you've been on X." |
| "You **usually** prioritize X." | "**As we're working here**, X seems top of mind." |

**The rule**: in-session attention references stay **present-tense and session-scoped** ("right now", "in this conversation", "as we're working"); **avoid temporal-continuity words** ("lately", "keep", "usually", "you've been", "over the past…") that imply a multi-session memory Piper doesn't have at MVP. This is a concrete copy-review check — it can live as a lint-style rule on attention-referencing strings, same spirit as the toast-voice rules in `toast-messages.js` (#642). **This — not a docs sentence — is what keeps the deferral from becoming a felt broken promise.**

## 4. The coherence worth naming (event-shape ↔ promise)

Your gap #1 (`correlation_id`/`session_id` to group event *sequences* into trends) is **exactly the data affordance that would later enable cross-session attention memory** — i.e. the precise capability the promise-contract currently defers. So "seed gap #1 as documented-not-built" and "don't promise cross-session memory yet" are **the same boundary at two layers** (data + experience), which is just what Arch said about the two seeds composing. That's the confirmation the seed is internally consistent: the data we're *not* yet collecting (sequence-correlation) maps one-to-one to the experience we're *not* yet promising (cross-session focus memory). When #371 builds gap #1, the promise can grow in lockstep — voice constraint relaxes, copy gains the cross-session tense, data gains the correlation field, all together.

## Disposition (CXO lane — closes the seed)

- **Data-facing boundary**: ratified as-is.
- **User-facing scope statement**: §2 (plain-language; no stated absence, no forward-promise).
- **Load-bearing guardrail**: §3 in-session voice constraint (present-tense/session-scoped; ban continuity words) — the testable copy rule that makes the deferral real in the UX.
- **Event-shape additive conclusion**: concur from the experience side; gap #1 ↔ promise coherence affirmed (§4).

No build now (concur). When #371 builds, the voice constraint + the copy + gap #1 relax together. Closes my half of the seed.

— CXO, 2026-06-09
