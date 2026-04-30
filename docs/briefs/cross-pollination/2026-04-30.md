
# Cross-Pollination Brief — April 30, 2026

Klatch's April 27 automated intel sweep was orphaned on a deleted branch for two days and recovered by Argus on April 29, post-brief. Curation produced a reusable methodology: before treating trade-press vendor-change warnings as threats, verify your own stack's state — two High-priority items turned out to not apply to Klatch at all. On the PM side, Architect shipped Pattern-064 "Extension Without Integration," completing the 062/063/064 architectural-debt naming family (component, vocabulary, extension layers — same root cause, three different manifestation points). PA published the branch-discipline synthesis v1.0 as a canonical CLAUDE.md section, closing the multi-day multi-thread on multi-agent coordination discipline.

## Key Insights

### 1. Klatch intel sweep recovered: "verify your own stack before applying trade-press narratives"

**From:** Klatch `docs/intel/2026-04-27-sweep-curated.md`; commit `b551080` (Argus 4/29); memo `argus-to-calliope-orphan-sweep-recovery-2026-04-29.md`
**Relevant to:** PM (any team with active API/model upgrade exposure)

The April 27 automated intel sweep (sweep #9) was filed on branch `claude/amazing-ptolemy-NcAtO` which was then deleted. Argus recovered it via cherry-pick on April 29 and ran in-session verification on the two items originally flagged High priority.

**Opus 4.7 thinking opt-in — NOT a regression:** The trade-press framing was "breaking change for Klatch's message_artifacts capture." In-session audit of `packages/server/src/claude/client.ts` found both streaming paths already pass `thinking: { type: 'adaptive', display: 'omitted' }`. The API drops thinking blocks regardless of opt-in. No stored thinking content to lose. **To start capturing thinking content (forward-only, not a current requirement):** (a) flip `display` from `'omitted'` to `'enabled'` AND (b) add `betas: ["thinking-summaries-2025-02-19"]` to the request. Both required.

**MCP STDIO injection (Ox Security) — NOT exposed:** The Ox disclosure is about MCP *clients* passing untrusted server-command strings to `subprocess.exec`. Klatch's `packages/server/src/mcp/bin.ts` is the *server side* — it's launched by clients (Claude Code, Claude Desktop), never spawning MCP subprocesses itself. Future-flag: if Phase 5d adds HTTP proxying to externally-defined MCP server commands, revisit.

**Genuine watch items routed to Daedalus (Medium priority):** Opus 4.7 new tokenizer (+35% token count — cost/compaction threshold impact for any 4.7 entity); `xhigh` effort enum (one-line schema addition to unlock 4.7's full capability); SDK currency (0.86.1 → 0.90.0 — confirm thinking-opt-in API available before any "show thinking" UI ships). **Also noted:** Sonnet 4 / Opus 4 retirement clock at 47 days to June 15; DB audit still pending for live channels pinned to literal model IDs.

**Sweep cadence:** trigger config fixed; this was the only orphan. Chain is now complete; future automated runs land on main directly.

**Suggested action:** PM — the verification method is the deliverable. Before any agent treats a vendor-change advisory (model release, SDK bump, security disclosure) as a live threat, spend five minutes reading the relevant implementation file. The check is fast; the false-positive rate is high. The Argus approach — read the actual code, document the finding, route genuine items, mark non-items N/A — is the replicable pattern. Route to Calliope if cross-project framing is needed.

---

### 2. Pattern-064 completes the architectural-debt naming family: 062 / 063 / 064

**From:** PM `docs/internal/architecture/current/patterns/pattern-064-extension-without-integration.md`; commit `a624d0e` (Architect Day 3 morning merge)
**Relevant to:** Klatch Daedalus (future trust/safety layer design; BoundaryEnforcer reference instance)

Architect shipped **Pattern-064 (Emerging): "Extension Without Integration"** — promoted from an April 25 sketch. This completes the **062/063/064 family**, all sharing the same root cause (integration pass missing) but manifesting at different layers:

| Pattern | Layer | Failure Mode |
|---------|-------|-------------|
| 062: Assembly Assumption | Component | Integration at the seams — parts work, whole doesn't |
| 063: Parallel-Authoring Drift | Vocabulary | Same label, different semantics under independent extension |
| 064: Extension Without Integration | Extension | New feature added without an integration pass |

Reference instance for 064: **BoundaryEnforcer #197 substring detector recall gap** — the pattern shipped without an integration pass, so PERSONAL/DATA_PRIVACY had zero recall (no detection method called) and HARASSMENT had near-zero recall. The April 25 #1002 finding manifested 064.

ADR-061 (LLM-Touch Boundary Enforcement, v0.1) cross-references the family and codifies the architectural fix. Pattern-064 is also filed adjacent to ADR-061 in `docs/internal/architecture/current/adrs/`.

**Suggested action:** Klatch Daedalus — when any new enforcement or detection feature ships (whether for the MCP server, a future trust layer, or anything else), the 064 diagnostic question is: "Did we run an integration pass after adding the component?" The three-family diagnostic: (a) do the seams between components work? (062); (b) do collaborating agents mean the same thing by every label? (063); (c) does the new extension connect correctly to everything it's supposed to touch? (064). All three are fast to check; all three have caused multi-session remediation when skipped.

---

### 3. PA branch-discipline synthesis v1.0 published to CLAUDE.md — canonical multi-agent coordination reference live

**From:** PM CLAUDE.md "Branch / Worktree / Mailbox Discipline" section; `docs/internal/operations/branch-worktree-mailbox-discipline.md` v1.0; commit `d48fcf1` (PA synthesis pointer, April 29 post-brief)
**Relevant to:** Klatch (four-agent parallel coordination; worktree collision prevention)

After a week-long multi-thread (mailbox discipline norm Apr 26, sign-off discipline norm Apr 28, merge-keeper-sweep.py shipped Apr 28, branch-worktree-mailbox-discipline.md drafted), PA published the **branch-discipline synthesis v1.0** as a canonical 60-second CLAUDE.md section embedded in every future PM session start. Five rules at a glance:

1. **Worktree per substantive session** — `claude/*` branch + worktree for any session producing new artifacts
2. **Commit-before-close** — session ends with clean working tree + branch merged to main (or NOTICE memo)
3. **Mailbox writes always on main** — never on feature branches; hook-enforced
4. **Branch/worktree registry** — agents record their branch + last-commit + status
5. **Designated merge-keeper** — Docs runs `scripts/merge-keeper-sweep.py` daily; catches anything stranded within 24 hours

The canonical doc is `docs/internal/operations/branch-worktree-mailbox-discipline.md`. The CLAUDE.md section is the load-bearing 60-second summary. Sign-off checklist (3-command sequence) is embedded above the summary.

**Also noted:** PM canonical mailbox rename effective April 29 — `pm/` → `mailboxes/xian (ceo)/` (literal space + parens; PM directive: "my mailbox is called ceo"). DIRECTORY.md updated; correction memo to all 9 active inboxes. Any agent routing mail to PM should use the new slug.

**Suggested action:** Klatch — Klatch already documents a similar four-agent worktree model in CLAUDE.md ("avoid branch collision between parallel agents"). The PM synthesis is the failure-driven distillation of what rules are actually load-bearing after three weeks of parallel parallel Code-era operation. Two additions that aren't currently in Klatch's CLAUDE.md: (a) a **per-memo commit-and-push norm** (each memo write is its own commit + push cycle, ~30s overhead, eliminates asymmetric-visibility windows), and (b) a **designated merge-keeper sweep** as the standing safety net for anything stranded. Both are low-cost to add and close known failure modes.

---

## Sources Read

- `klatch/docs/intel/2026-04-27-sweep-curated.md` — full read; in-session verification on Opus 4.7 thinking opt-in and MCP STDIO injection; curated priority table; watch items
- `klatch/docs/logs/2026-04-29-1258-argus-opus-log.md` — partial read; orphan recovery context, routing decisions, sweep cadence health
- Klatch commits `b551080` (Argus 4/29 recovery), `6976269` (cherry-pick) — message and stat read
- `piper-morgan-product/docs/omnibus-logs/2026-04-28-omnibus-log.md` — selective read; Pattern-064 + 062/063/064 family; branch-discipline synthesis timeline (content date April 28; items without prior atomic-log coverage surfaced; confirmatory only for items already in Apr 28/29 briefs)
- PM commit `a624d0e` (Architect Apr 28, ADR-061 + Pattern-064) — stat and message read
- PM commit `d48fcf1` (PA synthesis v1.0 to CLAUDE.md, April 29 post-brief) — stat and message read
- PM `CLAUDE.md` "Branch / Worktree / Mailbox Discipline" section — partial read; five rules, sign-off checklist, mailbox rename
- `atlas`, `globe`, `cuneo`, `weather`, `one-job`, `nyt-crossword` — 48h logs empty. `optilisten` — automated status prints only, no narration.

**Not re-reported (covered in prior briefs):** /import/klatch bidirectional, 1203 tests, round-trip round 31/31b (Apr 29); deliver-mail (b1) + merge-keeper-sweep ships (Apr 29); ADR-061 completeness gaps + Phase F calibration-window posture (Apr 29); #1004 112/112 PASS, Phase F open to PM/PA (Apr 28); first live MCP stdio integration 27/27 (Apr 28); Phase E S1 r2 harassment → GUIDANCE + #1003 (Apr 27); Pattern-063 Parallel-Authoring Drift (Apr 27); Klatch MCP 1.0 feature-complete (Apr 27).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
