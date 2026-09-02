# pmorgan.tech scoping proposal — curate the public docs site to its visitor-facing surface

**Author**: Docs · **Date**: 2026-08-12 · **Status**: **RATIFIED + APPLIED** — CIO ratified
2026-08-12 ~16:5x PT with one change (judgment call 3: `user-guide.md` moved to EXCLUDE, agreeing
with Docs's own recommendation; calls 1–2 kept as proposed, with CIO's file-level-discretion
condition on `testing/` recorded below). `_config.yml` change applied same evening. · **PM**: plan
approved 2026-08-12.

> **CIO's condition on `testing/` (keep)**: if the scrub pass finds genuinely internal-ops content
> mixed in (CI infrastructure specifics, methodology-as-code internals, cohort-context-assuming
> files), pull those specific files rather than the whole directory — Docs's scrub-phase
> discretion, made explicit.

## The problem, one paragraph

pmorgan.tech (GitHub Pages, Jekyll, serving `/docs` on `main`) is the "documentation site" every
Weekly Ship P.S. points readers at. What a visitor actually gets: a page titled
`piper-morgan-product` (the repo slug — no site title configured), rendering nearly the whole
1,814-file docs tree — 740 files of `internal/` (ADRs, ops runbooks, sprint planning, the
editorial calendar with candid working notes rendered as HTML), 146 cross-pollination briefs, 30
role briefings, 11 reboot handoffs — with the ~160 genuinely visitor-facing pages drowning in it.
**This is a curation problem, not a privacy one**: the repo is public by design ("Yes, you can
copy it"), so nothing here is secret; it's that the site has no editorial stance about what it
*is*. The current `_config.yml` exclude list is a 9-pattern denylist whose one big save (the 443
omnibus logs) is a filename-pattern accident (`**/*log*.md`), and it has never had a deliberate
pass — which is also how the build sat dead for 2.5 months unnoticed (fixed by Janus 2026-08-12).

## The principle

**The docs site is product documentation for visitors, alpha testers, and developers. The working
corpus stays on GitHub, one click away, for anyone who wants the open-development view.** Scoping
the *site* does not hide anything — it gives the site a legible purpose.

## Proposed scope

### EXCLUDE from the build (working corpus — ~1,655 files)

| Surface | Files | Rationale |
|---|---|---|
| `internal/` | 740 | ADRs, methodologies, ops, planning, comms working material — team-facing |
| `omnibus-logs/` | 443 | Already excluded by pattern accident; make it explicit and deliberate |
| `public/comms/` | 208 | Blog drafts + published-draft archive + calendar working files — the *blog* is the public face of these, at pipermorgan.ai |
| `briefs/` | 146 | Cross-project agent briefs — team-facing |
| `operations/` | 58 | Duty-cycle design, cohort ops — team-facing |
| `briefing/` | 30 | Role briefings — agent-facing |
| `refactor/` | 8 | Completed refactor project's dated artifact trail |
| `handoff-*.md` (top level) | 11 | Reboot-day handoffs — agent-facing, transient |
| `agent-protocols/` | 6 | Agent-facing procedure docs |
| `processes/` | 3 | Internal env-sync/migration checklists |
| `reference/` (singular) | 1 | Pard's fleet runbook — infra-facing |
| `research/` | 1 | Internal MCP evaluation (2026-03) |
| `00-START-HERE-LEAD-DEV.md` | 1 | Agent-facing |

### KEEP in the build (visitor-facing surface — ~160 files)

- **Index**: `README.md` (already a decent front door; scrub in progress) + a real `title:` in
  `_config.yml`
- **Alpha testers**: `ALPHA_QUICKSTART`, `ALPHA_TESTING_GUIDE`, `ALPHA_FEATURE_GUIDE`,
  `ALPHA_KNOWN_ISSUES`, `ALPHA_AGREEMENT_v2`, `alpha/` (2)
- **Getting started / users**: `public/getting-started/` (8), `public/user-guides/` (16),
  `user-guide.md`, `guides/` (15), `installation/` (7), `setup/` (2), `troubleshooting/` (2) +
  `troubleshooting.md`, `features/` (5), `integrations/` (3), `configuration/` (2)
- **Developers**: `api/` (3), `public/api-reference/` (7), `TECHNICAL-DEVELOPERS.md`,
  `CONTRIBUTING.md`, `dev-tips/` (5), `TESTING.md` + `testing/` (7), `security/` (1),
  `api-key-management.md`, `database-production-setup.md`, `public/migration/` (1) +
  `migration/` (3), `VERSION_NUMBERING.md` + `versioning.md`
- **Record**: `releases/` (19), `legal/` (1), `accessibility/` (3), `references/` (2, citations)
- ~~`legacy-getting-started/` + `legacy-user-guides/`~~ **moved to EXCLUDE 2026-08-13**
  (post-ratification, Docs, same consistent-with-principle basis): self-described legacy/
  historical archives whose remaining broken links (12, all pre-reorg directory targets that
  never existed post-reorg — the #1584 flagged-residual class) make them worse-than-absent on a
  curated visitor site. They remain on GitHub as the historical record. Flagged, not silent.
- ~~`NAVIGATION.md`~~ **moved to EXCLUDE 2026-08-12** (post-ratification, Docs, consistent with
  the ratified principle rather than a scope expansion): its own header declares it
  internal-audience ("Agents, developers, architects, and internal contributors") and points
  visitors to README.md — and nearly everything it maps is in the excluded corpus. Rewriting it
  into a second visitor nav would duplicate README. It stays the internal navigation surface on
  GitHub; site-exclusion note added to its header, rot-prone counts stripped (all were stale when
  checked). Flagged to CIO for the record rather than silently applied.
- **Assets**: `assets/` (images used by kept pages)

### Judgment calls flagged for CIO (not silently decided)

1. **`testing/` + `TESTING.md`** — some content is internal test-ops rather than contributor
   docs; kept by default, CIO may pull either way.
2. **`dev-tips/`** — developer-facing but written team-inward; kept by default.
3. **`user-guide.md`** *(added 2026-08-12 after investigation)* — content is an aspirational
   "1.0 / production-ready" doc from 2025 that would mislead alpha testers; now carries an honest
   staleness banner pointing at the Alpha guides. **Recommend EXCLUDE until rewritten** (moves
   from the keep-list) — CIO to confirm with the rest of the scope.

### Duplicate pairs — investigated and resolved 2026-08-12 (no longer open calls)

- **`VERSION_NUMBERING.md` / `versioning.md`** — NOT duplicates: scheme vs. release strategy,
  both current (same 2026-07-17 commit), each with live referrers (alpha docs / the
  version-consistency script). Cross-linked with a two-docs-deliberately note in each header.
- **`troubleshooting.md` / `troubleshooting/`** — complementary (general guide vs. topic guides),
  but the directory README was auto-generated boilerplate that never mentioned the main guide.
  Rewritten as an honest two-surface index.
- **`user-guide.md` / `public/user-guides/`** — not a pair; the real problem was `user-guide.md`'s
  stale content (see judgment call 3 above).
- **`migration/` / `public/migration/`** — misleadingly-named but entirely different topics
  (account/router migration vs. an error-handling code-migration guide). Left as-is; the scoped
  site keeps both.

## Mechanics

One `_config.yml` change — extend `exclude:` with the 13 surfaces above (directory names + the
handoff/start-here globs), add `title: Piper Morgan Documentation`, keep the existing log/session
patterns as belt-and-suspenders. Fully reversible; no file moves; no content edits; GitHub
unaffected. The Pages build re-runs on push, and the result is verifiable the same way the
2026-08-12 revival was (run conclusion + spot-URL checks — a kept page 200s, an excluded page
404s).

## Status update, 2026-08-14: phase-2 staleness/link pass COMPLETE (Docs dimension)

Every KEEP surface swept across 6 batches (08-13/08-14): ALPHA_* · guides/+getting-started ·
features/+integrations/+configuration (with Comms tier-5) · installation/+setup/+troubleshooting
(with Comms tier-6) · api/+api-reference/+dev-tips · testing/+releases/+top-level (final; 42
files, 0 broken links; testing/ passed CIO's file-discretion check — 0 internal-signal hits in
all 7 files, no pulls needed). Totals across the pass: ~40 broken/wrong links repointed or fixed,
2 stale-content banners (feature-guide → PA-verified refresh in progress; user-guide → excluded),
5 phantom screenshots neutralized, the 64-file Documentation-Home pattern fixed in KEEP scope,
1 internal-audience warning rehomed, PM-NNN historical IDs glossed. Comms's register dimension
continues at their cadence (their remaining tiers overlap surfaces Docs has already link-swept).

## Sequencing (per the approved 3-phase plan)

1. **This doc ratified** → apply the `_config.yml` change (Docs) → verify build + spot URLs.
2. **Scrub the kept ~160 pages** (Docs, batched): README first (in progress), then NAVIGATION.md
   rewrite, then the duplicate pairs, then staleness/link pass per surface. Comms register pass
   rides on the scrubbed pages, not the pre-scrub ones.
3. **Guard rails**: #1593 (link-checker gate) wired for the kept surface; a scoping note in
   CONTRIBUTING ("what lands in the public build"); the exclude list gets an owner (Docs) and a
   review trigger (any new top-level directory in `docs/`).

## Status: ALL THREE PHASES COMPLETE (verified 2026-09-02)

Phase 1 (config + verify) and Phase 2 (scrub, logged complete 2026-08-14 above) were already done.
**Phase 3 (guard rails), verified complete today**: #1593 (link-checker gate) CLOSED;
`docs/CONTRIBUTING.md` carries the two-surfaces scoping note; `docs/_config.yml`'s `exclude:`
block carries the owner (Docs) + review-trigger (any new top-level `docs/` directory) comment.
**Live-verified**: `https://pmorgan.tech/` (kept surface) → 200; an excluded `internal/` page and
`NAVIGATION.html` → 404, both exactly as designed. Nothing further owed on this project.

## Division of labor (PM-set, 2026-08-12)

- **Docs**: execution — config, README, navigation, scrub, verification. Owns this doc.
- **CIO**: ratify/adjust the in/out scope above (governance of the project's documentation face).
- **Comms**: register/voice pass on kept visitor-facing pages after scrub (public-prose
  expectations now apply to them).
