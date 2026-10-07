---
type: proposal
title: "The cross-pollination corpus: digest, index, browse, verify, synthesize — proposal v0.1"
author: spec (Special Assignments), cloud session, Fable 5.1
date: 2026-10-07
status: DRAFT v0.1 for independent audit, then PM review. Nothing here is built; nothing in the hub changes without Janus's review and PM's approval.
evidence: dev/2026/10/07/spec-xpoll/ (X1 extraction + provenance pilot; X2 prior-work and practice-gap map)
---

# The cross-pollination corpus: a proposal

## 0. What PM asked for, in one paragraph

Research and propose a plan for reviewing the full cross-pollination newsletter corpus, then classifying,
indexing, and providing a way to browse, filter, sort and otherwise interact with it. Blue-sky extensions are
welcome: synthesis, derived work, refinement of the corpus, correcting past claims, and reporting on gaps
between **reported practice, actual practice, and recommended practice**. The goals stay speculative and
generative at this stage. Scope is the full hub archive. The result lives somewhere in `/internal/`,
coordinated with Janus. Ceiling: $50 of cloud credit.

## 1. The corpus as it actually is (measured this morning)

All numbers come from `metrics/xpoll_extract.py` over `designinproduct/src/internal/briefs/` at `39608c0`,
unless marked otherwise. Layer: static parse of markdown, plus git queries against the Piper Morgan repo.

| Fact | Value |
|---|---|
| Briefs | **234** files (233 `*-brief.md` + `2026-04-11-brief-rev2`), 2025-06-01 → 2026-10-07; 223 substantive, 11 nominal; ~271k words |
| Daily cadence | Monthly since 2026-03 (31/31/31/30/31/31/30); 2025 has one brief a month, retrospective in origin |
| Key Insights | **592** (`### N.` or, since 2026-07-03, unnumbered `###` headings — 105 insights, 17.7%, would be missed by a numbered-only parser) |
| Per brief | Mean 2.53; mode 2 (36%); 47% of briefs carry more than 2; 11 exceed 4; max 8 |
| Source mix | Piper Morgan 60% · Klatch 31% · Mediajunkie 7% · DinP 5% · others ≤2% each (keyword attribution on the From line) |
| Evidence cited | commit SHA 36% · repo path 68% · issue ref 31% · **suggested action 92%** · stated audience 94% |
| Provenance (pilot) | PM-attributed SHAs resolve in PM's git **216 of 220 (98.2%)**; paths cited in PM-attributed insights were touched at or before the brief date 33 of 44 (75%) in a sample. Non-PM citations can't be checked here (Klatch etc. not available) |
| Letters to xian | 8 distinct letters, 70 appearances (re-featured across briefs), all 8 answered |
| Corrections | 4 items in 3 briefs (09-08, 09-09, 10-05) via the pending-corrections flow |
| Unpublished slice | 4 + 4 per-project briefs (2026-03-19→22, "from Klatch for Piper Morgan" and the reverse) sit in `internal/cross-pollination/briefs/` but not in the published archive |
| Rendering gaps | rev2 file is outside the `briefs` collection glob; nominal briefs render a fixed sentence even when they carry Background items *(inferred, site not built here)* |

**Prior work this builds on, not over** (X2 §1): Janus's 2026-06-28 history audit (headline ~48 REMOVE/~57
DEMOTE, itemized 18/37; 17 removed 06-28, 32 demoted 07-08); the 2026-03-23 cadence recommendations (never
applied); the glossary (last updated 04-10, absent from the live sweep prompt); the pending-corrections flow
(working since 09-08); the cross-project harvest architecture (PM `docs/internal/design/…-2026-08-29.md`) whose
Tier-2 destination is `/internal/patterns/`; and the Practice scaffold. About **100 briefs since 06-28 have never
been audited** by any method.

## 2. Stated vs actual vs recommended practice (first pass; the proposal makes this a standing report)

| Practice | Stated | Actual | Note |
|---|---|---|---|
| Readers | 7 (`publishing-flow.md`, delivery prompt, health check expects `7/7`) | `projects.json` registers 4; `delivery-log.md` says 11 reader repos, 169/170 rows "11/11"; the live sweep scans 13 repos | Four different numbers in four places |
| Insights per window | "0–2 typical; zero common; four an extremely unlikely maximum" | 47% of briefs exceed 2; since the bar (06-28, n=102) zero-insight briefs are 1 of 102 | The spec describes a distribution the sweep doesn't produce |
| Timing | Sweep "~12:00 UTC"; `sweep-prompt.md` says "7 AM PT (12:00 UTC)" | 12:xx on 131 of 197 logged runs, 11:xx on 32 | Roughly holds; the PT conversion is wrong |
| Cadence recs (03-23) | "to be applied to daily-sweep.md" | Not applied; no cadence log, skip tier, relevance test, or Temporal Note | Six months unapplied |
| Glossary | Mandatory before defining acronyms | Zero references in the live prompt; stale since 04-10 | Rule without a mechanism |
| Readers act on briefs | "Agents read `current.md` at session start" | 167 of 1,295 PM session logs (Jul→Oct) mention the brief; 125 of those file it as "loaded but not referenced"; 1 of 15 sampled acted on it | Real use exists (CIO, Exec, Arch) but is rare |
| Audit coverage | Brief-worthiness bar applies to all | ~9% of ~535 entries executed; 100+ later briefs unaudited | |
| Hub browsing | Archive | Month pages only. No search, filters, tags, insight anchors, related links, or machine-readable feed | X2 §3, confirmed against templates |

## 3. Design constraints (from Janus's own documents; confirm with Janus)

1. **Briefs are never retro-edited**; corrections are forward-only. So classifications and verification results live as **sidecar metadata**, not front-matter edits. The index is generated, never hand-maintained.
2. **`/internal/patterns/` is the sanctioned Tier-2 promotion path** with its own bar (recurrence across projects, outcome-framed, carries a trigger) and fires on upstream nomination, not on a schedule (harvest §4.3). This proposal does **not** create a competing promotion path; it makes the corpus legible so nomination is possible, and it links insights to the patterns they fed.
3. **URL stability**: brief URLs are canonical in 150+ files. New surfaces are additive. Everything stays `noindex`.
4. **Confidentiality gates** (OpenLaws/Kind never appear) apply to any derived output exactly as to briefs.
5. **Janus is the curator**; build work hands to bounded subagents under Janus's "major-domo" model. Spec proposes and prototypes; Janus reviews anything that ships; PM approves.
6. The corpus grows daily; everything here must be **regenerable at build** (Eleventy data or a pre-build script), with the denominator printed.

## 4. The proposal: five layers, each useful on its own

### Layer A — Data: a canonical structured index
- `insights.jsonl` / `briefs.jsonl` / `letters.jsonl` / `corrections.jsonl`, generated by a script that lives in the
  designinproduct repo and runs at build. Stable ids `YYYY-MM-DD#N`. Fields as in X1, plus classification and
  verification sidecars (Layers B and D).
- Published as `/internal/insights.json` (and a per-brief JSON) so **agents can query the index instead of reading
  `current.md`**. This connects to assignment 1's R6: `current.md` is loaded by every role at session start.
- Parse coverage is a printed denominator: "592 insights parsed from 234 briefs; 0 unparsed sections" or the
  list of what didn't parse.
- Fold the 8 unpublished per-project briefs in as a flagged "pre-unification" era, or document why not.

### Layer B — Classification: a pre-registered taxonomy, two classifiers, an adjudicator, a gold set
- **Taxonomy** (proposed; PM and Janus edit before anything runs):
  - *Type*: pattern · technique · decision-with-reasoning · discovery · incident-lesson · anti-pattern · tooling · status/news (the class the bar excludes).
  - *Topic* (multi-label, ~12): agent coordination · prompt/context architecture · verification & evidence · git/worktree discipline · CI/testing · credentials/security · LLM routing · product/UX · publishing/newsletter · observability · memory/continuity · process meta.
  - *Transferability* against the bar: "would another team do something differently?" yes / weak / no.
  - *Status*: live · superseded-by `id` · corrected-by `date` · promoted-to-patterns · unknown.
  - *Audience fit*: does the stated "relevant to" match the content?
- **Method**: two independent Sonnet classifiers per insight (different prompts), a third pass adjudicates
  disagreements; **agreement is reported** (percent and κ per field). A **gold set of ~60 insights**, hand-labelled
  by PM and/or Janus, calibrates both and bounds the error rate before the full run.
- Output is sidecar JSON only. Nothing in a brief changes.

### Layer C — Interface: browse, filter, search, link
- `/internal/insights/`: a filterable list (project, topic, type, date range, has-evidence, has-action,
  status), each insight with a permalink anchor into its brief.
- Per-brief additions: anchors per insight, "related" and "corrected-by" links, previous/next.
- **Search**: Pagefind (static, builds into Eleventy output, no server), scoped to `/internal/`.
- Letters get the same index treatment (one record per letter, not per appearance).
- Everything additive; Janus reviews; a **prototype ships first as an artifact** (static HTML over the JSON) so PM
  and Janus can click before any site change.

### Layer D — Verification and correction
- **Provenance**: extend the pilot to every cited SHA, path, issue and ADR; show a per-insight evidence status
  (verified / unverifiable here / not found). Klatch and other reader repos become checkable only if attached.
- **"What became of it"**: for each suggested action aimed at Piper Morgan (the 354 PM-sourced and the
  PM-targeted ones), look for evidence the action was taken (commits, issues, CLAUDE.md lines, skills) within
  60 days. Report a hit rate with denominators. This is the newsletter's **effectiveness measure**, and it
  doesn't exist today.
- **Corrections back-links**: forward-only corrections stay as they are, but the index marks the *affected*
  insight "corrected by <date>", so a reader of the old brief sees it.
- **Lineage and dedup**: cluster near-duplicate insights (same lesson, different months) into threads; show
  the thread on each member. The repeated-lesson count is itself a finding.

### Layer E — Synthesis and derived work (blue sky; ranked, not all funded)
1. **The practice-drift report** as a standing `/internal/` page: §2 above, regenerated, with a "last checked" date.
2. **Audit-forward**: apply the 06-28 method to the ~100 unaudited briefs, with Janus, producing dispositions
   not edits. Also reconcile the audit's headline vs itemized counts.
3. **A field guide**: 592 insights distilled into threads, each with the strongest-evidence instance and its
   outcome. The Practice page is its natural consumer.
4. **Agents as subscribers**: a role reads only insights tagged for its lane from the JSON index, with a cursor.
   Measure the session-start token saving against `current.md`.
5. **Temporal Note / knowledge-gap detector** (the 03-23 lead): the sweep flags artifacts holding lessons not yet
   captured in any agent-facing document. The index makes "already captured?" answerable.
6. **Registry reconciliation**: one source of truth for readers (4/7/11/13), surfaced on the hub.

## 5. Phases, cost, and checkpoints (ceiling $50)

| Phase | Work | Tier | Est. |
|---|---|---|---|
| P0 | Taxonomy + gold set with PM/Janus; schema freeze; Janus review of this proposal | Spec + humans | $2 |
| P1 | Harden extraction (done in research); fold pre-unification briefs; CI coverage print | Sonnet | $2 |
| P2 | Classification run: 592 × 2 classifiers + adjudication; agreement report | Sonnet ×2, Opus adjudicate | $12 |
| P3 | Prototype interface as an artifact over the JSON; then an Eleventy implementation as a PR for Janus | Sonnet build, Spec review | $8 |
| P4 | Verification: full provenance; "what became of it" pilot on PM-targeted actions; corrections back-links; dedup threads | Sonnet + scripts | $8 |
| P5 | Synthesis drafts: practice-drift page; field-guide sample (3 threads); subscriber feed spec | Opus | $8 |
| P6 | Independent verification of the whole (re-derive 3 headline numbers; refute top findings); handoff memo to Janus | Opus | $4 |
| | **Total** | | **≈ $44** |

Checkpoints: PM reads the usage page at the end of P2 (~$18) and before P5 (~$32). Stop if over plan.
Research so far (two Sonnet agents, ~370k tokens) is already spent, roughly $3–4.

## 6. Verification discipline (how we'll know it's right)
- Taxonomy and thresholds are **written down before** classification runs; changes afterward are logged.
- **Gold set** before the full run; inter-rater agreement reported per field; items below threshold are shown as
  "contested", not smoothed.
- Every number carries its denominator and layer; the index prints its own coverage.
- An **independent verifier** re-derives headline figures with its own scripts and tries to refute the top findings.
- **Nothing ships to the hub without Janus**; nothing public without PM.

## 7. Decisions for PM (and Janus)
1. Taxonomy depth: the ~12 topics above, or fewer? (Fewer is more reliable.)
2. Sidecar metadata in the designinproduct repo (recommended) vs a separate data repo?
3. Fund the "what became of it" measure? It's the most original piece and the best test of whether the
   newsletter works, but it's the most labor.
4. Which of the six blue-sky items (Layer E) to fund now; my ranking is as listed.
5. Fold the 8 pre-unification briefs into the published archive, or index them separately?
6. Who hand-labels the gold set: PM, Janus, or both (about an hour)?

## 8. Risks
- **Classification drift**: LLM labels vary. Mitigated by two classifiers, adjudication, the gold set, and
  reporting agreement rather than hiding it.
- **The corpus moves daily**: a hand-maintained index would rot in a week. Everything is build-time generated.
- **Janus bandwidth**: the hub is one agent's product. The proposal hands Janus review, not work.
- **Unverifiable half**: 40% of insights come from repos not attached here; their provenance stays "unverifiable
  here" unless PM attaches Klatch and others read-only.
- **Confidentiality**: derived pages inherit the OpenLaws/Kind gate; the classifier output is checked for it.
- **Over-reach**: six blue-sky items is more than $50 buys. Layers A–D are the proposal; Layer E is the menu.

## 9. Open questions for Janus
- Is the harvest architecture's Tier-2 nomination flow live, and would an insight index help or compete?
- Any planned index/search work on the hub we should align with?
- Preferred location: `/internal/insights/` and `/internal/insights.json`?
- Which of the §2 discrepancies are deliberate?
