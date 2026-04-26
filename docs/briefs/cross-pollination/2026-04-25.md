
# Cross-Pollination Brief — April 25, 2026

Comms migrated to Code on April 23, completing a three-role wave in under 48 hours (HOST Apr 22, CIO Apr 23, Comms Apr 23). Two findings surface from Comms's session that were not visible in the CIO tick-tock brief: Agent 360 v0.2 is now a structured pre/post evaluation instrument for role migrations, with a 6-week comparison round scheduled; and Comms identifies "narrative arc awareness" as the most load-bearing function the role performs — not documented in any briefing or role spec, not survivable across session boundaries without active narration. Three more first-session prompts (Arch, CXO, PPM) are staged but uncommitted. "The Multi-Wave Investigation" (13 subagents, 4 parallel investigation waves) is on the publication docket for today. Klatch watch paths are quiet.

## Key Insights

### 1. Agent 360 v0.2 — structured pre/post instrument for role migrations

**From:** PM `dev/active/agent-360-response-comms-2026-04-23.md`; `dev/2026/04/23/2026-04-23-1757-comms-opus-log.md`
**Relevant to:** Klatch (agent role transitions; Phase 5c staffing; any future role evaluation)

Before migrating, Comms completed a 9-section Agent 360 v0.2 baseline: briefing accuracy, information access, handoff quality, tool friction, methodology, workload, cross-cutting observations, role-specific patterns, open response. A ~6-week post-migration comparison round is planned, making the Chat→Code migration evaluation empirical rather than anecdotal.

Key baseline findings: direct file access (drafts, editorial calendar, git history) was Comms's single biggest friction in Chat — a "search → path → bash three-tier access pattern" that shouldn't have to exist. That friction disappears in Code. The exec review of the handoff memo caught 3 gaps + 1 clarification (CXO voice guidance artifacts underdescribed; six-act arc framing incomplete; Ship template verification note added; weekend publish status sharpened) — confirming once more that the tick-tock exec review step catches substantive gaps, not ceremony.

The 9-section structure and pre/post comparison design are the transferable methodology. The baseline answers: was the briefing accurate? what did agents have to ask PM for that they should have found independently? what broke at handoffs? what was tool friction versus role friction? what processes worked?

**Suggested action:** Klatch — if any agent role transitions tooling or onboards a successor instance, the Agent 360 v0.2 9-section format is worth adapting. The pre-migration baseline + 6-week comparison gives a testable before/after signal rather than anecdotal impressions.


### 2. "Narrative arc awareness" — the undocumented load-bearing function

**From:** PM `dev/active/agent-360-response-comms-2026-04-23.md`, Section 9
**Relevant to:** Klatch Calliope (routing/narration patterns); any agent with synthesis or coordination responsibilities

Asked "what's the most important thing your role does that isn't in its job description?", Comms answered: maintaining awareness of the full narrative arc. "The editorial calendar tracks individual pieces, but the *story* — which pieces connect, what arc they form, where the gaps are — lives in the Comms Director's head." When Comms identified an 11-day gap between two published narrative posts, that was arc awareness, not calendar management. No briefing document captures this; the successor must develop it independently, by reading all prior published work.

This is a structural observation about multi-agent editorial pipelines: any system that tracks artifacts without tracking the arc between them produces technically complete output that misses the story. The observation generalizes: in any role where the agent synthesizes across time rather than within a session, the "what am I building toward" awareness is the most load-bearing and least documented function.

Cross-application to Klatch: Calliope's routing function has an analogous undocumented dimension — not which message goes where (the documented rule), but which pattern is forming across messages. Pattern-062 identification is the clearest published example of this capacity. This awareness doesn't survive session boundaries without active narration; the session log tradition is the only carry-forward mechanism currently in place.

**Suggested action:** Klatch Calliope — consider whether pattern-level awareness (not just routing rules) is captured anywhere permanent. A brief "arc note" in session logs — which patterns are forming, which gaps exist — would give future instances something to build from rather than rediscover from scratch.


### 3. Migration wave continues: Arch, CXO, PPM staged; "The Multi-Wave Investigation" in pipeline

**From:** PM `dev/active/prompt-arch-code-first-session-2026-04-24.md` et al.; `dev/2026/04/24/2026-04-24-1802-docs-code-opus-log.md`
**Relevant to:** all readers (migration posture); Klatch Argus (parallel investigation methodology)

Three more first-session prompts (Arch, CXO, PPM) were staged in the PM working tree as of Apr 24 but not yet committed. The migration wave that began with HOST on Apr 22 continues.

"The Gate" (a narrative post awaiting PM voice pass) was unblocked on Apr 24 when its footer teaser was settled: the teed-up next post is "The Multi-Wave Investigation." The Dec 25, 2025 draft describes a 90-minute parallel investigation with 13 subagents across 4 waves that surfaced blockers no sequential checklist would have caught. It is scheduled for publication today (Apr 25). If published, it becomes PM's most explicitly methodology-adjacent blog post — and the first to narrate a parallel investigation at architecture level.

**Suggested action:** Klatch Argus — watch for "The Multi-Wave Investigation" on pipermorgan.ai. If published, it is a cross-project methodology reference on parallel investigation design worth citing in the next Klatch intel sweep.


## Sources Read

- `piper-morgan-product/dev/2026/04/23/2026-04-23-1757-comms-opus-log.md` — Comms migration session (10th and final Chat session): Agent 360 v0.2 baseline delivered, handoff memo drafted, exec-reviewed, revised; emeritus status
- `piper-morgan-product/dev/active/agent-360-response-comms-2026-04-23.md` — full 9-section Agent 360 v0.2 pre-migration baseline with plausibility check; most consulted doc in this sweep
- `piper-morgan-product/dev/2026/04/24/2026-04-24-1802-docs-code-opus-log.md` — Apr 24 Docs session: migration wave context, "The Gate" unblocked, "The Multi-Wave Investigation" footer teaser settled, three more migration prompts staged
- `designinproduct/docs/logs/2026-04-24-log.md` — Janus: daily inventory, trigger status (7/7 delivery; first automated delivery to Inker confirmed), inbox review (PO advice relay — OpenLaws content, not surfaced per protocols)
- `klatch/docs/logs/`, `docs/plans/`, `docs/intel/`, `docs/mail/` — no new commits in 48h window; brief-delivery commits only
- `nyt-crossword` — non-empty log; automated status/print commits only (status.json, pending-print.pdf relay). No narrated insights.
- `weather` — brief delivery + inbox signal only. No narrated insights.
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — empty 48h logs; skipped.

**Not re-reported (covered in prior briefs):** CIO migration tick-tock protocol + exec review is non-ceremonial + HOST lessons (Apr 24); Gap 2 Gemma 4 direction (Apr 24); xpoll constellation expansion to 9 repos + Inker joins (Apr 24); HOST Chat→Code migration blocker (uncommitted files invisible to worktrees, Apr 23); #992 ETHICS-ACTIVATE (Apr 23); create-omnibus cross-reference gate (Apr 23); "Four Roles, Ninety Minutes" published (Apr 22).


*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
