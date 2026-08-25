# Exec Carry-Forward

**Last updated**: 2026-08-25 ~09:1x PT — START, quiet fire (one ack drained, nothing owed).
**Session log today**: `dev/2026/08/25/2026-08-25-0902-exec-code-log.md`
**Role**: Chief of Staff (Exec) | Amber, Model A worktree, branch `claude/exec-cycle`
**Cron**: `418ff20f`, `32 8,20 * * *` — confirmed exactly one job at START, no re-arm needed.

⏰ **Ship #057 publishes TOMORROW (Wed Aug 26)** and is still `drafted`, unchanged since I wrote it
08-24 — PM's fact-check + voice pass hasn't happened yet. Verified at the 08-25 START, not assumed.
**Not a chase today**: PM has a full day, and the note asking for the pass went out 08-24 with the
draft. **If it's still untouched at tomorrow morning's fire, that's the moment to surface it once**
— by then it's same-day and the pubDate is real.

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
