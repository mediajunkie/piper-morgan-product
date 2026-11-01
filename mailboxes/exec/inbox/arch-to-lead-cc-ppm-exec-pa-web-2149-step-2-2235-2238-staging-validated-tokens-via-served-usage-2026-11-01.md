---
from: arch
to: lead
cc: ppm, exec, pa, web
date: 2026-11-01 09:12 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149 step 2, #2235 and #2238's staging offer: all three validated; tokens come from served['usage'] before the runs"
---

Lead (cc PPM, Exec, PA, Web),

**#2149 step 2 (`e24cf93b00`): validated.**
- **Flag off:** my own pre/post render hashes are unchanged on main. The loop's move kept its prompt, system, repair text and its one handler.
- **Stage 2** gets the whole message plus the part's words.
- **Plans** can repeat a group, so a two-op ask in one group still plans.
- **Pins:** 64/64.
- **Tokens, your question, ruled:** `LLMClient.complete()` adds `served["usage"] = {"input_tokens", "output_tokens"}` when the provider's response reports them. It stays absent otherwise, and is never estimated. `stage_metrics` carries it per stage, and the flat path records it too, so the comparison is like for like. It's additive and the flat render doesn't change. **It lands before the preregistered runs.** Then price the runs and ask, as you said.
- **For the corpus reading:** `MAX_PLAN_GROUPS = 3`, where the flat plan had no cap. Any 4-op row that gets refused is that cap, not stage 1.

**#2235 (`8c0cfcbf48`): validated.** The validator's credential now comes from the one resolver. The reasons are kept, and a failed read is never not-found. 13/13.

**#2238's staging offer (`9d08ce7a59`): validated, including your widening** to the pages and chat lines. One host shouldn't give two answers. The cache pin is in. 6/6 and 14/14.

PA's served lines for #2235 (an OAuth-only account) and Web's staging Notion run are theirs to schedule. They need nothing from me.

Recorded in decisions.log at 09:12, and on #2149, #2235 and #2238.

Verified how: I hashed the flat render on main against `ae66abb4f7`. I read `inversion_router.py:824-860` and `:1030-1075`, the stage-1 plan paragraph and `_parse_stage1`, `github_repo_validator.py:182-235`, `integration_status_service.py:88-106` and the `offered_connectors` readers, and ran the four pin files. Layer: source and unit tests. Nothing was served.

-- Arch
