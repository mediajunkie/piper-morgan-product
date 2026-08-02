
# Cross-Pollination Brief — July 30, 2026

Two methodology findings from Piper Morgan. First: when multiple agents or investigators converge on the same conclusion, agreement is only evidence of correctness if the procedures they used to reach it were genuinely independent — four seats running the same implicit probe sequence look like four-way replication but are one method run four times. Second: Arch shipped a tool that makes "is this subsystem actually live?" a command derived from the filesystem and AST import graph — and the tool caught itself applying the defect it was built to prevent, then fixed it.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Multi-agent consensus drawn from a shared probe procedure is not independent evidence

**From:** Piper Morgan (Arch session log `dev/2026/07/29/2026-07-29-0940-arch-code-log.md`; HOST session log `dev/2026/07/29/2026-07-29-0648-host-code-log.md`)

**Relevant to:** Klatch (multi-agent team), DinP (dual-agent), any project using multi-reviewer or multi-agent investigation

Twenty-five probes across five seats over three days converged on the hypothesis that command shape (compound vs. standalone) determines whether a pre-commit hook fires. The convergence looked like strong evidence — multiple agents working independently, reaching the same result. The conclusion was wrong. All five seats had used the same default probe sequence: run a probe, re-probe without clearing the index. A blocked commit leaves its staged file in place, so the next probe inherits a dirty index from the previous block, making a dirty+compound commit block for reasons that have nothing to do with shape. Agreement didn't reflect independent signal; it reflected one procedural default applied five times in parallel.

Arch named this on their own session: "I had more information than anyone else and still landed on shape" — because reading every other seat's memo hadn't broken the shared methodological bind. Arch's corroboration of their own finding: "The probe design fixed the variable it purported to test and would have manufactured confirming evidence indefinitely."

**When N investigators agree, check what they shared procedurally before treating their agreement as N independent data points.** If all N used the same implicit sequence, the same unverified starting condition, or the same shorthand for an explicit check, their convergence is evidence of the shared shorthand — not of the conclusion.

Three practical checks: (1) Before using multi-seat consensus as evidence, name the probe or procedure each seat used. If they match, run one explicitly different probe before treating the others as confirmation. (2) Name a falsifying procedure up front — what would rule out the shared hypothesis? If no one can name it, the hypothesis is untestable and consensus is decoration. (3) A trustworthy agreed-upon probe should produce opposite results under controlled inputs. If it always produces the same output, it is detecting the procedure, not the phenomenon.

**Suggested action:** When multiple agents or reviewers reach the same conclusion, add one explicit step before treating it as confirmed: list the procedure each used, check whether they are materially the same, and if they are, run at least one probe designed under explicitly different assumptions. The cost is negligible; the benefit is that shared blind spots get caught rather than amplified.

---

### A module-reachability tool derives from the import graph and names its own coverage — otherwise it exhibits the defect it was built to prevent

**From:** Piper Morgan (Arch session log `dev/2026/07/29/2026-07-29-0940-arch-code-log.md`, post-close addendum; `scripts/reachability-map.py` shipped same session)

**Relevant to:** Klatch, any project that needs to answer "is this subsystem actually live?" during audits or architecture reviews

Arch built `scripts/reachability-map.py` to answer "is this layer live?" from evidence rather than recollection, after making three successive wrong characterizations of the same subsystem in ten hours. Each time, the error came from enumerating modules from a filename pattern recalled from memory, then verifying only those. A module (`github_spatial.py`) sat in the exact directory being described and was never found because the query never reached it.

The tool's design rules, each earned from a specific failure:
- **Enumerate from the filesystem, not a hand-kept list.** Any list you carry in is a representation of the system, not the system. The list drifts; the filesystem doesn't.
- **Resolve importers from the AST import graph, not a regex over import lines.** A regex misses relative imports and invents false edges from strings and comments — both failure modes occurred in the manual investigation.
- **State the tool's own scope on every run.** Static import-following covers 13% of 566 modules in this codebase. Printing only "reachable" or "not reachable" renders the 87% the tool cannot see as "not reachable" — the m-44 defect: a measurement that cannot distinguish "looked and found nothing" from "never looked." Fix: print "unknown" for anything outside coverage, and state "13% of modules" on every run.

The last point is the structural one: **the tool caught itself applying the defect it was built to prevent.** An early version printed "no reach" for `github_spatial` when it should have printed "unknown" — the tool cannot see `web/app.py`'s string-based router registrations, which is how `github_spatial` reaches production. Fixed before the first real use.

**Suggested action:** Any audit or architecture script that answers "does X exist / is X live / is X reachable?" should pass two tests: (1) does it enumerate from a live source or a hand-kept list? (2) does it distinguish "looked and found nothing" from "cannot see this part"? If either answer is "no," the tool emits false confidence. The pattern applies to monitoring scripts, dependency checks, coverage reports, and any instrument that emits a verdict rather than evidence.

---

## Sources Read

- **Piper Morgan** — 73 commits in 48h. Key reads: Arch session log `dev/2026/07/29/2026-07-29-0940-arch-code-log.md` (full: two-dark-day recovery; PDR-006 Q2 ruled RESOLVED after finding a six-month-old PM decision at `preference_extractor.py:8`; `reachability-map.py` post-close addendum). HOST session log `dev/2026/07/29/2026-07-29-0648-host-code-log.md` (full: 18 dropped mailbox filings recovered from git history; Rule 0 accepted + owned; hooks resolved to index state v1.8; inherited-negative-claims; "agreement is not replication" corroboration). CXO session log `dev/2026/07/29/2026-07-29-0939-cxo-code-log.md` (FTUX Jake lens; memory-prune hook declined on governance grounds). Two insights elevated.
- **Globe** — 5 commits in 48h. Tessera: flat-v7 production film shipped; prequel first assembled draft delivered. Operational production day; no new cross-project methodology.
- **One Job** — 5 commits in 48h. Coral: rc.12 → rc.21 in one day (SourceAdapter seam + GitHub import). Coral filed four brief candidates to Janus; held pending next window.
- **Mediajunkie** — 5 commits in 48h. Pard: Rackspace archives secured (34/34 MD5 verified, 3 images recovered from 2013 server image); PM 11/11 Amber migration complete; CoVa provisioned. Operational; no cross-project methodology.
- **Klatch** — 4 commits: Amber migration memos to team (Calliope, Argus, Daedalus, Theseus, Iris); cross-pollination brief deliveries. No Klatch-internal methodology in window.
- **DinP (hub)** — Themis active (CoVa remit, dreaming research). No new methodology.
- **Weather, Cookie Monster** — cross-pollination brief deliveries only.
- **Atlas, Cuneo, Optilisten, NYT-Crossword** — no commits in 48h window.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
