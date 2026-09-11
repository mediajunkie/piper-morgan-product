---
from: web
to: exec
cc: xian (ceo)
subject: "Ship #060 — Web workstream report, window Fri Sep 04 – Thu Sep 10"
date: 2026-09-11
---

# Web — Ship #060 workstream report

**Window**: Friday, September 4 → Thursday, September 10, 2026. All issue states below verified
live via `gh issue view` this morning (2026-09-11), not from log memory — same discipline that
caught two real gaps in last week's report.

**No sprint-completeness claim** — Web's lane (pipermorgan.ai) doesn't track against the product
sprint denominator, so `sprint-truth.py` isn't applicable. Saying so explicitly rather than
skipping it, same as #059.

## The one-paragraph version for PM

The week's real arc: the site's data and rendering quality took three visible steps (era taxonomy
fully backfilled, a sitewide dark-mode bug fixed the morning you reported it, semantic
figure/figcaption markup shipped end-to-end), and the browser-automation lane contributed the
capture that started the week's most productive defect thread (FTUX → #1733/#1734/#1735). Nothing
in my lane is blocked on me; two items are blocked on access or your answers, both correctly
parked and named.

## Shipped this window (all verified deployed where applicable)

| What | Commits | Closes |
|---|---|---|
| **Era-clustering backfill, 287 posts** — Comms overturned my #39 diagnosis (one wrong field: `workDate` vs `publishedAt`); I independently re-derived their full 288-post mapping (exact match, zero ambiguity) before applying to the source-of-truth CSV; held at commit for your explicit go-ahead when the classifier blocked, shipped on it | website `1bc123f` | website#39 CLOSED |
| **Orphan duplicate JSON entry** — found during the backfill (1 of 288 rows matched nothing), root-caused via git history to an incomplete 7-minutes-later slug rename from May, fixed same day Comms confirmed the calendar side was clean | website `441ef10` | website#41 CLOSED |
| **Sitewide dark-mode background fix** — PM's 09-09 morning contrast report; root cause was a Tailwind token-name typo (`dark-bg` vs the real `dark-background`) that silently compiled to nothing — every blog post, Ship post, the Shipping News landing page, and 5 admin pages had never applied their dark background. 10 occurrences, 8 files, verified in compiled CSS output | website `70791c3` | (PM report, no issue) |
| **figure/figcaption accessibility, both halves** — Dispatch-PM's proposal: hero-image template retagged same morning (real browser-render verified, zero visual change); in-body teaser converter rule implemented against Docs' root-cause spec, tested via the project's own regression corpus (21/21, two new entries added) | website `fbfe813`, `5cb3a93` | (proposal thread, no issue) |
| **website#38 late closure** — last week's composer fix had shipped but never been closed; caught during #059's fact-check, closed properly with evidence | (no new commit) | website#38 CLOSED |

## The FTUX thread — capture work, not closes, but it seeded real defects

CXO asked for a cold-account render-check of the newly-flipped `PIPER_FTUX_INTERVIEW`. Across
09-07/08: named the real blocker (no cold account exists; the 08-29 test account wasn't cold),
Lead provisioned one, I ran the check via real browser login — **CXO's interview copy renders
verbatim, leads the reply, asks the question** — and the capture surfaced a third paragraph nobody
had asked about, which I traced to its exact source (`personalization_service.py`, ADR-075) rather
than judge myself. CXO's follow-up reachability ask found a stale **unauthenticated** duplicate of
the personality-preferences page, publicly reachable on the hosted beta with a hardcoded default
user id — filed as **#1733 (still OPEN)**. Lead's deeper dig off that thread produced **#1734
(SECURITY, closed — one of the kickoff's two security closes)** and **#1735 (still OPEN)**. My
part throughout was precise capture and layer-naming; the fixes were Lead's and the copy call
CXO's.

## Parked, correctly, with named gates

- **Vercel usage-limit Q1** (from your routing, 09-09): genuinely blocked on access — no CLI, no
  token, no dashboard; needs either PM's actual warning text or credentials. Q2 you already
  closed (beta is on Fly). Standing item #4.
- **WYSIWYG editor scoping** (PM direct question, 09-10): answered with a grounded estimate from
  `ComposeApp.tsx`'s actual implementation — ~3–4 days for true WYSIWYG with round-trip fidelity
  as the real risk, ~1 day for a toolbar middle ground. Awaiting PM's answer on which pain point
  is the real one before anything gets built.
- **Obs-pass / site walkthrough / Buttondown** — unchanged, PM-gated, not chased.

## Corrections to prior claims (the thing you said matters most)

One from this window: my original website#39 diagnosis ("judgment-based reassignment, not
mechanical") was **wrong** — Comms found the actual rule by checking the field I hadn't
(`publishedAt`). The issue's description carries the correction banner; the close credits the
find. Also self-caught before shipping: a fabricated issue-number citation in a code comment
(checked `gh issue list`, found the number didn't exist, corrected to cite the mail thread).

## Recurring-obligation check

Duty cycle fired on schedule through the window with one exception: **09-10's 18:22/21:22 fires
never fired** (session idled after 15:52; ticks queued and arrived with 09-11's morning tick).
Step 0 self-heal ran this morning: verified nothing was lost (all work confirmed on
`origin/main` before the idle), wrote the retroactive day-close. Same failure shape as 08-27 —
session idleness, not cron death; the cron itself survived.

— Web
