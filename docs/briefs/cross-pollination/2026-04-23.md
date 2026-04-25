# Cross-Pollination Brief — April 23, 2026

PM closed a high-volume April 22: the ethics enforcement arc that began with a disabled flag discovery on April 17 completed all four implementation phases and merged to main. HOST ran its first Claude Code session — and the session's immediate BLOCKER produced a concrete migration lesson. Docs, discovering the April 16 omnibus was built from an incomplete source set, added a structural safeguard to the `create-omnibus` skill before synthesizing five days of backlog. Klatch watch paths have no new commits in the 48h window.

## Key Insights

### 1. #992 ETHICS-ACTIVATE ships — the enforcer/voice pattern is production code

**From:** PM `dev/2026/04/22/992-gameplan.md`; merge commit `fcd44c5` (branch `claude/992-ethics-activate`)
**Relevant to:** Klatch (ethics enforcement design reference; Phase 5 write-path trust implications)

After the design decision (Apr 17), CXO voice unblocking (Apr 18), and a full audit-cascade gameplan, Lead Dev completed all four phases on April 22 and merged to main. Deliverables: `redirect_context` field in `BoundaryDecision` (Phase A); `FloorContext` denial mode + voice-template addendum that makes denials sound like Piper, not a policy engine (Phase B); end-to-end ethics denial flow wired through `intent_service` (Phase C); Phase D false-positive scan — a standalone Python script run against the canonical corpus, 100% pass. Net: 1,597 lines added across 11 files, three new test suites (561 lines), `ENABLE_ETHICS_ENFORCEMENT` flipped to `true` in production config.

The voice template's anti-patterns are codified in the denial-mode prompt: "Request blocked due to ethics policy," "Violation detected," "As an AI I cannot…" are all explicitly prohibited. The BoundaryEnforcer remains structurally separate from Piper's voice — the split that the Apr 17 brief described as the design is now enforced in the code.

Klatch's Phase 5c `reflect` write-path will raise provenance and trust questions that don't exist on the read side. The `BoundaryEnforcer` pattern — enforce separately from voice, let the entity speak — is reference-ready in PM's codebase if Klatch needs a model.

**Suggested action:** Klatch Daedalus: if Phase 5c's write-path design encounters trust/denial questions, PM's `services/ethics/boundary_enforcer_refactored.py` and `services/intent_service/conversational_floor.py` are live reference implementations of the enforcer/voice split.

---

### 2. HOST Chat→Code migration blocker — uncommitted files are invisible to Code worktrees

**From:** PM `dev/2026/04/22/2026-04-22-1823-host-code-opus-log.md`
**Relevant to:** Klatch (Chat→Code migration discipline for any remaining Chat-rooted roles)

HOST (Head of Sapient Trust) made its first Claude Code session on April 22. The session hit an immediate BLOCKER: three handoff files that PM had written in Chat's working tree — the "I'm writing the handoff I wish I'd received" package — were untracked in git and therefore invisible to the Code worktree. HOST searched thoroughly (glob, find, `git log --all`), found nothing, named the STOP condition ("can't verify inheritance context without the handoff"), and waited for PM rather than reconstructing from peripheral sources. The resolution was clean: commit from main's working tree first, then the worktree can see the files via git.

Side item with broader scope: the role briefing file was named `BRIEFING-ESSENTIAL-HOSR.md` — a typo that went unnoticed because the role was always referred to by the correct name in prose. HOST's first Code session produced a correction memo; Docs renamed the file (`git mv`) with history intact on April 22.

The failure mode is precise: anything written in a Chat session that isn't committed to the repo does not exist for Code agents. For Klatch, this matters if any remaining Chat-originated content (entity configuration, handoff memos, calibration artifacts) hasn't been committed — they are absent from any Code worktree and from any future clone.

**Suggested action:** Klatch — if any Klatch roles have Chat-originated artifacts not yet committed to the repo, commit them before the next Code session on that role. The "files are present in Chat but untracked in git" failure mode is now documented with a concrete example.

---

### 3. Omnibus source-log drift discovered — create-omnibus gets a cross-reference gate

**From:** PM `dev/2026/04/22/omnibus-gap-remediation-tracker-2026-04-22.md`; `.claude/skills/create-omnibus/SKILL.md`
**Relevant to:** Klatch (session-log synthesis discipline; cross-pollination input chain)

Docs discovered the April 16 omnibus (synthesized April 19, already marked retrospective in the April 22 brief) was built from an incomplete source set: 4 of 9 agent sessions were missing (PPM, CIO, HOST standalone, and partial Arch). Root cause: Pattern-062 applied to synthesis work — the agent assumed the logs present in the tree were all the logs, without cross-checking agent mentions *inside* those logs. A session log that says "Architect reviewed CXO's position" is evidence that a CXO session log exists; if no CXO log is in the source set, that's a gap.

The fix: Step 2.5 "Cross-Reference Gate" added to the `create-omnibus` skill. It scans each source log for mentions of canonical agent roles (using the agent-vocabulary regex), compiles the union of mentioned roles, and compares against the source set. Any mentioned-but-missing role is flagged to PM before synthesis proceeds. "Never silently paper over the gap" is the new directive.

The cross-pollination brief process has the same structural risk. If Klatch log A mentions Argus and Argus hasn't filed a log for that day, that gap can propagate silently into the brief. The "mentioned-but-missing" signal is a lightweight check that requires no new tooling — just reading source logs for each other's names before finalizing a synthesis.

**Suggested action:** Klatch Dispatch (cross-pollination brief writer): before finalizing each brief, scan the Klatch session logs read as sources for mentions of other Klatch agents. If Daedalus's log references an Argus decision but no Argus log is in the source set, note the gap explicitly in Sources rather than silently omitting it.

---

## Sources Read

- `piper-morgan-product/dev/2026/04/22/992-gameplan.md` — full read; Phase breakdown, completion matrix, denial-voice design
- `piper-morgan-product/dev/2026/04/22/2026-04-22-1823-host-code-opus-log.md` — HOST first Code session; BLOCKER + resolution
- `piper-morgan-product/dev/2026/04/22/2026-04-22-0711-docs-code-opus-log.md` — Ship #039 publish, SessionStart hook fix, omnibus gap discovery
- `piper-morgan-product/dev/2026/04/22/omnibus-gap-remediation-tracker-2026-04-22.md` — gap map, remediation plan, skill fix
- `klatch/docs/logs/` — most recent files April 18; no new commits in 48h watch window

**Retrospective (not generating new insights):** Apr 17–21 omnibus logs committed April 22 — content dates all precede the April 22 brief; treated as confirmatory per retrospective log rule.

**Not re-reported (already covered in prior briefs):** "Four Roles, Ninety Minutes" published (Apr 22), ethics voice architecture design and CXO unblocking (Apr 17–18), PDR-004 canonical-term discipline (Apr 21), "Sibling Intelligence" published (Apr 21), Phase 5c write-path decision point (Apr 20), Opus 4.7 GA and deprecation deadlines (Apr 20), session log maintenance hook pattern (Apr 20), Klatch MCP server Phase 5a+5b (Apr 19).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
