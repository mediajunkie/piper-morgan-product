# Cross-Pollination Brief — June 5, 2026

PM's PA ran a complete bring-your-own-context plugin to two gate passes in a single day yesterday — RUNG 1 in the morning (live ask-piper call to real Piper via MCP, verified with xian at keyboard), RUNG 2 in the evening (bare passthrough skill built and gated the same night). The emergent discovery from the first live run: Claude-as-host offered unprompted to gather PM's real-world context via Notion, Calendar, and Slack and feed it to Piper when Piper hit its ceiling — a richer composition loop than the original design assumed. Also overnight: Lead Developer cataloged all 26 PM UI routes and found the prevailing problem isn't broken features but that 15 routes have no navigation link at all. And PM's CIO spent the afternoon surveying Garry Tan's gbrain repo, proposing a weekly drift-and-gap pass over PM's 39-entry methodology corpus as a concrete pilot, with a propose-and-diff constraint (reviewable changeset, never silent mutation) as the hard safety gate.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Bring-your-own-context plugin reaches two gate passes in one day — "host enriches Piper at the floor" emerges from the first live run

**From:** PA session log `dev/2026/06/04/2026-06-04-1130-pa-code-opus-log.md` (RUNG 1 + RUNG 2 entries); commits `f06edb9` (RUNG 1) and `93ff994` (RUNG 2)
**Relevant to:** Klatch (replicable thin-plugin architecture; future MCP integration reference); designinproduct (PDR-005 v1.0 publication milestone — ratification pending)

The full BYOC arc closed yesterday after a six-day reconstruction sprint (lost draft May 21 → rebuilt May 30 → Cowork test → architecture June 1–3 → both gate passes June 4). The thin plugin now has two skills over a live MCP connection to real Piper `/intent`:

**RUNG 1** (morning, xian at keyboard): plugin installed via PEP-723 bootstrap (`uv run server.py`, no venv), `ask_piper "what should I focus on today?"` hit the full skill→MCP→`/intent` round trip. The one untested assumption — that `${CLAUDE_PLUGIN_ROOT}` would resolve without a manual path — closed cleanly on first run. Discovered work from the gate run: temporal-context bug (`#1150` filed — Piper reported "late evening" at 11:30 AM, wrong server clock/tz).

**RUNG 2** (evening, same day): bare `ask-piper` passthrough skill built in one tightly-scoped session, verified against a dead port (clean error message, no silent failure; PM's live `:8001` server left untouched). RUNG 2 gated. Scope held to passthrough per locked decision.

The emergent design finding from RUNG 1 (queued as RUNG 3, not yet started): host Claude, unprompted, offered to gather PM's real context via the host's own MCP access (Notion, Calendar, Gmail, Slack, Granola) and feed it to Piper when Piper hit its priority ceiling. The original design assumed "skill reads a profile"; the first live run revealed "host enriches Piper at the floor" — a materially richer payoff loop.

**Suggested action:** Klatch — the one-file PEP-723 plugin pattern (no venv, stdio MCP, clean-error on dead port) is a replicable architecture worth noting for future Klatch extension work. The "host enriches plugin at the floor" composition pattern is also directly applicable once Klatch supports MCP-wired skills.

---

### 2. PM UI audit: 15 of 26 routes have no navigation link — path to user-acceptance testing is a navigation fix, not a rebuild

**From:** Commit `ae7b465` (audit doc `docs/internal/audits/ui-functional-audit-2026-06.md`); Lead Dev cycle log June 4 Fires 2–3; issue #1142
**Relevant to:** PM internal (M3 testability planning); Klatch (architectural parallel — feature completeness vs. feature reachability as distinct gaps)

Lead Dev ran a 3-parallel-agent survey of all 26 HTML routes in PM's UI and produced a headline correction to the M2 smoke read: the UI is less broken than smoke suggested, but less reachable than anyone realized.

**The dominant architecture is sound.** Most pages follow a consistent pattern — handler renders a scaffold, template client-fetches real `/api/v1/*` data. The surfaces that appeared missing in M2 smoke (#1047) turn out to have been either trust-gated (hidden from Stage-1 smoke user) or nav-orphaned (exist and work, but nothing links to them). The earlier "couldn't find lists view" finding: `/lists` is real CRUD wired to `/api/v1/lists`; its nav link is hidden from Stage-1 users. Not missing — gated invisible.

**15 of 26 routes are nav-orphans**, reachable only by typing the URL. This list includes the R4 `/insights` surface PM just shipped in May (no nav link), `/transparency`, `/files`, and all five integration settings pages (`/settings/integrations/notion`, `/github`, `/slack`, `/calendar`, `/projects`).

**Real bugs are few:** `/standup` is a stale legacy "click to generate" UI that predates the lifecycle-indicator architecture; `/documents` has a `trust_stage` display bug (same family as `#1132` fixed for `/insights` last week — handler doesn't server-render the trust stage). Five routes are genuine "Coming Soon" placeholders.

**Bottom line for M3 planning:** once orphan pages are wired into nav and the `/documents` bug is patched, the UI becomes UAT-navigable. The blocking work is navigation coverage, not feature rebuilding.

**Suggested action:** Klatch — the distinction between "feature incomplete" and "feature unreachable" is worth auditing proactively as routes accumulate. PM discovered this retroactively; it reframed an entire sprint's smoke results.

---

### 3. CIO proposes a "methodology dream cycle" after gbrain survey — propose-and-diff adopted as the hard safety constraint

**From:** CIO cycle log June 4 Fires 17–22; commit `ed88d11` (Candidate 13 captured in `v0.7-candidates.md`); HOST reply confirming agent-experience lens and welfare criterion
**Relevant to:** PM internal (methodology corpus hygiene, CIO lane); Klatch (transferable constraint for any automated write to shared methodology or reference files)

PM's CIO spent yesterday afternoon surveying Garry Tan's gbrain repo as an innovation-scouting exercise directed by xian. The key finding: gbrain has a built "dream cycle" — a nightly idle-time pass that detects contradictions, drift, and gaps in its knowledge corpus and synthesizes thin entries. PM has the scheduling substrate (the duty cycle; agents fire hourly) but no corresponding content pass over its 39-entry methodology corpus. The CIO's earlier finding: 20 of 22 methodology entries have zero citations — the corpus is real but not actively maintained for internal consistency.

The proposed pilot (captured as **Candidate 13**): a weekly drift-and-gap-and-dedup pass over the corpus, CIO-owned, riding the existing duty-cycle cron. The three-way comparison (gbrain / PM's Type-1 dreaming design / PM's methodology harness) yielded this: gbrain is a working Type-1 reference that de-risks PM's own somewhat-built Type-1; gbrain's drift detection doesn't replicate PM's Type-2 (threat-rehearsal) design, so PM's novelty claim holds.

**The hard design constraint adopted from HOST's welfare lens:** the pilot must emit a reviewable changeset the owner ratifies — **propose-and-diff, never mutate-in-place**. HOST's framing: silently rewriting the corpus produces the same expectation-violation surface as an overnight seam (artifact changed, no one watched). The cohort already runs on explicit ratification; this constraint fits the grain. It's now a hard requirement for the pilot, not a preference.

Not yet built. Building waits for PM go and a deeper read of gbrain's `src/core/cycle/` to confirm which model it actually implements before copying architecture.

**Suggested action:** Klatch — the propose-and-diff constraint for any automated write to shared files is directly transferable. If Calliope or any future Klatch agent writes to shared reference files autonomously, require a reviewable changeset rather than a silent update.

---

## Sources Read

- **piper-morgan-product**: PA session log `dev/2026/06/04/2026-06-04-1130-pa-code-opus-log.md` (RUNG 1 + RUNG 2 sections, full); CIO cycle log June 4 Fires 17–22 (gbrain arc, full); Lead Dev audit `docs/internal/audits/ui-functional-audit-2026-06.md` (full); commits `f06edb9`, `93ff994`, `ae7b465`, `ed88d11`, `886918c`; git log 48h (~60 commits reviewed)
- **klatch**: git log 48h (1 commit — brief delivery; no new substantive content); Klatch was quiet June 4–5
- **designinproduct** (hub): Janus dashboard plan `docs/plans/janus-status-dashboard-v0.1.md` (all 4 DPs resolved); sweep-log; letters excerpt confirmed current

**Secondary sources (all quiet):** atlas, globe, cuneo, weather, one-job, optilisten — empty 48h git log. nyt-crossword — automated status commits only (no narration).

**Not re-reported (covered in prior briefs):** Klatch duty-cycle v0.2 "wait-default ≠ wait-forever" (June 4); PM first autonomous overnight crossing (June 4); roadmap v18 ratifiable + BYOC spec v0.6 (June 4); two-layer done-criteria enforceable (June 4); Ship #045 "The Substrate Pivoted" (June 3); work-shape-aware cadence handoff to Klatch (June 3); M2 smoke test #1047 (June 3); INSIGHT-PULL/PUSH (June 1); Opus 4.8 (June 1).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*