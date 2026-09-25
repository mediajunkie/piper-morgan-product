# Session Log — 2026-09-24 1704 — Coding Agent (prog) — web3

**Role**: Coding Agent (prog)
**Model**: Sonnet (dispatched by Lead, tier stated)
**Issues**: #1737, #1750, #1498
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: `templates/`, `web/static/`, `web/assets/`, `web/api/routes/ui.py`'s greeting-context only.
Not committing/pushing — Lead reviews and commits the explicit file set.

## Context

Three small, unrelated web-UI issues dispatched together. Two other lanes concurrently
editing other files in the same worktree (action_registry.py cohort; list-remainder/portfolio
render cohort in canonical_handlers.py / conversational_floor.py / intent.py / etc.) — confirmed
via `git status` those files are dirty from other lanes, not touched by me, ignored throughout.

## #1737 — chat composer: input → textarea, autogrow to ~6 rows, then scroll

**Files**: `templates/components/chat-widget.html`, `templates/components/chat-inline.html`,
`web/static/css/chat.css`, `web/static/js/chat.js`, `tests/unit/web/templates/test_chat_widget.py`

Found both live chat surfaces: `chat-widget.html` (floating widget, included by `nav_rail.html`
on every page) and `chat-inline.html` (home page's always-visible chat). Both had
`<input type="text" class="chat-input">`.

- Converted both to `<textarea rows="1" class="chat-input">` (attrs otherwise preserved:
  `name="message"`, `placeholder`, `autocomplete="off"`, `required`). `.value`/`.focus()` work
  identically on textarea, so most existing chat.js code needed no change.
- `chat.css` `.chat-input` rule: added `font-family: inherit`, `line-height: 1.4`,
  `resize: none`, `overflow-y: hidden` — no transition/animation added, so
  `prefers-reduced-motion` has nothing to disable (confirmed by a dedicated pin).
- `chat.js`: new `COMPOSER_MAX_ROWS = 6` + `autoGrowComposer(textarea)` (scrollHeight-driven,
  resets to `"auto"` first so it shrinks on delete, caps at `lineHeight * 6 + padding + border`,
  flips `overflow-y` to `auto` only past the cap). Wired into: the `input` event (grows as you
  type), submit (`input.value = ""` → collapse back to 1 row), `restoreDraftMessage`,
  `handleSessionExpired`, `setExample` (all three set `.value` programmatically and needed a
  matching resize).
- Enter/Shift+Enter: textarea doesn't submit-on-Enter by default (input did), so added a
  `keydown` listener: `Enter && !shiftKey && !isComposing` → `preventDefault()` +
  `form.requestSubmit()`. No prior IME-composition guard existed in this file to preserve —
  added fresh (`e.isComposing`). Shift+Enter needs no handler — default textarea behavior
  (insert newline) is exactly right.

**Pins added** (`tests/unit/web/templates/test_chat_widget.py`, new `TestComposerAutogrow1737`
class + updated the pre-existing `test_chat_input_type` → `test_chat_input_is_textarea`, which
was asserting the OLD `type="text"` and would have failed against the fix): textarea presence on
both templates, `rows="1"`, `resize: none` in CSS, no transition/animation on `.chat-input`,
`COMPOSER_MAX_ROWS = 6` + `autoGrowComposer` defined, `scrollHeight`-driven, wired on `input`
event, Enter-sends/Shift-Enter-newlines source pins, `isComposing` guard present, composer
collapses after send.

**Discovered (report only, not fixed)**: `chat-widget.html` and `chat-inline.html` both hard-code
`id="chatForm"` / `id="chat-window"` / `id="chat-container"`. On the home page BOTH components
render simultaneously (home.html includes chat-inline directly; app_shell → nav_rail includes
chat-widget on every page). Pre-existing duplicate-ID collision — `document.getElementById`
silently grabs only the first match, so only one of the two forms actually gets chat.js's submit
wiring on home. Not introduced or worsened by this fix (my `autoGrowComposer` calls are all
scoped via `form.querySelector`, not `getElementById`, so they're unaffected), but worth a
tracking issue if not already filed.

**Gates**: `tests/unit/web/templates/test_chat_widget.py` 132 passed. `ruff check`/`format` clean.
`node -e "new Function(...)"` on `chat.js` — syntax OK.

**Verified how**: method = pytest + node syntax check on the actual files; layer = source-level
pin (template attributes + JS source text), matching `test_static_cache_policy_1859.py`'s
precedent since no JS harness exists in this repo (m-43: this proves the code is wired, not that
a browser renders it); denominator = both live composer surfaces (widget + inline), 100% of the
`.chat-input` instances found by repo-wide grep.

## #1750 — `web/assets/standup.html` stale unauthenticated twin

**Files**: `web/assets/standup.html` (deleted via `git rm`), new
`tests/unit/web/test_assets_stale_standup_page_1750.py`

Swept for live referents: `grep -rln "assets/standup.html" templates/ web/ services/ docs/` hit
only docs (`false-trails-audit-2026-08-08.md`, `docs/public/user-guides/features/morning-standup.md`,
an omnibus log, `learning-dashboard-technical.md`) — no code referent. Basename `standup.html`
alone (without the `assets/` prefix) appears in `ui.py`, `services/standup/assembler.py`,
`services/features/morning_standup.py`, `services/domain/models.py` — all referring to the REAL
`templates/standup.html` via the `/standup` route, confirmed by reading `ui.py:376-381`.

`git rm web/assets/standup.html` (the one dead static file this task pre-authorized removing).

New pin test mirrors `test_assets_stale_personality_page_1733.py`'s pattern exactly (real
`TestClient(app)` against the real ASGI app, real JWT via `AuthContainer.get_jwt_service()`):
`/assets/standup.html` → 404, `/assets` mount still serves live JS (guard), `/standup`
unauthenticated → 401 (mounted + gated), `/standup` with a real cookie → 200. Added one more
check beyond the 1733 pattern: `TestAssetsDirClassRestored.test_assets_dir_has_no_html_pages` —
globs `web/assets/*.html` and asserts empty, which is #1750's own AC ("after this, web/assets/
contains no HTML pages") and is the whole-class closure the two per-file tests individually
can't provide (#1733 covers its file only, this covers this file only, but together with this
glob check the CLASS is closed).

Ran `tests/test_completion_ratchets.py::test_dark_assets_ratchet` before asserting the fix needed
no allowlist change: `_dark_assets()`'s basename-matching logic (matches by filename only, not
full path) means `web/assets/standup.html` was NEVER flagged dark in the first place — its
basename `standup.html` collides with the live `templates/standup.html` reference in `ui.py`, so
the ratchet's corpus scan treated it as "referenced" even though it was the wrong file being
referenced. Confirmed: 10/10 ratchet tests still pass after the delete with the file simply
absent from `_tracked()` now — no allowlist row to remove (it was never added).

**Noted, not touched** (another lane's file, per task scope): `services/auth/auth_middleware.py`
line 143 comment reads `# Static assets. CSS/JS/images don't have user-bound responses.` — still
names the class correctly now that `web/assets/` genuinely contains no HTML pages. Left as-is.

**Gates**: new file 9/9 passed (run together with the 1733 sibling test — both green).
`tests/test_completion_ratchets.py` 10/10 passed (dark_assets ratchet unaffected, confirmed by
direct read of `_dark_assets()`'s matching logic, not just by the test passing).

**Verified how**: method = real `TestClient` against the real ASGI app + real JWT crypto (same
pattern as the #1733 precedent this mirrors) + a live glob of `web/assets/*.html`; layer =
full-stack HTTP request through the actual StaticFiles mount and AuthMiddleware, not a
route-table or on-disk-existence stand-in (m-43); denominator = the one file named in #1750,
plus a whole-directory-class check (`web/assets/` has zero `.html` files) that closes the
sibling #1733 fix's denominator gap too.

## #1498 — live "Good afternoon" header renders over historical conversation turns

**Files**: `web/api/routes/ui.py` (home() route context only), `templates/home.html`, new
`tests/unit/web/test_home_greeting_historical_1498.py`

Traced the render path: the greeting (`#greeting-text` / `#greeting-time`) is 100% client-side —
computed once in `initializeGreeting()` from `new Date()` on `DOMContentLoaded` and never touched
again, regardless of which conversation is on screen. Conversation switching
(`switchConversation()` in `home.html`, fired both by the left rail's full-page `/?conversation=`
reload and by the history-sidebar's in-page `handleHistorySelect()` → same function, no
distinguishing signal between them today) fetches `/api/v1/conversations/{id}/turns` and repaints
the chat window but never touched the header — so an old thread's turns rendered under a NOW
header. Confirmed `/api/v1/conversations/{id}/turns` orders by `turn_number` (ascending) by
reading `web/api/routes/conversations.py:154` — `turns[0]` is the conversation's earliest turn.

**Design decision** (documented in code + test docstring, since it's a judgment call under scope
constraints): the repo has no reliable signal distinguishing "conversation just resumed" from
"conversation opened from the archive" — both the nav-rail path (full page reload) and the
history-sidebar path (in-page JS call) land on the identical `switchConversation()` call with no
`source` flag, and threading one through would touch `nav.js`/`nav_rail.html`/
`history_sidebar.html`, all outside this task's scope. Chosen rule instead: **any conversation
with turns loaded shows its own face ("Conversation from ‹its earliest turn's date/time›"); only
a genuinely blank/new conversation (zero turns) keeps the live greeting** — because that's the
only state where "now" is an honest claim. This directly fixes the reported defect (NOW header
over old turns) without inventing an arbitrary recency threshold.

Zone handling: added `user_timezone` to `home()`'s template context via
`services.utils.datetime_utils.user_timezone_name(user_id)` — the #1576 getter, same one every
other face on the account is rendered against (total/never-raises, degrades to
`DEFAULT_USER_TIMEZONE`). `home.html` turns this into `const USER_TIMEZONE` (defaulted via
`|default(none)|tojson` so templates omitting the var — an existing cross-template test does —
still render) and a shared `faceOptions()` formatter used by both `initializeGreeting()` (live)
and the new `renderConversationFace(firstTurnCreatedAt)` (historical), plus a
`greetingWordFor(date)` helper so the morning/afternoon/evening word itself also respects the
configured zone rather than only the date/time text next to it.

Wiring: `switchConversation()` — after turns load, `turns.length > 0` → `renderConversationFace
(turns[0].created_at)`, else → `initializeGreeting()`. `createNewConversation()` — calls
`initializeGreeting()` explicitly (a fresh conversation has zero turns, restoring the live state
in case the header was showing a previous conversation's face).

**Adjacent oddity from the issue** ("your calendar isn't connected yet" reply reads as live when
re-opened) — not fixed, per the task's instruction. Assessment: the header fix makes the
SURROUNDING context honest ("Conversation from Friday, August 7 at 8:33 AM" now sits above that
reply), which gives a reader a correct temporal anchor for the whole thread, but it does not
change the reply's own text — "your calendar isn't connected yet" is still phrased as a live
present-tense claim and reads that way in isolation if quoted or screenshotted without the
header. The header fix mitigates but does not resolve the adjacent oddity; it would need its own
fix (rephrasing that specific reply class to past/conditional tense, or a stored fact vs. live
claim distinction) — out of scope here as instructed.

**Pin test** (`test_home_greeting_historical_1498.py`, 13 tests): real Jinja
`Environment(loader=FileSystemLoader("templates"))` rendering `home.html` directly (matching the
existing `test_learning_dashboard_template_1430.py` precedent for direct-template pins in this
repo) — `TestServerSideTimezoneWiring` (3: resolved tz flows into `USER_TIMEZONE` verbatim,
missing tz degrades to `null` not a crash, tojson doesn't HTML-entity-escape into broken JS),
`TestLiveState` (5: `initializeGreeting`/`faceOptions`/`greetingWordFor` defined and used
correctly, `DOMContentLoaded` calls `initializeGreeting()`, `createNewConversation()` restores
it), `TestHistoricalState` (5: `renderConversationFace` defined, label is "Conversation from" not
a greeting word, formats `firstTurnCreatedAt` not `new Date()`, `switchConversation()`'s
`turns.length > 0` branch is wired to it with the else-branch staying live, `turns[0]` not
`turns[turns.length - 1]`). Docstring names the layer honestly: this is a render pin proving the
server→client wiring and that both code paths exist and are call-site-wired, not a browser test
proving DOM behavior at runtime (no JS harness exists in this repo).

Fixing this test surfaced a real cross-template bug: my first draft used
`{{ user_timezone|tojson }}` unconditionally, which broke
`tests/unit/templates/test_app_shell_migrations_1171.py`'s existing home.html render (that test
doesn't pass `user_timezone` at all, and bare Jinja `Undefined` isn't JSON-serializable →
`TypeError`). Fixed with `{{ user_timezone|default(none)|tojson }}`. Re-ran the full
`tests/unit/templates/` suite after the fix: 1016/1016 passed.

**Gates**: new file 13/13 passed. `tests/unit/templates/` 1016/1016 passed (confirms the
cross-template regression is actually fixed, not just the new test). `tests/unit/web/` 901/901
passed. mypy before/after `web/api/routes/ui.py` (via `git show HEAD:… > /tmp` since I can't
stash/checkout in this worktree) — same 3 pre-existing `var-annotated` errors on
`lists_data`/`todos_data`/`projects_data` both before and after (line numbers shifted by my
insert, error count/kind unchanged) — no new mypy errors introduced.

**Verified how**: method = real Jinja `Environment().get_template("home.html").render(...)`
executed and asserted against, twice per test class (live-state context, historical-state
context) plus the full pre-existing `tests/unit/templates/` + `tests/unit/web/` suites re-run
end-to-end; layer = template-render + source-presence pin (m-43 named honestly in the test
docstring — proves server context wiring and that both JS code paths exist/are wired correctly,
NOT that a browser executes them, since no JS harness exists here); denominator = the
greeting/conversation-face header on `home.html` only (the one surface #1498 named); explicitly
does not cover the adjacent "calendar isn't connected" reply-text oddity, reported not fixed per
instruction.

## Suite-wide gates (all three issues)

```
tests/unit/web/templates/test_chat_widget.py .......................... 132 passed
tests/unit/web/test_assets_stale_standup_page_1750.py
  + test_assets_stale_personality_page_1733.py ......................... 9 passed
tests/unit/web/test_home_greeting_historical_1498.py .................. 13 passed
tests/unit/templates/ ................................................ 1016 passed
tests/unit/web/ ....................................................... 901 passed
tests/test_completion_ratchets.py ..................................... 10 passed
scripts/run-sweep.sh smoke ...................................... 559 passed, 1 skipped
ruff check (touched files) ............................................ clean
ruff format --check (touched files, after `ruff format` applied) ..... clean
mypy web/api/routes/ui.py (before vs after, via git show HEAD:…) ...... no new errors
node -e "new Function(...)" on chat.js + home.html's 7 inline <script> blocks ... syntax OK
```

## Files touched (mine only — confirmed via `git status` that all other dirty/untracked files
belong to concurrent lanes and were left alone)

- Modified: `templates/components/chat-widget.html`, `templates/components/chat-inline.html`,
  `templates/home.html`, `web/api/routes/ui.py`, `web/static/css/chat.css`,
  `web/static/js/chat.js`, `tests/unit/web/templates/test_chat_widget.py`
- Deleted (`git rm`, pre-authorized): `web/assets/standup.html`
- New: `tests/unit/web/test_assets_stale_standup_page_1750.py`,
  `tests/unit/web/test_home_greeting_historical_1498.py`

## Discovered work (report only, not filed as a new issue — flagging for Lead to triage)

- Duplicate `id="chatForm"`/`id="chat-window"`/`id="chat-container"` across `chat-widget.html`
  and `chat-inline.html`, both live on the home page simultaneously. Pre-existing, not
  introduced/worsened by #1737's fix. Worth a tracking issue if not already filed under an
  existing MUX/nav-consolidation umbrella.
