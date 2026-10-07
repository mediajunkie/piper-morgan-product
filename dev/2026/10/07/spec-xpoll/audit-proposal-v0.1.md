---
type: audit
target: proposal-xpoll-corpus.md (v0.1)
auditor: independent plan auditor (did not write the proposal)
date: 2026-10-07
---

# Audit: cross-pollination corpus proposal v0.1

**Verdict: approve with changes.** Layers A–D are what PM asked for, and the headline numbers re-derive. Four problems need fixing first: the corpus already breaches its confidentiality gate and indexing would amplify it; two §2 rows are framed harsher than the evidence; "what became of it" uses the wrong denominator; the budget omits the expensive work.

## Numbers re-derived (my own grep/awk/git, not the metrics scripts)

| Claim | Mine | Result |
|---|---|---|
| 234 briefs (233 + rev2), 2025-06-01 → 2026-10-07 | 233 `*-brief.md` + rev2; first 2025-06-01, last 2026-10-07; ~279k words with front matter | Match. The briefs dir is unchanged between `39608c0` and HEAD `932518a` (empty diff) |
| 592 insights; 105 unnumbered | 594 `###` total. 2 sit under "Corrections to the record" (09-08), leaving **592 under Key Insights**. Numbered/unnumbered over all 594: 487/107 | Match (105 + the 2 corrections = 107) |
| 47% of briefs carry more than 2; 11 carry more than 4; mean 2.53 | 110/234 = 47.0%; 11; 2.53 | Match, but see F2 |
| Readers: projects.json 4, publishing-flow 7, delivery-log 11 (169/170) | projects.json lists 4 (Klatch, Mediajunkie, PM, Tectonic Globe); publishing-flow says "7 reader repos" at L5, L11, L77; delivery-log has 169 rows of "11/11" out of 170 | Match, but see F3 |
| Every resolved PM SHA predates its brief | 355 of 356 resolved SHAs (Apr–Oct, my own regex) were committed on or before the brief date; the single exception is a one-day timezone edge | Supports the pilot at the existence and date layer |

Minor slips: "Monthly since 2026-03" should read "daily"; 2025 isn't one a month (no July, two in June).

## Findings, most severe first

**F1. Indexing amplifies an existing confidentiality breach.** OpenLaws is named in **9 published briefs** (for example 2026-04-05 L16 and L81, "xian's new OpenLaws project at Kind"; also 07-26 and 08-10), despite `sweep-prompt.md:46`. `/internal/` sits on public designinproduct.com and is only `noindex`. A public `insights.json`, Pagefind index and topic filters would make that leak one query away; §8 only checks *classifier output*, and briefs can't be retro-edited. **Fix:** add a P0 confidentiality screen of the source corpus. Exclude or redact flagged items from every derived surface, and add to §7 whether the JSON is published at all.

**F2. The "insights per window" row compares post-bar rules against all-time data.** The 0–2 rule dates from 06-28. Since then (n=102) the counts are {0:1, 1:20, 2:66, 3:14, 4:1}: **85% are ≤2, and only one brief reaches 4.** X2 row 2 says this correctly ("the bar worked"). The proposal swaps in the all-time 47%. **Fix:** quote the post-bar distribution. The real discrepancy is narrower: "zero is common" doesn't hold (1 of 102).

**F3. Other §2 rows overstate the gap.**
- *Readers*: projects.json (OVERVIEW L24–28) and the "13 repos" are **sources**; the reader gap is 7 stated vs 11 delivered.
- *Audit coverage*: "~9% of ~535 executed" implies 91% skipped; 49 of ~55 itemized flags were executed (~89%).
- *Cadence recs*: X2 records partial adoption, and the 06-28 bar replaced the tiers; "not applied" overstates.

**Fix:** reword all three.

**F4. "What became of it" measures the wrong thing and ignores censoring.** It targets "the 354 PM-sourced" insights. Those describe PM's own work, so finding the action in PM git is reverse causality. The real transfer denominator is **142 non-PM-sourced insights that are PM-relevant and carry an action**. Only **116** of them have the full 60 days of follow-up; 122 insights date after 08-08. **Fix:** restrict to the 142, report censoring and 30/60/90 days, and count as influence only changes that cite the brief or insight.

**F5. Classification is too thin for 12 multi-label topics.** 60 gold items leave most topics under 5 positives, so per-topic error can't be bounded. Cohen's κ is undefined for multi-label (use per-label κ or Krippendorff's α with MASI). Two Sonnet classifiers share errors, so agreement measures consistency, not accuracy. Janus labelling gold is an LLM grading LLMs, and 60 items × ~270 words × 5 fields is 2–3 hours, not one. **Fix:** ~6 topics; an 80–100-item gold set, stratified by era and project, labelled by PM; per-label F1 against gold as the accuracy measure.

**F6. The budget omits the expensive work.** Assuming Sonnet $3/$15 and Opus $5/$25 per MTok: 1,184 per-item classifications (~3.4k in, 250 out) cost ~$17 uncached, over P2's $12 before adjudication. 12-topic multi-label means ≥50% disagreement, so ~350 Opus adjudications add ~$10. Batching and caching bring P2 to ~$8, but each recalibration rerun adds about that again. "What became of it" as agentic git search (142 × ~30k tokens) is ~$13, against $8 for all of P4. The spec's own orchestration session is unbudgeted.

**Fix:** batch 10–20 items per call with a cached prompt, budget one rerun and orchestration, and pilot "what became of it" on 40 items.

**F7. Daily growth and format drift are half-solved.** Parsing runs at build; classification can't (no LLM keys in the Pages deploy, recurring cost), so ~2 new insights a day go unclassified with no named owner. The 07-03 heading drift shows printing coverage isn't enough. **Fix:** fail the build on any unparsed section, show "unclassified since X", and add a §7 decision: sweep-emitted tags (Janus's prompt) or an owned periodic job.

**F8. Some of Layer E crosses ownership lines that §3 says it respects.**
- *E3 and the D dedup threads*: "strongest-evidence instance per thread", mined in bulk, is a Tier-2 corpus by another name, against X2 constraints 2–3. Frame threads as nomination candidates to `/internal/patterns/`; admission stays Janus's.
- *E4 and Layer A's "query instead of current.md"* change the PM session-start hook, which X2 says is **CIO-owned**. Name CIO.
- *E5 and E6* edit Janus's live sweep prompt and registries: proposals *to* Janus, not deliverables.

**F9. The "recommended" column PM asked for is missing.** §2 has Stated | Actual | Note. **Fix:** add Recommended, even if it reads "Janus to decide".

**F10. Smaller gaps:**
- *Pagefind* needs a post-build step in `deploy.yml` and `data-pagefind-body` scoping, and its index is public too (F1).
- *Accessibility*: no UI criteria (keyboard-operable filters, WCAG AA).
- *Klatch* (31% of insights): attaching it read-only belongs in §7, not §8.
- *Provenance*: 98.2% holds at the existence-and-date layer only, not that the commit supports the claim, and covers 123 of 354 PM insights. The path figure is n=20 insights (44 paths, ±~13pp), some misses cross-repo. Say so.
- *Cut* E4's token-saving measurement; keep Letters indexing (8 records, cheap).
- *Referent*: expand "assignment 1's R6".

## §7 decision-readiness

Q1–Q3 and Q5 are answerable. Q4 isn't a-or-b (offer "fund E1+E2 now: yes/no"); Q6 should be "PM labels / Janus pre-labels, PM confirms". Missing:
- (a) Confidentiality handling, and whether the JSON is public.
- (b) Attach Klatch: yes/no.
- (c) Ongoing classification owner (sweep-emitted vs periodic job).
- (d) Topic count of 6 vs 12, tied to gold-set size.

## The three changes that matter most

1. **Confidentiality screen before any index exists** (F1): the only finding that can cause harm, and indexing worsens it.
2. **Fix the §2 framing and add the Recommended column** (F2, F3, F9): as written it mischaracterizes Janus's 06-28 bar and audit execution, which costs credibility with the reviewer the plan depends on.
3. **Re-scope the measurement core** (F4–F6): influence measured on the 142 cross-project items with censoring; fewer topics with a larger PM gold set and F1 as the accuracy metric; a batched cost model that budgets a rerun and orchestration.
