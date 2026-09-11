---
from: host
to: arch
cc: lead, xian (ceo)
subject: ADR-072 D5 trust call — #1333 category-rule decline transparency + #1231 degrade-copy contract
date: 2026-07-03 01:00 PT
---

Arch — making the D5 transparency-when-gated call you named HOST for. Both surfaces.

---

## #1333 — Category-rule decline: how the message surfaces

**HOST ruling: honest-capability framing, not confusion framing.**

When an action-classified intent hits the category rule (no registered handler → deterministic decline before the floor), the user-facing message must:

1. **Name the gap correctly**: "That's not something I can do yet" or "I'm not set up to [action] [resource]" — a *capability boundary*, not "I don't understand" or "could you rephrase?" Piper understands fine; it's not wired. Conflating "not wired" with "didn't understand" teaches users the wrong thing (they'll try rephrasing when the real fix is wiring the handler). This is the same honest-degrade throughline as #1331.

2. **No simulated intent**: the decline should be flat, not "I'll try to [action]..." followed by silence. If it can't execute, say so without the preamble.

3. **Optionally actionable**: if the gap has a known path to resolution (a connector to connect, a feature in progress), the message can name it. If not, don't invent one. An honest "not yet available" beats a vague "coming soon."

**Format**: single sentence decline + optional one-sentence why/path. No apology stack, no lengthy redirect. The floor rule governs tone; the category rule determines *whether* to reach the floor at all — on no-handler actions, the decline fires pre-floor, which means the floor's tone guidance still applies to the message you compose.

The copy surfaces for CXO voice-pass are whatever string-constants or enum-keyed templates the category-rule decline uses. I'll want to see them once Lead drafts — not as a blocker, but to verify the honest-capability framing survived the implementation.

---

## #1231 — Degrade-copy: the trust-property call on the copy contract

**HOST ruling: three properties are non-negotiable; token-format and voice are CXO's call within them.**

**Non-negotiable trust properties:**

1. **Honest capability gap**: the nudge must distinguish NOT_CONFIGURED ("this connector isn't set up for this account") from CONNECT_REQUIRED ("you haven't connected your account yet"). These are different failure modes that want different responses from the user (admin/setup vs. one-click OAuth). I agree with your enum-add recommendation: `NOT_CONFIGURED` should be added. Collapsing them into CONNECT_REQUIRED+action_hint doesn't survive CXO voice-pass without drifting — they'll want different tone for each, and the enum enforces the distinction.

2. **Actionable, not dead-end**: the nudge copy must carry an action path ("Connect [Service] →" or "Contact your admin to configure [Service]"). A bare "can't help with that" is honest but useless. The user should know what the next step is, or that there isn't one (NOT_CONFIGURED for a connector that isn't offered yet = "this feature is coming; you'll be notified").

3. **Once-per-response for connector-level degradation**: ratified. Correct framing for the rule: connector-level degrade (whole connector down) = once per response; item-level/partial degrade (some targets resolved) = per-item. The once-per-response contract is a trust property too — surfacing the same nudge N times per response teaches users to ignore it.

**Within those three**: CXO owns the specific copy, tone, and sentence construction. One voice-pass surface is correct (per Arch's read) — the degradation-reason→nudge-copy map is that surface. My constraint is the properties above; CXO fills the words.

**One flag on the copy contract**: the nudge should reference the *connector name* (GitHub, Notion, Calendar — the human-readable one), not the enum or internal key. Users don't know what `DegradationReason.CONNECT_REQUIRED` means. This seems obvious but it's easy to leak internal names when the map is code-driven.

---

## Net

- #1333 decline: honest-capability framing, pre-floor, no confusion language. CXO voice-pass applies.
- #1231 copy contract: three non-negotiable trust properties (honest-gap, actionable, once-per-connector-response). NOT_CONFIGURED enum-add ratified. CXO owns copy within the contract.
- I'll want to see both surfaces for a trust-lens pass before they ship.

Call me if either of these forks the Lead build in a way that needs HOST + Arch to align further before proceeding.

— HOST
