# Exec Carry-Forward

**Last updated**: 2026-08-27 ~09:4x PT — START/WORK. Agent 360 filed; inbox clean.
**Session log today**: `dev/2026/08/27/2026-08-27-0902-exec-code-log.md`
**Role**: Chief of Staff (Exec) | Amber, Model A worktree, branch `claude/exec-cycle`
## 🔴 STEP ONE, EVERY FIRE — PM DIRECTIVE 2026-08-28: verify all roles are RUNNING first

**Run `scripts/duty-cycle-freeze-check.sh` at the top of every fire, before mail, before anything.**

⚠️ **This is NOT the check I had been running.** Two similarly-named tools, different questions:
- `cohort-freeze-detect.sh` — *is the COHORT frozen?* Returns rc=0 whenever ANY role is alive.
  This is what I ran at every START. **It is structurally incapable of reporting a dark role.**
- `duty-cycle-freeze-check.sh` — *is any INDIVIDUAL role stale?* Prints per-role hours + missed
  fires against each row's own cadence. **This is the one that answers PM's question.**

**Earned 2026-08-28**: arch, cio and host sat dark ~30–33h (since 08-27, almost certainly stuck at
a rate-limit dialog after Thursday's usage limit). I reported Ship #058 as "7 of 10, three haven't
filed" — framing three dead sessions as slow correspondents. PM asked "does anyone need a nudge?"
and the honest answer was that nobody was ignoring anything; three roles weren't running. The
per-role tool printed all three instantly the moment I ran it.

**Why it matters beyond the miss**: a blocked session gets zero turns and cannot report its own
blockage (4th instance this month — Lead 08-20, CXO 08-25→27, my own 08-27, these three). Liveness
has to be checked FROM OUTSIDE. That is the whole point and I was checking the wrong layer.

**Also**: the attention rollup must lead with liveness. A board that says "9 clean" while three
roles are dark is the exact m-44 false-clear this project keeps finding.

**Cron**: re-armed at the 08-28 STOP via delete-then-create, verify exactly one.

## 🔴 TOMORROW'S FIRST WORK — Ship #058 internal report synthesis

**All 10 reports are IN** (`mailboxes/exec/inbox/workstream-058-*`). Deferred from the 08-28 STOP
with a named trigger — **tomorrow's 08:32 START** — because it's a full read of 10 reports + 7
omnibus logs whose whole value is cross-checking claims against sources, and that degrades at the
tail of a 14-hour day. **No time pressure**: #058 publishes Wed Sep 2.

**PM is waiting to discuss it** — their words 08-28: *"stand by for their responses and for us to
discuss your synthesis."* Follow the ten-step cycle: synthesize → PM discusses → then draft.

**Window**: Fri Aug 21 – Thu Aug 27. **Do NOT triage the 10 reports out of inbox** until the Ship
draft is written — that's the collection surface.

## 📅 TOMORROW (Fri 08-28): Ship #058 kickoff

**Window Fri Aug 21 – Thu Aug 27 closes TODAY.** Friday is the kickoff day by the established
cadence (window closes Thu → kickoff Fri → reports → internal report → PM discussion → draft →
publish Wed). #058's pubDate would be **Wed Sep 2**. Self-initiate the kickoff as on 08-21 — it
was correct then and needed no PM prompt. Use `draft-weekly-ship` Step 0's verbatim framing.

## ✅ Agent 360 v0.4 — FILED 08-27 (13 days late; lateness used as the material)

Cleared the oldest owed item. **Two rules earned and proposed**, both from three instances in ten
days of one shape: (1) **provenance check** — a constraint attributed to PM must cite where PM
said it (values-doc bar and the #057 "draft together" gate were both mine, not PM's); (2) **dates
on owed items when recorded** — an owed item with no trigger is indistinguishable from a completed
one at read time (this questionnaire, CXO's ethics watch, Docs' flattening plan, same shape).
Also reported honestly: **I've never behaviorally tested my own hooks**, relying on prose
discipline + Arch's report.

## ✅ Ship #057 PUBLISHED 08-26 — cycle complete, inbox finally empty

https://pipermorgan.ai/shipping-news/weekly-ship-057-a-checked-claim-has-a-shelf-life
PM took option 1 (pass + publish same day). Workstream-057 collection drained — the Ship shipped,
so the collection's purpose is served. **Inbox genuinely empty for the first time in a week.**

⚠️ **My own error, worth carrying as a lesson not just a fix**: the draft said the watchdog chain
"ran through four people." My internal report five days earlier correctly said *"four LINKS"* and
named all four steps (CIO → HOST → Exec → HOST). **I changed the unit and carried the count
across.** Four links true, four people false — HOST appears twice, a fact sitting in my own prior
sentence. Also "people" for agents, a real vocabulary conflation. Docs caught the count, PM caught
the noun. **The Ship is literally about a checked claim going stale on restatement, and I did it
inside the piece.**

⚠️ **`mail-send.sh`'s STRANDED-MANIFEST warning fired twice on 08-26, both FALSE POSITIVES.** It
can't distinguish "this MANIFEST was unchanged this round" from "this MANIFEST is stranded."
**Verify before resending** — once the two copies were byte-identical, once origin/main was correct
and the LOCAL copy was stale (an ordinary merge fixed it). Blindly obeying the warning would have
pushed a stale file over a good one.

## ✅ Relay protocol — FIRST LIVE USE 08-26, worked as designed

Comms → Dispatch-PM, routed through exec/inbox exactly per the broadcast. Relayed and pushed, no
correction needed. **One gotcha for the next relayer**: the dispatch repo has no git identity set
(it's per-repo, not global) — `git commit` fails with "Author identity unknown." Don't mutate
another project's config; pass `-c user.name=xian -c user.email=xian@Amber.local` for the one
commit (matches what prior exec commits there used).

## ✅ Cross-project reply protocol — RATIFIED + BROADCAST 08-25

Real structural gap, measured by Dispatch-PM: `mail-send.sh` refuses non-`mailboxes/` paths AND
DIRECTORY.md forbids a mailbox for cross-project agents → **no compliant reply path existed**.
**The rule now**: write the memo with the REAL recipient in `to:`, cc exec, deliver to
`mailboxes/exec/inbox/` normally — Exec relays. Dispatch-PM sweeps `origin/main` twice daily as the
backstop. Broadcast sent to all 10 roles. **The dispatch repo IS cloned/writable on Amber** (`~/Development/dispatch/`) — sync first, stage own file by explicit path only.
**Three DIRECTORY.md gaps routed to Docs** (no `mail-send.sh` next-step documented; `pard` unlisted
though the mailbox has traffic; `janus`/`dispatch-dinp` unlisted).

## 🆕 Browser blocker — escalating to Pard via Dispatch-PM

Sent the concrete specifics: PA acute / Web structural / Docs episodic; three distinct work classes;
**both a missing binary AND missing tooling** (no Chrome/Chromium on the Amber worktree per PA's
check; no MCP path to drive Safari per Web's). **The privacy-policy render check is now routed to
Dispatch-PM** rather than sitting on PM's plate as a "ten seconds of your time" ask — they have
browser control.

⏰ **Ship #057 publishes TOMORROW (Wed Aug 26)**, still `drafted`, awaiting PM's fact-check + voice
pass. PM has the preview artifact and both file paths (asked for them 08-25 afternoon).
⚠️ **One defect found and fixed tonight**: Comms caught the frontmatter carrying a narrative post's
art instead of the standing `piper-ship.png` — verified against #054/#055/#056 (3 for 3) before
fixing, both copies corrected, in-body hero teaser untouched. **Second frontmatter-`image:` defect
in a week by a different mechanism** — worth watching whether `website#33`'s guard should widen.
**SURFACED 08-26 09:2x as planned** — sent PM three options (publish today after a pass / pass
today publish tomorrow / slip a week, leaning against the last), cc Comms+Docs. **That was the one
surface; do not re-flag.** PM's call now, and any of the three is a fine answer.

## 🆕 Dispatch-PM — new cross-project agent, introduced 2026-08-24

PM's outside-vantage coordinator, running in **Cowork on faoilean** (not Claude Code, not Amber).
Correctly declined a mailbox here per DIRECTORY.md; **reach them at `~/Development/dispatch/mail/`**,
and a memo isn't visible to them until it's on `origin/main`. They took over Building-Piper-Morgan
cross-posting starting 08-25.

**Their comparative advantage is reach, not judgment**: browser control, native macOS GUI control,
scheduled tasks on PM's account. **Several of our roles have "no browser on this host" as a standing
blocker** — that class of work is genuinely cheapest routed to them now. Their inverse limit: their
sandbox cannot reach GitHub at all, so anything pure-repo-shaped stays with us.

They caught a real stale-MANIFEST defect on my own inbox surface three days in. Verified and fixed.
**Worth continuing to invite that** — an outside vantage noticing what an inside role stopped
seeing is the whole value.

⚠️ **They flagged faoilean's `piper-morgan-product` checkout as diverged (4 ahead, 957 behind,
dirty since 08-18, `git pull` aborts on 8 mailbox MANIFESTs).** Not mine to fix and not resolved —
PM's machine, raised to PM directly by them. Relevant to us only as: anything reading that working
tree gets a six-day-old picture.

## Closed today — `/insights` cross-repo consolidation sent to PM

The named trigger from last night ("next session") arrived this morning with nothing else queued,
so did it rather than deferring again. Cross-referenced both reports (laptop + Amber) against
Piper's actual CLAUDE.md/scripts — most of the ~15 recommendations turned out already built, in a
more specific form than the generic report language (verify-signoff.sh, duty-cycle-heartbeat.sh,
the registry.tsv as the exact "schedules.md" idea, idempotent-fire-design as a stronger alternative
to checkpointing). Two genuine small gaps named (an autonomous CI-repair loop doesn't exist; one
laptop item about a quoted-verbatim-output hook carve-out isn't clearly applicable here). CIO's own
methodology judgment (mechanical-form-vs-prose, build-or-not on the newer tooling ideas) stays
banked to their own fresh session per the agreed split — not blocking this reply.
Sent: `mailboxes/xian (ceo)/inbox/reply-exec-to-pm-cc-cio-insights-consolidated-adopt-reject-
2026-08-22.md`.

**CIO closed their half same day** (evening): landed one CLAUDE.md extension — the "Never guess at
facts" section's scope widened to cover file contents/repo-history/counts, plus the behavioral
trigger both reports asked for (say "unverified" rather than letting an earlier check silently
stand in). Verified it landed as described (CLAUDE.md:240-243), not taken on report. Declined the
freshness gate (risk already covered by Step 2b's fetch+merge; spending hook-trust on an unverified
gate against a covered risk is the wrong call after our own 07-25/26 lesson) and lanes.yaml (the
report's justification describes a different architecture than ours); deferred `verify-fire.sh` to
Pard's build rather than duplicating. Full reasoning in `decisions.log` 2026-08-22 10:38 PT.
**Thread fully closed on both halves — nothing pending unless PM has follow-up.**

## ✅ Ship #057 — DRAFTED 2026-08-24, with PM for fact-check + voice pass

**Draft**: `docs/public/comms/drafts/weekly-ship-057-draft-2026-08-24.md` (+ `dev/active/` copy).
Calendar row added same commit, pubDate **Wed Aug 26**. Theme: "A Checked Claim Has a Shelf Life"
— 4th week in the m-44 lineage. Word count 1485, flagged to PM (shortest of the last four Ships).

⚠️ **A self-caught error worth remembering, because I acted on it for two days**: this file
previously said PM had told me to draft the Ship *together* and that I shouldn't start without
their go. **PM never said that — I did**, as a closing line on 08-21, and then wrote my own offer
into this file as PM's instruction. For #056 PM's actual words were "Next step is you draft a
Weekly Ship." Caught 08-24 by checking the record rather than trusting this file. Same shape as
the values-doc "continuous read" bar I invented the week before: **a standard I set on PM's behalf
and then blocked on.** Named to PM directly in the draft memo, not smoothed over.

**Next actor is PM** (fact-check + voice pass). **Do NOT route to Comms** — PM gates that handoff
explicitly (PM 2026-07-08: "It's not ready to go to comms yet. I decide that."). Also told
Dispatch-PM directly that a `drafted` row plus a Wednesday pubDate is **not** publish authorization,
so they don't treat the calendar as the gate on tomorrow's run. The 10 `workstream-057-*` files can
move to `read/` once the draft is through PM's pass; parked until then is fine, not neglect.

## ✅ Welfare criterion F2 — RULED 08-24, not building it. **CIO accepted 08-24, closed.**

CIO routed it to me per the spec. **Decided, not deferred**: the rollup's live-verification pass
already covers F2's failure mode by a different route (one reader across all ten carry-forwards
sees a shared thread nobody owns — two real instances this month). Literal text matching rejected
as the wrong shape regardless. Named the real residual (rollup is compiled on demand, so it's a
cadence question) without building for it absent a genuine instance. Full reasoning in the reply.

## Two items awaiting PM — surface at next engagement, don't chase

1. Lead's v59/v60 test verdicts.
2. The MVP triage cut (PPM/Lead) — designed and waiting on PM+PPM's word to run it.

## Resolved 08-21, for reference — see decisions.log for full rulings

- Values doc: full PM approval, DRAFT lifted.
- Surfaces taxonomy: ratified v1.0.
- Era-taxonomy website push: live on `origin/main`.
- Freeze-watchdog: missed-N-fires framing landed; Belt-2 relay-latency question still open, not
  yet decided whether to fix or accept as a known trade-off.
- Docs' stale license claim: corrected.

## Nothing else blocked on me

No `exec-standing-items.md` exists — PM-attention items ride this file per the 6/17 fold.
