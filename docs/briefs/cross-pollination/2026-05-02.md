
# Cross-Pollination Brief — May 2, 2026

Klatch's formal UX walkthrough began April 30: Iris and xian created a two-pass working doc (`docs/ux/walkthrough-findings.md`) and captured Surfaces 1 and 2 with 12 specific findings before pausing mid-walkthrough. The sweep also surfaces a missed publication: Ship #040 "The Methodology Audits Itself" was published April 29 on pipermorgan.ai/shipping-news — after the April 29 brief ran and missed in subsequent sweeps.

## Key Insights

### 1. Klatch Iris Session 7: formal walkthrough begins — Surfaces 1-2 documented, 12 findings, 2 cross-cutting patterns

**From:** Klatch `docs/ux/walkthrough-findings.md`; `docs/logs/2026-04-30-0754-iris-opus-log.md`; commit `bd78739` (May 1, 15:21 UTC — after May 1 brief)
**Relevant to:** PM (any product past feature-complete entering a pre-polish or pre-alpha review phase)

Iris and xian ran the first session of a formal two-pass walkthrough of the running Klatch v0.10/1.0-beta app. The working document is structured: Pass 1 (surface skim across 8 surfaces — observable issues at a glance) + Pass 2 (realistic scenario: set up the Shipping News weekly review workflow, capture friction). MAXT round-trip testing planned for after the walkthrough. Session paused after 2 of 8 surfaces; resume planned for Friday afternoon (Surfaces 3-8 + Pass 2 still pending).

**Surface 1 — First-load impression (6 findings):**
- F1.1 Type is small and low-contrast throughout (gray-on-white, small-caps project headers)
- F1.2 Large empty content area with no clear call to action; visual hierarchy doesn't direct the user
- F1.3 Default channel system prompt ("You are a helpful assistant") rendered as a visible header — functional artifact from early development, never revisited; reads as boilerplate
- F1.4 Empty-state copy frames Klatch as a generic chat app ("Start a conversation / Send a message to begin") rather than as a stage for a cast of characters
- F1.5 API key configuration invisible from the UI — no setup flow, no "connect your Anthropic account" (flagged as a 1.0-beta gap, out of scope for the day's review)
- F1.6 "Functional artifacts surviving early development" named as a category; F1.3 is the first instance, others expected

**Surface 2 — Sidebar (6 findings):**
- F2.1 Type legibility carries through the entire sidebar (same problem as F1.1)
- F2.2 Reads as "list of chats" — Slack pattern-match; distinctive Klatch concepts (projects, klatches, entities, @ vs # prefix system) are present but not communicated
- F2.3 Section meaning unclear; project headers in small caps with count + chevron read as decoration, not interactive structure
- F2.4 Project name truncation breaks comprehension mid-word with no expand affordance
- F2.5 "Unassigned" section carries no contextual cue explaining what unassigned means
- F2.6 Footer grab-bag confirmed: dark mode toggle + Entities + Import + "+ New channel" stacked with no design rationale

**2 cross-cutting patterns established early:**
1. Type is small and low-contrast throughout (flagged for a typography/density pass after the walkthrough)
2. Functional artifacts surviving early development — things that work but were never revisited; F1.3 is the anchor instance; watch for others across remaining surfaces

**Note:** Carried-over items from prior sessions (composition gap, import findability/modal framing, visibility gap, sidebar IA, L4/L5 round-trip loss) are pre-populated in the working doc and will not be re-found during the walkthrough — the team distinguished "finding for the first time" from "confirming what we already know."

**Suggested action:** PM — the "functional artifacts surviving early development" pattern is a useful sweep category for any product that's been in active development for months. The question is: "which things are still there because they work, but were never revisited for fit?" Klatch's example is a default system prompt exposed as a UI string; PM analogues might exist in any surface that was configured for convenience and never updated for its user-facing role. A one-time artifact sweep before any user-facing review is low-cost and tends to surface high-signal mismatches.

---

### 2. Ship #040 "The Methodology Audits Itself" published April 29 — not covered in prior briefs

**From:** PM commits `4ed4622d` (Apr 29 13:53 -0700, canonical site), `efbc398d` (Apr 29 18:59 -0700, LinkedIn URL added); Apr 29 omnibus log (content date Apr 29, committed Apr 30)
**Relevant to:** Klatch Calliope (publication tracking; placement in PM's public narrative arc)

PM's weekly Ship newsletter #040 published April 29 on pipermorgan.ai/shipping-news/ under the title "The Methodology Audits Itself." LinkedIn cross-post confirmed same day. URL: `pipermorgan.ai/shipping-news/weekly-ship-040-the-methodology-audits-itself`.

Why not in prior briefs: published at 20:53 UTC April 29 — after the April 29 brief ran at 12:00 UTC. The April 30 and May 1 briefs did not scan the calendar commits; the May 1 brief's publication focus was on "The Floor Comes Alive" (Medium, Apr 30). This is the first time Ship #040 appears in the brief record.

PM's current public output channels: weekly Ships at pipermorgan.ai/shipping-news/ + longer narrative posts on Medium (Building Piper Morgan series). Published record to date: Ship #040 "The Methodology Audits Itself" (Apr 29); "The Floor Comes Alive" (Apr 30, Medium); "Four Roles, Ninety Minutes" (Apr 22, Medium); "Sibling Intelligence" (Apr 19, pipermorgan.ai). Ship #041 solicitation memo was distributed to the leadership cohort April 30; window closes shortly.

**Suggested action:** Klatch Calliope — note for the narrative record: PM has established a dual-channel publication rhythm (weekly newsletters + longer narrative arcs). The brief archive is the canonical internal record; publication events noted here help agents place public-facing content in the project timeline when building cross-references or planning analogous Klatch publications.

---

## Sources Read

- `klatch/docs/ux/walkthrough-findings.md` — full read; two-pass structure, Surfaces 1-2 findings, cross-cutting patterns, carried-over items
- `klatch/docs/logs/2026-04-30-0754-iris-opus-log.md` — commit `bd78739` message and stat read; partial content from commit diff
- `klatch/docs/COORDINATION.md` — change diff from `bd78739`; Iris status and resume plan
- PM commits `4ed4622d` + `efbc398d` (Ship #040 calendar) — message and stat read
- `piper-morgan-product/docs/omnibus-logs/2026-04-29-omnibus-log.md` — partial read; Ship #040 publication confirmation + LinkedIn syndication; two recovery incidents (confirmatory only — Apr 29 events already reported; runtime behavior changes not previously surfaced but CONFIRMATORY of branch-discipline synthesis v1.0 reported Apr 30)
- `weather`, `nyt-crossword` — 48h logs non-empty (brief delivery + automated status prints only); no narrated insights; not listed as sources_checked
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped

**Not re-reported (covered in prior briefs):** Phase F activation + ENABLE_ETHICS_ENFORCEMENT=true + #992 closed + alpha catch-22 (May 1); Iris Session 6 composition gap + transport-fidelity UX settled (May 1); The Floor Comes Alive published (May 1); verify-before-assuming methodology + Pattern-064 (Apr 30); branch-discipline synthesis v1.0 (Apr 30); /import/klatch bidirectional 1203 tests (Apr 29); ADR-061 completeness gaps (Apr 29).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
