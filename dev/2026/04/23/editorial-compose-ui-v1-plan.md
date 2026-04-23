# Editorial Compose UI — v1 Plan

**Opened**: 2026-04-23, ~7:45 AM
**Status**: Planning — awaiting PM sign-off before any code
**Owner**: Docs (orchestrator) + subagents for implementation chunks
**Related**: publish-to-blog skill v0.8 (the pipeline this tool hands off to); editorial calendar at `docs/internal/planning/comms/editorial-calendar.csv`; drafts at `docs/public/comms/drafts/`

---

## Problem

PM's current publish-editing workflow has three friction points that recur almost every publish:

1. **Placeholder sweep** — drafts contain `[ADD PERSONAL DETAIL]` and `[CONSIDER]` markers that PM must hand-resolve before publish. Easy to miss one.
2. **Metadata block editing** — image / alt / caption live in HTML comments or YAML frontmatter that PM hand-edits. Easy to typo (e.g., "leads as small boat" Apr 22) or forget a field.
3. **Handoff ambiguity** — "we're publishing today" signals PM intent but not actual handoff; Docs has repeatedly pre-scanned before PM finished editing (fixed by feedback memory `feedback_wait_for_publish_handoff.md` but the underlying cowpath friction remains).

The fix is a lightweight web UI that paves these three cowpaths: draft-aware editing surface, form-driven metadata, and an explicit "ready" signal that becomes an unambiguous commit Docs can watch for.

## V1 Scope (explicit in-scope)

- **Web page** served from existing FastAPI at `http://localhost:8001/admin/compose`
- Lists **posts needing finishing** pulled from `editorial-calendar.csv` (rows where `status=drafted` and `pubDate` is today or within N days)
- Opens a post in a **simple editing surface**: textarea for body (plain, no WYSIWYG), form fields for metadata (image filename, alt text, caption, footer tease)
- **Autosave** to `docs/public/comms/drafts/{slug}.md` every ~30 sec or on pause; writes YAML frontmatter + body
- **Image upload** — file-input saves to `docs/public/comms/drafts/{slug}.{ext}` alongside the markdown
- **"Mark ready" action** — commits the draft + image to main (message: `editor: mark {slug} ready for publish`), pushes to origin, updates calendar row status `drafted` → `ready`. This commit is the Docs handoff signal.
- **Footer-tease helper**: form field pre-populated with `Next on Building Piper Morgan: {title of next calendar row} — ...` that PM edits or overrides
- Local-only (no auth needed — `localhost` binding is sufficient)

## Out of v1 (explicitly deferred)

- WYSIWYG / rich-text editor (v2)
- Markdown preview pane (v2 — nice-to-have, not required)
- Auto-publish triggered by "ready" (v2+; v1 keeps Docs as the pipeline runner)
- Auto-syndication to Medium / LinkedIn (v3)
- Auto-capture syndication URLs back into the calendar (v3)
- Multi-user / remote access (v4+ if ever)
- Undo / version history within the UI (use git)
- Inline-image insertion in body (depends on skill v0.8's new preserve-HTML-comments behavior being exercised; defer)
- Placeholder-sweep verification ("block ready if `[ADD PERSONAL DETAIL]` still in body") — small enough it could slip into v1 if trivial; otherwise v1.1
- Staggered scheduling / calendar management from inside the UI (v3)

## Architecture

```
piper-morgan-product/
├── web/
│   ├── app.py                       # existing FastAPI, unchanged except for router registration
│   ├── routers/
│   │   └── admin_compose.py         # NEW — all /admin/compose routes
│   ├── templates/admin/
│   │   └── compose.html             # NEW — Jinja2 template with form + textarea
│   └── static/admin/
│       ├── compose.css              # NEW — minimal styling
│       └── compose.js               # NEW — autosave, form handling
└── services/
    └── editorial/
        ├── __init__.py              # NEW — module marker
        ├── calendar.py              # NEW — read/write editorial-calendar.csv
        ├── draft.py                 # NEW — parse/write markdown + YAML frontmatter
        └── git_ops.py               # NEW — commit-and-push wrapper for "ready" action
```

**Dependencies** (all already in requirements.txt or standard library):
- FastAPI (present)
- Jinja2 (present)
- Python standard library `csv`, `subprocess`, `pathlib` — no new pkg
- Frontend: plain HTML + vanilla JS, no build step (no React/Vue/etc for v1)

**Data flow**:
```
PM opens /admin/compose
   → GET /admin/compose renders list of drafted rows from calendar
PM clicks a post
   → GET /admin/compose/{slug} renders compose.html with the parsed markdown + metadata fields
PM edits body or metadata
   → POST /admin/compose/{slug}/save  → autosave writes file; returns 200
PM uploads image
   → POST /admin/compose/{slug}/image → saves to drafts/ alongside markdown
PM clicks "Mark ready"
   → POST /admin/compose/{slug}/ready → validates (image present? body non-empty?) → git add/commit/push → calendar CSV update → returns success
```

**No database, no state beyond filesystem.** Server restarts are harmless. `git status` always tells the truth about where things are.

## Phases

Suggest building in four phases, each independently shippable and PM-testable:

### Phase 1 — Scaffolding + Read (~1 small subagent task)
- Wire up router, templates dir, static dir in `app.py`
- `services/editorial/calendar.py`: read drafted rows from CSV
- `services/editorial/draft.py`: parse `.md` into `(frontmatter dict, body string)`
- `GET /admin/compose`: list view
- `GET /admin/compose/{slug}`: detail view, renders form pre-populated but read-only
- **Validation**: PM opens `localhost:8001/admin/compose`, sees the drafted rows, can click through to view a draft with metadata parsed out. No editing yet.

### Phase 2 — Edit + Autosave (~1 medium subagent task)
- `POST /admin/compose/{slug}/save`: writes back YAML frontmatter + body to file
- `compose.js`: autosave on textarea + form field change (debounced)
- **Validation**: PM edits in UI, saves, checks file on disk reflects changes.

### Phase 3 — Image Upload (~1 small subagent task)
- `POST /admin/compose/{slug}/image`: file-input handling, writes to drafts/ alongside `.md`, updates frontmatter `image:` field
- **Validation**: PM uploads a PNG, confirms it lands in drafts/ with correct filename, confirms frontmatter references it.

### Phase 4 — Mark Ready + Git Handoff (~1 medium subagent task)
- `POST /admin/compose/{slug}/ready`: validates (image exists? body non-empty? frontmatter complete?), git add + commit + push, updates calendar row status → `ready`
- Error handling: if push fails (e.g., SSH port 22 blocked — see CLAUDE.md workaround), return clear error to UI
- **Validation**: PM hits ready, observes commit on origin/main, Docs sees the commit land and runs publish pipeline as before.

**Nice-to-have folded into Phase 4 if easy**:
- Placeholder-sweep check (block ready if body still contains `[ADD PERSONAL DETAIL]` / `[CONSIDER]` / similar markers unless PM overrides)

## Build approach — orchestrated subagents

Recommended execution model: **Docs orchestrates, Task-tool subagents implement phases**.

**Why subagents rather than Docs writing it directly**:
- Docs role is documentation + coordination + review, not production code. I can write the code, but each large implementation chunk pulls me out of the Docs lane.
- Subagents with tight, bounded briefs keep the main Docs context clean (no 800 lines of FastAPI cluttering the conversation). Better for the long-running session continuity.
- Review-and-integrate is a natural Docs-fit: each subagent returns a diff / commit, I verify against the phase spec, commit or iterate.
- Keeps Lead Dev fully on #992 ETHICS-ACTIVATE Phases E-H without diverting them.

**Why not just spin up a dedicated Coding Agent top-level session**:
- Could — but the phases are small enough that dispatching subagents from here is faster than context-loading a fresh session.
- If v2/v3 becomes substantial, spinning up a Coding Agent session is the right move. For v1 four small phases, subagents suffice.

**Execution proposal**:
1. PM approves this plan
2. Docs files a tracking issue (`EDITORIAL-COMPOSE-UI-V1` or similar) so the work has a GitHub home
3. Phase 1 subagent brief written by Docs; subagent writes code; Docs reviews + commits + reports to PM
4. PM tests Phase 1 at `localhost:8001/admin/compose`; reports fit / gaps
5. Repeat for Phases 2-4

**Subagent brief template** (each phase):
- Scope (what to build, what NOT to build)
- Files to create / modify (explicit paths)
- Conventions (YAML frontmatter format per skill v0.8, error handling style, test expectations)
- Acceptance (PM-testable behavior)
- Out-of-scope explicit callouts (prevent scope creep)

## Success criteria for v1 as a whole

PM can:
- Open `localhost:8001/admin/compose`
- See the drafts needing finishing pulled from the calendar
- Click into a draft, resolve placeholders, fill in metadata via form fields, upload an image
- Autosave works without hand-saving
- Click "Mark ready," see the commit land on origin/main
- Docs still runs `publish-to-blog` pipeline against the committed draft (no skill change needed for v1 — the markdown file is the canonical input, same as today)

Measured improvement over current workflow: zero hand-editing of HTML-comment or YAML metadata blocks; one-click handoff to Docs instead of rename + "edit done" message; image upload via file-picker instead of drag-to-drafts-folder.

## Risks

1. **FastAPI app already serves the Piper product** — admin routes share that process. Probably fine for localhost, but if the product server crashes, the admin UI dies with it. Mitigation: admin routes are separate router, low traffic, unlikely to affect main surface. Monitor in v1; separate if it becomes a problem.
2. **Git operations from inside a web handler** could block if SSH hangs. Mitigation: timeout + clear error surface; reuse the SSH-over-443 workaround pattern from CLAUDE.md if needed.
3. **Autosave + concurrent edit** — if Docs reads the draft while PM is mid-autosave, partial state visible. Mitigation: `feedback_wait_for_publish_handoff.md` already says Docs doesn't read until "ready"; v1 relies on this behavioral norm. If it bites, add atomic-write (write-to-tempfile + rename).
4. **Calendar CSV corruption** — direct write to CSV has risk. Mitigation: use Python's `csv` module (not `echo >>`), write-to-tempfile + rename, keep a `.backup` per edit (matches pattern used by `sync-csv-to-json.js` in the website repo).

## Decisions needed from PM

- [ ] Approve this plan as v1 scope
- [ ] Approve the orchestrated-subagent execution model (vs. alternative: spin up a dedicated Coding Agent session)
- [ ] Name preference for the tool / route — I've been calling it `/admin/compose`; alternatives: `/admin/editor`, `/admin/editorial`, `/admin/workbench`, something else
- [ ] File GitHub issue for tracking? (My recommendation: yes, so the phases have a home and the subagents can reference an issue number in commits)
- [ ] Which phase boundary gets real testing stops (all four? just 1 and 4?)

## Non-decisions (these can be deferred)

- Styling / visual design — plain functional CSS in v1; polish later
- Error message copy — just-works-enough in v1
- Form field order on the compose page — reasonable default; iterate based on PM use
- Exact autosave interval (30s? 60s? on-blur?) — pick a reasonable default, tune by feel

---

*This plan is a working document; amend as PM reactions land. Commit this file once PM approves and wants it in the record.*
