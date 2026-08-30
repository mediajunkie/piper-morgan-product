---
last_updated: 2026-08-29
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — last rewritten 2026-08-29 (see frontmatter, which is the checkable claim; this
line is prose and MUST NOT be trusted over it).

## 🔴 NEXT FIRE (08-30 START): rotate the cron FIRST, then the ESSENCE trifecta response

1. **Cron rotation** — `cd9b3ddc` expires ~08-31. Delete-then-create, verify one job, record old→new.
2. **ESSENCE.md v0.1 full read + trifecta response** — Arch's direct ask to CXO+PPM, due **Wed 09-02**,
   deliberately deferred from 08-29 with a named trigger. Read the WHOLE document (six commitments, the
   "what it is NOT" boundary, the classification), not just the surface sections I read against my mapping.
   Partial engagement already sent (Web cell superseded / MCP cell promoted) is **not** the response.
   PPM is deferring on the same split and lands theirs by Wed too.

## Live threads (all with others)

- **#1688** (empty-state interview) — MVP, on the board; scope narrowed to MCP-only tonight; Lead's
  one-mechanism question partly dissolved. Lead builds.
- **#1658 tension** — PPM flagged, I supplied the regression-vs-absence lens, **Arch's or PM's call.**
- **Staleness check** — design mine (shipped), build CIO's (`--currency-check`, next fire). HOST is the
  fifth data point either way.
- **#1635 / #1539 / #1509** — Lead's builds and PM's live rounds.

⚠️ **Why this file now has frontmatter** (2026-08-29): its old header claimed *"rewritten 2026-08-28 at
STOP"* while `git log` showed it modified 08-29 — a false currency claim, in the very file I was using to
design the cohort-wide staleness check (`docs/internal/design/tracked-state-staleness-design-2026-08-29.md`).
Prose headers drift because updating content and updating the header are two acts joined only by memory.
The frontmatter above is machine-checkable; the prose is not. **Adopted here first so the design has a live
reference implementation, not just a spec.**

⚠️ **CRON ROTATION WATCH**: `cd9b3ddc` expires ~08-31. **Rotate proactively at the 08-30 START**
(delete-then-create, verify exactly one job, record old→new id) — the 08-18 and 08-24 rotations are the
worked precedent; don't wait for the silent death.

## ✅ The trigger-time refresh check is CIO's, not mine — verified 2026-08-29, dropped from my queue

**CIO accepted it into their lane and banked it to a fresh session** (their 08-28 day-close log, `~19:40`
entries: *"accepting CXO's mail-send.sh trigger-time-check proposal into CIO's lane, banked with the same
day-close-is-the-wrong-moment reasoning CXO used themselves"*). **Verified in their log rather than inferred
from HOST's mention of it** — my own carry-forward said "unless CIO takes it," and acting on that
conditional without checking is how two agents build the same thing.

*Retained for context, since I originated the diagnosis*: HOST's 4th lapse showed my diff-mode checker
fixed the wrong half — their failure isn't "edited content, forgot the bump," it's the gap between the
**trigger firing** (filing a workstream review) and the refresh beginning. The fix belongs in
`mail-send.sh` (run the audit when a memo matches a role's `refresh_trigger_glob`), **not** auto-bump.
**Nothing owed by me here** — HOST has accepted being the fifth data point either way.

## What closed 2026-08-28 (the densest day of the cycle)

- **Ship #058** written + sent; **portfolio §2 fully refreshed**.
- **FTUX surface mapping delivered** (`ftux-surface-mapping-2026-08-28.md`) on PM's direct ask — lens
  applied *first*, ~40 speculative cells → 2 live ones + the empty-state gap. **PPM filed the gap as #1688
  (MVP, on the board)**; PM's §1 ruling (existing chat view, no new home view) landed in the doc and on the
  issue — it had existed only in chat.
- **Three PM ratifications executed into artifacts**: the floor/ethics split (retire floor-quality as a
  *coverage statement*; ethics-decline VOICE half → triggered, with method + denominator); **§4's
  "must not be asked to" column** — which was `experience-across-surfaces.md`'s **last** open item, so that
  page is now fully ratified; **sync-before-mail** as a standing rule (CIO landed it as skill v1.30, my n=2
  denominator carried forward honestly).
- **Lead unblocked directly** on both "quiet" threads; they root-caused both (stale carry-forward row; an
  opener that listed the inbox before merging) and fixed their opener.

## Open at handoff

- ~~The trigger-time check~~ — **CIO's, confirmed 08-29.** Not mine; don't rebuild it.
- **#1688** — Lead's one-mechanism-vs-two-builds call is the live question; PPM owns the board.
- **#1635 build** — Lead's, queued behind an in-flight lane (real trigger, not "no rush").
- **#1539 close** — after PM's next live round exercises the shipped purpose line.
- **#1509** — rides the next deploy; PM's live retest closes it.
- **Ethics-decline VOICE watch** — now TRIGGERED: fires on a deploy touching floor/decline copy, or a live
  decline observed. Method: Colleague Test. Report with a denominator, never a bare all-clear.
- Watch: the taxonomy's PDR-005 citation fix (small, unclaimed).

---

*(Prior header below — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-27 22:4x PT at the POST-FREEZE wake. Day closed; next fire 06:47
on 08-28, opening ~07:17.

## Read this first: the 08-25→27 freeze, and what happened at the wake

**An infrastructure event froze this session from 08-25 ~13:30 through 08-27 22:17** — 15 cron ticks queued
(not dropped) and arrived as one wake; the freeze-watchdog correctly flagged "3 roles silent." **Cron
`cd9b3ddc` SURVIVED** (verified at the wake; expires ~08-31, rotation watch from ~08-30). Gap days
08-25/08-26 have truthful retroactive closes in their logs.

**Drained at the wake**:
- **#1635 false door — my position delivered to Lead** (2 days late, freeze-caused, said so): Radar card
  YES, with two build rules (placeholder never outranks real held state + suppressed on empty Radar, where
  the FTUX interview owns the moment; copy claims future never present) and final strings ("not watching
  anything yet" as the self-honesty clause). Lead builds when sequenced.
- **Slack descope (PM-ratified via PA's BYOC conversations 08-26/27) — confirmed from the FTUX side**:
  convergence with the ratified F-Integrations set; one timing nuance recorded (the taxonomy's
  #1481-batch re-evaluation trigger moved further out with Fast Follow). **The BYOC conversation with PA
  HAS now happened** — which was the named trigger-input for my FTUX surface-mapping pass.
- Exec's cross-project reply protocol: read in (`to:` names the real recipient, deliver via exec's inbox,
  Exec brokers).

## Open going into 08-28 — the surface-mapping is now un-gated

- **FTUX surface-mapping** — mine, and **its named trigger condition is now satisfied** (the BYOC/connector
  conversation landed; PA's memo + decisions.log entries carry the outcome). Next fresh working fire with
  a clear queue = do it. Inputs: the ratified FTUX model, the ratified taxonomy, PA's connector-architecture
  finding, the Slack descope.
- **§4's "must not be asked to" column** — with PM (five cells, approve/adjust/strike), 6 days pending, PM's
  been in heavy testing+BYOC conversations — a gentle re-surface is fair when next in direct contact, not a
  chase.
- **#1539 close** — PM's next live round exercises the shipped purpose line.
- Watch: HOST's checker cycle · #1635 build (Lead) · the taxonomy's PDR-005 citation fix (small, unclaimed).

---

*(08-24 22:2x header below, left as the pre-freeze record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-24 22:2x PT at STOP. Day closed (rotation done at START, then five
quiet fires); next fire 06:47 on 08-25, opening ~07:17.

**Second fully quiet day running** — the board is correctly with others: §4's column (PM) · FTUX
surface-mapping (mine, fresh-session trigger, ideally post-BYOC-conversation) · #1539 close (PM's next
live round) · HOST's checker cycle · the taxonomy's PDR-005 citation fix (small, unclaimed). **Cron**:
`cd9b3ddc`, healthy, expires ~08-31, watch from ~08-30.

---

*(08-24 07:3x header below, kept as the rotation record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-24 07:3x PT

✅ **CRON ROTATED as flagged**: `c84a440a` → **`cd9b3ddc`** at the 08-24 START (delete-then-create,
CronList-verified exactly one job), expiry pushed to ~08-31. Registry row updated. **Next rotation watch:
from ~08-30.**

**08-23 was fully quiet** (five checked fires; its 21:47 tick queued overnight and stacked with Monday's
06:47 — one wake, 08-23's close written at it, recorded not backfilled).

**Open going into the week** (unchanged): §4's column (PM) · FTUX surface-mapping (mine — fresh session,
ideally post-BYOC-conversation) · #1539 close (PM's next live round exercises the shipped purpose line) ·
HOST's by-hand checker cycle (their report) · the taxonomy's PDR-005 citation fix (small, unclaimed).

---

*(08-22 22:3x header below, left as the weekend's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-22 22:3x PT at STOP. Day closed; next fire 06:47 on 08-23, opening
~07:17.

⚠️ **CRON ROTATION WATCH ACTIVE**: `c84a440a` expires ~08-25 (7-day cap from the 08-18 rotation). *(DONE
08-24 — see header above.)*
**Rotate proactively at the 08-24 START** (delete-then-create, verify exactly one job, record old→new id) —
same play as 08-18's clean rotation; don't wait for the silent death.

## What closed on 08-22 (a five-for-five Saturday)

1. **#1536 CLOSED by Lead** — the cold-account leg was covered by the no-connector canary pins; Lead
   re-ran the full suite same day before closing. **The four-week Jake first-contact arc is complete.**
2. **#1539's purpose-line strings SHIPPED same evening** ("what I'm already keeping track of… you don't
   need to hold this list — I've got it") — the handed-back grep-old-fragments lesson caught the pins in
   the #1615 suite AND a floor-directive echo of the old framing. AC-2 met at next deploy; **close follows
   PM's next live round (AC-3's falsifier)** — watch for that, then Lead closes.
3. **The checker diff mode BUILT + behaviorally verified + independently verified by HOST** (their own
   probe method, not mine). HOST runs it by hand for a real cycle; their honest report decides hook
   wiring. My listen, not my chase.
4. **#1674/#1675 closed** (Lead, same-day fixes of Run-14's findings).
5. **#1539 loop-closed on-issue** with PM's 1-1 confirmation (the morning's first act).

## Open going into 08-23

- **§4's "must not be asked to" column** — with PM, the single remaining 1-1 item (five cells,
  approve/adjust/strike; clarified to PM 08-21 evening).
- **FTUX surface-mapping** — mine, the named next phase. **Named trigger: a fresh session, ideally after
  PM's BYOC conversation with PA lands** (its outcome shapes the chat-host column; the Web half doesn't
  strictly depend on it, but mapping once with full inputs beats mapping twice).
- **#1539 close** — after PM's next live round exercises the shipped purpose line.
- Watch quietly: HOST's by-hand checker cycle; the taxonomy's PDR-005 citation fix (named in the ratified
  doc §2a as post-ratification mechanical work — unclaimed, small, could be mine or Docs').

**Cron**: `c84a440a` (rotation watch above). **Worktree**: `~/Development/piper-morgan-worktrees/cxo`
(Model A) · **Branch**: `claude/cxo-cycle`.

---

*(08-21 22:3x header below, left as the prior day's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-21 22:3x PT at STOP. Day closed; next fire 06:47 on 08-22, opening
~07:17. **The biggest CXO day since the reboot — read this header fully before assuming any prior state.**

## What closed TODAY (all verified, all on origin/main)

1. **Surfaces taxonomy RATIFIED v1.0** (PM's word on naming, morning). Fully closed.
2. **The FTUX 1-1 happened and CONCLUDED ALIGNED** (PM live via remote-control, 11:03–~18:0x). Outcome
   doc: **`docs/internal/design/ftux-experience-model-2026-08-21.md`** v0.1 (PM co-owns; captures the
   meeting-a-good-colleague frame, Piper-speaks-first + the BYOC greeting variant, three-states-one-
   principle, wizard-as-offer-inside-FTUX, ceremony-scaled-to-novelty, Radar briefing logic, held-state
   parity). **Notification sent to Arch/PPM/Lead/PA cc PM** — all three of Arch/HOST/PA closed their loops
   same evening (PA integrating it ahead of PM's BYOC conversation with them).
3. **§3 + §6 of `experience-across-surfaces.md` RATIFIED live** and applied to the doc; Surface-1/Surface-3
   questions closed via the taxonomy. **The ONE remaining ✏️ there: §4's "must not be asked to" column** —
   clarified to PM cell-by-cell on request, awaiting approve/adjust/strike. Last open item from the 1-1.
4. **#1386 criterion-2 SIGNED OFF** (same-day commitment honored): Lead ran keyed canonical Run 14 tonight
   (98.4% routing, 100% quality, ZERO skips, three failures honestly triaged → #1674/#1675). Verified at
   three layers (memo/issue/CSV) before signing. **My "seats lack keys" claim was STALE** — keys were
   provisioned since the July record I kept citing; correction accepted on the issue. *Verification notes
   have expiry dates.*
5. **#1673 filed** (held-state parity audit, PM's principle, can-wait) — Arch already attached the
   ADR-078-D4 boundary to it (verified on-issue).
6. **#1509's disclosure copy fixed** (mine), verified by Lead (my honest not-run flag caught two old-copy
   literals), staged. **#1509 itself reopened after my commit-message slip auto-closed it** — owned,
   explained on-issue. Ship #057 filed; portfolio refreshed (also fixed stale #1466 row).

## Open going into 08-22

- **§4's column** — with PM, the single remaining 1-1 item.
- **Surface-mapping of the FTUX model** — the named next phase (model first, then map — PM's framing);
  waits on nothing but bandwidth and possibly PM's BYOC conversation with PA landing first.
- **The checker diff-mode build** (HOST's 3-lapse data; design committed in mail) — **named work item for
  the next working fire**; HOST watching, not chasing.
- **#1536** — confirm remaining legs with Lead (cold-account case + board reconciliation) now that PM's
  v58 PASS is on record. **#1539** — the value-prop candidate is effectively CONFIRMED by PM in the 1-1
  ("on-target, aligns with the website line") — worth closing the loop on the issue itself next fire.
- Watch: #1625's lean (in the model now via Radar-briefing-logic), #1674/#1675 (Lead's, from Run 14).

**Cron**: `c84a440a`, healthy, expires ~08-25 (rotation watch from ~08-24).

**State of the conversation** (full content in the live session; key facts):
- **Surfaces taxonomy RATIFIED v1.0 this morning** (PM's word on §1 naming, via Exec). Fully closed.
- **PM confirmed the value prop on-target**, aligned with the website line *"Piper holds the threads so you
  can focus on the decision."* Suggested that line may be the better §3 formulation for
  `experience-across-surfaces.md` — open, PM considering.
- **My FTUX working model is on the table awaiting PM's pushback**: meeting-a-good-colleague frame; Piper
  speaks first; three states as one principle (demonstrate what's held, make handing-over cheap; the
  interview IS the value delivery in the empty state); wizard becomes an offer inside FTUX, not its gate;
  every conversation opens from held state, ceremony scaled to novelty (standup = mature form of the
  first-contact rail); Radar filtering follows briefing logic (PM: Radar needs toning down, MVP-blocking
  only if it spoils FTUX; dormant home-screen rollup idea back on the table eventually). Offered to draft
  as a one-page co-owned experience model once discussion settles.
- **Corrected my own stale carry live**: PM DID test #1536's demo (v58 round 08-18, PASS, via #1615's
  closure). Remaining legs: cold-account case + board reconciliation — confirm with Lead what's left.
- **#1386 criterion-2 unblock path named to PM**: one keyed run via the #1597-proven live harness (or a
  provisioned key); offered to send Lead the direct ask — awaiting PM's word.

**Also this afternoon**: Lead verified my #1509 disclosure-copy fix — suite failed first run (two
assertions carried old-copy literals away from the marker constant), my honest "not run" flag paid for
itself; both fixed, green, staged. **Lesson adopted: grep for old-copy fragments, not just the marker.**
Answered HOST's checker question: committed to a **diff mode for `check-refresh-promises.py`** (edit-time
catch, claim stays deliberate, advisory wiring) — **named work item for the next working fire.**

**Watch list**: taxonomy ✅ closed · #1536 (confirm remaining legs with Lead) · #1539 (PM, and directly in
play in the 1-1 — the value-prop sentence) · #1625's lean (in play in the 1-1 — Radar toning) · #1509
(staged, rides next cut) · #1386 (unblock path offered to PM).

---

*(07:2x header below, left as this morning's record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-21 07:2x PT

**07:17 START — did the flagged gut-check properly**, widening past the usual three-issue glance to every
thread named in recent STOPs. **Found #1605 closed 08-17** (PM live-verified the ratified verb-
disambiguation design working correctly in production) — had simply dropped off my narrow daily check,
nothing wrong, nothing more needed. Everything else confirmed genuinely quiet, not overlooked: taxonomy
doc unchanged since 08-16; FTUX conversation still has no trace anywhere in the cohort (searched session
logs, mail, decisions.log broadly, not just my own inbox) — 4 days pending, Lead's log confirms using my
prep but not that the conversation happened. Still not chasing; PM sets the pace.

**Watch list going forward, now verified accurate**: taxonomy (PM), #1536 (Lead), #1539 (PM), #1625's lean
(posted, awaiting response), #1509 (Lead builds), #1386 (unchanged). #1605 removed — closed, resolved
positively.

---

*(08-20 22:2x header below, left as yesterday's fuller STOP record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-20 22:2x PT at STOP. Day closed (fully quiet, six checked fires,
second idle day in a row); next fire 06:47 on 08-21, opening ~07:17.

**Cron**: `c84a440a` — confirmed present all six fires, healthy, expires ~08-25. **Worktree**:
`~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**Two idle days running** — nothing has moved on any tracked thread since 08-18 evening. FTUX conversation
now 4 days pending, still correctly not chased. Everything else (taxonomy, #1536, #1539, #1625, #1605,
#1625/Radar, #1509, #1386) unchanged since the weekend/Monday work. **Worth a light gut-check at the next
fire on whether the accumulating quiet on any of these deserves a check-in** — not tonight's call, but
flagging so it doesn't just silently extend to a third and fourth idle day unexamined.

---

*(08-19 22:2x header below, left as yesterday's fuller STOP record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-19 22:2x PT at STOP. Day closed (fully quiet, six checked fires);
next fire 06:47 on 08-20, opening ~07:17.

**Cron**: `c84a440a` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires, healthy, expires
~08-25, no watch needed. **Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**:
`claude/cxo-cycle`.

**Today (08-19) was fully quiet** — zero movement on any tracked thread across all six fires. The FTUX
conversation still hasn't visibly happened, now two days since prep was sent
(`reply-cxo-to-lead-cc-pm-ftux-prep-my-read-before-the-conversation-2026-08-18.md`) — check at next START,
still not worth chasing. Taxonomy doc, #1536, #1539, #1625 all unchanged since 08-16-18.

**Nothing owed by me right now.**

---

*(08-19 07:2x header below, left as this morning's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-19 07:2x PT

**07:17 START — checked thoroughly whether the FTUX conversation happened; it hasn't yet.** Searched
mailbox, `decisions.log`, and every mail file modified since the strategic brief landed — only my own prep
memo and its distribution exist. **Not chasing** — PM sets the pace per Lead's own brief. Prep
(`reply-cxo-to-lead-cc-pm-ftux-prep-my-read-before-the-conversation-2026-08-18.md`) is sent and ready
whenever it happens: platform-dependent reframe of chat-first vs. structured-first via the surfaces
taxonomy, #1625's upcoming-reminders question connected concretely.

**Board check**: #1536/#1539/#1625/taxonomy doc all unchanged. **Nothing owed by me right now** — still
watching for the conversation to happen, not manufacturing action while it's pending.

---

*(08-18 22:2x header below, left as last night's fuller STOP record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-18 22:2x PT at STOP. Day closed; next fire 06:47 on 08-19, opening
~07:17.

## 🔴 FIRST THING TO CHECK AT NEXT START: has the FTUX conversation with PM happened?

Lead flagged it as imminent this evening (08-18 ~19:00). Prep sent (`reply-cxo-to-lead-cc-pm-ftux-prep-my-
read-before-the-conversation-2026-08-18.md`) — platform-dependent reframe of chat-first vs. structured-
first, using the surfaces taxonomy; #1625's upcoming-reminders question connected concretely. **As of
08-18 22:17 STOP, no sign the conversation has happened yet** — could be live elsewhere and just not
visible in mail/GH, or genuinely hasn't started. Check for any trace (mail, GH comments, decisions.log)
before assuming either way.

**Cron**: `c84a440a` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires today, healthy on a
fresh ~7-day window (expires ~08-25, no active watch needed for several days). **Worktree**:
`~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**Today (08-18) in one line**: proactive cron rotation at START (the flagged priority, handled cleanly),
three quiet fires, then real design prep for the FTUX conversation late in the day. #1536/#1539 unchanged.

---

*(08-18 19:2x header below, left as this evening's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-18 19:2x PT

**19:17 fire — real prep work for an imminent PM conversation**: Lead briefed me ahead of PM coming
directly to discuss *"should FTUX even be a chat?"* — PM's discouraged after four live test rounds this
week kept finding interpretation-layer brittleness (10/15 chat tests passing, 5 misses all
first-impression-lethal). Read Lead's full strategic brief (`conversational-layer-strategic-brief-2026-08-
18.md`) before forming a position.

**My read, sent as prep not a ruling**: the "chat-first vs. structured-first" question is a false binary —
it's platform-dependent, and my own surfaces taxonomy (confirmed v0.2 this week) is the instrument that
shows why. On Web, structured-first is buildable and lower-risk (Radar/Files lead; matches F-FirstRun's
original May scoping as a templated, non-LLM-touch surface). On chat hosts, there's no separate structured
landing to lead with — #1536's first-contact rail (deterministic, minimal-interpretation first turn) IS the
structured-first equivalent for that platform, already built. Same principle, two platform-native
instantiations, not competing options.

**Checked #1625 rather than assuming it was still where I'd left the Radar review**: found PM live-tested
08-18 and was surprised by an empty pinned section (correct per the due-only ruling, but a real design
signal) — expected to see upcoming reminders somewhere. Connected this directly to the FTUX question: if
Web goes structured-first, an incomplete-feeling Radar on a new user's first visit undermines the whole
"Piper already knows your stuff" thesis. Posted a lean (show upcoming reminders as ordinary unpinned
entries) on the issue, not decided unilaterally.

**Sent the full prep to Lead cc PM**, explicit that it's ready-for-the-conversation, not a substitute for
it. #1536/#1539 still unchanged. **Watching for the actual PM conversation to happen — that's the live
thread now, more than any single tracked issue.**

---

*(08-18 07:2x header below, left as this morning's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-18 07:2x PT

**07:17 START — the flagged cron priority, handled**: `fa499dae` was ~6 hours from its 7-day auto-expiry
(would've landed ~13:18 PT today). Rotated proactively rather than waiting for a silent death: `CronDelete
fa499dae` → `CronCreate` same expression → `CronList` confirmed exactly one job. **New job id: `c84a440a`,
expiry pushed to ~08-25.** No gap, no missed fire.

**Board check**: mailbox empty, #1536/#1539 unchanged (#1536 now 8 days since merge), taxonomy doc
unchanged since 08-16 13:19 — still with PM, not chased. **Nothing owed by me right now.**

---

*(08-17 22:2x header below, left as yesterday's fuller STOP record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-17 22:2x PT at STOP. Day closed (six quiet-but-verified fires);
next fire 06:47 on 08-18, opening ~07:17.

---

*(08-16 22:2x header below, left as yesterday's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-16 22:2x PT at STOP. Day closed (verified six fires this time, not
five); next fire 06:47 on 08-17, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires today, no rotation
needed. Re-armed 08-11 13:18 PT post-reboot, ~7-day expiry — five days in now, watch continues, not yet
urgent (2 days of margin left as of this writing). **Worktree**: `~/Development/piper-morgan-worktrees/cxo`
(Model A) · **Branch**: `claude/cxo-cycle`.

**Today (08-16) in one line — the fresh-session trigger paid off, then went quiet correctly**: wrote the
full surfaces-taxonomy v0.1 in the START fire (two axes, both forensic corrections resolved, the platform
axis's PDR-005 grounding). Both Arch and PPM consulted same-day; Arch's consult required accepting a real
m-49 correction (I'd cited PDR-005 prose as if it were verified code — it isn't) which I fixed in full
rather than defended; PPM resolved every cross-matrix cell with a durable general rule and then, on a
second pass, re-derived the notification-layer routing from first principles and strengthened the argument
further. Both fully confirmed by end of day. **Only PM's word on §1's naming stands between v0.2 and
ratification.** Three fires after that were genuinely quiet — correctly logged as such, not padded.

**Open at handoff**: the taxonomy (PM, no deadline), #1536 (Lead, ~5 days quiet), #1539 (PM), #1605's tiny
phrasing (Lead), #1625/Radar (Lead), #1509 (Lead builds), #1386 (unchanged), the four ✏️
`experience-across-surfaces.md` items — **likely superseded by the taxonomy now, worth confirming once PM
responds rather than assuming**. **Nothing owed by me right now.**

---

*(08-16 13:2x header below, left as this afternoon's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-16 13:2x PT

**13:17 fire**: both Arch and PPM independently VERIFIED v0.2's applied fixes rather than trusting my
summary — Arch checked §3's correction actually landed as described; PPM re-derived the notification-layer
routing against the L4 vision doc from scratch (had suspected a reactive-vs-proactive mismatch, found the
column's own out-of-session-only definition resolves it) and strengthened the doc with that finding.
Incorporated PPM's stronger reasoning into §4. **Taxonomy is now fully confirmed by both consults — the
only thing left is PM's word on §1's naming.** Nothing more to do on this thread until that lands.
#1536/#1539 still unchanged, ~4 days. **Nothing owed by me right now.**

---

*(08-16 10:2x header below, left as this morning's fuller record — not re-derived.)*

**10:17 fire — both consults landed same-day, one required a real correction, applied to v0.2**: Arch
ratified the F-AuditTransparency split AND caught something in my own draft — I'd cited PDR-005's design
prose (capability-claim layer, client-identifier dispatch) as "receipts" that the platform axis already
operates in code. Arch checked: **it doesn't** — zero references anywhere in `services/`. Exact m-49 shape
("Described Is Not Running"), caught before shipping uncorrected. Fixed §3 with the full correction plus a
genuinely useful forward pointer (`CommandRegistry`/`CommandInterface` has the right shape, unused
`SETTINGS` slot). PPM resolved all seven open cross-matrix cells with a general rule (cells gated by an
already-ratified hold — #1481's Slack hold — inherit that status automatically) rather than seven one-off
guesses, plus caught that my own document used PM's illustrative example as if it were a build signal —
fixed. Routed the notification-layer question to #1174 rather than ruling on it myself. **v0.2 sent, both
consults acknowledged plainly (accepted Arch's correction without defending the original), nothing left
before ratification except PM's word on §1's naming.**

**#1536/#1539 still unchanged.** Nothing else owed by me right now.

---

*(08-16 07:2x header below, left as this morning's fuller v0.1 record — not re-derived.)*

---

*(08-15 22:2x header below, left as last night's fuller close record — not re-derived.)*

## 🔴 TOP OF QUEUE, NEXT SESSION: the surfaces taxonomy — real, foundational, prepped, no deadline

PM (via Exec, 08-15 16:40 PT) wants the "Surface 3 phantom" question superseded by a formally rectified and
**ratified two-axis taxonomy**: a NEW platform/touchpoint axis (desktop/mobile/CLI/Slack/voice-class,
explicitly non-exhaustive) crossed with the EXISTING seven functional surfaces (history, privacy, settings,
integration wizards, search, first-run, audit/error). **PM's proof they're orthogonal**: Settings needs both
a web-app screen AND a conversational path — same functional surface, two platforms, which a single
flattened list would hide. **PM named me lead**, consulting **Arch** (does the platform axis carry real
architectural consequences, or is it presentation-only) and **PPM** (which axis-combinations are MVP-
required vs. aspirational). **No deadline. PM's own words**: *"beware the strong tendency to flatten it
into semantically compact ideas that lose the modeling."* Full brief:
`mailboxes/cxo/read/brief-pm-to-cxo-relayed-by-exec-rectify-ratify-the-surfaces-taxonomy-two-axes-not-one-2026-08-15.md`.

**Forensic findings already in the brief, don't re-derive**: Surface 3 ("Settings/preferences") is real —
Lead Dev's 05-14 memo, CEO-ratified by name in my own Round 2 synthesis (05-15/16), scoped tiny
("account profile editing + basic notification opt-outs only"), never phantom — it just never made it into
PDR-005's own citation. Surface 7 genuinely conflates two things (error/degraded states + the
audit-transparency read-surface, folded in mid-process as a "keystone").

**Source material located, ready to open**: `mailboxes/cxo/sent/mux-ui-gap-cxo-round-1-synthesis-2026-05-15.md`,
`...round-2-synthesis-2026-05-15.md` (the one place all seven were named together), origin memo
`mailboxes/cxo/read/memo-lead-to-cxo-cc-ceo-mux-guidance-ui-architecture-gap-2026-05-14.md`.

**Deliberately not drafted 08-15** — tail of a long Saturday, no deadline, and rushing it would be the
exact flattening PM is asking me to prevent. Named trigger for the deferral: a fresh session. **This is
that session, whenever it arrives** — start here, not at the bottom of the file.

**Also check**: my carried `experience-across-surfaces.md` four ✏️ items are likely downstream of this
taxonomy rather than parallel to it (Exec's read, I agreed) — confirm once a real draft exists, don't
assume.

---

*(Everything below was accurate as of 08-15 22:2x STOP; re-verify before treating as current.)*

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires today. ⚠️ **Auto-expires
~2026-08-18 (re-armed 08-11 13:18 PT post-reboot) — three days out. Watch for silent expiry; both deaths
(session-end, 7-day cap) emit nothing.** **Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A)
· **Branch**: `claude/cxo-cycle`.

**Today (08-15) in one line**: agreed on #1509's outwardness consent axis (real reasoning, a scope
boundary, a mechanism note); PPM independently stress-tested and confirmed. Caught a real "one name, two
objects" citation error in the first-contact criterion's ratification — fixed in mail, the doc's status
line, and (PPM caught what I missed) `decisions.log`'s entry too. Reviewed #1625's shipped Radar
pinned-reminders code and sent two concrete fixes (wrong color token, missing count) plus two flagged
questions. Lighter day than 08-13/08-14 but every substantive fire found something real.

**Open at handoff**: #1536 (Lead, ~6 days quiet, already flagged in Ship #056 — don't re-flag), #1539 (PM),
#1605's tiny remaining phrasing (Lead), #1625/Radar (Lead, no urgency), #1509 (agreed both sides, Lead
builds), #1386 (unchanged), four ✏️ items on `experience-across-surfaces.md` + Surface 3 (PM, over a week).
**The cron expiry is the one thing needing active attention over the next three days** — everything else is
correctly parked with someone else.

---

*(08-15 16:3x header below, left as this afternoon's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-15 16:3x PT

**16:17 fire — three items, all handled**:
1. **PPM agreed** on the outwardness axis (independently stress-tested my scope boundary against
   `close_issue`, held). Settled, Lead builds. No action from me.
2. **First-contact criterion ratified** — PM's condition was joint sign-off on the *merged document*
   specifically. Read it fully, gave real sign-off. **Caught a numbering error in Exec's justification**:
   my 08-12 review was of item 2 (only-Piper-could) in this doc's numbering, cited as "item 3" — item 3 is
   the fabrication/citation gate, which I'd never reviewed until this fire. Corrected in the mail and
   **directly in the doc's own status line**.
3. **Radar pinned-reminders review** (#1625, PM-ruled, merged, not yet deployed) — read the actual shipped
   code (template CSS/JS, `ReminderEntitySource`, the radar route) rather than reviewing from description.
   Two concrete recommended changes (wrong color token — primary blue instead of the warning-amber token;
   no count in the section heading) + two flagged-not-blocking questions (no cap on pinned accumulation;
   pinned cards intentionally not clickable, ties to my own #1605 work from yesterday). Sent to Lead.

#1536/#1539 still unchanged. **Nothing else owed by me right now.**

---

*(08-15 13:2x header below, left as this morning's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-15 13:2x PT

**13:17 fire**: PM ruled (leaning YES) on the #1509 outwardness-consent-axis question, conditional on
CXO+PPM agreement. Read #1509 in full plus Lead's original build comment before answering. **Agreed**,
grounded in the Colleague Test (effect measures undo-difficulty; outwardness measures who witnesses the
action, orthogonal axis) — offered a scope boundary (communication-act only, not "theoretically visible
later," to keep the dimension discriminating) and a mechanism note (disclosure line under TRUST mode,
matching this week's #1510/#1605 "consent tier isn't weakened by mode, transparency is the cheap safety
valve" precedent). Sent to Lead cc PPM/PM, posted on #1509. #1536/#1539 still unchanged, ~5-6 days.
**Nothing else owed by me right now.**

---

*(08-14 22:2x header below, left as the prior day's fuller STOP record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-14 22:2x PT at STOP. Day closed; next fire 06:47 on 08-15, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires today, no rotation
needed. Session-only, auto-expires ~2026-08-18 — **watch for this; getting close.** **Worktree**:
`~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**Today (08-14) in one line**: #1569/#1605 fully closed (copy seams reviewed, ALWAYS_ASK question answered,
PPM confirmed). Agent 360 v0.4 answered in full with real evidence from the week, catching and fixing a
stale freeze-watchdog registry row along the way. Ship #056 workstream report written and sent under a
same-evening deadline compression — the missing original kickoff turned out to be a real mail-send
accident (Exec's own follow-up call deleted it 22 seconds after sending), resolved this evening, confirming
my earlier "delivery gap, not a personal miss" read. `ROLE-PORTFOLIO-CXO.md` §2 refreshed in the same fire
since the report was its own trigger. Report spot-checked clean against the 08-13 omnibus.

**Open at handoff**: #1536 (Lead, live-verification, ~4 days quiet — worth a light mention if it crosses a
week), #1539 (PM, candidate posted), #1605's tiny remaining V2-under-ALWAYS_ASK phrasing (Lead, not
urgent), #1386 (unchanged, still withheld), four ✏️ items on `experience-across-surfaces.md` + Surface 3
naming (both with PM, over a week now, flagged again in tonight's report). **Nothing owed by me right now**
— everything above is with someone else or is a small build item not mine to build.

---

*(08-14 19:3x header below, left as this evening's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-14 19:3x PT

**19:17 fire**: Exec corrected this morning's Ship #056 kickoff — PM wants responses **tonight**, not
Saturday. **Never received the original kickoff** (checked whole mailbox tree, confirmed with Docs' own
report noting the same gap — a real delivery gap, not a personal miss). Wrote and sent the full #056
workstream report (window Fri Aug 7–Thu Aug 13) using the #055 template (progress-against-goals table,
notable-events narrative, what-the-window-taught, commitments, window shape, open PM ask). **Refreshed
`ROLE-PORTFOLIO-CXO.md` §2 in the same fire** since the report is exactly its own refresh trigger —
verified via `check-refresh-promises.py` that it now reads current. Sent to Exec cc PM, well within the
tonight deadline.

**16:17 fire**: HOST fielded Agent 360 v0.4 (cohort-wide, ~2-week window). Queue was otherwise empty, so
answered it this fire rather than deferring — real, specific content from this week's work throughout
(the two stale-tracker catches, the #1510/#1591/#1569/#1605 threads, the mailbox-hook block, the reboot
survival gap). **Found my own freeze-watchdog registry row was stale** (still referenced the pre-reboot
cron id) while answering §10.4 — fixed it, cited the fix honestly in the response rather than hiding it.
Sent to HOST, full response at `mailboxes/host/sent/agent-360-response-cxo-2026-08-14.md` /
`mailboxes/cxo/sent/`.

**10:17 fire**: PPM confirmed the ALWAYS_ASK answer (re-verified against #1510's ruling text directly, no
disagreement). **#1605/#1569 is now fully closed on the design side** — posted on GH, handed the one-cell
V2 phrasing change to Lead to sequence. #1536/#1539 still unchanged, ~3 days. Nothing else moved.
**Nothing owed by me right now.**

**08-14, 07:17 START**: PPM signed off #1569/#1605 overnight (verified Lead's matrix claim personally,
no objection) — that design thread is fully closed. Lead's build landed (`e9ef395a1`): ratified copy pinned
verbatim, #1569's per-item render rule shipped in the same commit. **Reviewed the three flagged copy seams
myself this morning** — all clean, no changes needed, said so explicitly rather than leaving them silently
unconfirmed. **Answered the one remaining open design question** (should ALWAYS_ASK flush/re-verify a
stored verb mapping?): no — a verified preference is a prior explicit answer, not an assumption, per
#1510's own verified≠inferred line; but V2's *form* should shift to an actual question under ALWAYS_ASK
while still leading with the stored value. Sent to Lead/PPM/PM, posted on #1605.

**#1536/#1539**: still unchanged, ~2.5 days. `experience-across-surfaces.md`/Surface 3: still unchanged,
~4 days, both genuinely with PM (four ✏️ items + naming call), not stalled on me — offered the delete
already if PM prefers verbal. Not manufacturing urgency on any of these.

**Nothing else owed by me right now.**

---

*(08-13 22:2x header below, left as the prior day's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-13 22:2x PT at STOP. Day closed; next fire 06:47 on 08-14, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present all six fires today, no rotation
needed. Session-only, auto-expires ~2026-08-18. **Worktree**: `~/Development/piper-morgan-worktrees/cxo`
(Model A) · **Branch**: `claude/cxo-cycle`.

**Today (08-13) in one line — the most substantive design day since the reboot**: PM ruled the #1510
declared-vs-inferred fork this morning; connected it to #1591 same fire; both built and shipped by Lead by
early afternoon; reviewed and endorsed two implementation judgment calls. Separately, PM ruled the
"unmapped verb → ask" policy for #1605/#1569 and jointly assigned PPM+me the UX design; drafted a full
proposal, PPM audited it twice (both passes found real, non-trivial gaps — thread-scoping vs. per-item
origin, and a WRITE/DESTRUCTIVE copy asymmetry that would have let a destructive action skip its blocking
confirm), both resolved with code-verified answers rather than assertions, design now **settled**, final
three-variant copy handed to Lead to sequence the build.

**Open at handoff**: #1536 (Lead, live-verification, quiet ~2 days), #1539 (PM, candidate posted ~2 days),
#1569/#1605 (settled, check if Lead's build landed), #1386 (unchanged all week, still withheld), the four
✏️ items on `experience-across-surfaces.md` and Surface 3 naming (both with PM, now ~4-5 days untouched —
worth a light check, not a chase). **Nothing owed by me right now** — everything above is with someone
else. Next fire: check for movement across the board rather than assuming any one thread is still where
this entry left it.

---

*(08-12 22:2x header below, left as the prior day's fuller record — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-12 22:2x PT at STOP. Day closed; next fire 06:47 on 08-13, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present and correctly expressioned at all five
fires today, no rotation needed. Session-only, auto-expires ~2026-08-18 — **CronList at START.**
**Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**08-13, 10:17 fire**: PM ruled the #1510 declared-vs-inferred fork (low-confidence inference → read back
to user → verify → store, not re-infer; meta-feedback about the verification process is a separate signal
from task-preference feedback). **Posted the connection to #1591** (standup invitation persistence, which
was explicitly waiting on this): the invitation-properties design already IS the read-back mechanism the
ruling describes — no redesign needed, just noting the fit and that #1591's "honest interim, no store yet"
caveat is now stale. #1536/#1539 still unchanged (no PM/Lead response, ~27h). Also closed a second stale
standing-items.md entry this fire (spatial ADR item A — done 07-29, never marked).

**08-13, 13:17 fire**: both #1510 and #1591 got **built** since the last fire (Lead, riding the verified-
inference rail from the morning's ruling) — the connection I posted at 10:17 was picked up fast. Lead
flagged two judgment calls explicitly for CXO/PPM eyes: (1) symmetric anti-nag — declining either standup
ask quiets both, session-scoped; (2) the #1511 teaching-line changed so a stored interview preference can't
trap the user out of reaching the plain report by name. **Reviewed both, endorsed both** (GH comment on
#1591) — call 1 is the right generalization of "cheap to decline" beyond what my original three properties
literally covered, call 2 fixes a real trap without touching property 3. Noted PPM should still confirm on
their own slice's copy. **Remaining on both issues: PM's live retest** — not mine, not attempted.

**08-13, 16:17 fire**: new mail — Lead relayed PM's ruling on #1605/#1569 (unmapped verbs over stateful
ops → ask, never map-by-decree; effect-weighted per #1557; #1510 rail is the machinery). Jointly assigned
to PPM+me: the disambiguation UX shape (#1605) and how it sits with the reminders-presentation question
(#1569). **Drafted and sent a design proposal** (mail to PPM cc Lead/PM/Arch/Exec, GH comments on both
issues): #1569 candidate = keep the unified data model, differentiate presentation by how an item was
*surfaced* (reminder-triggered vs. todo-list-requested), not by storage — no new store needed; #1605
candidate = disambiguation copy that borrows that framing, asked once via the #1510 meta-channel,
deliberately NOT bundling in scope-confirmation (that's #1563's dangling-offer bug, not this design's job
to paper over). Noted the cheap sequencing if #1569 ships first. **Awaiting PPM's read** — this is joint,
not mine to decide alone.

**08-13, 19:17 fire**: PPM audited the #1569/#1605 candidate — real, honest audit (checked code directly),
found two genuine gaps: (1) my original rule was thread-scoped but origin is a per-item property (mixed
reminder+todo listings are structurally possible via #1566); (2) "I'll remember for next time" had no
revision path if the stored default is wrong for one instance. Lead also confirmed the #1605 mechanism
(`decide_verb_interpretation`) is already built and waiting on final copy. **Resolved both gaps**: checked
`context_assembler.py` directly rather than trusting Lead's tentative "origin isn't threaded" belief —
origin already exists as separable data (distinct context keys), so the #1569 rule becomes per-item not
per-thread, no data change needed. Gap 2 resolved via transparency, not a settings UI: every auto-applied
default states itself aloud ("that's what 'clear' has meant for you — say so if you meant X this time"),
which doubles as the same-turn correction path; no #1510-style durative marker needed since the question
itself (not an unprompted statement) already makes durative scope explicit. **Sent full resolution + updated
copy to PPM/Lead/PM/Arch/Exec, posted on both issues.** Awaiting PPM's confirm before Lead treats it as final.

**Today in one line**: closed out 08-11; reviewed #1536's build, unstuck #1539; connected the ruled #1510
fork to #1591 and endorsed two implementation calls; designed #1569/#1605, PPM audited it, resolved both
gaps with code-verified answers. **Real, iterated design output this fire.** Next: re-check
#1536/#1539/#1569/#1605 for response.

---

*(08-12 10:5x header below, left as the fuller record of that fire's reasoning — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-12 10:5x PT

**Superseding the 08-11 16:2x version below — updated in place after acting on two of the open items this
fire (#1536 conformance review, #1539 candidate articulation). Read this header block; the table further
down is still accurate for everything else and wasn't re-verified again this fire beyond what's noted.**

**This fire (08-12, ~10:17–10:5x)**: closed 08-11 properly (no STOP had been written; no activity found
18:47–21:47 on 08-11, not a stall, cron stayed armed). Inbox was empty (0,0). Reviewed #1536's just-landed
build (commit `43d2a4fce`) against the gate criteria I co-defined — **item 3 (only-Piper-could) reads as
met**, posted as a GH comment; flagged that live user-verification is still Lead's "next cut," not done by
me, not assumed done. While reviewing that copy, found a concrete connection to **#1539** (mine, previously
untouched, no comments): the #1536 demo is impressive but doesn't *name* the uncertainty it resolves —
posted a candidate one-sentence articulation (✏️ pending PM) plus the specific gap in the shipped copy.
**Neither #1536 nor #1539 closed by me** — #1536 isn't mine to close (user-verification pending, and it was
never mine to certify alone); #1539 is explicitly "PM+CXO's to answer," and I offered a candidate, not a
ruling.

---

*(Everything below this line is the 08-11 16:2x rewrite, left as-is — still the best record of the fuller
open-item table and standing discipline. Update it in place at the next STOP rather than re-appending.)*

# CXO carry-forward — rewritten 2026-08-11 16:2x PT, first fire after the Amber reboot

**⚠️ This file was stale for two days (last real content update 08-09 07:12) while a full reboot
stand-down happened and the handoff (`docs/handoff-cxo-2026-08-11.md`) carried the current state instead.
That's the exact drift this file exists to prevent — noting it so it isn't repeated silently. This rewrite
supersedes both the 08-09 content below the fold and the handoff §4 table; going forward, **this file is
the state again.**

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — re-armed 08-11 13:18 PT after the reboot killed
`aa1a0c1e` (session-scoped, dies silently; confirmed via `CronList` showing zero jobs, then rebuilt from
the restore spec written into the handoff *before* the reboot). Session-only, auto-expires ~7 days from
re-arm (~2026-08-18) — **CronList at every START.** **Worktree**: `~/Development/piper-morgan-worktrees/cxo`
(Model A) · **Branch**: `claude/cxo-cycle`.

**Dates, so this file doesn't itself go stale on the thing it's warning about**: beta moved back a month
(PM, 08-08); *"out of alpha"* = the **public** beta (PM, 08-10); private beta stays invite-only until the
PUB sprint (#1537–#1540) completes. **Don't trust a cron-prompt date line over this one, and don't trust
this one past its own next rewrite either — check `decisions.log` if it matters.**

---

## ✅ CLOSED 2026-08-11 — standup empty-case resolved, both parties agree, recorded on #1591

**PPM's finding held**: my three invitation properties ("report first, complete, unconditional") were
stated in universal form but are conditional — they govern the case where there's data to report. PM had
already named the exception on #1511: *"if they contain no information or have never been done before,
maybe they go into an interactive sequence."* PPM's resolution: the empty case is governed by a rule
already ratified elsewhere — **#1536 AC3, fail honestly, no fabricated demonstration** — not an exception
to my rule, a different rule taking over at the boundary (discriminator: did the read produce anything).

**My reply sent 08-11 16:18** (`mailboxes/ppm/inbox/reply-cxo-to-ppm-...-2026-08-11.md`, cc lead/PM/exec/
arch/host/pa): agreed in full, named it the same shape as my own §7a defect (universal-sounding criterion
hiding its own scope — **second instance of this exact failure mode in gate language I've written**, worth
watching for a third). **No build action from me** — PPM's GH comment on #1591 (2026-08-11 13:48 PT) is
already the record for whoever implements it. **Thread closed.**

## 🔴 What's actually open — the handoff §4 table, carried forward and reverified against GitHub (16:2x PT)

| Item | State | Owner |
|---|---|---|
| **`docs/internal/design/experience-across-surfaces.md` v0.1** | DRAFT, unchanged since 08-09. **Four ✏️ items still await PM** (§7): the §3 one-sentence formulation · §4's *"must not be asked to"* column · §6's same-colleague corollary · is Surface 1 in the 1.0 five. Offered PM the delete if he'd rather it stay verbal. | **PM** |
| **#1536 first-contact** (FTUX-COLDSTART) | ✅ **Built and merged 08-10** (`43d2a4fce`, Lead-merged, 2510 tests green). **CXO conformance-reviewed 08-12**: item 3 (only-Piper-could) meets the bar. **Still OPEN** — live user-verification is Lead's flagged "next cut," not yet run by anyone as far as I can see. Check before assuming done. | Lead (verification) |
| **#1539 legibility half** (FTUX-PURPOSE) | OPEN. **Candidate articulation posted 08-12** (✏️ pending PM): *"Piper reduces 'is anything actually tracking this for me'..."* — plus a concrete, evidence-based gap: #1536's shipped copy demos capability but doesn't name the uncertainty it resolves. **With PM now**, not stalled on me. | PM (to rule on the candidate) |
| **#1463 deployed-host retest** | OPEN, confirmed. Blocked on **#1462** (also OPEN) — UNBUILT not undeployed; `services/mcp/server/` absent from `main` and the deployed artifact. Promised same-day retest once the package is shippable — **check #1462 status before assuming still blocked.** | #1462 |
| **Standup invitation (#1511 → #1591)** | ✅ Design settled (see above). #1591 tracks the Production/PUB build; both governing rules are on the issue for whoever picks it up. | Lead / whoever builds |
| **#1510 fork** | ✅ **RULED 08-13, BUILT same day** (`836c5a188`, Lead) — `verified_inference.py` + wiring, 41 unit + 4 real-Postgres integration tests, ratchets/smoke green. Remaining: PM's live mode-flip retest. Not mine. | PM (retest) |
| **#1591 standup invitation** | ✅ **BUILT 08-13** (`43d9e8230`, Lead) on the verified-inference rail. Every CXO/PPM spec pin has a named test. **Two judgment calls flagged for CXO/PPM — reviewed and endorsed both** (symmetric anti-nag; #1511 teaching-line trap fix). Remaining: PM's live retest + PPM's word on call 2's copy touch. Not mine further. | PM (retest), PPM (copy confirm) |
| **#1569 + #1605** (reminders-are-todos framing + 'clear' disambiguation) | Candidate → PPM audit (2 real gaps) → both resolved with code-verified answers (per-item origin exists today, no data change; revision path = state-it-aloud, not new UI). Final copy sent, **awaiting PPM's confirm**, then Lead builds (mechanism already exists, `decide_verb_interpretation`). | **PPM to confirm**, then Lead |
| **#1386 criterion-2 sign-off** | OPEN, confirmed. Still **WITHHELD** — keyless suite skips and reports green. Committed to same-day sign-off once a keyed run exists. | me |
| **Surface 3** | Still a phantom — one corpus mention, same sentence that rates Surface 1 "weaker." PPM's ask to PM: name it or strike it. **Now 5+ days open — was 4 at handoff time.** | PM / PPM |

## Standing / carried from before the reboot (unverified this fire — check before treating as current)

- **`dialog.js` latent defaults** — 4 false strings proposed for deletion + `message` made required. Lead's to apply.
- **Colleague Test tier question** — with PPM/PM.
- **⚠️ #950 / #992 watch is UNATTESTED since arriving on Amber.** Read scorer outputs directly, not memos summarizing them.
- **D2 design-system portfolio** (#1286/#1290/#1284/#1269) — flagged to PM in Ship #054 §6 as a decision, was drifting as of early August; recheck.

## ⭐ Fire-time reminders earned the hard way (unchanged, still load-bearing)

0. **Absence in our surfaces is not absence in the world** — before recording a person as owing something, ask whether the discharge would even be visible to me.
1. **Verify a correction before accepting it** — including corrections *of me*.
2. **A methodology entry I wrote doesn't install itself in me** — I've violated my own written rules within days of writing them, twice.
3. **A green on something I just fixed proves nothing.** Negative-control it against the state it was built to catch.
4. **Don't write the convenient sentence** — a specific false claim is worse than an accurate hedge.
5. **grep for ISO dates AND surface forms; never `cut`/filter a command's output to the lines you expect** — that hides the one saying it didn't run.
6. **A coverage report whose denominator is its own registration cannot report what it exists to report.**
7. **My simplifications remove what's one layer down** — I optimize for the layer I can see; what I drop is always beneath it.
8. **zsh does NOT word-split unquoted `$VAR`** — use arrays.
9. **A hand-count is not a substitute for the mechanism.**
10. ⭐ **NEW, earned this fire**: **a carry-forward that says "rewritten at every STOP" and isn't, is worse than one that admits it's stale** — the handoff caught what this file missed only because the reboot forced a from-scratch write. The lesson isn't "write better handoffs," it's **check this file's own git log before trusting its header.**

---

*Next STOP: rewrite this file again, don't just append. If a fire ends without touching this file, that's
the same silent drift that produced tonight's two-day gap — say so explicitly rather than let the next
fire discover it.*
