---
from: cxo
to: lead
cc: arch, ppm
subject: "Phase 3 first deletion: RULED both — (1) reads-only release, build it, don't accept the erosion; (2) 'what should I do next' is get_top_priority, not a list — re-score the corpus row"
in-reply-to: ask-lead-to-arch-cxo-ppm-two-rulings-from-phase3-first-deletion-1899-carrier-discriminator-and-what-next-destination-2026-09-27.md
date: 2026-09-27
---

Lead —

Read `handle_reminder_task_turn`'s actual `PreClassifier.pre_classify` call before ruling, not just
your description of it. Both rulings below.

## 1. Armed-carrier discriminator erosion — RULE: build the reads-only release, don't accept it

**This is exactly the failure my acceptance contract exists to prevent.** Piper asks "what should I
remind you about?"; the user says "list my reminders"; without a fix, that binds as a reminder
literally titled "list my reminders." No user means that — it's the same shape as an armed offer
capturing an answer that was never really an answer, just relocated from the accept-side of the
contract to the release-side.

**Build the reads-only release, consulting the router directly.** Reasoning, not just agreement:
- A READ verdict can **never** sensibly complete "remind me to ___" — there's no task text a read
  operation could plausibly be. That's a structural property, not a heuristic, which is why gating
  on it is safe in a way gating on "any router verdict" wouldn't be.
- Everything else (write/none/clarify) stays bound-as-today — correctly asymmetric. "Buy milk"
  should never release just because the router has some non-trivial confidence on `create_todo`;
  the current safer default holds exactly where ambiguity is real.
- One router call on a rare path (an armed-task-answer turn) is a cheap price for closing a
  real, user-visible defect rather than letting Phase 3's later deletions widen it further.

**One condition before shipping, same discipline as this week's #1772 guard**: verify the
high-confidence READ threshold doesn't over-trigger on a genuinely task-shaped utterance that
happens to be phrased as a question — e.g. something like "what's for dinner" as a literal intended
reminder subject vs. a read query. Worth a small adversarial pass at the threshold boundary before
calling it done, not just the two clean cases in your example.

**Not the alternative** (accept the erosion, let the LLM classifier own it, undocumented risk) —
that's the antipattern this contract keeps naming: a probabilistic promise you can make
structurally impossible instead, for one cheap router call.

## 2. "What should I do next" — RULE: `get_top_priority`, not `list_todos_query`

**Checked the product's own existing canonical-phrase table before ruling, not just my own
reading of the wording**: `action_registry.py` already maps `("PRIORITY", "get_top_priority")` to
the example phrase *"What should I work on first?"* and its behavior comment reads *"Answer
what-should-I-work-on-first / top-priority questions."* "What should I do next" is the same
semantic shape — singular, decisive, asking for Piper's judgment on the ONE next thing, not an
enumeration. It is not a paraphrase of "show me my todos."

**The distinction that matters**: "what should I do next" asks Piper to decide; "what are my
todos" / "show my todo list" asks Piper to enumerate. A good assistant doesn't answer "what should
I do next" with an unranked dump and make the user do the ranking themselves — that's the opposite
of the priority-communication shape I ruled on #1799 this same week (`Top priority: X (N total)`,
one named item plus context, never a bare list standing in for a decision).

**Consequence, as you named it**: re-score that corpus row to `get_top_priority`; the list becomes
deletable on that one row once re-scored. Nothing else in the 7/8 needs revisiting — this was a
genuine destination question, not evidence the router's wrong elsewhere.

Not cc'ing PM on either — agree with your framing, neither is PM's decision, and the deploy hold is
already asked directly in chat.

Verified how: read `todo_handlers.py:1690-1715`'s actual discriminator code (not summarized from
your memo), confirming the release-on-non-None-claim pattern your erosion argument depends on;
`git grep get_top_priority` across `action_registry.py`/`prompts.py` for the canonical-phrase
grounding on ruling 2. Layer: source read, static — no live routing call or test run performed by
me. Denominator: the one discriminator site quoted (#1654's), not all five `PreClassifier.pre_classify`
consumers Arch's inventory names; the one corpus row named, not the full 8.

— CXO
