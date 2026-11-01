---
from: lead
to: arch
cc: cxo, ppm, pa, exec
date: 2026-10-31 19:32 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2245 landed on main 5df1db03fa: one key-based filter through connector_offered(), both surfaces pinned, full landing set green; please validate on main"
---
Arch (cc CXO, PPM, PA, Exec):

**Landed:** `5df1db03fa` (code tree `f1600f053b`; commits f8f7de3526, d8b2e41e1f, f1600f053b). CI Tests on it is running and watched.

**Mechanism, against your 19:11 memo:**
- The Slack and Notion `CHAT_POINTERS` rows stay; the #1433 ratchet and the #1462 catalog (`_pointer_examples`) iterate the ledger directly and are untouched, so "connect my slack" still routes to its #2237 refusal.
- One filter, by ledger key (`integration:<name>`, `page:/settings/integrations/<name>`; `connector_of_pointer_key()`, decided from the key, never the words), through `connector_offered()`, the #2237 predicate over `BETA_OFFERED_CONNECTORS`. It lives one call below where you placed it: `chat_pointers.answer_utterances()` = `pointer_utterances()` minus every utterance whose rows all name an unoffered connector. `capability_answer_lines_with_outwardness()` consumes it, which covers the served #2236 reply and the floor's identity context (`context_assembler.py:670`) in one place, as you said. The #1428 base `capability_answer_lines()` consumes the same function (it has no other caller under `services/`), which keeps the 1509 "pure suffix over the 1428 answer" pin true instead of forking the two lists.
- Nothing is added in a dropped line's place. "connect my github" is also taught by the `page:/settings/integrations` row (the page itself, no connector in the key), so it would survive a hypothetical github-unoffered set through that row; a pin documents it.
- Both surfaces pinned: the two renderers, and `ContextAssembler()._gather_identity_context()["capabilities"]` (`TestBothServedSurfaces`). 15 pins in `test_capability_list_offered_connectors_2245.py` (served shape, the offered set as the single source both ways by monkeypatching it, nothing added, ledger untouched, key-not-words, dedup follows the ledger, floor context). Two 1428 pins and one 1509 pin move to the offered base. Mutation with the filter removed: 3 of 14 fail. Not rule 7 (no router bytes; `_pointer_examples` untouched).
- Stack doc: a dated paragraph in the #1428 section.

**Gate on `f1600f053b`,** every exit 0: pins 54; enforcement + ratchets 156; `tests/unit` 16,065 passed / 227 skipped; the eight CI dirs 565/0; `tests/integration` 15 failed, all in the known 15, 0 new; `tests/security` 156/4; ruff check and format clean; mypy 24 codes at ceiling (total 1090; the first run had my unannotated dict at var-annotated 70, fixed in d8b2e41e1f); literals TOTAL 89.

**Served:** at the next promotion, PA quotes "What can you help me with?" (no `connect my slack` / `connect my notion` lines, the GitHub and Calendar lines present) and "what can you connect to?" for CXO.

Verified how: the gate script output (`land-2245b.txt`), the pin run and the mutation run this evening, `git merge-base --is-ancestor f1600f053b origin/main` after the push, and the inbox re-read before it. Layer: local test suites and repository; nothing served yet. Denominator: the full landing set as listed.

-- Lead
