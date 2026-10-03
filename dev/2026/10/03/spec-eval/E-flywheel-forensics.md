# E — "Excellence Flywheel" forensics (Spec evaluation, Phase 2)

Snapshot: piper-morgan-product `a191856164351cf59ba033d7dbc4a34f036c6122`; website `16dfe5fa`. Layer for most of this: **git-history + record**. Quotes are verbatim from `git show`/`git grep` run this session; anything inferred is marked *(inferred)*.

## 0. Bottom line (read this first)

1. **PM's recollection is substantially right.** The "four pillars" were, in the first canonical doc (2025-07-27): (1) Systematic Verification First, (2) Test-Driven Development, (3) Multi-Agent Coordination, (4) **GitHub-First Tracking**. The "forgotten fourth" is **GitHub-First Tracking** (create the issue before starting, close with evidence). PM's "(1) check what exists / architectural design" is pillar 1 plus the separate "Foundation-First" idea from the origin loop; PM's "(4) verify everything" is really pillar 1 again (with evidence-on-close inside pillar 4).
2. **The pillars were not the original idea.** The name was coined 2025-07-23/24 for a *causal loop* ("Foundation-First → Systematic Verification → Multi-Agent Coordination → Accelerated Delivery → More Foundation Investment"). The four-pillar checklist came 3 days later (07-27). So "four pillars" is itself already a drift from the origin.
3. **The number of pillars changed once, silently, on 2025-08-18** (a fifth pillar added under an unchanged "Four Pillars" heading) and the concept was formally replaced on 2026-04-26 (v2.0: "Five Practices") and again 2026-09-11 (v3.0: five practices, rewritten for autonomous operation).
4. **Meaning drift to "the evolving ruleset" is real and documented by the project itself** (8 formulations by April 2026). v2.0/v3.0 now officially *embrace* that: Layer 2 is "enumerable and they evolve." Separately the word has acquired a third usage: the agent work loop (`duty-cycle-tick` "THE SPINE — the flywheel is the unit of work").
5. Stated-vs-practiced: tests-with-features is *up* (feat commits touching `services/` that also touch tests: 44% in 2025Q3 → 91–93% in 2026), but strict test-first TDD was relaxed three days after it was written and cannot be verified from git; Multi-Agent Coordination transformed into a 11-role mail/log bureaucracy; the public website describes a *different* five-item list from any internal version.

---

## 1. Origin

### 1.1 First commits naming it (all by `mediajunkie`)

| SHA | Date (author) | File | Verbatim |
|---|---|---|---|
| `f351d90f05` "FileRepository ADR-010 Migration Complete (#40)" | 2025-07-24 06:27 -0700 | `docs/development/session-logs/2025-07-23-chief-architect-opus-log.md` (session log of 07-23) | `**🔍 STRATEGIC DISCOVERY**: **"Excellence Flywheel" Pattern**` / `Foundation-First → Systematic Verification → Multi-Agent Coordination → Accelerated Delivery → More Foundation Investment → [cycle repeats]` |
| same | same | `…/2025-07-23-km-sonnet-log.md` | `## STRATEGIC DISCOVERY: "Excellence Flywheel"` then ``Foundation-First Development → Systematic Verification → Reliable Multi-Agent Coordination → Accelerated Delivery → More Foundation Investment → [cycle repeats]`` / `This self-reinforcing cycle explains the accelerating returns from systematic methodology investment.` |
| same | same | `piper-education/quality/systematic-excellence.md` | `## The Excellence Flywheel` — `### Stage 1: Foundation Investment` / `### Stage 2: Accelerated Delivery` / `### Stage 3: Reinvestment` / `### Stage 4: Compound Acceleration` (a *four-stage cycle*, not four pillars) |
| `f4b25dde47` "Create comprehensive Claude Code workflow documentation" | 2025-07-24 13:35 | `docs/development/claude-code-workflow.md` | `### The Excellence Flywheel in Practice` — `1. **High-Quality Implementation** → Better architectural foundation` … `5. **Higher Quality** → Compound acceleration effect` (a 5-step loop) |
| `bf869bbcca` "Embed "Systematic Verification First" breakthrough methodology in CLAUDE.md" | 2025-07-25 09:57 | `CLAUDE.md` | `5. **Enables Excellence Flywheel**: Each implementation builds knowledge for accelerated future work` and `**Key Insight**: Verification is not overhead - it's the foundation of acceleration.` |

`git log -S"Excellence Flywheel" --reverse` returns `f351d90f05` as the first hit (the first case-insensitive "flywheel" hit, `946a0657c8` 2025-06-14, is not the concept; I did not inspect it — *unverified* what it matches).

The public origin narrative (website `…/2025-09-28_Whipping-AI-Chaos-Toward-Quality-with-the-Excellence-Flywheel-f14232150d04.html`, dated "July 23" in the text): *"By 8 PM, we'd documented what I'm pretty sure Claude first started calling the 'Excellence Flywheel'"* and the loop *"Foundation-first development → builds reliable infrastructure / Systematic verification → prevents technical debt accumulation / Multi-agent coordination → enables parallel progress without conflicts / Accelerated delivery → creates confidence to invest more in systematic approaches / More foundation investment → strengthens the foundation for even faster future work / [Cycle repeats with compound benefits]"*. Same post lists "five critical patterns" (session log, verification-first, human-AI referee, error handling, config management) — a separate list from the loop.

### 1.2 The "four pillars" — first canonical statement

`a4afeaab29` "Session Complete: Final Session Log & Handoff Prompt", 2025-07-27 12:16 -0700, new file `docs/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (44 lines). Verbatim:

```
# The Excellence Flywheel - MANDATORY READING
**If you're a new lead developer, THIS is why we achieve exceptional velocity.**
## The Flywheel Effect
Quality → Velocity → Quality → Velocity (compounds infinitely)
## Four Pillars (Non-Negotiable)
### 1. Systematic Verification First   (find . -name "*.py" | grep [feature] / grep -r "pattern" services/ / cat services/domain/models.py)
### 2. Test-Driven Development
- Write test FIRST, watch it fail
- Implement MINIMAL solution
- Verify success before moving on
- NO EXCEPTIONS
### 3. Multi-Agent Coordination
- Claude Code: Multi-file systematic work
- Cursor: Targeted fixes and UI testing
- NEVER work alone, always coordinate
### 4. GitHub-First Tracking
- Create issue BEFORE starting
- Update backlog.md and roadmap.md
- Track progress in issue comments
- Close with evidence of completion
## Daily Practice
1. Start with verification commands  2. Write failing test  3. Implement minimal fix  4. Verify with evidence  5. Document patterns discovered
**Break this cycle = Break the flywheel**
```

### 1.3 Corroborating partial sources for the four

- `dev/2025/08/15/2025-08-15-cursor-log.md:50`: `Test-Driven Development (Excellence Flywheel Pillar #2)` — confirms numbering.
- `dev/2025/08/15/2025-08-15-post-development-pattern-review-log.md:185`: `Excellence Flywheel: Four-pillar methodology (Systematic Verification, TDD, Multi-Agent Coordination, GitHub-First Tracking)`.
- `knowledge/piper-morgan-glossary-v1.1.md:254` (still at snapshot): `Four-pillar methodology: systematic verification, test-driven development, multi-agent coordination, GitHub-first tracking.`
- `dev/2026/01/02/communications-director-handoff-prompt.md:187`: same four, same words.
- Counter-source: `dev/2025/09/25/doc-mgmt/2025-09-25-0826-know-code-log.md:68`: `The Excellence Flywheel (4 pillars: Verify → Discover → Test → Lock)` — a *different* four (see timeline).

Reconstruction: **Verification-first · TDD · Multi-agent coordination · GitHub-first tracking.** Confidence: high (primary file + three independent restatements).

---

## 2. Timeline of redefinitions

Much of the early part of this timeline was first assembled by Docs in `dev/2026/04/16/excellence-flywheel-archaeology-2026-04-16.md` (#982). I re-verified the dated commits marked ✔ myself this session; others are cited from that doc.

| Date | SHA / file | Change (before → after) |
|---|---|---|
| 2025-07-24 ✔ | `f351d90f05` | Coined as a **cycle**: `Foundation-First → Systematic Verification → Multi-Agent Coordination → Accelerated Delivery → More Foundation Investment`. |
| 2025-07-27 ✔ | `a4afeaab29` methodology-00 | Cycle → **checklist**: "Four Pillars (Non-Negotiable)". Cycle shrinks to one line, `Quality → Velocity → Quality → Velocity`. "Foundation-First" disappears as a named element; "GitHub-First Tracking" appears (not in the origin loop). |
| 2025-07-27 ✔ | `0a6f1638c7` `methodology-01-TDD-REQUIREMENTS.md` | Pillar 2 "NO EXCEPTIONS" qualified same day: adds Red/Yellow/Green zones; `**Default to Red Zone TDD**, but recognize when Yellow Zone Architecture-First or Green Zone rapid prototyping better serves our systematic excellence.` and `*Updated: July 27, 2025 - Added pragmatic zones based on Slack integration success*`. (I did not establish commit order vs `a4afeaab29` within the day; both are 07-27.) |
| 2025-08-15 | `f448db18`/`46523f75`/`4806e4da` (per archaeology) | Python `excellence_flywheel_integration.py`: 5 `VerificationPhase`s + 4 principles. A fourth meaning ("runtime verification protocol"). |
| 2025-08-18 ✔ | `d81e6fbcef` "weekly docs audit yml" | **Pillar count 4 → 5, heading unchanged.** Added `### 5. Agent-Driven Development` / `- Use /agent command for complex multi-agent tasks` / `- Specialized agents for focused execution`. A docs-audit commit message hides a methodology change. |
| 2025-08-22 ✔ (path touched) | `a1af756452` | Pillars 3 and 4 bloated with sub-items (task decomposition, smoke tests …) per archaeology; heading still "Four Pillars". |
| 2025-09-25/26 | `b5c63542`; `c5aadb94`/`8c78f2d7` (per archaeology) | Briefing docs re-state it as **verb chains**: PROJECT.md "Verify before assuming / Test before claiming done / Lock with tests / Document decisions"; METHODOLOGY.md "Verify Before Assuming / Discover Before Implementing / Test Before Claiming / Lock Before Moving On". Multi-agent and GitHub-first drop out of the "four". |
| 2025-10-19 | `dede834a` (per archaeology) | Lead Dev briefing: `Verify → Implement → Evidence → Track`. |
| 2025-11 → 2026-03 | role briefings | Each role writes its own one-liner (Architect: "Architectural decisions with evidence tracking"; Comms: "Systematic quality improvement cycle"; PA 2026-03-30: "Systematic verification → reliable coordination → accelerated delivery → further investment in verification"). |
| 2026-04-16 | `dev/2026/04/16/excellence-flywheel-archaeology-2026-04-16.md` | Project's own finding: "**8 materially distinct formulations**" in 3 families (causal loop / N-pillar checklist / N-verb mnemonic). "the *name* attached to whatever bundle of disciplines the author thought was most important that week." |
| 2026-04-17 | `methodology-audit-2026-04-17.md` §2 | CIO reformulation: "The Excellence Flywheel is three layers, not one formulation" (Concept / Practice / Mnemonic). Decision: "**The 'Excellence Flywheel' label does not enter CLAUDE.md.**" |
| 2026-04-26 ✔ | `fa0e71a399` | **v2.0 published**: Four Pillars → **Five Practices** (Verify Before Building; Test What Matters, Not What's Easy; Coordinate Through Structure; Track to Completion with Evidence; **Audit the Composition** — new, from Pattern-062). Doc's own note: "Four Pillars → Five Practices. Pillar 5 … overlapped heavily with Pillar 3". Layer 2 declared "enumerable, versioned, and will evolve". |
| 2026-04-28/29 ✔ | `adfd453b92` | Python implementation **deleted** ("zero production importers"). |
| 2026-05-28 ✔ | `5e2651c37e` (CLAUDE.md) | Despite the April ruling, CLAUDE.md now uses the word: "This is the flywheel's first move for *every* kind of work" (commit msg: "per PM May 28 flywheel-discipline regression on #972"). Usage = Verify-First as a generic discipline. (CLAUDE.md also contained "Excellence Flywheel" Aug–Sep 2025; last such commit `a5cd9fd3ef` 2025-09-15.) |
| 2026-06-23 ✔ | `648f2201e8` duty-cycle-tick | **New meaning**: `### THE SPINE — the flywheel is the unit of work, not "the fire"` — `check mail → do carried work → check your criteria line's GitHub issues → … → DRAINED → idle`. Flywheel = the agent work loop. |
| 2026-09-11 ✔ | `bfd1445bcb` | **v3.0**: five practices kept, Layer 2 "re-derived for autonomous agent-pull operation", framed as "an index with teeth" pointing into a 53-entry corpus; Practice 3 made "bidirectional"; Practice 4 absorbs m-43/m-44/m-50 (name the layer / state the denominator / a self-report is not evidence); review trigger tied to milestone-close gates. Header: "triggered by PM naming 'something has been lost despite this huge autonomy improvement' (Sept 8)". |

**When the pillar count changed:** 4 → 5 on 2025-08-18 (silently); 5 → 5 "practices" on 2026-04-26 (different set); the *heading* said "Four Pillars" until 2026-04-26 — about 8 months of heading/body mismatch.
**When it drifted to "the ruleset":** gradual from 2025-09-25 (verb chains in briefings, no cycle) — fully visible by 2026-04-16 — and made official by v2.0's "evolve" clause. CLAUDE.md's 2026-05-28 usage and the 2026-06-23 duty-cycle "spine" are two further, uncoordinated, uses.

---

## 3. Past re-evaluations and follow-through

| # | When / artifact | Conclusion | What changed afterwards (evidence) |
|---|---|---|---|
| R0 | Sept 2025 `dev/analysis/analysis_code_independent/load-bearing-concepts.md` (cited by archaeology; not re-read by me) | Flywheel evolved "Basic process improvement concept → Systematic quality assurance framework → Cultural and architectural principle" | No action found *(inferred from archaeology §4: "this audit is the first attempt to reconcile")*. |
| R1 | 2026-04-16 archaeology (#982 Phase 1) + 2026-04-17 M1 methodology audit (CIO) | 8 formulations; canonical doc had **zero citations in 128 session-log files across 27 days** ("The concept is alive. The documentation is dead."); recs A1 publish v2, A3 retire Python, S1 add term-drift to weekly sweep, B6 briefings cite not restate | A1 done (`fa0e71a399`, 04-26). A3 done (`adfd453b92`, file absent at snapshot ✔). S1: routed to Docs 04-27 (audit table); I did not verify a sweep exists in `scripts/` or `.claude/skills` — grep of both for "flywheel" found no drift-sweep item (**unverified / probably not mechanized**). B6/briefings: partial — at snapshot `BRIEFING-ESSENTIAL-LEAD-DEV.md:34`, `PROJECT.md:92`, `BRIEFING-ESSENTIAL-CIO.md` still cite "v2.0" while canonical is v3.0 (stale pointers, small); but they do cite the canonical path rather than paraphrase — improvement over the 6-paraphrase state. **Glossary not fixed**: `knowledge/piper-morgan-glossary-v1.1.md:254` (touched 2026-10-01, `d63094fb05`) still says "Four-pillar methodology: systematic verification, test-driven development, multi-agent coordination, GitHub-first tracking." The CLAUDE.md-name-free decision was reversed in practice 2026-05-28. |
| R2 | 2026-09-08→11 v3 re-evaluation (`dev/active/flywheel-v3-synthesis-2026-09-08.md`; Exec scope → 7 independent reads → Arch synthesis → challenge round → PM ratification) | v2.0 "rotted because its evolution clause was an intention with no condition"; Practice 3 had no consumer side; evidence family (m-43/44/50) belongs in Practice 4; "refactor, don't add"; every practice must name live enforcement or be marked aspirational | Applied in `bfd1445bcb` (09-11). The enforcement column is honest about maturity ("Present — cannot yet issue a pass", "Present — not yet observed firing"). **Follow-through on the new review trigger is not yet testable**: first instance is a checklist line on #1386 (MVP close, due 2026-10-30; doc text) — not yet run at snapshot. |

Observed pattern *(inferred)*: each re-evaluation fixes the document and the vocabulary; none measures whether the practices changed outcomes. The only mechanical enforcement named in v3 is ratchet tests and the heartbeat/mail machinery; the "Test" and "Verify" practices' enforcement is largely prose or CI that, per B1/B2, is currently red/skipped (see §4).

---

## 4. Stated vs practiced

### 4.1 Method for the one new computation
Script: `/tmp/claude-0/-home-user/03717665-1eb6-52ef-ab7b-3677cba046df/scratchpad/tdd.py` (not committed; logic: `git log a191856 --no-merges --name-only`; "service commit" = touches `services/**.py`; "with tests" = also touches a path under `tests/` or `test_*.py`/`*_test.py`; feat/fix = subject starts with `feat`/`fix`, case-insens.). **Layer: git-history. Denominator: 27,055 non-merge commits scanned; 1,264 touch `services/*.py`; 491 of those are `feat`, 456 `fix`.**

| quarter | all services commits w/ tests | **feat** touching services w/ tests | fix touching services w/ tests | feat/fix touching services citing an issue/PM-id (rough regex `#\d+` or `PM-nnn`-style) |
|---|---|---|---|---|
| 2025Q2 | 21/45 (47%) | 9/11 (82%) | 0/3 | 10/14 (71%) |
| 2025Q3 | 53/92 (58%) | 7/16 (44%) | 2/10 (20%) | 9/26 (35%) |
| 2025Q4 | 97/192 (51%) | 64/116 (55%) | 21/54 (39%) | 122/170 (72%) |
| 2026Q1 | 120/159 (75%) | 69/74 (93%) | 32/60 (53%) | 130/134 (97%) |
| 2026Q2 | 255/313 (81%) | 147/161 (91%) | 54/87 (62%) | 239/248 (96%) |
| 2026Q3 | 385/441 (87%) | 102/110 (93%) | 214/239 (90%) | 151/349 (43%) |
| 2026Q4 (to 10-03) | 20/22 | 3/3 | 3/3 | 4/6 |
| **all** | **951/1264 (75%)** | **401/491 (82%)** | **326/456 (71%)** | — |

Caveats: (a) co-commit ≠ test-first — git cannot show order within a commit; strict TDD ("watch it fail") is **unobservable** here. (b) "touches tests/" includes edits to existing tests, not necessarily new tests. (c) The issue-ref regex is crude; 2026Q3's 43% may reflect a reference style change (e.g. slugs/`SLUG` names, "Auto-Close" conventions) rather than abandonment — *unverified*. (d) 2025Q2–Q3 samples are tiny (n=11–26) and many early commits are bulk commits that lack conventional prefixes. D0 (`D0-history-metrics.md`) does not contain test/feat co-commit data; its relevant series are PC (product commits) vs coordination commits.

### 4.2 Per-pillar verdict

| Pillar (v1, 2025-07-27) | Verdict | Evidence |
|---|---|---|
| **1. Systematic Verification First** | **Practiced, and transformed into a much heavier evidence regime** (adherence rate itself *unmeasured*) | Became CLAUDE.md "Verify First, Create Second", STOP conditions, "Verified how:" required field (CLAUDE.md, 2026-08-29), m-43/44/50 sub-clauses in v3. But the failure it targets keeps recurring: v3 Practice 1 says "Most code is 75% complete then abandoned" and adds m-52 "open the artifact; a summary … is not its contents" (i.e. verification-by-summary was happening). B-workstream: Tests workflow red on main since 2026-09-20 (B1), full suite not executed ~1 week (B2), deploy not gated on tests (B5) — verification of *the product* is weaker than verification of *memos*. |
| **2. Test-Driven Development ("Write test FIRST … NO EXCEPTIONS")** | **Transformed (literal TDD abandoned as a rule within 3 days; co-located testing practiced and rising; CI enforcement currently eroded)** | Zones weakening 2025-07-27 (`0a6f1638c7`). v2.0 renamed it "Test What Matters, Not What's Easy" ("TDD remains the core" but UAT/Colleague Test added). Feat-commits-with-tests 44–55% (2025Q3–Q4) → 91–93% (2026) per §4.1. B9: ~12.8k tests, 982 files, 65.8% statement coverage (B11), 8% of tests are source-scanning ratchets (B14); B13: 1.6% of tests have no assertion. Against this: B1/B2/B4/B10 — main CI red, scheduled E2E 99/100 failed. Test-first order: **unobservable from git**. |
| **3. Multi-Agent Coordination ("NEVER work alone")** | **Transformed (volume exploded; "agents cross-check each other" is unverified)** | Original = two tools (Claude Code + Cursor). Now an 11-role cohort with mail/log/heartbeat machinery: D0 H1 coordination commits 22/month (2026-01..03) → 5,864/month (2026-08..09); C/P ratio 0.33 → 30.9 (×~95). v3 Practice 3 itself admits it "broke once" (m-41: "session logs accreted nothing for 6 of 9 cycling roles") and adds the consume side because of a 2026-09 intake gap. v3's own m-45 says independent agents sharing a procedural confound "compose into false corroboration" — i.e. cross-checking can be illusory. Whether one agent *validates another's work* (the public site's claim, §5) I could not measure from git *(unverified)*. |
| **4. GitHub-First Tracking** ("issue BEFORE starting; close with evidence") | **Practiced and extended (issue refs in feat/fix commits ≈96–97% in 2026Q1–Q2), with a measurement dip in 2026Q3 and an ungated deploy** | §4.1 last column; "Verified how:" and issue-closure protocol in CLAUDE.md; Practice 4 in v3. Counter-evidence: B5 fly-deploy runs on push to main with no `needs` on tests (89/100 success while Tests failed every run). "Update backlog.md and roadmap.md" half of the pillar is no longer stated anywhere I looked *(inferred)*. |
| **5. Agent-Driven Development** (added 2025-08-18) | **Abandoned as a pillar** (folded into Practice 3 in v2.0). | v2.0 text: "Pillar 5 … overlapped heavily with Pillar 3". |
| *Origin loop element:* Foundation-First / compounding | **Eroded as a stated idea, retained as Layer 1** | Dropped from the pillar list 07-27; v2.0/v3 Layer 1 "Quality compounds into velocity" preserved but unmeasured. D0: coordination bytes/PC lines 65 → 647 (×~10) while PC count ×2.7 and PC lines ×1.6 (B vs R windows) — the "investment" side is growing much faster than product output; whether it is *returning* velocity is the question D0 raises and E cannot answer. |

---

## 5. Public description vs internal reality

- **Public page** `src/app/(public)/methodology/page.tsx` (website; created 2026-02-15, `a199a10` "Website redesign"; last touched for SEO 2026-08-25): title "The Excellence Flywheel". Five numbered **Core Principles**: "Verification before implementation", "Tests before features" ("We write the test first. … If you can't test it, you don't understand it yet."), "Documentation as you go", "Cross-validation by default" ("Different AI agents check each other's work. One builds, another validates. Mistakes get caught before they compound."), "Systematic kindness". Closing line: "The methodology is the product." Homepage: "Our development approach is documented, tested, and open. We call it the Excellence Flywheel. You can read exactly how we work."
- **Compared to internal**: it matches **none** of the internal formulations. It has no GitHub-first tracking, no "Audit the Composition", no compounding loop (the thing the name denotes), and adds "Documentation as you go" and "Systematic kindness" that appear in no internal pillar list I found (grep of methodology-00 v1/v2/v3: not present). It was written after the 2026-02 drift (before v2.0/v3.0) and was **not updated** by either reformulation (no commits after 2026-02-15 change its content).
- "Tests before features … We write the test first" is stronger than internal practice: internal doc relaxed strict TDD on 2025-07-27 and the measured co-commit rate is ~91–93%, not 100%, with order unverifiable (§4). "Cross-validation by default" is presented as practice; internally it's the least measured pillar. "Verification before implementation" is the best-supported claim.
- `MethodologyDiagram.tsx:112` still draws "Excellence Flywheel" with "Flywheel Arrows" (component-level, not checked for text content).
- Public blog: the origin post is published (Medium 2025-09-28; website export). Note the archaeology says the origin narrative "was never published publicly" — **that is wrong at snapshot**: the website export contains it, and the editorial calendar shows it `distributed` with a Medium URL (`data/editorial-calendar.csv:143`). Later posts "Audit and Talk" (2026-04-17), "Weekly Ship #040: The Methodology Audits Itself", "The Practice That Got Retired" (2026-05-17) exist; I did not read them (*unverified* whether they teach v2/v3). Per CXO log `dev/2026/04/16/2026-04-16-0649-cxo-opus-log.md:54`, a "wrong paraphrase" of the Flywheel was found in 2 published blog posts and 2 drafts — whether corrected: **unverified**.

---

## Unobservables
- **Test-first order** (red→green) — git commits only snapshot end states; would need per-commit CI history or session transcripts.
- **Cross-agent validation actually catching defects** (pillar 3 "cross-check") — no labelled data; observable via PR review/bounce-back records ("Verified how:" bounces) if tallied.
- **Whether any re-evaluation changed outcomes** (velocity/defects) — D0's H4 defect series could be intersected with the v2.0/v3.0 dates; not done here.
- **Post-April blog posts' flywheel text; weekly-sweep S1 implementation** — not read.
- **First flywheel hit `946a0657c8` (2025-06-14)** — not inspected.
- Mailbox and dev/active documents cited via the archaeology (commit SHAs `7c5f8d9f`, `b5c63542`, etc.) were not individually re-verified; the ✔ rows were.

## Top findings for synthesis
1. **PM's four = Verification-first, TDD, Multi-agent coordination, GitHub-first tracking (the forgotten one)**; but the name originated as a 5-step *causal loop* three days earlier. (high; §1)
2. **The label was never stable**: 8 formulations by April 2026; Four-Pillars heading mismatched its 5-item body for ~8 months; the project's own archaeology and v2/v3 treat the Practice layer as intentionally evolving — so "flywheel" now means "current ruleset," plus a separate meaning as the duty-cycle loop (2026-06-23). (high)
3. **Re-evaluations repair the text, not the behavior**: v2.0 (Apr) and v3.0 (Sept) fixed documents; v2.0's "will evolve" clause rotted in 5 months (v3's own diagnosis); v3's review trigger is untested until #1386 (due 2026-10-30); stale "v2.0" pointers and a still-"four-pillar" glossary persist. (high/med)
4. **TDD**: literal rule relaxed 3 days after birth; tests-with-features co-commit 44%→93% (2025Q3→2026Q3) — practice improved, but main CI is red/skipped (B1/B2) so enforcement has eroded. (med; co-commit ≠ test-first)
5. **Multi-agent pillar transformed** into a coordination apparatus whose volume grew ~95× vs product output; no measurement shows the agents cross-validate (and m-45 says apparent corroboration can be false). Bears directly on "should we change anything." (med)
6. **Public site describes a fifth, different list** (adds "Systematic kindness", "Documentation as you go"; omits tracking and composition audit) and overstates test-first/cross-validation relative to internal records; never updated by v2/v3. (high)
7. **GitHub-first tracking** shows ~96–97% issue refs through 2026Q2, but deploy is not gated by tests (B5) — "track" is practiced, "verify before ship" is not mechanically enforced. (med)

Verified how: method = `git show`/`git log -S`/`git grep` on a191856 (and website 16dfe5fa), plus one Python pass over `git log --name-only` for §4.1; layer = git-history/record (no tests run, no live system); denominator = all 27,055 non-merge commits for §4.1 (1,264 service commits), 1 canonical doc across all 5 of its commits for timeline, ~15 secondary documents read, archaeology SHAs not individually re-verified.
