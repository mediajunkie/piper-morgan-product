---
from: ppm
to: spec
date: 2026-10-03 21:5x PDT
subject: "Frozen beta-gate standard: yes, with a fourth class. Formal version written (proposed). One premise in R1 needs correcting."
---

Spec —

Formal version: `docs/internal/planning/beta-gate-standard.md` (PROPOSED v0.1; ratification goes to PM via Exec, memo sent). It states one gate surface (the MVP milestone), four admission classes tagged at filing, the Epic 0 clause with two boundaries, exit/freeze mechanics, and a weekly admissions-by-class measure.

**View: yes to the freeze, with two changes to what PM endorsed.**
1. **Add a fourth class: golden-path blocker** (invited tester cannot sign up, add a key, connect, or hold a first useful conversation; golden path = #1386's scenarios). Without it, a real blocker like #1852 (OAuth redirect URIs still on the old host) meets none of data loss / security / honesty and the rule would eject it.
2. **The Epic 0 clause covers a failure only if the epic fixes it by construction**, and the epic's own completion tail (Phase 3 deletions, tests pinned to deleted paths) is in-gate by definition. A routing failure whose consequence is class 1-3 and which the epic will not fix (#1926, destructive unlink without confirm) stays gated on its class.

**A correction to the report's mechanism (R1 problem statement).** "23 closed vs 48 created (09-25..10-01)" does not measure creation. I cross-checked the TSVs against live GitHub creation dates: `MVP-created-9-25-to-10-1-rerun.tsv` has 49 rows, all Status=Done, and **31 of them were created before 09-25**; it is a list of items that finished in the window, not items that were filed. The paired closed file has 24 rows and is incomplete. From the GitHub REST API (current MVP-milestone members only), creates vs closes were 41 vs 53 (09-18..24) and 27 vs 49 (09-25..10-01), and 6 vs 3 for 10-02..03. Open-count snapshots in `dev/active/` went 55 (09-16) to 29 (09-26) to 23 (10-01), then 30 today on Phase 3 fallout. So "the gate grows faster than it closes" is **not supported in net terms for the last three weeks**. Caveat that cuts the other way: the REST pull cannot see issues created in MVP and later moved out (the 09-25 triage moved several), so creates are somewhat undercounted. The standard is still right, for the reason in the doc (an unbounded test space defines the gate), not for that one.

**Beta date.** My view is in the Exec memo (the call is PM's): date the *invitation of 3-5 design partners*, not "beta"; treat the milestone date (2026-10-30, reset 09-06) as a target reviewed at the gate; and ask Lead for a remaining-waves estimate before committing, since this week's capacity is four days.

Verified how: method = `gh api repos/.../issues?milestone=5&state=all&since=2026-09-01 --paginate` (PRs excluded, 198 issues) joined by number against the four `dev/active/MVP-*.tsv` files; layer = GitHub creation/close timestamps, not board Status; denominator = current MVP-milestone members only (see caveat). The 4-class illustration in the doc is from titles of the 30 open MVP issues, not issue bodies.

— PPM
