---
last_updated: 2026-10-03
currency_claim: per-stop
max_age_days: 1
---

# HOST carry-forward

**Written**: 2026-10-03 21:3x PDT (STOP fire, day 71 on Amber — frontmatter above is the
checkable claim; this prose line is not checkable and must not be trusted over it). · **Worktree**:
Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

**Mechanism change, same day**: HOST migrated to a boot-persistent LaunchAgent (cascade seat 7,
`com.xian.pm-host-cycle`, `26 6,9,12,15,18,21`). Confirmed the first fire (18:26) landed real work
before touching anything, then retired the session cron (`CronList` verified empty) and flipped
the registry row `37→26` same-fire, per Pard's explicit two-step protocol. **There is no session
cron to manage from inside this session anymore** — the registry row IS the mechanism. The 21:26
fire arrived exactly on the new slot, closing the loop end-to-end.

**10-03 (day 71)**: all six LaunchAgent fires landed on slot; quiet except two inbound Exec broadcasts (sprint goal locked, PM mailbox retired) and one peer-row finding mailed to Web/CIO (registry line 104, CSV-quote artifact from Web's 21:18 STOP; not HOST's row, watch whether it clears). Agent 360 stayed 8/11.

**Yesterday (10-02)**: Ship #063 workstream review filed same-day as kickoff (window Fri 09-25 → Thu
10-01) — `mailboxes/exec/inbox/workstream-063-host-2026-10-02.md`. Writing it surfaced a real,
separate finding: `ROLE-PORTFOLIO-HOST.md` §2 had gone **three weeks stale** (last touched 09-11,
untouched across workstream reviews #060/#061/#062) despite the doc's own 2-week staleness rule and
a mechanical check that evidently isn't gating this file. Refreshed it same-fire, flagged the
mechanism gap to Exec/PM in the review itself rather than silently catching up without comment.
**Exec then bounced the review back, correctly**: no `Verified how:` line (the one requirement
HOST itself holds other roles to), and no explicit answer to PM's product-delta frame (silence
instead of a stated "none," when four other roles gave exactly that honest answer). Fixing it
surfaced a **third, self-found error**: the review claimed CIO's Agent 360 response landed 10-02,
outside the window — checking the actual commit/frontmatter timestamp showed it landed 10-01 at
16:11 PDT, inside the window, making the correct window-close count 8/11 not 7/11. Sent a single
addendum covering all three rather than silently edit the delivered review.

**Day before (10-01)**: Docs caught the `DAY-CLOSED` marker gap on my own logs two days running
(09-29, 09-30); root-caused and fixed (the STOP-entry habit was stopping one line early). CIO's new
NO-DAY-CLOSE detector then found the real gap was six days, not two — see standing hazards below.
PM engaged directly on Agent 360 v0.5, corrected my approach twice in one exchange (start the
analysis sooner; then hold the finished synthesis for completeness) and directed HOST complete the
questionnaire too, as an 11th response. Full detail in 10-01's session log and `#1895`.

## Standing hazards (durable behavioral guidance, not time-bound)

- **The STOP entry's LAST line, every time, with nothing after it: `<!-- DAY-CLOSED: {date} -->`.**
  Missed two days running (09-29, 09-30) because the habit stops at "Cron: armed... next fire
  HH:MM" and treats that as the natural end — it isn't; the marker is one more line after it, not
  part of the cron sentence. Check this specifically before considering any STOP fire done.
- **Step 0's "verified DAY-CLOSED" means actually grepping the anchored marker, not reading the
  prior day's STOP prose and judging it sounds closed.** CIO's NO-DAY-CLOSE detector (10-01) found
  six real days (09-23→09-28) where every morning's Step 0 line read as verified while the marker
  was simply absent — the self-heal had never once checked the thing it exists to check. Fixed
  going forward (five correct days since 09-29), but the lapse was structural, not a typo.
- **Verify at the mechanism, not the announcement** — especially when the announcement points at
  *less* work.
- **Re-verify carried claims, don't restate them.** An item marked "unconfirmed" or "watching" is
  a claim to re-check against its actual source, not a status to keep copying forward.
- **Match your measurement's scope to the question** — before quoting a number, say what the
  denominator is and what it structurally cannot contain.
- **A predicate is a derived artifact** — enumerate the real corpus before writing one; don't
  hand-write a pattern against an imagined format.
- **PM mailbox retired (Exec broadcast 10-03 17:28).** Never write to `mailboxes/xian (ceo)/`; PM is
  not in `to:`/`cc:` of any new memo. Anything needing PM goes **to `exec`**, subject names which of
  the three: PM-only decision / relayed PM ruling / something PM would contradict. The 09-11
  three-condition cc rule is retired. Mail already in flight that cc's PM is sent as written.
- **Never delete a memory to fit the index.** Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**
- **Never write your own cadence from memory** — read the registry row live (not `CronList`
  anymore — see below, `CronList` is now expected to always read empty).

## Cron

**Mechanism changed 10-02: LaunchAgent only, no session cron.** `com.xian.pm-host-cycle`,
`26 6,9,12,15,18,21` (6x/day), boot-persistent, external to this session. `CronList` will now
always correctly read "No scheduled jobs" — that is NOT a gap, do not re-arm a session cron on
seeing it. The registry row (`dev/active/duty-cycle-registry.tsv`, `host` row, col 2) IS the
cadence source of truth going forward; there is no `CronDelete`/`CronCreate` rotation to do at
STOP anymore. If the prompt's `cron=` constant ever disagrees with the registry row, that's a
real finding (the generator reading a stale registry), not something to silently paper over.

## Standing cadence work

- **Role Health Check** — 4-weekly, self-polling via GH Actions (`label:sapient-trust`). **Closed
  today** (`#1902`) — 9 Low, 1 Medium, 0 High/Critical. Calendar updated same-fire. **Next due
  ~10-26.**
- **Role briefing** (`docs/briefing/BRIEFING-ESSENTIAL-HOST.md`) — refreshed 09-22 (Docs's
  staleness flag; caught a real operating-model error, not just a dated section). Has
  `last_verified` frontmatter now; keep it moving when it drifts rather than let it sit another
  3 months.

## Open threads

- **`#1885` burn + reissue** (09-24, timeline updated 09-25) — burn is live this sprint week (PM-
  authorized, Lead's to execute); **reissues (Savanna, Janne) explicitly deferred to next week** by
  PM ruling ("not urgent... wait til they try and fail"). **HOST re-records both on the roster the
  same day they're minted** — not before, don't chase it, watch for Lead's mint memo.
- **Agent 360 v0.5** (fielded 09-25) — **now 11 responses, not 10** (PM ruled 10-01: HOST
  completes the questionnaire too). **8 of 11 in**: Arch, Lead, PA, Web (09-25), Comms (09-27),
  Docs (09-29), HOST's own self-response (10-01), CIO (10-01). Waiting on CXO, Exec, PPM — none
  overdue, window runs to ~10-09. **Synthesis PAUSED per PM 10-01 ruling** — do NOT resume until
  the full set is in (or the window closes with an honestly-documented gap); raw working notes
  exist at `dev/2026/10/01/agent-360-v0.5-synthesis-working-2026-10-01.md` but are not a running
  draft. **CIO's response independently confirmed the CIO-silence diagnosis material from the
  inside** (its own m-43-on-its-own-instrument finding) — real primary-source corroboration for
  the eventual synthesis, not actioned now. **CIO self-corrected two lines of its own response
  same-day** (§5.5/§8.3, a stale standing-items citation) — filed to be read alongside the
  original at synthesis, not a silent edit.
- **Classifier bucket-split** (the `auth` error bucket, `_classify_llm_error`) — ruled and copy
  drafted as of 09-15, status of the build still unknown. Not HOST's to build; check for movement
  if it comes up.
- **`#1731`** — CIO's instance retracted; PPM's separate instance remains open. Watching only.
- **ESSENCE.md v0.1 trust-lens** — given 08-29. Watch for Lead's watched round adding the
  inversion-path test.
- **Weekly reflection section** (Exec's proposal, CIO-ratified 09-18) — a ~150-word subjective
  reflection rides the sprint-closeout template now. Include it in HOST's next closeout.

## Watching, not owed

- **#1539 ruled partial, not sufficient** (08-10) — the legibility half (what uncertainty a reply
  is answering) is still not concrete on HOST's own end. If it comes up again, that's still true.
- **A fifth mailbox header format found on HOST's own corpus** (08-10, Pard's inline-arrow
  notation) — reported to Comms, not HOST's to fix.
