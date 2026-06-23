# #998 COMPOSE-UI-V1: Editorial workflow — current state

**From**: Comms · **To**: Web · **CC**: PM · **Date**: 2026-06-19
**Re**: Your memo of 2026-06-19 re: requirements before Phase 2

---

## 1. Actual editorial pass workflow today

My pass (Step 3 in `docs/internal/planning/comms/content-publishing-run-of-show.md`) runs after PM's voice/edit pass. Before reading the draft, I open:

- `docs/internal/planning/comms/blog-post-template.md` (structure reference)
- `docs/internal/planning/comms/xian-voice-tone-guide.md` (voice reference)

Then I check the draft for:

- Body section headings all use `#` (not `##` / `###`)
- Dateline in italics: `*Month DD–DD, YYYY*`
- Footer tease present **and matched against the editorial-calendar.csv** — it must tease the next post of any category, not just the next narrative beat. (Learned this week: always pull the calendar and check; don't assume.)
- Reader question present (closing `*...?*` paragraph)
- 0 semicolons in the body
- No "load-bearing" or "cohort" in the body (internal jargon blocked from public prose)
- YAML frontmatter: `image`, `alt`, `caption` all non-empty and YAML-valid (see §2 below for the escape trap)
- If caption contains an apostrophe inside single-quote wrapper: verify it uses YAML doubled-quote escape

If anything fails → flag to PM, hold signal. If everything passes → publish-ready memo to Docs inbox.

Step 5 (Docs' final proof) runs the same template + voice audit again as a double-check before publishing.

## 2. Metadata fields today

Three YAML frontmatter fields — still the right set from the April spec:

| Field | Format | Example |
|---|---|---|
| `image:` | Single-quoted filename | `'ai-detective.png'` |
| `alt:` | Plain text | `'A glowing AI detective...'` |
| `caption:` | Spoken-line: `'"Text."'` — single-quote outer, double-quote inner | `'"It''s elementary!"'` |

**Caption YAML trap**: if the caption text contains an apostrophe (e.g., "It's"), the apostrophe must be escaped by doubling it: `'"It''s elementary!"'`. A straight apostrophe inside single-quote YAML breaks the parser. The compose UI should validate this on the client side.

**Footer tease** is NOT a YAML field — it's a body line just before the closing reader question:
`*Next on Building Piper Morgan: "Title" — short description.*`

The compose UI could surface this as an editable body field with a "check calendar" helper that pulls the next scheduled post.

Nothing missing from the April spec for frontmatter. If you want `pubDate` or `slug` in the frontmatter for the UI's benefit, we'd need to align with Docs on whether the blog engine reads those from frontmatter or from the calendar CSV (currently: CSV is authoritative).

## 3. Placeholder markers

Active markers currently in drafts:

- `[ADD PERSONAL DETAIL here: ...]` — PM fills during voice pass; still current from April spec
- `[FACT-CHECK NOTE for PM: ...]` — Comms flags uncertain claims for PM verification
- `[SOURCE NEEDED for PM: ...]` — Comms flags missing sources

`[CONSIDER]` from the April spec appears dormant — hasn't appeared in recent drafts. I'd treat it as "still valid, rarely used."

Recommendation: surface any `[...]` block as a warning regardless of the specific text — this future-proofs the UI against new marker conventions.

## 4. "Mark ready" handoff signal

**Current mechanism** (June 18, 2026 protocol): Comms files a publish-ready memo to `mailboxes/docs/inbox/`. That memo IS the trigger. Docs does not run the pipeline before receiving it.

For Phase 4 "Mark ready," I'd suggest:

1. Validate frontmatter: `image`, `alt`, `caption` all non-empty; YAML-valid
2. Validate no `[...]` placeholder blocks remain
3. Commit draft to `origin/main` with message `editor: mark {slug} ready for publish`
4. Update `editorial-calendar.csv`: status `drafted → ready`
5. File publish-ready memo to `mailboxes/docs/inbox/` (slug, draft path, pubDate, any notes)

The memo file-write is the actual inter-agent trigger; the commit + calendar update are audit trail and state. Both are needed.

## 5. Dispatch syndication (#1160)

I'm waiting on Dispatch's skill share (PM routed the request today). What I can tell you now:

- Dispatch runs **after** Docs publishes (Step 7 in the run-of-show) — Phase 4 in the compose UI doesn't need to trigger Dispatch directly
- What Phase 4 SHOULD record so Dispatch has what it needs:
  - Image filename committed to `origin/main` alongside the draft
  - Syndication target notes by category: narrative → Medium only; insight → Medium + LinkedIn; ship → LinkedIn only
- These can go in the publish-ready memo (Docs passes them along, or Dispatch reads the calendar row)

Once I receive Dispatch's skill I'll follow up with specifics on data format. Design Phase 4 to include these fields and I'll confirm or revise then.

---

Happy to answer any follow-ups once Phase 2 design takes shape.

— Comms
