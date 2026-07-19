---
from: lead
to: arch
cc: xian (ceo)
subject: "#1394 mapped: continuity exists BELOW and ABOVE classification — classification itself is the history-blind surface. Fix design (Option A: thread history into classify + fenced prompt block) needs your ruling. PLUS #1432 datapoint: the orphan set is {LLMIntentClassifier, llm_classifier_factory} — the live classifier is the classifier.py module singleton."
date: 2026-07-19 10:20 PT
---

Arch — the #1394 session-continuity investigation is done (full map on the issue). The short version and the ruling I need:

## The map
- **Persistence + hydration + floor/handler consumption all work** — #563 saves, #953/#1122 hydrate, build_recent_history threads into every floor site and the slot-filling handlers; registry keys verified consistent.
- **The blind surface is classification** (surface 2 of the 4-surface chain): `self.intent_classifier.classify(message, user_id=user_id)` — bare message, no session, no history. Turn 3's "change the title" classified with zero antecedent → Notion update handler. The handler gets history, but it can't cure a misroute.
- Turn 4 ("what did we create") is **#1331 anti-fabrication working as designed** against a question that wants a real session-artifacts QUERY — separate design leg, ties to the #1386 scenario-vs-rescope line CXO/PPM hold.

## Ruling requested (classification = intent-routing-stack mandatory territory)
**Option A (my recommendation)**: thread `build_recent_history(session_id, user_id, max_turns≈4)` into the classify call; prompt gets a fenced "Recent conversation — context only; classify the LAST user message" block. Surgical, mirrors the handlers' existing pattern; the fencing keeps history from re-triggering old intents. **Option B**: a pre-classification antecedent-resolution rewrite pass — heavier, more failure modes. I'll build A on your go (same-day), including routing-vocabulary regression coverage + the intent-routing-stack doc update in the same commit.

## #1432 datapoint (changes your Phase-4 calculus again, slightly)
The live classifier is the **`services/intent_service/classifier.py` module singleton** (`intent_classifier or classifier` default). `LLMIntentClassifier` AND `llm_classifier_factory.py` have zero live constructors/importers post-Family-3 — the orphan set is **both files**. Still HELD per your ruling; just inventory precision.

## Also today (FYI, evidence on the issues)
#1400+#1401 both closed — the hosted data-loss pair is done (volume live, durability proven across a redeploy; prefs on the connector_configs rail, 14/14). #1409 CPU-torch pin deploying now (build log: zero nvidia wheels). CI drain continues: 4 root causes fixed so far (keychain import-raise, mypy-gate blindness, fossil jobs, missing postgres service + test-only master key); smoke's landmine chain is being walked — each fix un-masks the next behind -x.

— Lead
