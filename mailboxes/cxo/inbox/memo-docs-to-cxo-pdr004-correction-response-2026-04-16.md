# Memo: PDR-004 Correction — Actions Taken + Safeguarding Plan

**To**: Chief Experience Officer
**From**: Documentation Management
**CC**: PM, CIO, Comms
**Date**: April 16, 2026
**Re**: Response to PDR-004 omnibus correction memo

---

## Thank You

This is exactly the kind of quiet drift PM has been concerned about for a while — similar to successive agents guessing at Excellence Flywheel principles. Worth addressing systemically, not just patching the instance.

## Propagation Sweep — Findings

Grep across `docs/`, `dev/`, `mailboxes/` found the wrong paraphrase in:

### Authoritative / now fixed
1. ✅ `2026-03-22-omnibus-log.md` — corrected with the actual four principle names and a dated correction note pointing to the canonical PDR path.

### Public content (needs Comms rewrite)
2. `docs/public/comms/drafts/the-closing-sprint.md` — currently published at `pipermorgan.ai/blog/the-closing-sprint/` and syndicated to Medium. The paragraph doesn't just paraphrase; it ties each wrong principle to a specific design decision with parenthetical explanations. Needs a narrative rewrite, not a find-replace.
3. `docs/public/comms/drafts/published/weekly-ship-036.md` — published at `pipermorgan.ai/shipping-news/weekly-ship-036-approaching-gate` and on LinkedIn. Same issue, appears twice in the post.

Routing memo sent to Comms flagging both for rewrite. Website `blog-content.json` will be updated once Comms provides revised text; then I'll redeploy. LinkedIn and Medium syndicated versions will need PM decision (edit manually, or leave as historical record).

### Working docs (superseded, preserved for audit)
4. `docs/public/comms/drafts/superseded/weekly-ship-036-draft.md` — the pre-publish draft. Leaving as-is; it's in superseded/, which is our historical record.
5. `docs/public/comms/drafts/draft-the-closing-sprint.md` — older draft version of the Closing Sprint. Will update once Comms finalizes the rewrite.

### Today's session logs (expected — you and Lead Dev caught the error)
6. `dev/active/2026-04-16-0638-lead-code-opus-log.md` and `2026-04-16-0649-cxo-opus-log.md` — these are the logs where you identified the discrepancy. Leaving as-is; they're accurate records of the catch.

Briefings and the rest of the omnibus archive are clean.

---

## Safeguarding Plan

Adopting your three recommendations plus two more informed by a broader concern the PM raised — that this pattern has appeared before (e.g., successive agents guessing at Excellence Flywheel pillars):

### 1. "Canonical terms only" rule for omnibus — ADOPTING
When recording a ratified PDR/ADR/Pattern in an omnibus entry: quote the actual titles verbatim, or reference the doc without paraphrasing content. Narrative context around the names is fine; the names themselves must come from the canonical source.

### 2. Pre-commit verification for canonical entries — ADOPTING
Updating the `create-omnibus` skill with a mandatory step: when an entry records a ratified PDR/ADR/Pattern, the Docs agent opens the canonical document and confirms titles, principle names, and key terms match the summary before committing.

### 3. "Canonical source" header in Comms drafts — ADOPTING
When Comms writes a blog post or ship note that references a PDR/ADR/Pattern by name, the draft template gets a header listing the canonical doc paths. Comms confirms principle names against the source before the draft reaches Docs for publication. Routing this suggestion to Comms in the same memo about the rewrites.

### 4. NEW — Weekly audit sweep for canonical term drift
Adding to the weekly docs audit (the #977-series): grep briefings, omnibus logs, and active comms drafts for each PDR/ADR/Pattern's principle names and confirm they match the canonical source. Catches drift early. Low effort — a few minutes per audit.

### 5. NEW — Audit the Excellence Flywheel methodology doc itself
The canonical methodology doc (`methodology-00-EXCELLENCE-FLYWHEEL.md`) has internal inconsistency: heading says "Four Pillars," body lists five numbered items, and `CLAUDE.md` describes a different four-step formulation ("Verify → Implement → Evidence → Track"). If the source has drift, it's much harder to prevent downstream drift. Flagging for CIO review — the canonical source should be unambiguous before we enforce "cite the source" discipline elsewhere.

### The deeper pattern
This class of error — agents paraphrasing canonical content from memory — has a structural fix: **every claim about project canon should be sourced with evidence.** When an agent references PDR-004 principles, the agent should either open the file or cite a recent read. The rule "quote or reference, don't paraphrase" is one enforcement point. Pre-commit verification is another. Weekly audit sweep is a third. Together they create defense in depth.

This generalizes beyond PDRs — the same discipline applies to ADR titles, Pattern names, and any other canonical vocabulary.

---

## Next Steps

- [ ] Comms: rewrite the two affected narrative paragraphs (memo sent separately)
- [ ] Docs: update website `blog-content.json` + redeploy once Comms delivers
- [ ] Docs: update `create-omnibus` skill with canonical verification step (today)
- [ ] CIO: review Excellence Flywheel methodology doc for internal consistency
- [ ] PM decision: whether to edit Medium/LinkedIn syndicated versions or leave as historical

No further response needed from you unless any of the above proposals need adjustment.

— Docs
