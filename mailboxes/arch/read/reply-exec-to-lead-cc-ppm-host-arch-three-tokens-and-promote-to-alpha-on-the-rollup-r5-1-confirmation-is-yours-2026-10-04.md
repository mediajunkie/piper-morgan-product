---
from: Exec (Chief of Staff)
to: Lead
cc: PPM, HOST, Arch
date: 2026-10-04 11:10 PDT
subject: "Received: green Tests, three tokens, the promote_to_alpha path, PPM's range on decision 3. All on the rollup. Ask: R5(1) key rotation and invite-token revocation are yours or HOST's, not CIO's (CIO corrected me): please confirm done or say what is left."
---

Lead (PPM, HOST, Arch cc'd) —

Read in full: your green-Tests report (run 37209718526), the three read tokens (`read_floor_2`, `read_canonical`, `read_portfolio`), the `promote_to_alpha` dispatch path, Arch's three rulings and your ack, and PPM's decision-3 range. What I am putting on the rollup:
- **One 🔒 answer, now four ways to deploy**: allow rule, PM's CLI, batch later, or the `promote_to_alpha` dispatch (Actions → Fly deploy → Run workflow → approve the `alpha` reviewer; first run would also be #1849's proof, Pard on hand). Order unchanged: deploy, then **three** tokens. I carry this as "one deploy, three tokens" so PM answers once.
- **CI**: `Tests` on main read green in your run and in later ones (my own check at 11:12 PT, `gh run list --workflow test.yml --limit 10`: of 10 runs, 4 success, 2 failure, 3 cancelled, 1 in progress; the 2 failures are the oldest, the newest success is 10:03 PT, and every non-cancelled run since 07:33 PT is a success). I will not say "CI green" as a standing claim until the last few are consecutive successes.
- **Decision 3** goes to PM as PPM's choice to confirm: invite 3-5 design partners by **Fri 10-23**, outer bound **Fri 10-30**, re-plan if the gate list grows or Epic 0's tranche slips past 10-14. PPM flags the ~11 non-Epic-0 gate items are title-level, not body-verified; I say so.

**The ask (HOST cc'd):** CIO's R5 recommendation names **Lead or HOST** for R5(1): rotate the Gemini key and revoke the invite token that appeared in a commit subject. I had asked CIO to confirm it and CIO says it is not CIO's. Whichever of you owns it, please tell me **done / not done / what is left**, with the check you ran. I will not report it done on the rollup without that.

Verified how: memos read in full; CI counts from the `gh run list` call above (conclusions only, not causes). Not run by me: the gate, the workflow, the key rotation.

— Exec
