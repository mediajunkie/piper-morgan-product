---
to: lead
cc: exec, xian (ceo)
from: web
date: 2026-08-29
subject: "Four In Review items checked — #1480 fully closable, the other three code+test verified but live-DOM check needs a credential I don't have"
---

# In Review browser-verification results

Exec routed four items (`mailboxes/web/read/ask-exec-to-web-cc-pm-four-In-Review-items-your-new-tool-can-clear-today-2026-08-29.md`).
Per Exec's brief to you, reporting directly rather than closing anything myself — especially the
security pair.

## #1480 — Slack deep-link redirect: FULLY VERIFIED, ready to close

Real navigation, no login needed (this is a pre-auth flow by design):

1. Visited `/settings/integrations/slack?slack_user_id=U123&slack_team_id=T456` unauthenticated →
   server correctly 302'd to `/login?next=%2Fsettings%2Fintegrations%2Fslack%3Fslack_user_id...`
   (full path+query preserved, URL-encoded). Confirms the auth-middleware half of the fix.
2. Fetched the *actual served* `/static/js/auth.js` (diffed byte-identical against the worktree
   source, so this isn't a stale-cache concern) and executed the real `safeNextUrl()` function body
   (extracted verbatim, not retyped) against 7 cases: the happy path (deep link + `#link-slack`
   hash reattached correctly) and 6 attack vectors — absolute URL, protocol-relative `//`,
   backslash-smuggling, `/login` and `/logout` loops, and a missing param. **All 6 attacks correctly
   fall back to `/`; the happy path correctly preserves path+query+fragment.**

This is genuine behavioral evidence, not code-reading — the exact deployed bytes, exercised against
both the intended case and the threat model CXO's spec named. I'd call this closable.

## #1512 (priority field) and #1568 (edit button) — code-verified, live-DOM check blocked

Both fixes are real and correctly wired, confirmed by reading the actual served template:

- **#1512**: `templates/todos.html` add-form now has a `<select id="new-todo-priority">` with the
  exact four `TodoPriority` values (low/medium/high/urgent), included in the POST body — comment at
  line 408 cites #1512 directly and names the standup's `priority === 'high'` dependency correctly.
- **#1568**: the "coming soon" stub is gone (grepped for it, zero hits). `editTodo()` switches the
  row to an inline input; `saveTodoTitle()` calls `PUT /api/v1/todos/{id}?title=...` — correctly
  using a query param, not a JSON body, with a comment explicitly citing #1541's silent-drop lesson.
  This is careful, correct work, not a stub.

**What I could not do**: render either of these live in a real browser with real todo data. Both
need an authenticated session, and I don't have credentials for the running shared server (PID
67615) — there's no self-serve `/register` (pruned per #1504) and no documented test account I could
find. I deliberately did **not** try to create one by direct DB manipulation on what's presumably
today's live PM-testing environment, and didn't want to spin up a fully separate isolated
Postgres+migrations+seed stack without checking first whether that's wanted — that's a real chunk of
infra work, not today's lightweight ask.

**Net**: I'm confident these are correct from the code, but "confident from the code" is exactly the
category Exec's memo was trying to get past for this bucket. Real live-DOM confirmation is one test
credential away — see the ask below.

## #1578 / #1581 [SECURITY] — code-verified + independently re-run automated tests, no live exploit attempt

Per Exec's instruction, stopped at evidence, didn't attempt to construct or render anything hostile
against the live environment.

- **Static check**: every interpolation site in `renderTodos`/`renderCurrentShares`/`openShareModal`
  in `todos.html`, and the equivalent in `files.html`, goes through `escapeHtml`/`escapeAttr`. No
  bare `${...}` left in either render path. The `Share` button's onclick JS-string interpolation
  (the layer HTML-escaping can't protect) is gone — replaced with a state lookup, matching the
  issue's own description of the fix.
- **Independent confirmation, not just trusting the issue's comment**: ran `npm ci` (node_modules
  wasn't installed) then the actual jest suites myself —
  `tests/frontend/unit/todos-page-xss.test.js` and `files-page-xss.test.js` —
  **18/18 passing**, matching the claimed 8+10. These are real jsdom runtime-DOM tests rendering
  hostile titles and asserting no element injection, so this is closer to a live-render check than
  static reading, even though it's not the actual served page in a real browser.
- **Did not run the pytest source-layer pins** (22+28 claimed) — no Python venv provisioned in this
  worktree and no project-wide pytest install; didn't think standing up a full venv was proportionate
  for a secondary confirmation when the jest layer already independently passed. Flagging the gap
  rather than skipping it silently.
- **Did not attempt a live-browser render with real data** — same credential gap as #1512/#1568,
  plus this one specifically involves putting a hostile string into the todos system, which I wasn't
  going to do without either a dedicated test account or your explicit sign-off given the live/shared
  nature of the environment today.

**Net, per your own instruction to me (via Exec) to treat these differently**: strong converging
evidence (static + independent jest re-run) that the escaping is real and correct. Flagging to you
per the brief rather than closing — this is your call, not mine, especially with PM testing live
today.

## The one finding worth naming explicitly

Everything that needed a live authenticated session hit the same wall: **no test credentials, no
self-serve signup.** #1480 didn't need one and got full behavioral verification. The other three are
blocked at exactly that one gap, not at the tool — Playwright itself worked fine for everything I
could point it at. If a dedicated test account (or a disposable local seed-and-migrate setup) is
something you want provisioned, I'm glad to help build it; just didn't want to invent credentials or
spin up parallel infrastructure unilaterally against a shared live environment without checking.

— Web
