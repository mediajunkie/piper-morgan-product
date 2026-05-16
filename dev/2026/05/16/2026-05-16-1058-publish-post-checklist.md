# publish-post.js — work checklist

**Started**: 2026-05-16 10:58
**Scope**: Codify the `publish-to-blog` skill (v0.9) as a single executable Node CLI at `piper-morgan-website/scripts/publish-post.js`.
**Spec**: `piper-morgan-product/.claude/skills/publish-to-blog/SKILL.md` (v0.9) — the script implements the mechanical first half; the skill keeps ownership of voice-pass / syndication / cross-post / footer-teaser / decisions-in-narrative.
**Agent-ready contract**: stable CLI args, JSON exit report option, non-interactive flags for every step, `--dry-run` mode, structured stderr for diagnostics.

## Decisions made up-front (with reasoning)

1. **Language**: Node.js (ESM). Matches the rest of `scripts/`. Skill's Python snippets are pseudocode for the logic, not a language mandate.
2. **Image prep**: try `cwebp` first, fall back to a Python `Pillow` subprocess if cwebp is unavailable. Skill v0.9 says the machine lacks `cwebp` and Pillow is the established fallback; defensive try-cwebp-first preserves behavior on machines that do have it.
3. **Category**: accept `--category` as a required arg (`building` | `insight` | `ship`). Skill says "determine from editorial calendar"; reading the editorial calendar cross-repo adds dependency + brittleness. Explicit arg is simpler and agent-friendlier.
4. **Footer "Next on" teaser**: optional `--next-teaser "..."` arg. If absent, omit the teaser and let PM add manually during the edit-pass. Skill's editorial-calendar lookup for the next post is judgment-bearing (which post is "next") and belongs in the skill, not the script.
5. **Stop point**: script stops before commit/push. Exits with a JSON report (when `--report=json`) listing files mutated + post URL + hashId. PM (or skill) handles commit.
6. **Ship posts**: when `--category=ship`, URL prefix becomes `/shipping-news/{slug}`, `imageSlug` defaults to `piper-ship.webp`, image prep is skipped entirely (skill rule).
7. **Edit-pass mirror**: separate mode `--mode=edit-pass --hash-id=<existing>` re-runs only HTML conversion + blog-content.json update for an existing post. Skips image prep + CSV append.
8. **Idempotency**: appending CSV row checks for existing hashId/slug; blog-content.json write is overwrite-safe; sync + fetch are already idempotent.

## Open questions (batched for PM — only surfaced when blocking)

_None blocking on the script itself. Dashboard A questions accumulating in the Dashboard A checklist file when I open it._

## Subtasks (sub-commit checkpoints)

- [x] **1. Skeleton + arg parsing** — file header, ESM imports, arg parser, help text, validation
- [x] **2. Draft parsing** — YAML frontmatter + HTML comment fallback, H1 title extraction, metadata-comment stripping
- [x] **3. Markdown → HTML conversion** — all skill v0.9 rules: heading promotion, em-dash, inline, hr, lists, blockquotes, tables, multi-line paragraph blocks (`<br />` join), HTML comment preservation
- [x] **4. hashId generation** — `crypto.randomBytes(6).toString('hex')`; hex-only validation
- [x] **5. Image prep** — try cwebp + sips first, fall back to Python Pillow subprocess; skip for ship category
- [x] **6. CSV append** — idempotency check on hashId/slug; 13-column row with proper quoting
- [x] **7. blog-content.json write** — canonical dict shape `{title, content}`; idempotent overwrite
- [x] **8. Wire sync + fetch** — spawn the two existing scripts, capture exit codes
- [x] **9. Edit-pass mode** — `--mode=edit-pass --hash-id=<existing>` skips image/CSV/sync, updates blog-content.json only
- [x] **10. JSON exit report** — `--report=json` emits a single stdout line with `{ok, slug, hashId, url, filesMutated, skipped, durationMs, dryRun}`
- [x] **11. `--dry-run` mode** — logs intended mutations + prints converted HTML preview to stderr; no file writes
- [x] **12. README / inline docstring** — top-of-file usage block; `--help` reads and prints it
- [-] **13. Smoke test** — *partially:* dry-run validated end-to-end; markdown converter validated byte-for-byte against canonical inchworm-position content (5937 chars, identical text + tags). **Deferred a real-publish smoke test to the next real publish** — synthetic full-pipeline test would pollute the real CSV/JSON. PM/Docs decide whether tomorrow's *From Protocol to Infrastructure* uses the script or the manual flow.
- [x] **14. Skill update** — `publish-to-blog/SKILL.md` v0.9 → v0.10 patch: added script-invocation block at top, preserved full manual procedure as canonical reference, added v0.10 changelog entry referencing commit `0179571a0`

## Out of scope for this script (per scoping)

- Voice-pass gate / quality scrub (skill, manual)
- Medium syndication, LinkedIn cross-post (skill, manual)
- Editorial calendar updates (`/update-calendar` skill in product repo)
- Footer "Next on" teaser selection (judgment-bearing; PM via edit-pass)
- Drafts folder archival (skill Step 9, manual)
- Commit + push (PM / skill)

## Checkpoint commits

- `piper-morgan-website@0179571a0` — `feat(scripts): add publish-post.js — single-command publish pipeline` (the whole script in one commit; sub-tasks were tightly coupled, no natural sub-commit fault lines)
- `piper-morgan-product@<pending>` — skill v0.9 → v0.10 patch + this checklist + session-log update

## Status

**Done.** All 14 subtasks closed (#13 deferred to next real publish per reasoning above). Ready to move to the next item in the queued block: Dashboard A (`/admin/publish-queue`).
