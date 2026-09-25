---
from: host
to: exec
cc: xian (ceo)
subject: "Ship #062 workstream review — HOST, window Fri 09-18 → Thu 09-24"
date: 2026-09-25 10:12 PT
---

Exec —

Filing within the 10:45 window rather than sending an ETA.

## PM's organizing question first, honestly answered

**What can a user or alpha tester do today that they couldn't on September 18?** For HOST's lane
specifically, the honest answer is mostly **indirect** — HOST doesn't ship product code — but one
item is directly, concretely product-facing:

**A new alpha signup that was silently, unconditionally broken on 09-18 now works.** The `/setup`
wizard's Step 1 hard-blocked *every* new user reaching an already-initialized instance (a swallowed
403 detail plus a wrong frontend fallback asserting infra was down). Web found and reported it,
HOST filed it same-day since nothing tracked it (`#1875`), Lead/CXO fixed all three stacked causes
same-day, Web verified live through a real rendered-browser session. **Before this fix, the planned
alpha-invite email would have sent every recipient to a dead end at the very first screen** — this
wasn't a cosmetic bug, it was the entire rollout's front door. That's a real "couldn't → could"
delta, not activity.

**A no-answer this cycle, stated plainly rather than dressed up**: HOST didn't ship any other
product-facing change this window. The rest of the work — described below — is trust/process
infrastructure that the product rollout depends on, not the product itself.

## Sprint truth (required)

```
MVP: 29 not done (10 Sprint Backlog, 2 In Progress, 3 In Review, 14 Product Backlog); 1190 done.
```
Unchanged since the last read 19 minutes before this one (`+0`/`+0`) — HOST's own work doesn't
move this board directly; noting the number because the instruction says to, not because it's
mine to claim credit or blame against.

## What actually happened, in order of weight

**The alpha rollout's front door was fixed** (above) — the window's one real product delta from
HOST's lane.

**A real credential-leak incident, twice** (09-21, then 09-24/25) — the heaviest thread this
window, in trust terms. A live invite token leaked in full form to the public repo (09-21);
HOST's own leak, acknowledged directly. Separately and more seriously, a new lint's first full-repo
run found **three more live, unused invite tokens in full form in tracked files** (`#1885`,
09-24) — two via HOST's own historical session logs. HOST verified the scrub independently rather
than trusting the report, corrected a wrong claim in a 2-month-old log entry (dated, not silent),
and found a genuine gap in the alpha roster's own coverage (a tester who'd never actually been
recorded there — only in a session log, which is exactly how she leaked). PM ratified `#1845` as a
durable cohort rule same week (bearer credentials never travel through the repo; CLAUDE.md +
decisions.log). **Then HOST's own review memo of that exact rule tripped the exact gate**, twice
in the same night, from using real/realistic test strings instead of obviously-fake placeholders —
named plainly rather than minimized, and it drove two real structural fixes (case-insensitive
lint + low-entropy mock rejection + a pre-push doorway on `mail-send.sh` itself, so this class of
mistake gets refused before landing rather than caught after).

**The 8.5-hour "gate fired, nobody looked" lesson** (`#1892`, filed by Lead, HOST commented): the
`#1845` gate caught the real hit correctly and then sat red on `main` for 8.5 hours across ~35
pushes from six other seats before anyone noticed. Not a HOST-owned fix (CIO/Exec's lane per
Lead's routing), but squarely a trust-property finding — a mechanism that fires correctly and
whose output nobody reads is indistinguishable from outside from one that never ran. Added the
distinction that matters for whoever implements the fix: this is a *routing* failure, not a
*detection* failure, and a "print the conclusion at START" fix is a visibility increment, not a
response guarantee — worth being explicit about which bar actually gets met.

**A real trust-zone-split test under genuine pressure** (`#1344`, throughout): HOST never touched
the DB despite multiple points where it would have been the fast path (verifying Lead's prod
`SELECT` on `#1885`, chasing Savanna Booth's send-status). The split held under real incident
pressure this window, not just the calm case — worth naming since a boundary that's never actually
tested is a claim, not a demonstrated property.

**Admin cross-owner file-access audit logging** (`#1502`, 09-23): Lead asked whether a new
cross-owner bypass should log an audit line; HOST verified the memo's claim against source rather
than at face value, found the gate at 4 sites not the 2 named (one a WRITE, not a read), and
recommended a scoped fix. Lead landed exactly that shape same-day, tests pinned. Smaller than the
credential thread but a real, closed trust-surface item.

**Agent 360 v0.5 fielded this morning** (`#1895`, self-fired on schedule): reviewed v0.4 for
staleness, found the questionnaire's own template pointer in the workflow issue was itself stale
(pointed at `dev/active/`, the file had already moved to its dated home), retitled a section whose
"three weeks in" framing had gone stale, added one new question surfacing this week's `#1892`
lesson cross-role, fielded to all 10 other roles + PM. Responses ~2 weeks out, synthesis ~4 weeks.

**Earlier in the window** (09-18/19/20, lighter but real): filed the required sprint closeout for
09-11–17; wrote an urgent Amber-restart handoff doc same-fire before other queued work; accepted
and fixed a real correction to HOST's own prior investigation in both places it had landed; multi-
day work on Janne Lammi's alpha invite (a send-blocker caught in the draft, a hosted-alpha-vs-
local-install confusion resolved by researching PM's own actual sent mail, a HOLD PM chose over
"send with a caveat"); a self-corrected claim about a host reboot ("the reboot never reached this
seat" — wrong, fixed with a dated correction after Exec/Pard's forensics); the droplet→Fly hosting
migration's HOST-side steps (identity-mapping check on 4 "stale" accounts that turned out to be
PM's own, not external testers — caught before the freeze, not after).

## Setbacks and corrections named plainly, since that's the most valuable line per the kickoff

- **The 09-21 credential leak was HOST's own mistake** — a token sat in a public 09-13 memo for
  eight days before anyone caught it.
- **Both `#1845`-gate trips this week were HOST's own mistakes too** — real test-case values and a
  Crockford-shaped placeholder, in the very memos reviewing the mechanism meant to catch exactly
  that. Named directly to Lead both times, not smoothed over.
- **A genuinely wrong claim about a host reboot**, corrected only after another role's forensics
  caught it, not self-discovered.
- **A 2-month-old log entry's claim about a token's usage status was wrong** — corrected this week
  once a fresh, authoritative prod read contradicted it; no surviving record of what the original
  claim was based on.

## What's next / still owed

`#1885`'s burn-on-prod and two reissues (Savanna, Janne) are PM-queued, explicitly not urgent —
HOST re-records both on the roster same-day they land. Agent 360 v0.5 responses tracked over the
next ~2 weeks, synthesis ~4 weeks out. Role Health Check due ~09-28.

**Verified how**: `sprint-truth.py` run this turn (denominator above, delta against a 09:53 read
19 minutes prior); every issue number above cross-checked against this week's own session logs
(`dev/2026/09/{18..25}/...host-code-log.md`) and, for `#1875`/`#1885`/`#1892`/`#1895`, against the
live GH issues directly rather than memory of the mail threads. Layer: own session-log record +
live `gh issue view` reads, not a summary of a summary.

— HOST
