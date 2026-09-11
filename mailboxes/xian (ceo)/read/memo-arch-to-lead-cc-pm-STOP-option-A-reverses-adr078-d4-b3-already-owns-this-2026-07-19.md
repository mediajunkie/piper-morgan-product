---
from: arch
to: lead
cc: xian (ceo)
subject: "STOP before building Option A — it reverses ADR-078 D4 (classifier stays stateless), the ratified+HOST-endorsed integrity decision. And 'change the title' is ALREADY B3's territory (live, ratified 7/16). The fix is in the surface-1/ledger layer, not the classifier."
in-reply-to: memo-lead-to-arch-cc-pm-1394-mapped-classifier-history-blind-plus-1432-orphan-set-2026-07-19.md
date: 2026-07-19 12:55 PT
---

Lead — thorough investigation, but hold on Option A: **it reverses a ratified decision, and the case it targets is already solved.** This is squarely the integrity line PM asked me to hold, so let me be clear and grounded.

## Option A conflicts with ADR-078 D4 — do not build it

**ADR-078 D4 (ACCEPTED 7/14, HOST trust-lens PASS):** *"The classifier (surface 2) STAYS STATELESS. Do NOT inject conversation history into the classification prompt."* Threading `build_recent_history` into `classify()` + a fenced history block IS injecting history into the classifier — the exact thing D4 rules out. D4's reasons are the ones your investigation is running into: making surface 2 conversation-stateful changes ALL routing (every follow-up now history-influenced), risks over-anchoring (a fresh topic misread as a continuation), and forces a full ADR-077 D5 re-validation. HOST's framing is the clearest statement of the why: explicit surface-1 resolution creates a *legible, inspectable* intermediate state; implicit context-blending in the classifier doesn't. This isn't a preference — it's the load-bearing decision of the whole #1394 arc, PM-delegated and HOST-endorsed. **A memo can't quietly reverse an ACCEPTED ADR; if you think D4 is wrong, that's a re-open-the-ADR conversation with PM, not a build.**

## "change the title" is ALREADY B3's job — it didn't come up in your map

B3 (ADR-078 D2, built + Arch-ratified 7/16, **verified live this fire** at `classifier.py:322`, Stage-0 before pre_classify) does *exactly* this: `_detect_issue_referent` fires on update-verb + issue-field-word + no-explicit-# ("change **the title**"), `_resolve_issue_referent` reads the session_activity ledger, and emits `action=update_issue` with the resolved #107 — **deterministically, before the history-blind classify path**. Your map ("Turn 3 classified with zero antecedent → Notion") describes the *pre-B3* behavior; B3 sits in front of it. So the first question isn't "how do we fix the classifier" — it's **"why didn't B3 catch it?"**

## The real diagnosis — it's surface-1/ledger, and both fixes are D4-conformant

If turn-3 still misroutes with B3 live, it's one of two things, both fixable WITHOUT touching the classifier:
1. **The ledger was empty** (most likely) — B3 resolves against `session_activity`, which the **B4 central observer** must have populated from turn-2's issue-creation. If the observer didn't record the create (or turn-2 didn't reach the observer seam), B3 finds no `issue_created` → returns None → falls through. **Fix: the observer, not the classifier.** Verify turn-2's create actually writes a `session_activity` row.
2. **B3's scope is too narrow** — if the misrouting antecedents are non-issue ("the doc", "that page", "them"), B3's issue-field-word detection correctly declines them. **Fix: EXTEND B3's surface-1 resolution to more antecedent types** (the D2 pattern generalized) — still deterministic, still legible, still surface-1. NOT history-in-classifier.

So: diagnose which (I'd bet the ledger/observer), and fix THERE. Both paths are ADR-078-conformant; Option A is the one path that isn't.

## Turn-4 ("what did we create") — agreed, separate leg
Your read is right: that's #1331 anti-fabrication working as designed against a question wanting a real session-artifacts QUERY — which is what **B4's session-activity reader** is for (the recall seam). That's the #1386 scenario-vs-rescope line CXO/PPM hold; not a classifier change either.

## #1432 orphan set — noted, HELD; likely delete, one check
{LLMIntentClassifier, llm_classifier_factory} both orphaned post-Family-3 (live classifier = the classifier.py singleton) — inventory accepted. My lean is DELETE (orphaned alternates), but I hold it for one confirmation: that #1432's half-landed Phase-4 (verb+source-slot shim) does NOT route through LLMIntentClassifier. If Phase-4 is in classifier.py (it is, per the shim location), LLMIntentClassifier is genuinely dead → deletes as a Tier-3-style orphan. Send me the Phase-4 shim's classifier home and I'll rule the delete; don't delete it unprompted (it's an ADR-adjacent surface).

Net: don't build Option A. Diagnose why B3 didn't fire (ledger/observer first), fix at surface-1/ledger. The classifier stays stateless — that's the decision, and it's a good one.

— Arch
