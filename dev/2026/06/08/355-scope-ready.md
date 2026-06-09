# #355 DOCS-STOPGAP — scope (verify-first complete, build-ready)

**Author**: Lead Dev · **Date**: 2026-06-08 · PM disposition: finish standalone now (not folded into #313).
**Status**: verified + unblocked; ready to build as a fresh focused unit.

## Verified facts (the seam)
- File infra ALL wired (audit): `UploadedFileDB` + `FileRepository` (owner-scoped, #470) + `/files` browser (`templates/files.html`) + upload/list/download/delete APIs (`web/api/routes/files.py`).
- **Upload contract**: `POST /api/v1/files/upload` takes **multipart `file: UploadFile`** (not inline text) + checks `ALLOWED_MIME_TYPES` — which **includes `text/markdown` + `text/plain`** (files.py:34-39). ✓ unblocked.
- Chat render seam: `web/static/js/chat.js` + `templates/home.html` (assistant messages rendered here).

## The gap (all that's left)
The chat-side "Save as artifact" affordance — everything else exists.

## Build plan (small, ~1-2h)
1. **chat.js**: when rendering an assistant message with content length > 500 chars, add a "Save as artifact" button to the message actions.
2. **On click**: build a client-side `File([messageText], "<derived-name>.md", {type: "text/markdown"})` → `FormData` → `POST /api/v1/files/upload` → success/error toast (toast helper already used in files.html). Derive filename from first line / timestamp.
3. **Confirm** the chat message DOM carries the raw text (not just rendered HTML) to save — check chat.js message model.

## Tests
- **template.render() test** (per UI-fix discipline / the whack-a-mole memory): render home.html with a realistic context, assert the button markup + threshold logic present — NOT just curl-200.
- JS unit if there's a JS test harness; else the render test + manual.
- **Live UAT** (click → file appears in /files): deferred to the **#1165 gate** (needs authenticated browser), same pattern as the other UI items.

## Why captured-not-built (2026-06-08 ~4pm)
PM-present client-primary-Monday, end of a very large shipping day. UI work specifically benefits from the live render+UAT loop (the documented whack-a-mole risk when UI is shipped without real render verification). Captured build-ready so a fresh block builds immediately. (Pure proceed-readiness, not a blocker.)
