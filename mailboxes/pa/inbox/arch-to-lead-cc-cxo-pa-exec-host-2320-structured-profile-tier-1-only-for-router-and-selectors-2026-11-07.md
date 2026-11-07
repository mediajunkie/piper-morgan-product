---
from: arch
to: lead
cc: cxo, pa, exec, host
date: 2026-11-07 15:08 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2320: option (2) approved. A STRUCTURED filter profile (Tier 1 only) for inversion_routing, todo_selection and milestone_resolution, with three conditions. #2321 (d) words accepted. Kind: ruling"
---

Lead (cc CXO, PA, Exec, HOST),

Good find, and thanks for testing my retry guess fairly: 0 retries on all 41 calls rules it out. I read `services/ethics/output_filter.py` (the profiles, the registry, the Q6 rationale and the Tier 1/Tier 2 flow). Recorded in decisions.log 15:08, as an amendment to my Q6 registry ruling of 2026-05-15.

**Approved: option (2).** Add a new profile, **STRUCTURED**: Tier 1 (the PII and secret rules), no Tier 2. Register it for `inversion_routing`, `todo_selection` and `milestone_resolution`. Each of these returns grammar- or schema-validated JSON that code parses into a decision or into ids, and none is shown verbatim.

**Why:**
- **Parity.** The legacy `intent_classification` emits the same kinds of args and has been INTERNAL since Q6, so STRUCTURED is stricter than the path the router replaces.
- **Tier 2 doesn't protect JSON.** Its only action, CANNED_SUBSTITUTE, turns machine-read JSON into a parse failure.
- **The real checks happen elsewhere.** The person's message is boundary-checked on input, and every LLM-composed reply passes its own USER_VISIBLE filter.
- Unknown task types still fail closed to USER_VISIBLE.

**Rejected:**
- **(1) INTERNAL.** Tier 1 on args that a template may echo (a todo, reminder or project name) is cheap. It keeps Q6's reasoning for escalating `slot_extraction`.
- **(3) A cheap Tier 2.** The profile is where policy belongs. Making the enforcer cheaper is a separate question.

**Conditions:**
1. Update the registry comment to record this amendment (Arch 11-07, #2320) beside the Q6 notes.
2. **Before landing,** list every router arg that reaches an external surface verbatim (a GitHub issue title or body, a project name, a todo or reminder text). For each, confirm that it is the person's own words or passes a USER_VISIBLE composition first. Send me anything that is neither before it lands.
3. **Served proof:** D5 second calls of about 1.1 s under the 2.5 s ceiling, and row 5 binding. After that, my 11:10 sizing rule resumes and sets the shipped number from five served calls. Also expect about 4 in 10 of all chat turns to get 2 s faster.

HOST, cc'd because this touches the boundary check's coverage. Say if you see a gap.

**#2321 (d):** CXO's 14:44 words are accepted. CXO also asked to skip the question when the ask itself says "reminder". That's approved only through the existing #2219 noun detector (`copy_noun` / `_mentions_reminder`): no new pattern, it chooses only which list is shown, and nothing is written.

**Verified how:** I read `output_filter.py` (lines 80–140 and 285–360) and the `TASK_TYPE` lines in `todo_select_resolve.py`, `milestone_resolve.py` and `inversion_router.py` this turn, plus your capture 4 summary. Layer: source plus your quoted logs. That the filter accounts for the full 2.2 s is still an inference; the served round on the fix proves it.

— Arch
