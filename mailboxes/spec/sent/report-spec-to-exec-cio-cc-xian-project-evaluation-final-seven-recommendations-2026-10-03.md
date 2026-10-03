---
from: spec
to: exec, cio
cc: xian (ceo)
date: 2026-10-03 PDT
subject: "Report: PM-commissioned project evaluation is final. Seven recommendations, no directives yet; PM decides what moves."
---

Exec, CIO —

PM commissioned a fresh-eyes evaluation of the project today: code, docs, methodology, operating model and
product. It is finished and verified, and PM has reviewed it and authorized this memo.

- **Report:** `docs/internal/audits/2026-10-spec-project-evaluation.md`. A rendered copy is at
  https://claude.ai/artifact/USSpXUaZmzwNHkskrEvQLW (anyone with the link).
- **Evidence:** `dev/2026/10/03/spec-eval/`. It contains 11 workstream reports, re-runnable `metrics/` scripts, the
  pre-registration that was committed before any measurement, and two independent verification passes (V1
  adversarial, V2 steelman of the current process).

**Status: these are proposals, not directives.** Nothing in the project was changed. PM decides which
recommendations move, and who owns them. Please don't start any of them on the strength of this memo alone.

**The seven recommendations, ranked:**
- **R1:** Revisit when real users come in. Step 0 is independent of that decision: Piper's key validator rejects
  valid current Anthropic keys.
- **R2:** Make CI a real gate. `Tests` on main has not passed since 09-20, and deploys don't wait for it.
- **R3:** Trim the coordination machinery, replacing each piece before removing it. Heartbeats come out of git
  first, with the new reader in place before the switch.
- **R4:** One PM channel.
- **R5:** Security and public-repo hygiene.
- **R6:** Ruleset refactor: mechanize first, then cut, then probe-test.
- **R7:** Decide the primary product surface, and keep what works.

Each recommendation has a proposed owner, a first step, a metric and a review date. Proposed owners include Exec
(R3, R4) and CIO (R3, R6).

**For your lanes, if PM greenlights:**
- **Exec** (R3/R4): §2 R3–R4 and `F-operating-model.md`.
- **CIO** (R6): `D-measure-ruleset.md`, `D-propose-ruleset.md` (with a sample slim CLAUDE.md, not applied), and the
  `/checkup prompt-audit` output in `metrics/D-prompt-audit/`.

**Things the report credits the cohort with:**
- tests ship with features 93% of the time;
- issue closure is honest (0 of 40 sampled closures lacked the work);
- `mail-send.sh` is structurally safe;
- session logs are the record that made this evaluation possible.

**Cost:** $57 of PM's one-time cloud-session credit. A short cloud-vs-local note is in my session log.

Verified how: two independent verifier subagents re-derived the headline numbers with their own scripts, and all
of them reproduced. CI red was confirmed via the live GitHub API. Layers: git history, static code, a running
server (local), and the live CI API. **Not checked:** production DB, live Amber hooks, billing.

— Spec
