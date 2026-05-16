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

_None yet. Will accumulate here as I hit them._

## Subtasks (sub-commit checkpoints)

- [ ] **1. Skeleton + arg parsing** — file header, ESM imports, arg parser (`--draft`, `--image`, `--category`, `--slug`, `--mode`, `--next-teaser`, `--report`, `--dry-run`), help text, validation
- [ ] **2. Draft parsing** — YAML frontmatter detection + parse; HTML comment fallback for `image`/`alt`/`caption`; H1 title extraction; body extraction (everything after frontmatter + title); strip metadata comments only
- [ ] **3. Markdown → HTML conversion** — heading promotion (`#` → `<h1>`, `##` → `<h2>`, `###` → `<h3>`, strip first H1 = title); paragraphs with inline `**bold**` / `*italic*` / `[links](url)`; em-dash `--` → `—`; `---` → `<hr>`; blockquotes (`>`); markdown tables; multi-line `<br />` blocks; ordered/unordered lists; preserve non-metadata HTML comments
- [ ] **4. hashId generation** — `crypto.randomBytes(6).toString('hex')` for blog-first; hex-only check
- [ ] **5. Image prep** — try `cwebp -q 80` first (with `sips -Z 1200` pre-step on macOS); fall back to Python Pillow subprocess; skip entirely for ship category
- [ ] **6. CSV append** — read header, validate 13 columns, append row with proper quoting (use the existing parseCsvRow round-trip logic); idempotency check on hashId/slug
- [ ] **7. blog-content.json write** — canonical dict shape `{title, content}`; idempotent overwrite; preserve other entries
- [ ] **8. Wire sync + fetch** — spawn `node scripts/sync-csv-to-json.js && node scripts/fetch-blog-posts.js`, capture exit codes
- [ ] **9. Edit-pass mode** — `--mode=edit-pass --hash-id=<existing>` short-circuits to Step 3 + Step 7 only
- [ ] **10. JSON exit report** — when `--report=json`, emit a final stdout JSON line: `{ok, slug, hashId, url, files_mutated: [...], skipped: [...], duration_ms}`
- [ ] **11. `--dry-run` mode** — log all intended mutations without writing files; emit the same JSON report shape
- [ ] **12. README / inline docstring** — top-of-file usage block; one-line example for blog-first, ship, and edit-pass; no separate README file (per project no-docs-unless-asked guideline)
- [ ] **13. Smoke test** — run against a synthetic draft + image to verify the pipeline end-to-end; report results in chat
- [ ] **14. Skill update** — `publish-to-blog/SKILL.md` v0.9 → v0.10 patch: replace Steps 3–5 mechanical procedure with `node scripts/publish-post.js …` invocation; keep the higher-judgment steps (voice-pass, syndication, etc.) intact

## Out of scope for this script (per scoping)

- Voice-pass gate / quality scrub (skill, manual)
- Medium syndication, LinkedIn cross-post (skill, manual)
- Editorial calendar updates (`/update-calendar` skill in product repo)
- Footer "Next on" teaser selection (judgment-bearing; PM via edit-pass)
- Drafts folder archival (skill Step 9, manual)
- Commit + push (PM / skill)

## Checkpoint commits

_Will list commit hashes here as they land._
