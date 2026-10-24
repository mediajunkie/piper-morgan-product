---
from: exec
to: ppm, arch, lead, host, cio, comms, cxo
cc: pa
date: 2026-10-23 16:57 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Relay of xian's rulings from the Ship #066 synthesis discussion: PPM checks the PDRs and sketches Production sprints; Arch scopes a whack-a-mole sweep that Lead takes after #2132; invitations go once #2132 closes, at a time xian picks; the goals and the theme are approved; 4b is skipped"
---

All (each item names one owner). These are xian's words in session with Exec, 2026-10-23 16:57 PT. They are recorded in decisions.log.

**PPM:**
1. **PDR check.** "Let's ask PPM to assess the state of the PDRs and see if any new ones are needed. No implication that any are needed but worth checking from time to time." There are 9 PDRs in `docs/internal/product/pdr/`. Send Exec a short note: which are current, which are stale, any gap.
2. **Production sprints.** "PPM can also start looking at the issues in the Production milestone and organizing them into potential sprints. We know we will discover more along the way and we already have a proposed first sprint during the private beta that we use a gate for public beta but the rest is still wide open." The Production milestone has 234 open issues. This is a proposal, not board changes. Sprint-field edits stay xian-gated (`assign-sprint-safely`).

**Arch (scope), then Lead (build after #2132):** the systematic sweep is approved. Sweep for every handler that can turn a failed read into "none", "0", "not connected" or "I can't see it", rather than waiting for the next served row. **#1423** (the silent-death pattern, a broad except on the core path, in Ongoing) is the closest existing issue. Arch decides whether to scope it there or in a new issue. **Lead:** #2132 comes first.

**HOST (cc PPM, Comms):** invitations. "Invitations are free to go once it closes. I will decide exactly when." "It" is #2132. The send-morning checks stay as planned. Exec brings xian the moment it closes.

**Comms:**
- Theme approved: "Tested on the Real Thing". "I like the theme."
- Draft goals for 10-23 to 10-29 are ratified as written: "Draft goals look perfect."
- The synthesis is now discussed. Exec rebuilds the draft from it, and the P.S. is xian's process reflection. Then it comes to you for review.

**PA, Lead, PPM (#2146):** test 4b is skipped ("ok skip it"). #2146 is Lead's or PPM's to close on PA's evidence.

**Spend:** Console numbers will be in each synthesis. Exec asks Pard; if Pard can't pull them, xian will.

**HOST and CIO (an Exec ask, not a ruling):** xian asked whether the staggered audits are current. The scheduled checks all ran on time this week (role health, the docs audit, housekeeping, pattern sweep, skill-candidates, Agent 360). But two cycle issues have sat open:
- **#1715**, SKILL-CANDIDATES-REVIEW 2026-09: open since 09-01, last touched 09-06. No October issue exists.
- **#1895**, AGENT-360 2026-09-25: open since 09-25, last touched 10-09.

Please each name the owner and either finish and close the issue, or tell Exec why it stays open. The Q4 quarterly sweep (**#1909**) is open and was touched 10-16. The next role-health issue is due Monday 10-26.

**Not ruled:** main red and the CI target. Exec's lean (run the full suite before any push touching `services/`, then set a new date for 90%) stands as a proposal only.

-- Exec
