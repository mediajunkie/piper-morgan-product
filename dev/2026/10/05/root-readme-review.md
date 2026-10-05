# Root README review — 2026-10-05 (Weekly Docs Audit #1938)

**Reviewer**: Docs. **Target**: `README.md` (repository view). Separate from `docs/README.md`.

| Check | Result |
|---|---|
| Outdated "NEW:" claims | 0 occurrences |
| External links | pmorgan.tech, pipermorgan.ai, Actions, Issues, CI badge, Apache license: all HTTP 200 |
| Dead link | **GitHub Discussions** line pointed at a feature that is disabled (`hasDiscussionsEnabled:false`). Removed in `c846688a57` |
| Setup instructions vs current process | Not re-executed this audit (read-only comparison against `docs/ALPHA_QUICKSTART.md`; no drift found at the text level) |
| Brief / evergreen / test artifacts | No stray test content or markdown artifacts found |

**Verified how**: `curl -sI` per link (network layer only, not a rendered-page check); `grep -n "NEW:"`; `gh repo view --json hasDiscussionsEnabled`. Denominator: every external link in the README.
