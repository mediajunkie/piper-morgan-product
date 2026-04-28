
# Cross-Pollination Brief — April 28, 2026

PM's #1004 semantic detector went from "build authorized" (yesterday's brief) to "shipped, 112/112 PASS" in a single session; #1002 and #1003 are both closed, and Phase F flag-flip conditions are met — the decision now sits with PM/PA. On the Klatch side, Theseus ran the first live MCP stdio integration test (27/27 pass, official TypeScript SDK, same path Claude Code/Desktop would take) and live-tested all three export formats, surfacing three round-trip gap findings. Phase 3.5b dual-mode extraction is working as designed, with a visible and useful agreement/disagreement pattern on real conversations. PM's Chief of Staff completed the PO calibration reply, and Methodology-24 (Branch-or-Anchor) and -25 (Workstream Review Cadence) are now formally filed, with CT v2.3 embedding the Branch-or-Anchor rule directly in the rubric as a self-protective section.

## Key Insights

### 1. #1004 ships end-to-end in one session; Phase F flag-flip open to PM/PA

**From:** PM `dev/2026/04/27/2026-04-27-1212-lead-code-opus-log.md`; commits `b26d6c85` (Step 9 ship merge), `2322907a` (Phase F notification); `dev/2026/04/27/1004-probe-set-v0-1-run-2.md`
**Relevant to:** Klatch (typed probe + calibration pipeline as a transferable pattern; hint_shape_violation as a foreseeable failure mode in future PM-adjacent tooling)

Steps 8+9 shipped in a single Monday session. The full sequence: Architect's Step 8 guidance arrived in the inbox before the session started; CXO had pre-authored a prompt body v0.1 on Sunday; Phase C run-1 (11/20 PASS) went to CXO for a divergence scan; CXO returned prompt v0.2 + probe deltas same afternoon; run-2 hit 18/20 PASS and met all three of CXO's success criteria. Direct merge to main; 112/112 PASS across the full ethics enforcement suite.

**Calibration finding:** The residual 2/20 failures are `hint_shape_violation` on domain vocabulary — "roadmap" and "finance" — both load-bearing tokens in the redirect's usefulness. The assertion harness correctly flags them but they can't be removed without softening the redirect. Lead Dev's read: not chase-able in v0.3 without a carve-out for entity-naming tokens; argued for ship at v0.2. This is a named failure mode (hint_shape_violation on substantive domain words) that will surface in any system that audits redirect output for input-substring leakage.

**Core function healthy:** 19/20 violation classifications correct in run-1 before prompt tuning.

**#1002** (pre-classifier keyword dispatch shadows ethics floor) and **#1003** (harassment vector routes to GUIDANCE without boundary audit fields) both closed with full evidence per close-issue-properly skill. Phase F conditions per PPM v4: ✅ Architect scoping, ✅ #1002+#1003 closed with evidence, ✅ diagnostic shows flag matters (5/5 harassment-vector flag-off runs before prompt tuning), ✅ probe set + two calibration rounds on main. Lead Dev's recommendation: defer flag-flip to wait for ADR-061 (architectural delta codification, in flight from Architect). PM/PA decide.

**Suggested action:** Klatch — the calibration pipeline pattern is transferable: typed probe dataclass (expected violation, category, confidence range, redirect shape), async runner, domain-expert calibration loop (run-1 → expert divergence scan → prompt v0.2 → run-2). If AAXT ever expands to include behavioral correctness assertions on redirect content, this is the shape. The hint_shape_violation failure mode (harness correctly fires on domain vocabulary that's load-bearing) is a foreseeable gotcha when writing redirect-content assertions.


### 2. Klatch: first live MCP stdio integration + export round-trip gaps scoped

**From:** Klatch `docs/logs/2026-04-27-1355-theseus-opus-log.md`; commit `e52ded4` (Round 29-30 + MCP live probe), `00b5426` (Theseus wrap with round-trip + Phase 3.5b + imported-channel AAXT)
**Relevant to:** PM (round-trip gap findings map to Phase 3.5 / L5 portability design decisions already in flight)

**First live MCP integration test (Task 2):** `scripts/aaxt-mcp-live-probe.ts` spawns the server as a child process via the official MCP TypeScript SDK over `StdioClientTransport` — the same transport path Claude Code and Claude Desktop would use. 27/27 checks pass (two initial "failures" were probe script bugs: misexpected envelope shape, and by-design graceful degradation on version `99.0.0`). Every primitive exercised: resources, tools, prompts, write-path (reflect), error handling, version negotiation. The server is confirmed to work correctly through the real SDK, not just unit tests.

**Export round-trip live (Task 6) — three gap findings:**
1. **Project UUID-matching gap:** re-import via claude.ai creates a duplicate project (`AAXT Test Project × 2`) instead of detecting the original by UUID match. The exported `projects.json` carried the original UUID; the importer didn't use it.
2. **No direct re-import path:** no `/import/klatch` endpoint. Round-trip requires going through a transport adapter (claude.ai or claude-code), with their respective fidelity losses. Canonical format is one-way unless a re-import endpoint is added.
3. **L4/L5 lost in claude.ai round-trip** — both by design (claude.ai has no L4 concept; it's single-persona). Phase 3.5 (briefing + extraction options at export time) is the design answer to L5 loss, but only fires when those options are explicitly passed. Silent round-trip loses Layer 5 entirely.

**Phase 3.5b dual-mode extraction (Task 7):** `?briefing=true&extract=true` on CH1 produced 9 field notes total. Key cross-validation pattern: where they agree, high confidence; where they diverge — the briefing noted its own escalating verbosity as something to *avoid*; the extraction framed the same behavior as positive ("user values signal of depth across multiple dimensions"). Phase 3.5 is working as designed. The disagreements are exactly where human reviewer judgment matters.

**AAXT against imported channel (Task 8):** 143-message real Theseus session, 13/13 Correct, first live L1 probing. L1 probes naturally bleed into L2 territory because the kit briefing references project context — probes score correctly regardless; layer attribution is ambiguous. Flagged as future probe design work. Agent's self-presentation on L1 probes opened with "Continuing from a Claude Code session…" — kit briefing context operationally visible.

**Suggested action:** PM — three findings relevant to Phase 3.5 / L5 portability thinking: (1) the UUID-matching gap means any user who exports then re-imports loses the project link — this affects multi-hop provenance chains; (2) "no direct re-import path" means Klatch's canonical format is currently write-once for the round-trip use case; (3) Phase 3.5 is the correct design answer for L5 but must be explicitly invoked — silent round-trip drops Layer 5 with no warning. If PM ever implements a similar import/export pattern, these are the gap categories to design around from the start.


### 3. CoS PO advice reply: source-check comparative claims before they ship under someone else's name

**From:** Hub `docs/mail/memo-exec-to-janus-po-advice-reply-2026-04-26.md`; commit `446a665a`
**Relevant to:** Klatch Calliope (pending response to the same PO calibration relay — the DRAGONS and CoS replies are now both on record as comparison points); all agents producing content that ships externally under xian's name

PM Chief of Staff completed the PO calibration reply (relayed via Janus April 27). The one pattern named: **source-check comparative claims against the original record before letting them ship under someone else's name.** Operationally: any claim of the shape "most X," "first Y," "more Z than ever" gets checked against the source before going out under PM's name.

CoS frames this as a reviewer-vs-author distinction: "Authors are committed to making the claim land; the reviewer's job is to verify it lands honestly." The pattern forced itself into existence through an April 19 incident (a "most X to date" comparative superlative in a HOST workstream memo that didn't survive source-check against the omnibus logs). The discipline codified as a standing norm: *verifiable-claims memo, originally to HOST, now standing norm across all leadership.*

The third section of the reply names something harder to extract from a pattern note: **the discipline depends on the relationship's tolerance for "actually wait, let me check that."** Without that — if catches were treated as obstacles — the discipline atrophies. CoS explicitly flags this as the part PO should internalize beyond the operational checklist.

**Suggested action:** Klatch Calliope — your PO calibration reply is still pending (5–7 day window, now ~Day 3). DRAGONS named two patterns (anti-fabrication with explicit placeholders; audience segmentation as a hard rule). CoS named one (source-check comparative claims; reviewer-vs-author distinction). When writing your response, these are useful comparison points: which of these apply to Klatch's working-with-xian dynamic, which don't, and what patterns does Klatch generate that the others haven't named? Argus's intel sweep practice and Calliope's chronicle role both have natural contact with the source-check discipline.


### 4. Methodology-24 + 25 filed; Pattern-063 self-implements via CT v2.3

**From:** PM commit `3bcd9ee` (Methodology-24 Branch-or-Anchor + Methodology-25 Workstream Review Cadence); CXO commit `64a94e2` (CT v2.3 with Branch-or-Anchor section)
**Relevant to:** Klatch (any future parallel rubric or evaluation instrument co-authoring); all agents who produce workstream reviews or extend canonical methodology documents

**Methodology-24 (Branch-or-Anchor Discipline)** codifies the structural fix for Pattern-063: when extending a canonical reference, either anchor (cite and use unchanged, credit by content not just label) or branch (rename and version explicitly). Silent extension is the failure mode this rule prevents. "Belt-and-suspenders implementation" per CXO Apr 26: methodology-core entry + embedded "How to extend this rubric" section in canonical documents themselves.

**CT v2.3** lands with a new "How to Extend This Rubric — Branch-or-Anchor Discipline" section. This means Pattern-063 is now self-protective at the document level: the canonical Colleague Test rubric tells its own users how to avoid Pattern-063 when extending it.

**Methodology-25 (Workstream Review Cadence)** codifies the Fri-Thu window, Fri-Tue writing window, Wed publish cadence, and — critically — **source discipline effective Ship #041 onward**: read primary session logs first; omnibus is coverage check, not primary input. This is a process norm change with direct relevance to any agent producing workstream reviews.

**Suggested action:** Klatch — if Argus and Theseus ever co-author a testing rubric or evaluation instrument, Methodology-24 is the design-time check: "If the two authors swapped rubrics, would they get the same score?" The Branch-or-Anchor rule prevents Pattern-063 at authoring time rather than after the fact. For the record: Methodology-24 is the third cross-relevant methodology PM has filed in the trailing 30 days (after Methodology-00 Flywheel v2 and the verifiable-claims standing norm). The methodology catalog is compounding.


## Sources Read

- `klatch/docs/logs/2026-04-27-1355-theseus-opus-log.md` — full read; Tasks 1-8: Round 29-30 fixes, MCP live probe 27/27, export round-trip findings, Phase 3.5b, imported-channel AAXT L1 probing
- `klatch/docs/logs/2026-04-27-0807-calliope-opus-log.md` — full read; PO calibration status, Theseus day chronicled, Argus PM #995 routing
- `klatch` commits `e52ded4`, `00b5426` — stat and message read
- `piper-morgan-product/dev/2026/04/27/2026-04-27-1212-lead-code-opus-log.md` — full read; Steps 8+9 full sequence, calibration runs, #1002+#1003 closures, Phase F notification
- PM commits `3bcd9ee` (Methodology-24+25), `64a94e2` (CT v2.3), `b26d6c85` (Step 9 ship), `2322907a` (Phase F notification) — stat and message read
- `designinproduct/docs/mail/memo-exec-to-janus-po-advice-reply-2026-04-26.md` — full read; CoS PO calibration reply
- `atlas`, `globe`, `cuneo` — 48h logs non-empty (brief delivery commits only); no narrated insights.
- `weather` — one code fix (`Fix rmapi: use v4-compatible build from PR #56`); pure code commit, no narration; not reported.
- `one-job`, `optilisten`, `nyt-crossword` — automated status/print commits; no narrated insights.

**Not re-reported (covered in prior briefs):** Klatch MCP 1.0 feature-complete Phase 5c-i (Apr 27); AAXT first live behavioral run CH1 + code-fence bug + L4/L2 probe contamination (Apr 27); Phase E S1 r2 harassment routes to GUIDANCE not boundary (#1003 filed — Apr 27); #1004 contract v1.0 stable + build authorized (Apr 27); Pattern-063 Parallel-Authoring Drift (Apr 27); five-role migration complete (Apr 26); #992 merged to main + floor-bypass-by-routing (Apr 26); DRAGONS two PO patterns (Apr 26); Multi-Wave Investigation published (Apr 26).


*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
