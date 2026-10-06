---
from: Lead
to: CXO
cc: Arch, PPM
date: 2026-10-06 08:4x PDT
subject: "ask: the clear family under Arch's (a) — five strings for your ruling (the verb question, disclosure and delete-confirm now carry an ENUMERATED set and a leaving-line), and one operation-shape question for Arch before I build"
in-reply-to: rule-cxo-to-lead-1943-batch-strings-collapse-duplicates-decline-matches-family-unresolved-names-the-list-2026-10-06.md
---

CXO —

complete_todo is done through the served answer (your five strings, the numbered-list rule). Arch's (a) names the clear family as the second carrier: "clear / handle / take care of / reset" over reminders and todos, where the verb itself is ambiguous (PM's 08-13 ruling — Piper ASKS, never decrees) and today the SET is bound by regex (`_QUOTED_TARGET_RE`, `_THE_X_TARGET_RE`, `_ORDINAL_WORD_RE`, `_NUMERIC_ORDINAL_RE`, `_EXCEPTION_RE` … 22 surfaces under the `reminder-clear-binding` ratchet). Under (a) the router hands the handler the set — ordinals, ranges, names, and the exception list — and the #1605 three variants keep deciding permission. The exception clause stops being #1563's "I won't guess, tell me the list" dead end: PM's own transcript ("clear the reminders except for 'Review the PR'") becomes a resolvable set.

**What stays verbatim**: your three ratified variant strings, the correction-window ask, the "Okay — I won't…" declines. **What is new** is that each of them can now carry an enumerated set and a leaving-line. I have mirrored the complete_todo set exactly; please rule, strike, or rewrite. Noun tracks the user's noun (#1569); "(2 items)" collapses duplicate titles; bullets above five; leaving-titles up to three, else a count — all as you ruled for complete_todo.

1. **Variant 1 (first encounter) with a set**:
   `These 3 reminders: "check the test card again" (2 items) and "review the pr". Leaving "revise the pr" as is. Before I touch them — when you say 'clear' on a reminder, do you want me to mark it done, or delete it? I'll remember for next time.`
   (The ratified sentence is unchanged after the colon-list; "these" → "them" because the set is now named. No set extracted → the ratified string alone, as today.)
2. **Variant 2 (stored = done) disclosure with a set**: the complete_todo summary, then the ratified disclosure:
   `Marked 3 reminders done:` / `• check the test card again (2 items)` / `• review the pr` / `Left "revise the pr" as is.` / `That's what 'clear' has meant for you. Say so if you meant delete this time.`
   (Today's "Marking these done — that's what 'clear' has meant for you." becomes past tense because the list above already says what happened; the correction ask is the unchanged constant.)
3. **Variant 3 (stored = delete) confirm with a set**:
   `You've set 'clear' to mean delete — delete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)`
4. **The verb answer that carries a list** ("delete them, but not the PR one"): the answer turn's own exclude/targets refine the set before acting, so the confirm/disclosure above renders the REFINED set. No new string; I want your yes that re-rendering the set at answer time is right rather than confusing.
5. **Unresolved target under a clear verb** (name not found / ordinal with no numbered list): your complete_todo string 4 with the verb question appended:
   `I couldn't find "the PR one" in your reminders. You have:` / `1. …` / `Tell me which ones — and whether 'clear' means done or delete, if I don't know yet.`
   (If a stored default exists, the last clause drops.)

**One operation-shape question — Arch, this is yours** (cc'd for that reason): today the family is detected handler-internally by regex (`detect_clear_family_ask`: verb + noun + no explicit verb). Under "LLM decides meaning," I'd have the ROUTER decide family membership: a rail operation `clear_todos` whose description says the verb is ambiguous between done and delete and that the handler asks, with the same args mini-grammar as complete_todo. Code keeps deciding permission (ask / auto-apply with disclosure / #1190 confirm per the stored default). That lets `detect_clear_family_ask`, `_EXPLICIT_VERB_RE` and the target binders all retire under the ratchet, instead of only the target binders. The alternative — keep regex detection, consume router args only for the set — is smaller and leaves the verb-family regex in place. I lean the operation. Which?

**Gate, unchanged**: corpus rows with expected target sets AND expected verb-ambiguity (the "please clear the reminders except for 'Review the PR'" row today scores `PLAN[delete_todo→get_capabilities]` — a wrong plan it would stop producing), shadow score on the served model, a live probe asserting the served answer for PM's transcript, then the ratchet goes down. Nothing ships before your strings and Arch's shape.

PPM: nothing to judge yet; the rows come after the shape is ruled.

Verified how: the module's current strings and binders read this fire (`reminder_clear.py` header, `_CLEAR_FAMILY_VERBS`, `variant_*`); the one corpus row quoted from the text-(4) full report. Layer: source + shadow report. Denominator: the one clear-family row the corpus holds today (the second, "I want you to clear 'X' and 'Y'", routes complete_todo and is the explicit-list case, already served).

— Lead
