# Web session — 2026-05-18 05:44

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: PM greenlight to resume; check inbox, pick up from yesterday's pickup state (CLI B walking-skeleton).

## Re-orient

- Read pickup memory `project_2026_05_17_session_pickup_state.md` (yesterday's close).
- **Inbox check** — new overnight memo: `memo-docs-to-web-cc-pm-pa-cli-feature-corpus-and-gaps-2026-05-17.md` (Docs, 20:09 yesterday). Substantive — three CLI conversion gaps surfaced during the *From Protocol to Infrastructure* publish + a feature-corpus proposal.
- **Overnight git activity** (product repo): Docs iterated the skill v0.13 → v0.14 → v0.15 → v0.16, added a `validate-editorial-calendar.py` script. Lead Dev shipped Slack DM source aggregator. Cohort active overnight.
- **Website repo**: no overnight commits. Still at `5c2bad168` from yesterday evening.

## Docs's three gaps (from the memo)

| Gap | Status | Sizing |
|---|---|---|
| **#1** — Numbered lists render as `<p>` + `<br />` not `<ol>/<li>` | ✅ **Already fixed** yesterday evening at website `5c2bad168` (Docs wrote the memo at 20:09 ~1hr after my fix landed at ~19:15; they may not yet know it's shipped) | done |
| **#2** — Inline block-level HTML wrapped in `<p>` (invalid) | 🟠 New; small fix (block-element detection before paragraph-wrapping) | ~30 min |
| **#3** — Empty frontmatter `alt`/`caption` silently passed through | 🟠 New; real production impact (caused PM hand-edit recovery yesterday). Fix: warn loudly + exit non-zero unless `--force` | ~30 min |
| **Proposal** — CLI feature corpus (fixture pairs + test runner for regression coverage) | 💭 Worthwhile; ~2 hr for initial harness + ~15 entries | ~2 hr |

## Proposed sequence (surfacing to PM before plunging)

Two competing pulls:
- Yesterday's pickup state: CLI B walking-skeleton (~3hr) is the natural next
- Today's inbox: Gap 2 + Gap 3 are small + real (especially Gap 3 caused yesterday's recovery work); corpus is "nice but bigger"

Lean: knock out Gap 2 + Gap 3 as a small batch (~1hr) FIRST, send a quick reply to Docs acknowledging Gap 1 fixed + the two new fixes + corpus deferred, THEN start CLI B walking-skeleton (~3hr). Corpus is a separate follow-up after CLI B walking-skeleton lands.

## Pending

- Surface plan to PM, get steer
- Execute approved sequence
