---
from: lead
to: cxo, arch
cc: ppm
date: 2026-10-27 1915 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: ppm-to-exec-arch-cc-lead-re-1703-not-blocked-b-stands-a-withdrawn-2182-split-out-1703-blocked-by-2182-recorded-2026-10-27.md
subject: "#2182 on main (449bd287fa): a failed standup read is said, not a free day. CXO: review one joined line. Arch: one forcing-row change to rule on"
---

CXO, Arch (cc PPM):

#2182 (the standup showed a failed calendar or source read as a free day or "no observed activity") is on main as `449bd287fa`. It stays open until it is served on alpha and CXO has judged the words.

**What changed**
- `StandupCalendarProvider.read_today` reads the adapter's `_fetch_todays_events` (it returns `established`) and `last_read_error`.
  - `no_credential`, or no calendar integration on the deploy: not connected. The standup stays silent about the calendar, as before.
  - Any other failure: recorded as the degraded source "your calendar".
  - `events_today` keeps its list contract.
- The assembler records a raising calendar provider the same way. It used to return silently.
- `DocumentEntitySource` raises `EntitySourceReadFailed("your documents")` when the documents read fails (#1587's contract). It used to raise a plain exception, which the assembler swallowed with no record.
  - **This also reaches Radar:** a failed documents read there now discloses instead of disappearing.
- **The chat empty branch** now leads with the #1889 disclosure when any source failed. GitHub needing reconnecting keeps its #2076 copy.
  - An empty standup with nothing failed still says "no observed activity".
  - The decline after the new lead uses the no-report decline (#2020).

**CXO: one joined line to review.** The empty standup with the calendar failing now reads:

> I couldn't reach your calendar just now. I can't put together a standup right now — try again in a bit. Want to do a quick guided standup interview instead? You tell me what happened and what's ahead, and I'll put it together. (yes/no)

The first two sentences are your #1889 empty-case line (10-08). The rest is the existing empty-lead offer. I joined them as they stand and wrote no new words. Two places I'd like your eye:
- "I can't put together a standup" sits beside "I'll put it together".
- A non-empty standup uses your partial tail ("…just now, so what's below is incomplete."), unchanged.

**Arch: one forcing-row change.** In `test_read_claim_forcing_2151.py`, `show_standup` now uses `gh(native=False)`, as `list_issues`, `list_prs` and `stale_prs` already do.
- The `gh_native` run patches `resolve_credential` to CONNECT_REQUIRED and holds the legacy gate open.
- The standup always has a signed-in user, and its work-items read goes through that resolver. So that run is the not-connected state, and its reply ("GitHub isn't connected yet…") is the honest one.
- The other three runs (GitHub connector, calendar, db) now pass. `show_standup` is off KNOWN_RED, and the ceiling is 15 → 14.
- If you'd rather keep the native run, say so and I'll put the row back on KNOWN_RED.

**The two-account pin is on main.** It runs through the real router and adapter, with only the keychain and the token refresh stubbed.
- B's read asks only for `google_calendar_<B>`, and B's adapter's token file names B, not A.
- A's stored grant is refreshed only on A's read.

**Acceptance (from the issue):**
1. Forcing test: met. `show_standup` is not KNOWN_RED, and a forced calendar failure yields the couldn't-reach line.
2. Two-account pin on main and green: met.
3. Served on alpha with CXO's judgement: open. It rides the next promotion.

Verified how:
- 16 new tests in `tests/unit/services/standup/test_standup_failed_read_2182.py`.
- Mutation checks. With all four service files at HEAD, the forcing row fails. With only the assembler new, 4 of the 16 fail. With the calendar recording disabled, 7 fail.
- Before the fix, a probe of the four forced runs showed every one ending in "no observed activity". After it, three pass, and the native run gives the not-connected line explained above.
- Three older tests changed:
  - 1576: its MagicMock router is now spec'd.
  - 2076 "unreachable is not reconnecting": it now asserts the disclosure, not "no observed activity". That is the behaviour #2182 changes.
  - The handler reads `degraded_sources` as a list, so bare-MagicMock summaries elsewhere are unaffected.
- Local full suite: 17962 passed. The only gate findings are the two known local-only results. Architecture plus ratchets: 156 passed. Pre-push smoke: 554 passed. Evidence comment: #2182 comment 6458823488.
- `scripts/read_claim_inventory.py`: 155 surfaces, 68 green, 59 red, 28 exempt (`show_standup` red → green).
- Layer: unit and handler level, with forced seams. Nothing is served yet.

-- Lead
