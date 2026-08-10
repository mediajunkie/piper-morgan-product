# Time-handling audit — the fragmented-clock class (PM-directed, 2026-08-10)

**Directive**: PM, after a morning of time bugs (#1562 wrong-day reminder, #1535 UTC clock face,
raw-ISO todos page): "it shows a fragmented approach to time and calls for an audit."

**Method (m-43)**: static analysis at 9b761b202 + one env-stripped execution probe (TZ=UTC, the
parser under a simulated fly clock — `parse_reminder_time`/`parse_relative_date` driven live at
07:59 PT). **Denominators**: 569 non-test .py files swept · temporal_utils.py (418 lines, every
branch) read in full · **85/85 DateTime columns** checked (83 database/models.py + 2
persistence/models.py) · **50 user-visible render sites** classified (67 templates, 23 JS files,
32 route files, 6 handler files, Slack, standup, Radar) · 9 parse anchors outside temporal_utils
· 233 naive `datetime.now()` sites in 62 files + 3 residual `utcnow()` counted · 79 migrations
grepped for a tz column.

## Root cause — ONE missing value, five improvised clocks

**No per-user timezone exists anywhere in the system — supply is 0%** (no column in any of 79
migrations, no production writer, no browser capture, no Slack read) **while the consumption
scaffolding is ~80% built** (ZoneInfo math in 5 modules, IANA validation, a dead `user_timezone`
parameter marking where the value was always meant to arrive). So each layer improvises its own
clock: parse anchors the SERVER clock, display renders five different faces (server, UTC-labeled,
config-file tz, source offset, browser-local), "today" means five different day-ranges. Storage
is the one unified layer — 85/85 columns timestamptz, instants correct — which is exactly why the
bugs present as "stored right, understood and shown wrong." #747/#750 (Feb 2026) fixed the
*server-side* half (aware datetimes, UTC storage) and explicitly deferred the per-user half;
every seed incident is the deferred half coming due.

## Findings (ranked by user-trust damage)

**F1 — every user-typed clock time binds the server's clock (PM's implied claim: CONFIRMED).**
`temporal_utils.py:45,253` — `now = datetime.now().astimezone()` = UTC on fly; the
`user_timezone` param (:18) is dead (body never reads it; 0 of 2 callers pass it;
`parse_reminder_time` has no tz param at all). Probe at 07:59 PT under TZ=UTC: "remind me at
4:30pm today" → stored 16:30Z = **9:30 AM PT — fires 7 hours early**. Day-correct reminders fire
at the wrong wall-clock hour for every non-UTC user; #1562's fix corrected the day, not the hour.
This is the audit's root finding: until a user tz reaches the parser, *no* absolute clock time a
user types can be stored as they meant it.

**F2 — display: 27 of 50 render sites show a wrong or unreadable face.** Breakdown: 13
UTC/server unlabeled · 10 raw ISO · 1 UTC-labeled · 3 config-tz labeled · **23 user-local
correct** (serialize-aware-ISO → browser `toLocale*` — the pattern that works). Worst: reminder
confirmation `todo_handlers.py:265` strftime of the server face, unlabeled (**#1535's "4:27 PM"**,
probe-confirmed "in two hours" → correct instant, face 4:59 PM = UTC); todos page
`templates/todos.html:233` prints `Due: ${todo.due_date}` verbatim → `Due:
2026-08-08T15:00:00+00:00` (the API at todos.py:278 correctly emits aware ISO — the page is the
only frontend consumer that skips `toLocale*`); reminder list `todo_handlers.py:425` "3:00 PM
UTC" (#1521 — labeled, honest, still the wrong clock for the user); standup renders
`web/api/routes/standup.py:339/404/468` strftime over a **naive** `generated_at`
(standup_orchestration_service.py:45); agenda meeting times raw ISO
(canonical_handlers.py:2439/2467/2511); floor prompt gets due dates as raw ISO
(conversational_floor.py:795-802). The one per-user-correct chat render:
`_current_time_for_user` (context_assembler.py:23-66, #1381) — precedence personalization-tz →
config-tz → *omit*, the fallback discipline the rest of the system lacks.

**F3 — "today" means five different day-ranges.** (a) parse "today"/calendar-query range = server
UTC day (temporal_utils:46, probe: 00:00Z–24:00Z = 5pm–5pm PT); (b)
`google_calendar_adapter.py:494-512` get_todays_events = "user" tz that is really the in-memory
default (F6); (c) same adapter :696/:1031 = server-local — **two different "today"s in one
file**; (d) "what's today" / floor date = config-file tz (canonical_handlers.py:252-258) or naive
now (context_assembler.py:745); (e) `document_service.py:231-243/:342-352` "yesterday" = rolling
24h window, not a calendar day, with the two functions defaulting differently (last_week vs
yesterday). After 5pm PT, a PT user's agenda, todos-due-today, and calendar all silently answer
about *tomorrow*.

**F4 — past-checks and rolls run on the wrong clock — including the honest ask.** Probe: "remind
me at 9:41am today" at 07:59 PT → the #1562 honest-ask fires, telling the user 9:41 "has already
passed on my clock" **while it is still 100 minutes in their future**. The ask is the right shape
on the wrong clock. Bare-clock roll (temporal_utils:389-394): "at 5pm" typed 10am PT → 17:00Z
already past → rolls to tomorrow — wrong day *and* wrong hour. **PM's question — "should the bare
clock case ever happen?" Audit answer: yes, but only on the user's clock, and visibly.**
Next-occurrence semantics for a bare "at 5pm" match user expectation and every scheduler
convention; the honest-ask alternative would add a clarifying turn to the *most common* reminder
shape (evening "remind me at 9am") for near-zero ambiguity — over-asking. The real defects are
(i) the roll currently computes on the server clock (wrong input, F1) and (ii) the rolled date is
shown in the UTC face (F2) so the user can't see it rolled. Fix the clock and label the face
("tomorrow at 5pm") and the silent roll becomes an informed one; keep #1562's never-roll rule for
explicit day words.

**F5 — LIVE naive/aware TypeError, swallowed, drops todos from the floor (#1556 residual).**
`_compute_deadline_proximity` (context_assembler.py:124-125) compares naive `datetime.now()`
against timestamptz-aware `due_date` → TypeError → caught at :1048-1050 as a *warning* → the
whole `pending_todos` block silently vanishes from floor context for any user with a due-dated
todo. Same shape as #1491 v30, one function over from its fix. Smallest fix, immediate payoff.

**F6 — the tz-preference infrastructure is a facade.** `UserPreferenceManager` is in-memory
(user_preference_manager.py:195 "would be replaced with database persistence") — 
`get_reminder_timezone` has IANA validation, getter/setter, and **zero production writers**; a
fresh manager per call means it can only ever return `America/Los_Angeles`. So even
get_todays_events' "per-user" boundary (F3b) is a hardcoded default for everyone, and the standup
scheduler's per-user firing (standup_reminder_job.py:187) — the one *architecturally correct*
tz consumer — reads the same always-default. Personalization-context tz: reader exists
(context_assembler.py:51), writer/schema absent. Slack `users.info` returns `tz` per user —
called nowhere. Browser tz shapes 23 renders and is never transmitted.

**F7 — naive residuals (denominator honesty).** 233 naive `now()` sites / 62 files, the great
majority in-memory-consistent or log-only; 3 `utcnow()` left, all
slack/oauth_handler.py:128/377/535 (naive-UTC pair, self-consistent). Real risks: SQL-side naive
cutoffs against timestamptz (repositories.py:2820; file_repository.py:114/132/151;
canonical_handlers.py:2707-2721 "yesterday's accomplishments" — silent UTC-day drift, no error);
the `datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()` idiom
(canonical_handlers.py:1706/3749, response_context.py:118/142) whose anchor silently depends on
whether the upstream string carried an offset; latent `user_preference_manager.py:161`.

**Verified CORRECT (the pattern to converge on)**: 85/85 storage columns aware · all four
context_assembler activity windows + todo_handlers due-splits + conversation_manager (8 sites)
compare in `datetime.now(timezone.utc)` · zero roll-forwards outside temporal_utils · 23/50
renders browser-local · `datetime_utils.py` (#750) exists with `utc_now`/`ensure_utc` ·
`_current_time_for_user`'s omit-when-unknown rule (#1381) · standup_reminder_job's per-user-tz
firing logic.

## The fix: ONE canonical clock chain (mirror of the status audit's "one canonical source")

**Capture → store → parse → display → compare, each with exactly one rule:**
1. **Capture** user tz at session: browser `Intl.DateTimeFormat().resolvedOptions().timeZone` in
   the login payload (attach points: auth.py:77 request model, :194 per-login write, :211 JWT
   claim, re-propagated at :282 /refresh); Slack surfaces read `users.info.tz` (one unreached
   call away, slack_client.py:326). Persist on the user row or personalization context *with
   schema and writer*; preference override on top. IANA-validate with the validator that already
   exists.
2. **Store** UTC instants always — already true (85/85); keep the ratchet.
3. **Parse** in the user's tz: one `user_now(user_id) -> aware datetime`; temporal_utils takes tz
   as a *required* argument (revive the dead param; give `parse_reminder_time` one); all
   today/day-boundary math on that clock.
4. **Display** in the user's tz, labeled: server-rendered surfaces use one shared formatter;
   web surfaces keep aware-ISO + `toLocale*` (already 23/50) — todos.html joins them. **When tz
   is unknown: omit the clock face or label it "UTC" — never an unlabeled face** (#1381's rule,
   generalized).
5. **Compare/roll** on aware UTC instants only (`utc_now()`); never roll over an explicit day
   word (#1562, keep); bare-clock next-occurrence roll allowed, computed on the user clock,
   surfaced in the confirmation label.

## Issue mapping

| Finding | Lands on |
|---|---|
| F1 parse anchor + F6 supply | **#747 reopened or successor issue** (per-user tz umbrella; #747 shipped only the server half) — with #1535/#1562 as satisfied-by |
| F2 display faces | #1535 (expand scope to the 13 unlabeled + 10 raw-ISO sites) + new todos-page/standup issues below |
| F4 wrong-clock ask/roll | resolves with F1; no separate issue needed beyond confirmation-label copy |
| F5 deadline-proximity TypeError | #1556 (residual list) or the dedicated issue below — fix-sized now |
| F7 SQL-naive cutoffs, utcnow, guarded idiom | #1556 |
| #1521 | already closed (reminder LIST); its "UTC" label retires under F2 |

**New issues for Lead to file** (titles; this audit cannot file):
1. *Per-user timezone: capture at login (browser) + Slack users.info, persist, thread into parse
   and display — the deferred half of #747* (umbrella; subsumes F1/F6).
2. *_compute_deadline_proximity naive-vs-aware TypeError is swallowed — pending todos silently
   dropped from floor context* (F5; urgent, small).
3. *UserPreferenceManager is in-memory only — every preference silently resets per process and
   per instance* (F6; broader than tz).
4. *Todos page prints raw ISO due dates — adopt the aware-ISO → toLocale\* pattern of its 23
   sibling renders* (F2).
5. *Standup/agenda: naive generated_at + raw-ISO meeting times; render in a stated tz* (F2/F3).
6. *Calendar adapter computes two different "todays" — unify on user_now()* (F3).
7. *document_service "yesterday" is a rolling 24h window and its two timeframe defaults disagree*
   (F3, minor).

Relates: #747/#750 (root history), #1535, #1562, #1556, #1521, #1491/#1493 (fixed naive-aware
class), #1381 (the omit rule), m-43/m-44. Probe script + full sweep detail: session record
dev/2026/08/10/2026-08-10-0756-prog-timeaudit-log.md.
