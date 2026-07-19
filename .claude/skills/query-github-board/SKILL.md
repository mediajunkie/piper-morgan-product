---
name: query-github-board
description: Read GitHub Projects-v2 boards and issue state WITHOUT silent truncation or stale claims. Use whenever summarizing sprint/board state for PM, counting open items, or making any "N of M" claim about issues. Companion to assign-sprint-safely (which covers WRITES; this covers READS).
scope: cross-role
version: 1.0
created: 2026-07-18
updated: 2026-07-18
---

# query-github-board

Make board/issue READS trustworthy. Exists because of a real incident (2026-07-18): a
`gh project item-list --limit 1200` pull silently truncated a 1280-item board, producing a
"27 of 28 closed" summary to PM that missed 8 genuinely-open sprint issues — including the
sprint's own close-out gate and a live data-loss pair. **The tell was in the payload the
whole time**: the JSON carries `totalCount`, and fetched < totalCount was never checked.

## The three rules

### 1. NEVER trust a single `item-list` pull — reconcile `totalCount` vs fetched
```bash
gh project item-list <N> --owner <OWNER> --format json --limit 1000 > /tmp/board.json
python3 - <<'PY'
import json
d = json.load(open("/tmp/board.json"))
total, got = d["totalCount"], len(d["items"])
assert got == total, f"TRUNCATED: fetched {got} of {total} — raise --limit or paginate; DO NOT summarize from this"
print(f"complete: {got}/{total}")
PY
```
If the board exceeds the max limit, paginate with GraphQL cursors (`items(first:100, after:$cursor)`)
until `hasNextPage` is false. **A truncated pull may not be summarized. Ever.** Say
"pull incomplete" instead — a wrong count presented confidently is worse than no count.

### 2. `item-list` does NOT carry issue open/closed state — join it
The `content` object omits state. Any open/closed claim needs a second source:
```bash
# batch-join states for the numbers you extracted
gh issue list --state all --json number,state --limit 1000 \
  | python3 -c "..."   # or: gh issue view <n> --json state per item for small sets
```
An item being ON the board says nothing about it being OPEN.

### 3. Per-item verification beats list-scraping for load-bearing claims
For any claim that drives a decision ("the gate items are all closed", "this issue is on
the sprint"), verify the SPECIFIC items via GraphQL — it's authoritative and un-paginated
for a single node:
```bash
gh api graphql -f query='
query { repository(owner:"OWNER", name:"REPO") {
  issue(number: N) { state projectItems(first:5) { nodes {
    project { number }
    fieldValueByName(name:"Sprint") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
  } } } } }'
```

## The discipline behind the rules
This is the **blind-sweep class** (4th instance named by Arch 2026-07-18): a check blind to
part of its space gives false confidence — rail-membership greps missing a dispatch surface,
mypy without the sqlalchemy plugin, absolute-only import sweeps, and truncated board pulls
are all the same bug. The cure is always the same: **enumerate the whole space or say you
didn't** — reconcile a completeness signal (`totalCount`, `hasNextPage`, both import styles)
before presenting any summary as fact.

## Known write-side gotchas (pointers, not duplication)
- Setting sprint/single-select values: use **assign-sprint-safely** (per-item mutation ONLY;
  `updateProjectV2Field` full-replaces the option list — the 1175-item wipe of 2026-07-05).
- Commit messages: close-keywords near `#N` auto-close regardless of negation — see
  `docs/internal/operations/github-and-tooling-gotchas.md`.

## Checklist for a board summary handed to PM
- [ ] `totalCount == fetched` shown (or explicit "incomplete pull" caveat)
- [ ] States joined from an issue-level source, not assumed from board presence
- [ ] Any "N of M" arithmetic reproducible from the pasted counts
- [ ] Load-bearing single items GraphQL-verified

## Changelog
- **v1.0** (2026-07-18, Lead Dev): Created after the truncated-pull incident, at PM's
  suggestion ("maybe we need some Working-with-GitHub skills?").
