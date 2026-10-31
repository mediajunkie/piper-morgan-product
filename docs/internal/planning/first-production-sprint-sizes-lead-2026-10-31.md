# First Production sprint candidates: Lead's sizes (2026-10-31)

**For:** PPM's candidates (`first-production-sprint-candidates-2026-10-30.md`) and xian's priorities talk. PPM proposed no sizes or dates; these are the sizes. Dates are xian's.
**Unit:** a Lead-day is one seat-day of build, the full landing gate, Arch's validation and the served check. Lanes run two bounded units at once, so calendar days are about half the Lead-days when units are independent. A rule-7 router screen is wall-clock bound (one to three hours a batch) and carries a price to Exec first.
**Confidence:** sizes marked (d) depend on a decision or a design that is not Lead's; the size is for the build after it.

## Tier 0: ship what is frozen

| Item | Lead size | Notes |
|---|---|---|
| One promotion carrying #2225, #2236, #2233, #2237/#2206, #2230's setter, the notice line, the text-block pick | 0 build; about half a day of served reads across CXO, PA and Lead | Row 4 (`tests/security` on the promoted sha) is Lead's, minutes. Dispatch is xian's under the grant until the freeze lifts. |
| #2230 flip (`set_default_repo` into the live set) | minutes, ops | xian's by-name word via Exec, CIO or HOST applies, PA probes. No code. |
| Closes with `close-issue-properly` for #2233, #2236, #2237, #2206, #2230 | about an hour | `fix:not-served` if a close comes before the serving. |

## Tier 1: strike known-issue lines

| Letter line | Issue | Lead size | What it needs first |
|---|---|---|---|
| 4 | #2184 family: #2186 unit 2 (declared argument keys rendered into the router grammar) | 1–2 days, including one rule-7 screen (about $4–5) | Nothing. It is a router-prompt change, so ×6 plus the full corpus run before it lands. |
| 4 | #2184 itself: a read that lists one milestone's issues (`milestone:` on the search rail) | 1 day | Rides on unit 2's args. One corpus row, no regex. |
| 4 | #2197: a named-milestone progress answer (title, due date, open and closed counts from code's read) | 1–1.5 days (d) | Arch's boundary between "the next milestone" and a name; CXO's words are mostly in the issue. |
| 4 | #2183, #2185, #2209 | 0 build | Fixes are on main (count and sort, the wording, the no-match line). They close on the served check after the next promotion. |
| 1 | #2149 catalog shape, then #2195's literal 32 | design first (Arch); then 2–3 days for a trimmed grouped catalog, or 3–5 days for a two-stage catalog, plus two full rule-7 runs (about $10) | Every single-field STATUS edit moved the milestone boundary ×6 (three controls 10-29/10-30), so no description or example retry before the shape. Literal 32 is half a day once the shape holds; the other 60 literals in 18 lists are a long tail, roughly a day per list, not a first-sprint whole. |
| 2, 3 | #2042: rung-3 census and the first fix | 2–3 days (d) | The census (b) needs served turns to read (Web's five on `web-pat-test` once signed in, plus partner traffic); the first fix follows what the census shows. Option (c) 2a waits on CXO's words. |
| 5 | #2021 soft delete with a 7-day undo | 3–4 days, and a promotion carrying a migration | Arch's design note exists. `deleted_at` is a migration, so that promotion needs xian's explicit word (not the standing grant). New `undo_delete` rail entry, every todo read filtered, the cascade redone, CXO's three lines, the purge job. Lifts #2019 on exit. |
| 6 | #2226 document search embeddings | half a day for an operator-funded embedding key with a user-facing spend line; 2–3 days for local embeddings in the image | xian's decision 4. Partners bind only an Anthropic key, and embeddings have used only an OpenAI key since #1819. |

Tier 1 in full: about 10.5–19.5 Lead-days, of which #2149 and #2021 are the two large ones.

## Tier 2: keep the beta safe to widen

| Issue | Lead size | Notes |
|---|---|---|
| #2165 per-account rate and abuse limits, per-IP on sign-in/invite/waitlist, an operator view, CXO's line | 3–5 days | Redis is already there. The operator view is the swing: an admin JSON read keeps it at 3; a page is Web's and adds the rest. Each limit pinned, and nothing in the path spends a user's key. |
| #1378 auth polish | CSRF alone 1–1.5 days; lockout 1 day; timeout warnings 1 day (Web) | CSRF is the public-beta gate item (PM 07-07). Cookie auth and bearer tokens both exist, so the CSRF token goes on the forms with a middleware check and a served check. |
| #2229 public site | 0 for Lead | Comms, CXO and Web after xian's decision 3. Web sizes it. |
| #2238 Notion N1/C1 | half a day | Already given 10-30. Required before Notion is offered. |
| #2235 repo validation for OAuth-only accounts | 1 day | Route the validator through `resolve_credential` (the one resolver) and keep each of the five callers' "not checked" meaning. Served check on PA's OAuth-only test account. |

## Tier 3: partner reports

Sized on arrival. Hold about 30% of the sprint's Lead-days for them; 10-30's shape (one report, one fix, a lane, served the next day) was about one Lead-day per report.

## The arithmetic on PPM's suggested set

Tiers 0 and 1, plus #2165 and #2229, with tier 3's slot: about 14–25 Lead-days of build. At two lanes that is two to three weeks of calendar before the 30% reserve, three to four with it. Two ways to make it two weeks: leave #2021 for the sprint after (it carries the migration promotion), and take #2226's half-day option. Without #2149 the sprint strikes line 4 but not line 1.

## Other sizes already given

#1442 Google connector port 3–5 days; Slack #1481 2–3 days plus #1514 (xian's); #2232 local fault-run harness about 1 day; #2239 half a day; #2227 (Haiku 5.5 re-baseline) is design, not a build.

Verified how: each issue's body and latest comment read with `gh issue view` this morning (#2186, #2183, #2185, #2197, #2209, #2149, #2021, #2226, #2165, #1378, #2235), PPM's candidates file at origin/main, and the landing history in Lead's 10-28 to 10-30 logs. Layer: issue text and the source paths the issues cite; no new source read for the sizes beyond what the issues name. These are estimates from the shape of each item, not measurements.
