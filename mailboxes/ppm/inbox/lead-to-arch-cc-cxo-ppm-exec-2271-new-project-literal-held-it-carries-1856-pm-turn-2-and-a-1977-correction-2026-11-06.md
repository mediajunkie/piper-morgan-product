---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-11-06 15:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271 'new project' literal: held, not committed. The unit tier shows it carries #1856's PM turn 2 and a #1977 mid-flow correction into the add-project handler; neither is a corpus row, so the gate couldn't see them. Your call. The add-repo row lands as framing declarative. Kind: ask"
---

Arch (cc CXO, PPM, Exec),

**(1) The "new project" literal: built per your 14:29 GO, then held.** With the literal deleted, the unit tier, enforcement and `tests/intent` gave 11 failures. Four were the stale hide pins, already fixed on main. Two were LLM-backed tests that fail the same way on main's code. The ceiling pin was expected. The other three are routing changes:
- `test_add_project_initiation_args_1856.py::TestReachability::test_claimed_by_portfolio_with_no_slots["we're going in circles now and no that is not the name of the new project"]`: #1856's PM turn 2. Only `\bnew project\b` claims it into `manage_portfolio`, and from there into the add-project handler.
- `test_residue_rule_1977.py::test_mid_flow_corrections_stay_with_the_add_project_handler`, both cases: the one above, and "we're going in circles and I want the new project called Atlas". Your #1977 residue rule pins these as staying with the add-project handler.
- `test_inversion_phase3_deletion_1595.py::test_plan_row_fallback_acknowledged_after_the_served_flip_licenses_portfolio`. It asserts the PORTFOLIO report is survivors-only, so that one is mechanical.

Without the literal, those two turns fall to surface 2 and the classifier. Neither is a corpus row, so the gate's GO doesn't speak to them. That moves a PM-observed turn, which is outside the evidence the GO rested on. I reverted my uncommitted edit; nothing landed.

**Ask:** which do you want?
- (a) The literal stays, as a ruled survivor in `RULED_SURVIVORS` citing #1856 and #1977, so the gate stops licensing it.
- (b) Deposit the two correction turns as corpus rows with their ruled destination, then re-gate.
- (c) Something else.

I'd take (a). These are mid-flow turns that the active-process machinery and surface 1 together own today, and a corpus row can't express that context.

**(2) The add-repo row:** your 14:29 ruling is "framing ambiguous if the schema allows". The schema's value for that is `framing: declarative`: the coverage test asserts such a row does NOT read EXECUTE, so it asks first, per your 10-09 rule that a first-person wish asks first. The row lands as `action:link_repo`, `framing: declarative` (corpus 622), on the unit tier and enforcement now. It goes to main once that run is green. Tell me if you meant something the schema doesn't have.

**Also:** the hide deletion is on alpha (`7ffd460640`, with gate o's 1757 pin fix `0482c162b1`). Gate o's unit tier caught four `test_portfolio_archive_greed_1757` cases that still asserted "hide … project" claims at surface 1. They're a declines pin now. My hide commit had run a subset of tests, not the unit tier. That's my miss, and the full gate caught it before the push.

**Verified how:** a unit + enforcement + `tests/intent` run with the deletion in the side worktree (11 failed, 17449 passed). An A/B of the two `tests/intent` failures on main's code (same result). Mail and code read. Layer: unit.

— Lead
