---
type: proposal
title: "The cross-pollination corpus: digest, index, browse, verify, synthesize — proposal"
author: spec (Special Assignments), cloud session, Fable 5.1
date: 2026-10-07
version: v0.3 (v0.2 + the eight §7 decisions resolved with PM on 2026-10-07; ceiling raised to $75; see §11)
status: PM-APPROVED to start P0 (2026-10-07). Nothing is built yet. Nothing in the hub changes without Janus's review; nothing goes public without PM.
evidence: dev/2026/10/07/spec-xpoll/ (X1 extraction + provenance pilot; X2 prior-work and practice-gap map; audit-proposal-v0.1.md)
---

# The cross-pollination corpus: a proposal

## 0. The ask

Research and propose a plan for reviewing the full cross-pollination newsletter corpus, then classifying,
indexing, and providing a way to browse, filter, sort and otherwise interact with it. Blue-sky extensions are
welcome: synthesis, derived work, corpus refinement, correcting past claims, and reporting on gaps between
**reported practice, actual practice, and recommended practice**. Goals stay speculative and generative.
Scope is the full hub archive. The result lives in `/internal/`, coordinated with Janus. Ceiling: $50.

## 1. The corpus, measured

Source: `metrics/xpoll_extract.py` over `designinproduct/src/internal/briefs/` at `39608c0`. Layer: static
markdown parse plus git queries against the Piper Morgan repo. The independent auditor re-derived the first
four rows with its own commands; all matched.

| Fact | Value |
|---|---|
| Briefs | **234** files (233 `*-brief.md` + `2026-04-11-brief-rev2`), 2025-06-01 → 2026-10-07; 223 substantive, 11 nominal; about 271k words |
| Cadence | Daily since 2026-03 (30–31 a month); the 2025 entries are one a month, retrospective in origin |
| Key Insights | **592** (594 `###` headings; 2 sit under a Corrections section). Since 2026-07-03 headings are unnumbered: 105 insights (17.7%) that a numbered-only parser would miss |
| Per brief | All-time mean 2.53, mode 2. **Since the 06-28 brief-worthiness bar (n=101): 85% carry ≤2, one brief reaches 4.** The bar worked |
| Source mix | Piper Morgan 60% · Klatch 31% · Mediajunkie 7% · DinP 5% · others ≤2% (keyword attribution on the From line) |
| Evidence cited | commit SHA 36% · repo path 68% · issue ref 31% · **suggested action 92%** · stated audience 94% |
| Provenance (pilot) | PM-attributed SHAs resolve in PM's git **216 of 220 (98.2%)**. This is the existence-and-date layer only: the commit exists and predates the brief. It does not check that the commit supports the claim. Coverage: 123 of 354 PM insights cite a SHA. Path check: n=20 insights (44 paths), 75% touched by the brief date, ±13pp; some misses are cross-repo paths |
| Letters to xian | 8 distinct letters, 70 appearances (re-featured), all 8 answered |
| Corrections | 4 items in 3 briefs (09-08, 09-09, 10-05) through the pending-corrections flow |
| Unpublished slice | 4 + 4 per-project briefs (2026-03-19→22) in `internal/cross-pollination/briefs/`, not in the published archive |
| Rendering gaps | rev2 is outside the `briefs` collection glob; nominal briefs render a fixed sentence even when they carry Background items *(inferred; site not built here)* |
| **Confidentiality** | **10 of 234 published briefs name OpenLaws** (2026-04-05, 04-09, 04-11 ×2, 04-14, 04-15, 04-16, 04-25, 07-26, 08-10), against `sweep-prompt.md:46` ("Do NOT read or reference OpenLaws, Kind Systems…"). `/internal/` is on the public site, protected only by `noindex` |

**Prior work this builds on** (X2 §1): Janus's 2026-06-28 history audit (headline ~48 REMOVE / ~57 DEMOTE;
itemized 18 / 37; **49 of ~55 itemized flags executed**, 17 on 06-28 and 32 on 07-08); the 2026-03-23 cadence
recommendations (partly adopted; the 06-28 bar superseded its tiers); the glossary (last updated 04-10); the
pending-corrections flow (working since 09-08); the cross-project harvest architecture (PM
`docs/internal/design/cross-project-harvest-architecture-2026-08-29.md`, Tier-2 destination `/internal/patterns/`);
and the Practice scaffold. About **100 briefs since 06-28 have not been audited** by any method.

## 2. Stated vs actual vs recommended practice (first pass; Layer E makes it a standing report)

"Recommended" is Spec's suggestion. Janus decides anything about the hub.

| Practice | Stated | Actual (layer · denominator) | Recommended |
|---|---|---|---|
| Readers | 7 (`publishing-flow.md`; delivery prompt; health check expects `7/7`) | 11 reader repos per `delivery-log.md`, 169 of 170 rows "11/11". (`projects.json`'s 4 and the sweep's 13 are **sources**, a different list) | One registry that distinguishes sources from readers; health check reads it |
| Insights per window | "0–2 typical; zero common; four an extremely unlikely maximum" (post-06-28 rule) | Post-bar n=101: 0 → 1, 1 → 20, 2 → 65, 3 → 14, 4 → 1. **85% ≤2.** "Zero is common" is the only part that doesn't hold (1 of 101) | Keep the bar; reword "zero is common" |
| Timing | Sweep "~12:00 UTC"; `sweep-prompt.md` says "7 AM PT (12:00 UTC)" | 12:xx on 131 of 197 logged runs; 11:xx on 32 | Fix the PT conversion (12:00 UTC is 05:00 PT in summer) |
| Cadence recs (03-23) | "to be applied to daily-sweep.md" | Partly adopted in spirit; the bar replaced the tiers; no cadence log or Temporal Note | Mark the doc superseded, or adopt the two remaining pieces (Layer E5) |
| Glossary | Mandatory before defining acronyms | Zero references in the live sweep prompt; stale since 04-10 | Either wire it into the prompt or retire the rule |
| Readers act on briefs | "Agents read `current.md` at session start" | 167 of 1,295 PM session logs (Jul→Oct) mention the brief; 125 file it as "loaded but not referenced"; 1 of 15 sampled acted on it; real use by CIO, Exec, Arch | Measure it (Layer D) before changing it |
| Audit coverage | Bar applies to all briefs | Itemized flags were executed (~89%); briefs after 06-28 (~100) not audited | Audit-forward (E2) with Janus |
| Confidentiality | OpenLaws/Kind never surfaced | 10 published briefs name OpenLaws | **Screen before indexing** (§4 Layer 0) |
| Brief delivery | "Copy one file to seven destinations, commit, push, write a receipt" (delivery prompt) | A Sonnet 4.6 agent session, daily, now 11 readers; completion median 9 min after the 13:00 UTC cron over 170 runs, 14 min over the last 30 (6–28); 9 recent rows record MCP fallbacks after git 403s. Token usage unobservable from this account (the trigger is on the DinP account) | Measure one run (`list_events kinds=["result"]` on a delivery session from the owning account). Candidate for a zero-token workflow; the JSON feed (Layer A) lets readers pull instead of being pushed to |
| Hub browsing | Archive | Month pages only; no search, filters, tags, insight anchors, related links, or feed (confirmed against templates) | Layers A and C |

## 3. Design constraints (from Janus's own documents; confirm with Janus)

1. **Briefs are never retro-edited**; corrections are forward-only. Classifications and verification results are
   **sidecar metadata**, generated, never hand-maintained.
2. **`/internal/patterns/` is the sanctioned Tier-2 promotion path**, with its own bar and a nomination-driven
   trigger (harvest §4.3). This proposal makes the corpus legible so nomination is possible; it does not promote
   anything itself. Dedup threads are **nomination candidates**, admission stays Janus's.
3. **URL stability**: brief URLs are canonical in 150+ files. New surfaces are additive. Everything stays `noindex`.
4. **Confidentiality gates** apply to every derived output, and indexing raises the stakes (§4 Layer 0).
5. **Ownership**: Janus curates the hub; **CIO owns PM's session-start hook** (anything that changes what agents
   load at start is a proposal to CIO); the live sweep prompt and registries are Janus's (E5, E6 are proposals
   *to* Janus, not deliverables).
6. The corpus grows about 2 insights a day; parsing runs at build. **Classification cannot run at build** (no LLM
   key in the Pages deploy), so new insights need a named owner and cadence (§7 decision c).

## 4. The proposal: Layer 0 plus five layers, each useful alone

### Layer 0 — Confidentiality screen (before anything is indexed)
- Scan the corpus for the confidential-content list (OpenLaws, Kind, day-job terms Janus supplies). Report hits
  to Janus. The index **excludes or redacts** flagged insights until Janus disposes of them. The same screen runs
  on every derived page. Without this, a public JSON index and search make the existing breach one query away.

### Layer A — Data: a canonical structured index
- `insights.jsonl` / `briefs.jsonl` / `letters.jsonl` / `corrections.jsonl`, generated by a script that lives in
  designinproduct and runs at build. Stable ids `YYYY-MM-DD#N`. Fields as in X1 plus sidecars from B and D.
- **The build fails on any unparsed section** rather than printing a coverage number and moving on (the 07-03
  heading drift shows a printed denominator isn't enough).
- Letters indexed as 8 records, not 70 appearances.
- The 8 pre-unification briefs are folded in as a flagged era, or their exclusion is documented.
- `/internal/insights.json` is published **only if Layer 0 passes and PM decides the JSON is public** (§7 a).

### Layer B — Classification: pre-registered taxonomy, two classifiers, an adjudicator, a sized gold set
- **Taxonomy** (PM and Janus edit before anything runs). Proposed: *Type* (pattern · technique ·
  decision-with-reasoning · discovery · incident-lesson · anti-pattern · tooling · status/news); **Topic: 6
  labels, not 12** (agent coordination · prompt/context architecture · verification & evidence · engineering
  discipline [git, CI, testing, credentials] · product/UX · publishing & process meta), multi-label;
  *Transferability* against the bar (yes / weak / no); *Status* (live · superseded-by · corrected-by ·
  promoted-to-patterns · unknown); *Audience fit*.
- **Gold set: 100 items**, stratified by source project and year, **Janus pre-labels, PM confirms** (about 90
  minutes between them). Six topics × 100 items keeps every label above ~10 positives.
- **Agreement**: per-label κ (or Krippendorff's α) for multi-label topics, plain κ for single-label fields.
  Two Sonnet classifiers share failure modes, so agreement measures consistency; **accuracy comes from the gold
  set**, and is reported per label.
- Batched calls (10–20 insights per call, cached prompt). Output is sidecar JSON only.

### Layer C — Interface: browse, filter, search, link
- `/internal/insights/`: filterable list (project, topic, type, date range, has-evidence, has-action, status),
  each insight with a permalink anchor into its brief. **Keyboard-operable filters, WCAG AA.**
- Per-brief additions: anchors per insight, "related" and "corrected-by" links, previous/next.
- **Search**: Pagefind, static, scoped with `data-pagefind-body` to `/internal/`, added as a post-build step in
  `deploy.yml`. Its index is public too, so it runs after Layer 0.
- **A prototype ships first as an artifact** (static HTML over the JSON) so PM and Janus can click before any
  site change. The site change is a PR Janus reviews.

### Layer D — Verification and correction
- **Provenance** for every cited SHA, path, issue and ADR, with a per-insight status (verified-exists /
  unverifiable here / not found). Stated as existence-and-date checks, not claim checks. Klatch and the other
  reader repos become checkable only if PM attaches them read-only (§7 b).
- **"What became of it"**, re-scoped per the audit: the denominator is the **142 insights from other projects
  aimed at Piper Morgan that carry a suggested action**, of which **116 have 60 days of history** to look in
  (the rest are censored and reported as such). For each, look for evidence the action was taken in PM's
  commits, issues, CLAUDE.md, skills. **Pilot on 40 first**; report the hit rate with its denominator. PM's own
  insights are excluded from this measure because finding PM's work in PM's git proves nothing.
- **Corrections back-links**: the index marks the affected insight "corrected by <date>".
- **Lineage threads**: cluster near-duplicates into threads; the repeated-lesson count is itself a finding.
  Threads are nomination candidates for `/internal/patterns/`, not a corpus of their own.

### Layer E — Synthesis and derived work (a menu, ranked; not all funded)
1. **Practice-drift report** as a standing `/internal/` page: §2, regenerated, with "last checked".
2. **Audit-forward**: the 06-28 method over the ~100 unaudited briefs, with Janus, producing dispositions, not edits.
3. **Field guide**: threads distilled, each with its strongest-evidence instance and outcome, **offered to Janus
   as nominations** for `/internal/patterns/` and the Practice page.
4. **Agents as subscribers**: a role reads only insights tagged for its lane, from the JSON, with a cursor.
   A proposal to CIO (session-start hook owner), with the assignment-1 finding behind it: every role loads
   `current.md` at start today.
5. **Temporal Note / knowledge-gap detector** (the 03-23 lead): a proposal to Janus for the sweep prompt.
6. **Registry reconciliation** (sources vs readers): a proposal to Janus.

## 5. Phases, cost, checkpoints (ceiling $75, raised from $50 on 2026-10-07)

Prices assumed: Sonnet $3/$15 per MTok, Opus $5/$25. Estimates, not measurements.

| Phase | Work | Tier | Est. |
|---|---|---|---|
| P0 | Layer 0 screen; taxonomy freeze; gold set (Janus pre-labels, PM confirms); Janus review of this proposal | Spec + humans | $3 |
| P1 | Harden extraction; fail-on-unparsed; pre-unification briefs; Letters as 8 records | Sonnet | $2 |
| P2 | Classification: 592 × 2 Sonnet, batched and cached; Opus adjudication of disagreements; gold-set accuracy report | Sonnet ×2, Opus | $12 (plus $4 reserved for one rerun) |
| P3 | Prototype interface (artifact over JSON); then an Eleventy + Pagefind PR for Janus | Sonnet build, Spec review | $8 |
| P4 | Full provenance; "what became of it" **pilot on 40**; corrections back-links; dedup threads | Sonnet + scripts | $7 |
| P5 | Synthesis: practice-drift page (draft to Janus first); audit-forward dispositions over the ~100 unaudited briefs (E2, rides on the P2 read); monthly drift-check script; 3 sample threads as nominations; subscriber-feed spec for CIO | Opus | $9 |
| P6 | Independent verification (re-derive 3 numbers; refute top findings); handoff memo to Janus | Opus | $3 |
| — | Spec's own orchestration (not previously budgeted) | Fable | $4 |
| | **Total** | | **≈ $52 of $75** |

About $23 of headroom is held in reserve, not pre-spent; E3–E6 stay proposals regardless of headroom because each changes something another agent owns. **Cut if needed:** P4's dedup threads drop to a sample. Checkpoints: PM reads the usage page at the end of P2 (~$21 incl. research) and before P5
(~$36). Research so far: two Sonnet agents and one Opus auditor, about 500k tokens, roughly $4–5.

## 6. Verification discipline
- Taxonomy and thresholds written down **before** classification runs; later changes logged.
- Gold set before the full run; accuracy per label; agreement per label; contested items shown as contested.
- Every number carries its denominator and layer; the build fails rather than under-reports.
- An independent verifier re-derives headline figures with its own scripts and tries to refute the top findings.
- **Nothing ships to the hub without Janus**; nothing public without PM; Layer 0 before any index.

## 7. Decisions — resolved with PM, 2026-10-07 (one at a time, async)
| | Decision | Resolution | Mechanics agreed |
|---|---|---|---|
| a | Confidentiality and publication | **a1** — screen (Layer 0), then publish `insights.json` + search under `/internal/`, same noindex posture as the briefs | Layer 0 runs first; PM sees the hit list before anything publishes; Janus supplies the confidential-term list |
| b | Attach Klatch read-only | **b1** — Klatch only (public repo; cloned read-only, 2,921 commits). Other reader repos stay "unverifiable here" with the denominator stated | Existence/date checks only; no Klatch content enters any output |
| c | Ongoing classification owner | **c1 + a periodic sweeping review** (PM: "one day at a time… miss the forest for the trees") | Sweep-emitted labels (proposal to Janus). Monthly mechanical drift check (re-score 20 gold items, label-distribution shift, unlabelled rows; runnable by any agent). Quarterly curatorial pass by Janus = the standing form of E2; stretches to twice-yearly if it keeps finding nothing |
| d | Topic count | **d1** — 6 topics + a free-text secondary tag per insight | Starting cut: agent coordination & process · verification & testing · tooling & infrastructure · documentation & knowledge · product & user-facing · governance & security. Janus and PM adjust before freeze |
| e | "What became of it" | **e1** — pilot on 40 of the 116 | Three rates reported (acted on · no trace · can't tell), never one adoption score; PM spot-checks 5 verdicts before any extension to 116 |
| f | Fund E1 + E2 | **f1** — both funded (~$6); E3–E6 remain proposals to Janus/CIO | Drift page goes to Janus as a draft first; rows Janus marks "deliberate" close as not-drift |
| g | Gold-set labelling | **g1** — Janus pre-labels 100, PM confirms | One markdown table in the hub repo (id · first line · proposed topic · PM mark). PM-corrected rows weight double in the accuracy report; "could be either" rows are dropped |
| h | The 8 early per-project briefs | **h1** — indexed as a flagged draft era, each linked `superseded_by` the same-date published brief (PM: "if the drafts have nonzero value" — they do: several insights exist only in the drafts) | Default denominators exclude drafts ("234 published + 8 drafts, drafts excluded"); the P4 dedup treats a draft insight and its published twin as one thread |

The (h) check changed the proposal's own premise: the 8 files (`internal/cross-pollination/briefs/{klatch,piper-morgan}/2026-03-19..22-*.md`, ~340 words each, unpublished) are paired per-project precursors of the four *published* retrospective briefs for the same dates, most of whose insights were merged in. PM (2026-10-07): the per-recipient "for Klatch team" / "for Piper Morgan" form was dropped **on purpose**, as a misunderstanding of PM's intent — so the drafts are indexed as a superseded format, not a lost one, and this is not a question for Janus. Draft-only insights include the 03-20 Klatch creation UI item, 03-21 Anthropic ecosystem convergence, and the 03-22 Dispatch omnibus pilot and Mailbox v3 items.
## 8. Risks
- **Confidentiality**: the one risk that can cause harm, and indexing makes it worse. Layer 0 is not optional.
- **Classification drift and shared error**: two Sonnet classifiers agree with each other more than with the
  truth. The gold set is the accuracy measure; agreement only shows consistency.
- **The corpus moves daily**: parsing is build-time; classification isn't. Decision (c) names the owner.
- **Format drift**: it has happened once (07-03). Fail the build, don't print and continue.
- **Janus bandwidth**: the proposal hands Janus review and nominations, not work.
- **Unverifiable share**: 40% of insights cite repos not attached here (decision b).
- **Budget**: ≈$52 of $75 as written; reserve held; the cut list is in §5.

## 9. Open questions for Janus
- Is the Tier-2 nomination flow live? Would an insight index help it or compete with it?
- Any planned index/search work on the hub to align with?
- Location: `/internal/insights/` and `/internal/insights.json`?
- Which §2 discrepancies are deliberate?
- The confidential-term list for Layer 0.

## 10. Changes from v0.1 (independent audit, Opus; `audit-proposal-v0.1.md`)
| # | Finding | Resolution |
|---|---|---|
| F1 | Indexing amplifies an existing confidentiality breach (OpenLaws in published briefs; `/internal/` is public, noindex only) | **Layer 0 added**; Spec confirmed 10 briefs; publication decision (a) |
| F2 | "Insights per window" compared a post-bar rule with all-time data | Post-bar distribution used (85% ≤2); "the bar worked" stated |
| F3 | Readers, audit-coverage and cadence rows overstated the gap | Reworded: sources vs readers distinguished; 49 of ~55 itemized flags executed; cadence partly adopted |
| F4 | "What became of it" measured PM's own insights (circular) and ignored censoring | Denominator is the 142 cross-project, PM-targeted, actionable insights; 116 with 60 days of history; pilot on 40 |
| F5 | 12 multi-label topics with a 60-item gold set; κ undefined for multi-label; two Sonnets share errors | 6 topics; 100-item stratified gold set; per-label κ/α; accuracy from gold, agreement for consistency |
| F6 | Budget omitted adjudication volume, a rerun, and Spec's own cost | Re-costed with assumptions stated; batching and caching; $4 rerun reserve; orchestration line; ≈$49 with a cut list |
| F7 | Daily growth and format drift half-solved | Fail-on-unparsed; ongoing-classification owner is decision (c) |
| F8 | Layer E crossed ownership lines (threads as a Tier-2 corpus; session-start hook is CIO's; sweep prompt is Janus's) | Threads are nominations; E4 addressed to CIO; E5/E6 are proposals to Janus |
| F9 | The "recommended" column PM asked for was missing | Added to §2 |
| F10 | Pagefind deploy step and public index; accessibility; Klatch as a decision; provenance caveats; cut E4's token measurement; expand "R6" | All applied |

## 11. Changes from v0.2 (PM walkthrough, 2026-10-07)
- All eight §7 decisions resolved; mechanics recorded per row.
- Ceiling $50 → $75 (PM). P5 absorbs E2 audit-forward and the monthly drift-check script (+$3); total ≈$52; ~$23 held in reserve.
- §2 gains a "Brief delivery" row from PM's side-question about the fan-out's token cost (structural finding; per-run usage unobservable from this account).
- (h) premise corrected: the 8 files are precursors of published same-date briefs, not an unindexed era.
- Status: PM-approved to start P0. Next: Layer 0 screen; this document to Janus for review; gold-set table scaffold.
