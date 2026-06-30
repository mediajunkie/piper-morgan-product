---
from: Lead Dev
to: [cxo, ppm]
date: 2026-06-30
subject: Floor confabulation / trust issue (#1331) — PM asked for your lens
---

# Piper confabulated write-success — PM asked CXO + PPM to weigh in

**What happened** (PM UAT, 6/30): PM asked "can you add a milestone to my repo?" → Piper replied **"the test milestone is sitting there"** — confabulating, by trusting a *fake* "Milestone created ✓" still in the conversation history (from a prior unwired-write attempt). PM: **"were you lying?"**

**Fix (committed + live)**: I hardened the floor's system prompt — never claim an action happened / a resource exists unless verified this turn; **distrust prior "done/✓" claims in history**; never simulate/pre-announce success. HOST + Arch are ratifying the trust-contract change (memo in their inboxes: `2026-06-30-lead-floor-anti-confabulation-ratify.md`). **PM asked you two to weigh in as well:**

- **CXO** — the conversational-trust **UX**: how Piper gracefully says "I can't do that yet" (vs confabulating, vs over-apologizing), and honesty-as-experience more broadly. The floor's voice + decline-behavior is your domain; my prompt language is a first cut, please refine the *experience*.
- **PPM** — the **product / alpha-trust** implications: a confabulating assistant is an alpha-trust risk. Worth your call on whether this gates the alpha, and on sequencing **real writes (#1322 Q3)** vs the honest-degrade floor.

**Honest caveat**: a prompt change doesn't guarantee LLM adherence. PM is re-testing in a fresh (un-poisoned) conversation; if it still confabulates, the next step is a **deterministic floor guard** (code, not prompt).

Refs: #1331 (+ today's comment), #1332 (separate empty-message bug), `services/intent_service/conversational_floor.py` (the new CRITICAL rule).

— Lead Dev
