# Gold set scaffold — 100 insights for topic labelling (decision g: Janus pre-labels, xian confirms)

Generated 2026-10-08 by `gold_set_sample.py` (seed 20261008) from `insights.jsonl`: published unified briefs only, confidentiality `clear` only, stratified by quarter. Pool: 581 of 632 insights. Per quarter: 2025-Q2 7, 2025-Q3 8, 2025-Q4 8, 2026-Q1 15, 2026-Q2 27, 2026-Q3 27, 2026-Q4 8.

## Codebook (frozen 2026-10-08 per Janus C3) — one primary topic per insight

| # | Topic | Assign when the insight is mainly about… |
|---|---|---|
| 1 | agent coordination & process | how agents/roles hand off, schedule, message, decide, or govern their own work; duty cycles; mailboxes; session discipline |
| 2 | verification & testing | proving something works or didn't: tests, evals, checks, evidence standards, "verified how", false-clear failure modes |
| 3 | tooling & infrastructure | the machinery: CI, deploys, hosts, git mechanics, scripts, hooks, keys, environments, model/harness behaviour |
| 4 | documentation & knowledge | docs, briefings, logs, memory, glossaries, knowledge capture and retrieval — **including the sweep's own meta-insights about briefs, publishing and delivery** (the old "publishing & process meta" label folds here) |
| 5 | product & user-facing | what a user sees or does: features, UX, onboarding, surfaces (web/MCP/plugin), positioning, beta/launch |
| 6 | governance & security | rules, permissions, confidentiality, credentials, data boundaries, approvals, trust and oversight |

Secondary tag: free text, optional, your words (e.g. "worktrees", "ratchet tests", "Letters").

## How to fill it in
- **Janus**: put a topic number 1–6 in `Janus` for every row; add a tag if one jumps out. Same session it lands is perfect.
- **xian**: in `xian`, write **ok** to confirm, a **number** to correct, or **?** if it could be either (those rows drop out of the gold set rather than being forced). Rows you correct count double in the accuracy report.
- The "first line" is the insight heading only; open the brief (`src/internal/briefs/<date>-brief.md`, heading number in the id) when the heading is not enough.

## The 100

| # | id | brief date | first line | Janus | tag | xian |
|---|---|---|---|---|---|---|

| 1 | `2025-06-01#1` | 2025-06-01 | The No-Code Rejection and the Architecture That Resulted |  |  |  |
| 2 | `2025-06-01#2` | 2025-06-01 | The Naming Moment: From Tool to Teammate |  |  |  |
| 3 | `2025-06-01#3` | 2025-06-01 | "We Accidentally Built a Platform" |  |  |  |
| 4 | `2025-06-27#1` | 2025-06-27 | Knowledge Hierarchy: Four Tiers Reflecting PM Skill Acquisition |  |  |  |
| 5 | `2025-06-27#2` | 2025-06-27 | CQRS-Lite: The Insight That LIST_PROJECTS Is Not a Workflow |  |  |  |
| 6 | `2025-06-27#3` | 2025-06-27 | Duplicate Architecture Discovery: Archaeological Horror |  |  |  |
| 7 | `2025-06-27#4` | 2025-06-27 | Documentation as Governance for AI-Assisted Development |  |  |  |
| 8 | `2025-08-15#1` | 2025-08-15 | The Excellence Flywheel: Systematic Verification as Speed |  |  |  |
| 9 | `2025-08-15#2` | 2025-08-15 | The Three-AI Orchestra and the Emergence of Multi-Agent Coordination |  |  |  |
| 10 | `2025-08-15#3` | 2025-08-15 | The Reality Checks: When the Flywheel Self-Corrected |  |  |  |
| 11 | `2025-08-15#4` | 2025-08-15 | Building Faster Than Remembering |  |  |  |
| 12 | `2025-09-20#1` | 2025-09-20 | The 75% Pattern: Sophisticated Infrastructure, Incomplete Wiring |  |  |  |
| 13 | `2025-09-20#2` | 2025-09-20 | The ALL STOP: Architectural Clarity Over Panic |  |  |  |
| 14 | `2025-09-20#3` | 2025-09-20 | The Inchworm Protocol: Sequential Completion with No Exceptions |  |  |  |
| 15 | `2025-09-20#4` | 2025-09-20 | The GREAT Refactor: Five Epics in Seven Weeks |  |  |  |
| 16 | `2025-10-04#2` | 2025-10-04 | The Anti-80% Pattern and Structural Safeguards |  |  |  |
| 17 | `2025-10-04#3` | 2025-10-04 | Three Spatial Intelligence Patterns |  |  |  |
| 18 | `2025-10-04#4` | 2025-10-04 | GREAT-3 in Three Days: When Discipline Enables Speed |  |  |  |
| 19 | `2025-11-27#1` | 2025-11-27 | The Core Grammar: Discovered, Not Designed |  |  |  |
| 20 | `2025-11-27#2` | 2025-11-27 | Three Ownership Modes: Mind, Senses, Understanding |  |  |  |
| 21 | `2025-12-27#1` | 2025-12-27 | Pattern-045: Green Tests, Red User |  |  |  |
| 22 | `2025-12-27#3` | 2025-12-27 | Pattern-047: Time Lord Alert |  |  |  |
| 23 | `2025-12-27#4` | 2025-12-27 | The Pattern Sweep as Methodology |  |  |  |
| 24 | `2026-03-07#1` | 2026-03-07 | Day-One Roadmap — Dimension-Per-Step Structure |  |  |  |
| 25 | `2026-03-12#2` | 2026-03-12 | Wiring Bugs, Not Classifier Bugs |  |  |  |
| 26 | `2026-03-14#1` | 2026-03-14 | "The LLM is the Floor, Not the Ceiling" |  |  |  |
| 27 | `2026-03-14#3` | 2026-03-14 | Project Context Injection on Import |  |  |  |
| 28 | `2026-03-15#1` | 2026-03-15 | Floor Inversion — The Routing Was Backwards |  |  |  |
| 29 | `2026-03-15#3` | 2026-03-15 | AXT.md Formalized + Mnemosyne Onboarded |  |  |  |
| 30 | `2026-03-19#1` | 2026-03-19 | Nine-Agent Concurrent Operations — The Coordination Scaling Wall |  |  |  |
| 31 | `2026-03-20#1` | 2026-03-20 | Capability Awareness Gap — Five Sources of Truth, Zero Coordination |  |  |  |
| 32 | `2026-03-22#3` | 2026-03-22 | Dispatch Omnibus Automation Pilot — Automated Daily Synthesis |  |  |  |
| 33 | `2026-03-23#2` | 2026-03-23 | E2E + AAXT Testing Framework — Piper Morgan Adopts Klatch's Two-Track Model |  |  |  |
| 34 | `2026-03-23#4` | 2026-03-23 | Weekly Documentation Audit — Systematic Debt Recovery |  |  |  |
| 35 | `2026-03-24#3` | 2026-03-24 | Bookend-Sync Protocol — Formalized After Reliability Incident |  |  |  |
| 36 | `2026-03-25#4` | 2026-03-25 | Gate Verification Pattern Matures in Both Projects |  |  |  |
| 37 | `2026-03-28#4` | 2026-03-28 | Calliope's Calibration Notes: Externalizing Layer 5 |  |  |  |
| 38 | `2026-03-31#3` | 2026-03-31 | Cross-Pollination Hooks — PM Wants What Klatch Already Has |  |  |  |
| 39 | `2026-04-02#4` | 2026-04-02 | Intelligence Sweep #5 — Mythos/Capybara + Two API Deadlines |  |  |  |
| 40 | `2026-04-08#5` | 2026-04-08 | Backlog Pruning Yields MVP Clarity |  |  |  |
| 41 | `2026-04-12#4` | 2026-04-12 | Klatch Phase 1 design doc arrives next session — PM read offer open |  |  |  |
| 42 | `2026-04-17#2` | 2026-04-17 | Pattern-062 diagnosed in Identity queries — context assembly gap, not tone |  |  |  |
| 43 | `2026-04-19#3` | 2026-04-19 | Pattern-062 routed to AAXT — context assembly is the diagnostic before prompt adjustment |  |  |  |
| 44 | `2026-04-28#4` | 2026-04-28 | Methodology-24 + 25 filed; Pattern-063 self-implements via CT v2.3 |  |  |  |
| 45 | `2026-04-29#1` | 2026-04-29 | Klatch `/import/klatch` ships: canonical format is bidirectional; round-trip claim honest without hedging |  |  |  |
| 46 | `2026-04-30#1` | 2026-04-30 | Klatch intel sweep recovered: "verify your own stack before applying trade-press narratives" |  |  |  |
| 47 | `2026-05-07#3` | 2026-05-07 | Architect's soundness review fully closed: #1057 ships structlog + caplog incompatibility documented |  |  |  |
| 48 | `2026-05-10#1` | 2026-05-10 | M2f Group A+B complete: −2,229 LOC via dead-code disposition; Pattern-067 filed |  |  |  |
| 49 | `2026-05-11#2` | 2026-05-11 | #921 FastAPI upgrade ships via directional evidence; Monitor idle-spin Pattern-068 candidate |  |  |  |
| 50 | `2026-05-12#2` | 2026-05-12 | Opus 4.7 tokenizer +35%: plumbing shipped, default-flip explicitly held — both projects should recalibrate before flipping |  |  |  |
| 51 | `2026-05-13#2` | 2026-05-13 | Argus dreaming spike: Anthropic memory store ≅ Klatch L3 — import/export contract intact |  |  |  |
| 52 | `2026-05-14#2` | 2026-05-14 | M2g-A owner-reviews closed + #1087 / #1088 follow-ups filed |  |  |  |
| 53 | `2026-05-16#1` | 2026-05-16 | Workflow engine retired after months of silent bypass; the cleanup clinched Pattern-072 |  |  |  |
| 54 | `2026-05-25#2` | 2026-05-25 | Lead Developer's retroactive audit finds four premature issue closures — Pattern-045 case 4 filed |  |  |  |
| 55 | `2026-06-04#2` | 2026-06-04 | PM's cohort crosses a day boundary autonomously for the first time |  |  |  |
| 56 | `2026-06-07#3` | 2026-06-07 | PM's design token system already exists and passes WCAG-AA — the floor problem is inconsistent use, not a missing foundation |  |  |  |
| 57 | `2026-06-10#3` | 2026-06-10 | #1124 dispatch-chain cleanup reaches 10 of 28 legacy branches in one day — ratchet now test-enforced |  |  |  |
| 58 | `2026-06-13#1` | 2026-06-13 | Domain concepts that carry two jobs need an explicit contract for both — ADR-069 formalizes the pattern |  |  |  |
| 59 | `2026-06-13#2` | 2026-06-13 | Keyword-based safety classifiers have a systematic vulnerability when action names follow a naming convention that matches safe keywords (#1210, HIGH) |  |  |  |
| 60 | `2026-06-21#1` | 2026-06-21 | Klatch "New Klatch" spec complete — composition gate cleared, implementation handed to Daedalus |  |  |  |
| 61 | `2026-06-24#1` | 2026-06-24 | Mediajunkie: Local RAG + droplet-exposure pattern is live and reusable |  |  |  |
| 62 | `2026-06-24#2` | 2026-06-24 | PM: "Derive-don't-maintain" formalized as Architect signature pattern |  |  |  |
| 63 | `2026-06-25#3` | 2026-06-25 | 31 accumulated worktrees — prune-safety rubric now canonical |  |  |  |
| 64 | `2026-06-27#1` | 2026-06-27 | Klatch beta defined: when composition gesture is done and QA'd, cut the release |  |  |  |
| 65 | `2026-06-30#1` | 2026-06-30 | Partial capability migrations create a hidden confabulation risk — the LLM floor fakes success when handlers are missing |  |  |  |
| 66 | `2026-07-01#3` | 2026-07-01 | B1 spawn-fresh watchdog built and tested — the off-machine cure is a new process, not a woken one |  |  |  |
| 67 | `2026-07-03#1` | 2026-07-03 | An agent inbox as a mail slot, not shared custody — how a local-first app integrates with MCP without giving up device authority |  |  |  |
| 68 | `2026-07-06#1` | 2026-07-06 | Tool-specific safety rules don't self-generalize — write the principle, not just the example |  |  |  |
| 69 | `2026-07-08#1` | 2026-07-08 | Make multi-user data isolation inexpressible, not just detectable |  |  |  |
| 70 | `2026-07-13#1` | 2026-07-13 | "X is deprecated, use Y" in a system prompt doesn't suppress X — it activates both |  |  |  |
| 71 | `2026-07-27#2` | 2026-07-27 | `git fetch` updates the remote ref but doesn't move local HEAD — bare `git log` silently reads stale history |  |  |  |
| 72 | `2026-07-30#1` | 2026-07-30 | Multi-agent consensus drawn from a shared probe procedure is not independent evidence |  |  |  |
| 73 | `2026-07-31#2` | 2026-07-31 | A predicate derived from the corpus beats five attempts reasoned from prose |  |  |  |
| 74 | `2026-08-06#1` | 2026-08-06 | A loose predicate plus head truncation evicts the true positive — the noise is not noise, it is displacement |  |  |  |
| 75 | `2026-08-09#2` | 2026-08-09 | A freeze monitor that runs as a duty-cycle agent can't detect when the whole duty cycle freezes — the caller must be outside the frozen set |  |  |  |
| 76 | `2026-08-11#2` | 2026-08-11 | A correction count measures attention, not fault — at selection time, it selects for absence of scrutiny |  |  |  |
| 77 | `2026-08-13#2` | 2026-08-13 | Claude models apply their own discretion based on context provenance labels — without platform enforcement |  |  |  |
| 78 | `2026-08-15#3` | 2026-08-15 | For large local models running without memory-mapping, CPU-quiet and memory-available are different states |  |  |  |
| 79 | `2026-08-17#2` | 2026-08-17 | Anti-hallucination prompt examples can become templates for the wrong output they are meant to prevent |  |  |  |
| 80 | `2026-08-24#1` | 2026-08-24 | A deterministic pipeline makes failures visible and diagnosable; an adaptive layer hides them — prefer visible |  |  |  |
| 81 | `2026-08-26#2` | 2026-08-26 | A pre-registered prediction matching observed results does not confirm that the mechanism ran |  |  |  |
| 82 | `2026-09-05#1` | 2026-09-05 | A new monitoring instrument has no history — "never happened" is the wrong phrase for "no data yet" |  |  |  |
| 83 | `2026-09-09#1` | 2026-09-09 | Absence in a convenient channel is not absence in the world — the verification gap fires at the moment of dismissal, not use |  |  |  |
| 84 | `2026-09-10#1` | 2026-09-10 | Validating known CLI flags is not the same as rejecting unrecognized ones — and for destructive operations, the difference is the whole protection |  |  |  |
| 85 | `2026-09-12#1` | 2026-09-12 | A health check that lives inside the failing procedure cannot catch the failure of that procedure — Piper Morgan's DAY-CLOSED self-heal arc |  |  |  |
| 86 | `2026-09-13#3` | 2026-09-13 | A check that cannot see its target silently reports all-clear — Piper Morgan/Mediajunkie |  |  |  |
| 87 | `2026-09-14#1` | 2026-09-14 | A plan that records a label but re-resolves the key at apply time can silently bind the wrong record — Klatch Round 205 |  |  |  |
| 88 | `2026-09-16#2` | 2026-09-16 | The interval between agreeing a discipline rule and breaking it is exactly the duration of the next relevant action — DinP (Janus) |  |  |  |
| 89 | `2026-09-19#2` | 2026-09-19 | The "who imports this module" sweep cannot detect a write-deletion — Piper Morgan (#1810/#1814) |  |  |  |
| 90 | `2026-09-23#1` | 2026-09-23 | In Node.js ESM modules, `dotenv.config()` runs too late to reach constants read at module top level — Klatch Round 253 |  |  |  |
| 91 | `2026-09-25#1` | 2026-09-25 | A census figure is only valid for the population it explicitly names — Klatch Round 268 |  |  |  |
| 92 | `2026-09-29#2` | 2026-09-29 | Sorting by mtime in CI picks arbitrarily in a fresh checkout — sort by filename date instead — One Job `cd4a6f7` |  |  |  |
| 93 | `2026-10-02#1` | 2026-10-02 | A corpus absence-control must exclude the probe file from both the hits search and the owner lookup — Klatch, Theseus, Round 313 |  |  |  |
| 94 | `2026-10-03#1` | 2026-10-03 | When a routing layer prefers a rail entry's description, adapters must copy the registry text — a generic label silently breaks routing — Piper Morgan, Lead, commit `bf9569518` |  |  |  |
| 95 | `2026-10-03#2` | 2026-10-03 | A deploy readiness check must verify the commit SHA, not just the build status — Tectonic Globe, Tessera, commit `2ede091` |  |  |  |
| 96 | `2026-10-05#1` | 2026-10-05 | A check that filters to known names before counting confirms what you already have — Piper Morgan / Mediajunkie, Pard, commit `9cd5b43` |  |  |  |
| 97 | `2026-10-05#2` | 2026-10-05 | A delivery check that reads the rewritten copy always shows fresh — even on a stopped channel — Mediajunkie, Pard, commit `207c7f1` |  |  |  |
| 98 | `2026-10-06#2` | 2026-10-06 | A CI health script that hardcodes one workflow name misses every other gating check — Piper Morgan, CIO, commit `6c0116cb2b` |  |  |  |
| 99 | `2026-10-07#1` | 2026-10-07 | LLM decides meaning; code decides permission, checks meaning against real data, and shows before it acts — Piper Morgan, Arch, ADR-080, commit `8c7662e1e0` |  |  |  |
| 100 | `2026-10-08#1` | 2026-10-08 | A live probe of the served model caught an architectural ruling error that reasoning from ADR principles alone missed — Piper Morgan, Arch + Lead Dev, commits `19276a70b` · correction `0ece35153` |  |  |  |
