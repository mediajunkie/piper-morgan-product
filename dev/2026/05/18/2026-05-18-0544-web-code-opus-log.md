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

## Pending (was)

- Surface plan to PM, get steer
- Execute approved sequence

---

## 06:30 → 07:55 — three shipments per PM-approved sequence

PM approved the small-batch sequence at 05:50ish. Executed:

### Commit — website `aafe85a72` — Gap 2 + Gap 3

- **Gap 2** (block-level HTML pass-through): new branch in `convertToHtml` that detects lines starting with a block-level opening/closing tag (ol, ul, table, blockquote, pre, details, figure, aside, div, section, article, header, footer, nav, hr, p) and treats them as a raw-HTML run — collect consecutive non-blank lines, emit joined with `\n`, no `<p>` wrap, no `<br />` injection.
- **Gap 3** (empty-frontmatter alt/caption silent pass): pre-mutation check in publish mode (skipped in edit-pass and ship category). Exits non-zero with clear warning unless `--force`. New `isEmptyMetaValue` helper that treats quote-only-and-whitespace as empty (catches `''`, `""`, `'""'` placeholders).
- New `--force` flag added.
- Inchworm byte-exact regression still holds.

### Reply memo + log — product `0d7e9947a`

Memo to docs CC PM/PA: all 3 gaps closed (Gap 1 was already shipped at `5c2bad168` yesterday before they wrote the memo), corpus proposal accepted-and-sequenced, sized at ~2hr. Today's session log opened.

### Commit — website `bdee28bbf` — CLI B walking-skeleton

New files:
- `scripts/lib/queue.js` — engine module (per keep-shells-thin): `readCalendar()`, `getQueue()` (sorted asc by pubDate, undated to end), `slugify(title)`, `findDraftFile(slug)` (per skill v0.12 filename convention), `findImageForDraft(draftPath, slug)` (PNG/JPG/JPEG/WEBP matching slug), `themeToCategory(theme)`.
- `scripts/publish-cli.js` — orchestrator using `@inquirer/prompts`. Flow: pick from queue → confirm slug/draft/image paths → dry-run preview → confirm proceed → real publish (capture JSON report) → show git diff → commit prompt (y/e/N, default N) → auto-message `Add blog post: {title}`.
- `package.json`: `npm run publish` wired.
- `@inquirer/prompts` added as dep.

Honors resolved design decisions #1, #5, #6 from yesterday's discussion.

### Commit — website `2758093e1` — feature corpus harness + 15 entries

Per Docs's 5/17 proposal:
- `scripts/test-publish-post-corpus.js` — runner: iterates `publish-post-corpus/NN-name/` subdirs (each has source.md + expected.html); invokes `publish-post.js --dry-run --force`; extracts HTML preview from stderr; diffs against expected; per-entry pass/fail; exits non-zero if any fail. Single-entry debug via positional arg.
- 15 corpus entries: headings, paragraphs (single + multiline-br), bullet/numbered lists, inline formatting (bold/italic/code/link), em-dash, hr, blockquote, block-HTML multiline + singleline (Gap 2), standalone italic, table, HTML-comment preservation (v0.8 rule), mixed-blocks kitchen-sink.
- All 15 pass against current implementation.
- Wired as `npm run test:corpus`.

### Commit — product `1d9c7256c` + `390f1749f` — plan updates

HTML plan updated twice: first to reflect Gap 2/3 + walking-skeleton, then to reflect corpus. Current state: 14 shipped / 1 enriching / 0 queued / 1 deferred.

## 08:00+ — Docs memo response received

Docs replied at 06:25 with six observational answers to my feedback ask, drawn from yesterday's *Protocol* publish. Key signals for enrichment-pass design:

1. **Cross-repo path mental model is the friction**, not flag syntax. Slug-keyed fuzzy picker (already in CLI B) addresses.
2. **`--dry-run` validated** — caught real bug yesterday. Skill v0.13 codifies as mandatory; CLI B inherits.
3. **`--report=json` unused for publish step but high-value for structured handoff** — publish-post.js JSON should feed into `/update-calendar` next-step. **Implication for enrichment**: the Docs-notify memo body should include the structured JSON so the next /update-calendar invocation has the fields ready.
4. **Four warn-before-mutate prompt strings** Docs identified, ready to drop into CLI B verbatim:
   - `Image '{filename}' not found at docs/public/comms/drafts/. Search ~/Downloads? [Y/n/abort]`
   - `Frontmatter alt is empty. This is almost certainly an oversight. [a]bort / [c]ontinue / [e]dit frontmatter`
   - `Numbered list detected at line {N}. Known gap: ... [a]bort to fix / [c]ontinue with inline-HTML workaround / [s]hip anyway` (now moot — Gap 1 fixed — but pattern applies for future gaps from feature corpus)
   - `altText contains an unescaped comma. ... [a]bort / [q]uote it for me`
5. **Wall-clock baseline**: ~4 min pure publish, ~15-20 min with overhead. CLI B target: ~5 min pure operator time.
6. **Four orchestration handoffs** post-publish, three covered by CLI B per yesterday's design. **NEW scope candidate**: `--mode=archive` for Step 9 drafts archival (precondition: calendar status=published + at least one syndication URL). Deferred per PM-approval-for-scope-additions.

## Pending (now)

1. Brief reply memo to Docs (file-and-forget acceptable per their close, but courtesy ack is right shape)
2. Update CLI B sketch with the new enrichment-design signals (pre-flight checks vocabulary + JSON-in-memo)
3. Start enrichment build per PM "yes let's proceed in parallel"
