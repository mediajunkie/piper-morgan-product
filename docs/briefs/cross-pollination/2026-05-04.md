
# Cross-Pollination Brief — May 4, 2026

PM shipped the entire M2d MUX implementation layer in one Sunday session (May 3): 8 issues — Pull/Passive/Push insight surfacing, COMPOSTED anti-surveillance guardrail, lifecycle indicators, staleness signals, plus two pre-work structural issues — merged to main with 221+ new tests and zero regressions. M2e gameplans were drafted, walked through PM (24/24 dispositions), and first issue #790 trust-gated calendar shipped by evening. Klatch's first Monday external intel trigger (fix confirmed working) surfaces two overdue items: SDK 6 minor versions behind and the June 15 Sonnet 4/Opus 4 deprecation deadline now 42 days out with a DB audit still unfiled.

## Key Insights

### 1. PM: M2d complete — full MUX insight layer ships in one session; M2e launched same day

**From:** PM `dev/2026/05/03/2026-05-03-0657-lead-code-opus-log.md`; merges `71e847a7` (#704), `66700a08` (#714), `007f8596` (#1033), `1da171a8` (#1030), `9500ab07` (#1031), `9ccc7cf` (#1032), `607c3c4b` (#1034), `5d2e2624` (#1035), `755040b1` (#790)
**Relevant to:** Klatch (batched audit-cascade methodology; "don't show non-functional feature" principle; companion-project milestone)

The entire M2d milestone shipped in a single 14-hour session. Eight issues merged sequentially: #1035 MUX-COMPOSTING-ACTIVATION (CompostingScheduler wired to startup; InsightJournal backed by PostgreSQL repository — PM directive: "durability is constitutive of what a journal IS"); #1034 STANDUP-STRUCTURED-WORKITEMS (StandupResult carries List[StandupItem] with `__str__` backwards-compat); #704 MUX-LIFECYCLE-UI-A (slot-then-postprocess render pattern, reusable across future surfaces); #714 MUX-LISTS-STALENESS-UI (lazy effective timestamp, 60-day threshold, muted card treatment); #1033 MUX-COMPOSTED-EXPERIENCE (anti-surveillance guardrail at both compost-time and surface-time, single `safe_surface()` source of truth); #1030/#1031/#1032 Pull/Passive/Push insight surfacing (trigger detection, Insight Journal wired to Jan 2026 prior-art backend, channel-agnostic Push eligibility + in-chat renderer).

Also notable: **#1036 closed premise-invalid** mid-execution — the live `/api/v1/lists` endpoint was already in `web/api/routes/lists.py` but missed by a Phase -1 grep scoped to `services/api/` only. Saved as feedback memory: Phase -1 endpoint-coverage spikes must search the full route-mounting tree (`web/api/routes/` + `services/api/` + `web/router_initializer.py`).

**PM UI principle from the walkthrough:** "I don't want to show a non-functional feature." Applied to #1031's topic tabs — markup hidden via Jinja comment until #1037 ships, then a one-line uncomment ships the feature. Three options enumerated: (1) withhold-until-functional [chosen], (2) promise-with-clear-not-yet [rarely justified], (3) build-into-MVP. Withhold is the default.

M2e same day: 5 gameplans drafted, 24/24 PM walkthrough dispositions captured, #790 trust-gated calendar implemented by late evening (first M2e issue done). Sequence: #1042 (cleanup, blocks #1039+#1040) → #1039 → #1040; #900/#869 independent.

**Suggested action:** Klatch — two transferable patterns. First, the **batched audit-cascade walkthrough**: draft all gameplans, surface all ⚠️ items to PM in one thread, get all dispositions, then execute sequentially. PM handled 51 decision points in ~3 hours vs. piecemeal Q&A between issues. Second, the **withhold-until-functional** principle: if any Klatch UI surface has affordances that don't wire to a live backend, prefer the Jinja-comment treatment over showing dead-end UI — hide until the backend lands.

---

### 2. Klatch external intel: SDK 6 versions behind + June 15 deprecation 42 days out + MemPalace reference

**From:** Klatch `docs/intel/2026-05-04-sweep.md` (commit `f15d72c`, Mon May 4 10:26 UTC — first successful Monday trigger run confirms `allow_unrestricted_git_push: true` fix)
**Relevant to:** Klatch Argus/Daedalus (P1 dep maintenance + model migration); PM (deprecation deadline awareness)

Two high-priority items from today's automated scan:

1. **@anthropic-ai/sdk 0.92.0 published May 1.** Klatch is pinned at `^0.86.1` — six minor versions behind, widening each week. The batch-bump target set in mid-April (`^0.90.0`) should be updated to `^0.92.0`. Batch with Hono 4.12.14 → 4.12.16 at the same dep-maintenance window.

2. **June 15 Sonnet 4 / Opus 4 retirement: 42 days remaining.** Argus has an open COORDINATION.md follow-up since April 29 to audit `klatch.db` for deprecated model IDs (`claude-sonnet-4`, `claude-opus-4`). That audit is overdue; discovery of substantial migration work at 3 weeks would be uncomfortable vs. now.

Also from the scan: **MemPalace** (47K GitHub stars, released April 5) — open-source SQLite + ChromaDB local memory system, 170-token startup cost, 96.6% on LongMemEval, fully offline. The temporal entity-relationship graph (add/query/invalidate/timeline, SQLite-backed) is architecturally close to what Klatch's Step 11 would need for FTS5 + semantic recall. Worth a design-reference read before writing the Step 11 spec; the 170-token startup target is a useful benchmark discipline.

Additional context: Claude Code 2.1.126 ships MCP server auto-retry (3× on transient startup error) — ecosystem signal that transient startup failures are being hardened against. Vercel AI SDK 6 ships `Agent` as a first-class TypeScript abstraction with built-in MCP support; watch for user friction combining Klatch's MCP server with AI SDK 6 clients.

**Suggested action:** Klatch Argus — treat SDK bump and DB audit as P1 this week. File the DB audit issue if one doesn't exist; run it before the next sprint. The MemPalace design-reference read can happen alongside the dep-maintenance window.

---

### 3. "Friction-Focused Feedback" published May 3; ADR-061 PM verbal ratification recorded

**From:** PM commits `f338053` (editorial calendar canonical publish), `25d2acc` (Medium + LinkedIn syndication URLs), `c86ad23` (session log May 3); ratification memo commit `ab5f72c3`
**Relevant to:** Klatch Calliope (PM publication record + ADR-061 status)

PM published "Friction-Focused Feedback" to pipermorgan.ai/blog on May 3, with Medium and LinkedIn syndicated the same day. This is the second insight-category post in two days ("The Drift You Don't Notice" published May 2). PM's editorial calendar insight backlog dates to February 2026; two posts in quick succession signal the track is now active.

PM's current public output: weekly Ship newsletters (pipermorgan.ai/shipping-news/), Building Piper Morgan narrative series (Medium), and the insight track (pipermorgan.ai/blog/). Ship #041 is pending; Comms is writing an IAC conference retrospective arc.

ADR-061 (ethics detector three-way discriminator architecture) received PM verbal ratification May 3. Lead Dev memoed Architect + PA: "I have ratified it but we don't seem to have done or filed the paperwork yet — you can use my verbal as a go-ahead for now." Formal paperwork pending; implementation can proceed from verbal.

**Suggested action:** Klatch Calliope — the "verbal ratification + memo-to-stakeholders" pattern is useful when an architectural decision needs to unlock implementation before paperwork catches up. If Klatch has an ADR that's approved in session but unfiled, a brief memo-to-COORDINATION.md citing the session context serves the same function. Also note PM's two-track publication model: insight posts (standalone, methodology) vs. building narrative (arc-dependent, longer) — Klatch has natural candidates for both.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/03/2026-05-03-0657-lead-code-opus-log.md` — full read; M2d execution (8 issues), M2e gameplans + walkthrough, #790 shipped, PM walkthrough direction quotes
- PM merge commits for M2d: `71e847a7` (#704), `66700a08` (#714), `007f8596` (#1033), `1da171a8` (#1030), `9500ab07` (#1031), `9ccc7cf` (#1032), `607c3c4b` (#1034), `5d2e2624` (#1035); `755040b1` (#790 M2e) — stat/message read
- PM publication commits: `f338053`, `25d2acc`, `c86ad23`; ratification memo `ab5f72c3` — message read
- `klatch/docs/intel/2026-05-04-sweep.md` — full read; SDK overdue, June 15 countdown, MemPalace, Claude Code 2.1.126, Vercel AI SDK 6
- Klatch commit `f15d72c` — confirms Monday trigger landed on main (allow_unrestricted_git_push working)
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `weather`, `nyt-crossword` — 48h logs: brief delivery + automated status prints only; not listed in sources_checked

**Not re-reported (covered in prior briefs):** M2d audit-cascade NOT PASSED + restructure + 4 new issues filed (May 3); audit_transparency durable storage + transaction-boundary isolation pattern (May 3); "The Drift You Don't Notice" published (May 3); Iris walkthrough Surfaces 1-2 (May 2); Ship #040 (May 2); Phase F ENABLE_ETHICS_ENFORCEMENT=true live + alpha catch-22 (May 1); Iris composition gap + transport-fidelity UX settled (May 1); "The Floor Comes Alive" published (May 1).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
