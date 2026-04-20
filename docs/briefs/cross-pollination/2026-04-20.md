# Cross-Pollination Brief — April 20, 2026

Klatch's automated intel sweep surfaced Opus 4.7's general availability and two approaching model deprecation deadlines — one already past — that both projects need to act on. On the architectural side, Klatch's MCP server reaches its Phase 5c decision point (write-path), and PM has shipped a session log maintenance hook pattern worth importing into Klatch's agent discipline.

## Key Insights

### 1. Opus 4.7 GA — evaluate upgrade in both projects

**From:** Klatch intel sweep (automated, 2026-04-20)
**Relevant to:** Klatch, Piper Morgan

Anthropic released Claude Opus 4.7 on April 16. Key improvements over Opus 4.6: substantially stronger software engineering and long-running coding tasks; high-resolution vision (3.75MP vs. 1.15MP); and a new **task budgets** feature where the model receives a running token countdown and self-paces its tool use. Pricing is unchanged ($5/$25 per M tokens in/out). SDK version `@anthropic-ai/sdk` is now at 0.90.0 — Klatch is on 0.86.1, four minor versions behind.

The task budgets feature is directly relevant to both projects: Klatch's Step 10 export packaging involves multi-step tool orchestration that could benefit from budget awareness; PM's Excellence Flywheel tracking could use it to surface cost-per-session trends. Neither project should rush the upgrade before running their full test suites, but the evaluation should happen this sprint.

**Suggested action:** Klatch: bump `DEFAULT_MODEL` evaluation and `@anthropic-ai/sdk` to `^0.90.0` in next dep maintenance. PM: check for Opus 4.6-specific patterns (budget_tokens, which is deprecated on 4.6) before upgrading.


### 2. Two model deprecation deadlines — one already past (urgent)

**From:** Klatch intel sweep (automated, 2026-04-20)
**Relevant to:** Klatch, Piper Morgan

Two concurrent deprecation risks:

**Haiku 3 (deadline: April 19 — yesterday).** A prior sweep identified a MODEL_ALIASES bug in Klatch: the key `claude-haiku-3-20250307` had two typos vs. the real model ID `claude-3-haiku-20240307`. The fix was assigned but its ship status is unconfirmed. If it didn't land, any channel using the Haiku 3 model ID is broken as of yesterday and needs an emergency DB migration.

**Sonnet 4 + original Opus 4 (deadline: June 15 — 57 days).** `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire June 15. Migration targets are Sonnet 4.6 and Opus 4.7. Both projects may have these model IDs hardcoded in DB records, config, or channel exports.

**Suggested action:** Klatch: confirm Haiku 3 alias fix shipped before today's sessions; if not, treat as P0. Both projects: run a grep/DB audit for `claude-sonnet-4-20250514` and `claude-opus-4-20250514` before end of sprint. Add both IDs to MODEL_ALIASES as a safety net.


### 3. Klatch Phase 5c decision point — write-path with cross-producer implications

**From:** Klatch `docs/logs/2026-04-18-1256-argus-opus-log.md`, `docs/plans/STEP-10-PHASE-5-MCP-SERVER.md`
**Relevant to:** Piper Morgan (cross-producer coordination)

Phase 5a (read-only resources) and 5b (tools surface: `list_channels`, `get_context_package`, `get_manifest`) are complete — 1069 tests, zero failures. Argus has given Daedalus a clear signal to pause for the Phase 5c decision.

Phase 5c introduces the first write-path: `reflect(channel_id, note)` — a micro-reflection that a consumer agent writes back after using a context package. The plan document flags this explicitly: "the data-integrity and concurrency questions deserve their own evaluation." More critically, write-path coordination has **provenance and trust implications that read-paths don't** — the same note in the Phase 5 plan. PM is the sibling producer whose own eventual write-path (`save_artifact`) will need to interoperate.

This is a moment where PM Chief Architect input before Klatch finalizes 5c design would cost one memo and save significant retroactive alignment work.

**Suggested action:** PM Chief Architect: file a short position memo on write-path coordination timing — does PM's `save_artifact` design need to be in view before Klatch locks 5c? Even a "no strong opinion yet" answer unblocks Daedalus cleanly.


### 4. Session log maintenance hooks — PM pattern transferable to Klatch

**From:** PM `dev/2026/04/19/2026-04-19-0639-docs-code-opus-log.md`
**Relevant to:** Klatch (agent process discipline)

PM's Apr 19 docs session resolved an incomplete-log failure mode: the Apr 16 Lead Dev session log stopped at 8:45 AM despite work continuing until evening, with the afternoon reconstructable only from 28 git commits. The fix: a PostToolUse hook (`.claude/hooks/log-maintenance-reminder.sh`) that fires every 15th Bash call and warns if the log hasn't been updated in 30+ minutes. CLAUDE.md was updated to make log discipline non-negotiable, and a feedback memory file was saved to prevent recurrence.

Klatch has the same failure mode risk — multi-hour agent sessions with dense tool use. The hook pattern is a three-file change: hook shell script, settings.json registration, CLAUDE.md enforcement section.

**Suggested action:** Klatch Dispatch or Architect: evaluate importing PM's log-maintenance hook pattern. PM's implementation in `.claude/hooks/log-maintenance-reminder.sh` and `.claude/settings.json` is reference-ready.


## Sources Read

- `klatch/docs/intel/2026-04-20-sweep.md` — automated external scan, full read
- `klatch/docs/logs/2026-04-18-1256-argus-opus-log.md` — Argus Round 26b session wrap (Phase 5b sign-off)
- `klatch/docs/plans/STEP-10-PHASE-5-MCP-SERVER.md` — Phase 5c and open questions sections
- `piper-morgan-product/dev/2026/04/19/2026-04-19-0639-docs-code-opus-log.md` — docs session: Sibling Intelligence publish + log maintenance safeguards
- `piper-morgan-product/docs/briefing/BRIEFING-ESSENTIAL-COMMS.md` — communications role briefing


*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
