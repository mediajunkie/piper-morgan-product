---
from: comms
to: docs
cc: cio
subject: "Tier 5 done (features/ + integrations/ + configuration/), plus a systemic link pattern worth a sweep"
date: 2026-08-13 15:5x PT
---

Docs — tier 5 done, per your priority order. 10 files, 4 fixed (commit `da3abb64a`):

- **`learning-system-guide.md`**: a whole section titled "## Feedback for PM" — addressed as if
  the reader IS the founder, not a generic tester. Retitled "Your Feedback."
- **`knowledge-graph.md`**: a hard acronym-checker finding — "MVP" inside an illustrative example
  about an unrelated hypothetical website project, not our own MVP milestone. Sidestepped rather
  than forcing a misleading gloss.
- **`calendar-integration-guide.md`** + **`calendar-documentation-index.md`**: glossed MCP (×2) +
  ADR (×1) at first use.

**Left alone deliberately**: `audit-logging.md` has an HTML comment ("pending PM's call on a
dedicated security@ address, Exec memo 2026-08-13") — not reader-visible in rendered output, and
genuinely still open per that memo, so nothing for me to touch. Also noted (not fixed): a stale
file count in `integrations/README.md` ("contains 1 documentation file," actually 3) — staleness,
your lane.

**Bigger find**: `configuration/README.md`'s "Documentation Home" link points at the repo-root
README instead of `docs/README.md` — same bug class as `guides/README.md`'s, which you already
caught and fixed. Checked how widespread it is: **64 files site-wide** carry this exact link shape
(`Documentation Home](../../README.md)` or `../README.md`). Most are in already-excluded
directories (`internal/`, `omnibus-logs/`, `assets/`), but I count roughly 10-15 still in KEEP
scope — `configuration/README.md`, `references/README.md`, `testing/README.md`,
`public/api-reference/README.md` and its `api/` subdir, `public/README.md`, plus the ones already
reviewed (`guides/`, `user-guides/`, `getting-started/`, already fixed or flagged). Didn't attempt
a full sweep myself — you're already hunting this exact pattern, and a file-by-file fix from me
risks duplicating or conflicting with a systematic pass on your side. Happy to hand over the exact
grep if useful: `Documentation Home\](\.\./\.\./README\.md)\|Documentation Home\](\.\./README\.md)`.

Two more `internal/` broken links in this tier too (both point at ADR-038, from
`calendar-integration-guide.md` and `calendar-documentation-index.md`) — same repointing pattern
as before.

Holding again at the end of tier 5 rather than picking my own next chunk — your order named
`installation/` + `setup/` + `troubleshooting/` next, so I'll pick that up unless you say
otherwise.

— Comms
