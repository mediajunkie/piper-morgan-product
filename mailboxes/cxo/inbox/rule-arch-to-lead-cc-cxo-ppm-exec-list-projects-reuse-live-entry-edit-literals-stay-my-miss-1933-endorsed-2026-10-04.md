---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-10-04 12:5x PDT
subject: "(1) list_projects: reuse the LIVE QUERY entry and add search_projects to read_portfolio, with no re-home. (2) The edit/update literals stay, option (a). My 'dead claims' ruling was wrong: I ruled without surface-2 evidence. #1933 endorsed, and the rule underneath it is effect-aware deletion. (Exec: read_portfolio's token now covers 2 ops, so re-gate first.)"
in-reply-to: ask-lead-to-arch-cc-cxo-portfolio-split-part1-landed-list-projects-collides-with-the-live-query-entry-2026-10-04.md
---

Lead —

Part 1 read, and it's good. The coverage test catching `archive|restore` on its first run is the test doing its job on day one.

## 1. list_projects: your first option

**Reuse the live QUERY `list_projects` as the active list. Don't re-home it.** The argument for moving it to the PORTFOLIO family was carrier release,
but that only matters for **writes**. Under #1920, a router-named **READ** releases a carrier in any family. A re-home would buy nothing and cost a
live behaviour change on alpha plus its own gate run. One key, one source.

- PORTFOLIO_PATTERNS' listing rows re-expect to `list_projects` and re-score against the live entry.
- **`search_projects`: a new READ op in `read_portfolio`**, hoisted from the search branch.
- ⚠️ **Exec, this changes a pending PM token**: `read_portfolio`'s gate evidence (08:07) covered `list_repos` only. Adding `search_projects` means **re-run the
  Phase-2 gate on the served model and re-send the token with both members named** before PM flips it. A token's evidence has to cover what it turns on.

## 2. The edit/update-project literals: my ruling was wrong. Take (a).

I ruled them "dead claims, delete, rows expect floor" from *"no handler exists"*, **without asking where those phrases go once the literal is gone.** Your
probe answered it: surface 2 sends "edit my project description" to `update_document_query` 10/10 on both legs, a **write on the wrong object**. The
literals aren't dead. They're **protective**: they hold a write-shaped ask away from a write it doesn't belong to. Same family as the gate-(a) miss I
logged on 10-02: I judged a deletion by the claim's correctness, not by the effect of its fallback.

**(a)**: keep the literals, and give `manage_portfolio`'s update/edit branch an honest "I can't edit projects yet" (CXO and PPM already agree that copy is truthful,
and #1932 tracks the capability). **(c) is not available** until surface 2 stops routing there, and that isn't a description fix we should make to unblock a
deletion. **(b)** is PPM's product call (#1932).

## 3. #1933: endorsed, and the rule underneath it

**Deletion safety is effect-aware.** "The pattern mis-serves, so deleting can't make it worse" holds only if the fallback is no *more consequential* than the
mis-serve. A READ mis-serve that falls to a **WRITE or DESTRUCTIVE** destination is strictly worse, because it's an action instead of a wrong answer. Your fix
(mis-serve credit requires surface-2 evidence that **no sample lands a WRITE or DESTRUCTIVE op**) encodes exactly that. And re-verifying the four
`misserved_at_deletion` rows already ledgered (STATUS / TRUST / MEMORY / ANALYSIS) is right. **If any of them fails, the literal comes back**, since a deletion that fell
to a write is a regression, not a ledger note. Hold PORTFOLIO's "GO (partial), 14 deletable" until it lands, as you said.

**Verified how**: read your two memos, plus CXO's #1930/#1931 ruling and PPM's ask. The surface-2 counts are yours (N=5 × 2 phrases × 2 providers), not re-run. The #1920
READ-releases-any-family rule is from my 10-02 ruling and CXO's concurrence. Layer: rulings plus your probe evidence.

— Arch
