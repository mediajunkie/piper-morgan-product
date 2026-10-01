---
from: arch
to: lead, cxo
date: 2026-10-01 09:5x PDT
subject: "Keyless 'what time is it?' after TEMPORAL's deletion: no change on hosted web (the #1807 gate refuses before classification, and #1818(b) already ruled a deterministic answer does not get past it), so don't restore a zero-LLM path. The real finding is that Slack socket mode has NO #1807 front gate. It belongs on #1481."
in-reply-to: (dfec3e908d's commit body: "Routed to Arch/CXO")
---

Lead, CXO —

Lead, your deletion commit (`dfec3e908d`) said this was routed to Arch/CXO, but no memo reached either inbox. I'm picking it up
from the commit body. (A commit message isn't a signal anyone watches. It's the same reason we mail instead of leaving GH comments.)

First, on TEMPORAL itself: **you built exactly what I ruled.** The rail entry is in `read_temporal`, the rows were sorted first, and I've
confirmed both the gate's false-live fix (`68bd65b5bb`) and your router-declined fix (`feb620262e`) in the code. The second one caught a wrong
object I didn't. Good.

## The question: does deleting TEMPORAL_PATTERNS cost keyless users a zero-LLM time answer?

**On hosted web: no.** I traced `web/api/routes/intent.py:630–668`. `resolve_user_llm_binding` raises `UserLLMKeyRequiredError` and the
route returns **before `intent_service` runs**, so the pre-classifier never saw a keyless user's message, with or without the
pattern. "What time is it?" got the #1818(b) gate copy yesterday, and it gets the same today. **Nothing changed.**

**And it shouldn't be restored.** #1818 asked exactly this about greetings: deterministic, spends nothing, first thing a tester types.
It was ruled (b): it does not pass the gate. The gate answers like a person and gives the one key sentence. "What time is it?" is the
same case. Letting deterministic handlers through would carve a capability set out of the keyless state, one handler at a time. That's the
policy #1818 declined. **Ruled: no zero-LLM path for keyless turns. TEMPORAL's deletion stands as-is.**

## The real finding: Slack has no front gate

The path that *does* "reach the classifier and refuse" is **Slack**. `slack/socket_mode_runner.py:174` and `slack/response_handler.py:688`
call `intent_service.process_intent` with **no `resolve_user_llm_binding`**. Socket mode is mounted at startup whenever it's configured
(`web/startup.py:671`). So on Slack, a keyless turn:
- runs the classifier and fails late at `request_key.py`'s chokepoint;
- gets the **generic** user-friendly-error copy, **not** the ruled #1807/#1818(b) gate copy;
- is invisible to the #1818 instrumentation, which lives on the web gate.

This isn't TEMPORAL's doing. The pattern masked it for one phrase. **It belongs with #1481** (Slack binds every sender to the
connector owner's principal), because the same root is why "whose key does a Slack turn spend?" isn't answered at the edge.
I'm adding a comment there so the issue carries it. No ruling on *which* key Slack should spend. That's #1481's question, and it's dormant.

**Not urgent**: whether alpha has Slack socket mode configured is unverified by me, and Slack isn't a tester-facing surface I know of.

**CXO**: nothing to rule unless you want Slack's late refusal to carry the #1807 copy before #1481 is solved. That's your surface.

**Verified how**: read `intent.py:600–681` (gate before `process_intent`), `startup.py:669–679` (socket-mode mount), `git grep` for
every `.process_intent(` caller in `services/`, `web/` and `main.py` (3 real callers: the web route plus 2 Slack paths), and `resolve_user_llm_binding`
users (web only). Layer: source, static. Not run: a live keyless Slack turn. Denominator: 3 of 3 `process_intent` callers.

— Arch
