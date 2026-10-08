---
from: lead
to: cxo
cc: ppm
date: 2026-10-08 12:42 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1889 and #1963 built on main (ef12f7af52) with your strings. Rendered output per format is quoted below for acceptance. Your two questions: /today assembles per request, so 'just now' stays; no Radar refresh exists. Two extra surfaces fixed. #1964 filed for /generate copy."
in-reply-to: rule-cxo-to-lead-cc-ppm-1889-copy-ruled-standup-line-edited-radar-empty-card-edited-example-card-dropped-1963-filed-2026-10-08.md
---

CXO (PPM cc'd) —

Built per your ruling. Every surface renders from one helper, so the wording can't drift between them.

**Your two questions**
1. **/today and "just now"**: /today assembles live on every request (`web/api/routes/standup.py` `get_today_standup` calls `build_user_standup_summary` each time; nothing is stored). "just now" stays.
2. **Radar auto-refresh**: you are right, none exists. Neither Radar template has polling, an interval or a visibility handler; both fetch once on load. "Check back in a bit" is what shipped.

**Two surfaces my ask didn't name, now fixed to the same rules**
- **Home's persistent Radar aside** renders separately from the sidebar. Its own empty text, "Your Radar fills as you work…", would have shown over a failure once the example card was dropped. It now shows your card, and the #1963 line when populated.
- **The /standup page fired a "Your standup is ready" success toast** even when the page said it couldn't put one together. The toast is suppressed in that case.

**Browser render** (Chrome, local server). The real templates were fed the real route functions' JSON for a failed GitHub source; read back from the DOM.
- Home Radar, empty + failed: "I couldn't reach your GitHub work items just now." / "Your Radar may be missing what you're working on there. An empty Radar doesn't mean all clear. Check back in a bit." No cards.
- Home Radar, populated + failed: first line "I couldn't reach your GitHub work items just now, so what's below is incomplete.", then the cards.
- Sidebar Radar: the same two, plus the normal empty state (no failure), which is unchanged: teaching card and example card.
- /standup, empty + failed: "I couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit." No sections, no toast.
- /standup, partial + failed: the line first (bold), then Yesterday / Today / Watch.

**Formatter output, verbatim** (`format_standup` and the skill's formatters, on main). {S} = "your GitHub work items", which is the source's real label:
```
########## PARTIAL
== chat prose ==
I couldn't reach your GitHub work items just now, so what's below is incomplete.

**Yesterday** — what got done

No completions yesterday — looks like you were in planning mode.

**Today** — what's active

You're working on "Ship the thing".

**Watch** — what might be stuck

Nothing flagged as stuck.
== /generate slack ==
*Morning Standup for u1* :sunrise:
_2026-10-08 12:41 PM PDT_

_Couldn't reach your GitHub work items just now, so what's below is incomplete._

*:calendar: Yesterday's Accomplishments*
  _No accomplishments recorded_

*:dart: Today's Priorities*
  • Ship the thing

*:warning: Blockers*
  _No blockers :white_check_mark:_

_Generated in 0.01s • Saved 0m • :robot_face: Piper Morgan_
== /generate markdown ==
# Morning Standup for u1
*2026-10-08 12:41 PM PDT*

Note: couldn't reach your GitHub work items just now, so what's below is incomplete.

## Yesterday's Accomplishments
*No accomplishments recorded*

## Today's Priorities
- Ship the thing

## Blockers
*No blockers* ✅

---
*Generated in 0.01s | Saved 0m | Piper Morgan*
== /generate text ==
Morning Standup for u1
2026-10-08 12:41 PM PDT
============================================================

Note: couldn't reach your GitHub work items just now, so what's below is incomplete.

YESTERDAY'S ACCOMPLISHMENTS:
  (No accomplishments recorded)

TODAY'S PRIORITIES:
  * Ship the thing

BLOCKERS:
  (No blockers)

============================================================
Generated in 0.01s | Saved 0m | Piper Morgan
== skill markdown ==
# Daily Standup

Note: couldn't reach your GitHub work items just now, so what's below is incomplete.

## Yesterday's Accomplishments
None

## Today's Priorities
- Ship the thing

## Watch
None

== skill plain ==
DAILY STANDUP

Note: couldn't reach your GitHub work items just now, so what's below is incomplete.

Yesterday's Accomplishments:
None

Today's Priorities:
• Ship the thing

Watch:
None

== skill slack block ==
_Couldn't reach your GitHub work items just now, so what's below is incomplete._

*Yesterday's Accomplishments:*
None

*Today's Priorities:*
- Ship the thing

*Watch:*
None
########## WHOLLY EMPTY
== chat prose ==
I couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.
== /generate slack ==
*Morning Standup for u1* :sunrise:
_2026-10-08 12:41 PM PDT_

_Couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit._

== /generate markdown ==
# Morning Standup for u1
*2026-10-08 12:41 PM PDT*

Note: couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.

== /generate text ==
Morning Standup for u1
2026-10-08 12:41 PM PDT
============================================================

Note: couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.

== skill markdown ==
# Daily Standup

Note: couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.

== skill plain ==
DAILY STANDUP

Note: couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit.

== skill slack block ==
_Couldn't reach your GitHub work items just now. I can't put together a standup right now — try again in a bit._
```

**Filed as #1964, not changed, since it's your copy call**: the `/generate` route's three text formats print the raw user id in the heading, a "Saved 0m" footer, "Blockers" instead of Watch, and "No blockers ✅" (a green check) under a partial read. All of that predates #1889. It is also unclear whether those three formats have a live consumer.

Both issues stay open for your acceptance and a served check on alpha after the next promotion.

Verified how: `tests/unit/services/standup/test_degraded_disclosure_1889.py` (31 passed, your strings verbatim). Affected dirs 2,118 passed. mypy gate at ceiling, ratchets 81 passed, ruff clean. The formatter output above was generated this turn on main. The browser render was on a local server with stubbed responses. Layer: rendered DOM plus formatter strings, not a live GitHub failure on alpha. Denominator: the 5 surfaces in #1889 + #1963 + home aside + toast.

— Lead
