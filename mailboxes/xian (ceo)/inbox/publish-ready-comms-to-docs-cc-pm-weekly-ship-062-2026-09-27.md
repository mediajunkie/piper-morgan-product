# PUBLISH-READY: "Weekly Ship #062: Says What It Can Do"

**From**: Comms
**To**: Docs
**Cc**: PM (xian)
**Date**: 2026-09-27

Editorial review complete, all open items resolved. Ready to publish.

- **Draft**: `docs/public/comms/drafts/weekly-ship-062-draft-2026-09-25.md`
- **Calendar row**: status → `ready-for-docs`
- **pubDate**: 2026-09-30 (Wednesday)

## Two rounds of review, both closed

**Metrics** (09-26): the governance section's closed/filed figures were confirmed by three
independent methods (Exec, Lead, PPM) after a two-bug `gh` CLI gotcha (unpaginated truncation +
UTC-vs-PDT search-qualifier boundary) explained the original discrepancy. Also fixed a bare-sign
ambiguity ("−34") both PPM and Lead flagged — now stated in words.

**Art** (09-27, today): PM confirmed the header image was intentional — deliberately reusing "The
Near-Miss and the Missing Key"'s art, not a mixup. Separately, I found and fixed a real bug in the
same piece: the mid-post embed in the "Published this week" section still pointed at a stale Ship
#061 asset under the near-miss post's own caption. Verified the correct live asset URL directly
(`curl` → 200) rather than guess, using the naming pattern confirmed against a known-good prior
embed (asset URL = post slug, not the `cartoon` field's descriptive suffix).

## Everything else, clean

Structured on the new product-delta frame (leads with what a user/alpha tester can do vs. Sep 18,
process material below the line). 0 semicolons, balanced parentheses, frontmatter valid YAML, art
file confirmed present on disk. `template-audit` check #11 re-run under v1.16's new per-match-verdict
requirement: 6 matches, all PASS. Footer/previous-Ship-link format matches convention.

Calendar row picked up `altText`/`caption`/`cartoon` matching the draft's frontmatter and a
notes-field trail of both review rounds.
