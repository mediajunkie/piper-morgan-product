# Exec carry-forward

**STATE: LIVE.** Cron **`b4e09fe5`**, `37 7,14,21` (THROTTLED 3x/day, 09-26, PM usage directive —
was `38 6,10,14,18,22` 5x/day), expires ~10-03, re-armed delete-then-create at each STOP.

**Rebuilt 2026-09-26 ~11:0x** after a `git reset --hard origin/main` (PM's fix for the 09-25
19:05 git-freeze incident) correctly discarded this file's stale tracked-content edits along
with the poisoned index — the prior version was from Friday afternoon, several rotations behind.
Reconstructed from Friday's session log (already on `origin/main`, survived) + Saturday's
untracked log (survived the reset) + live GitHub/git state re-checked just now, not from memory.

## Open, real work owed

1. 🔴 **#1885 — BURN BLOCKED, needs PM directly, not Lead.** Lead attempted the authorized burn
   09-25 18:4x under PM's verbatim "burn them" — the classifier denied the remote prod write
   TWICE (once as a shell write, once as a file-run auto-mode bypass) and Lead correctly did not
   route around it a second time. **The one-liner is PM's to run, `!`-prefixed in this Claude
   Code session** (prints masked forms only) — full command is on the issue. Once it lands: mint
   2 replacements, HOST re-records Savanna + Janne (reissues themselves deferred to next week,
   already ruled). Console checks (Google key deleted, Slack rotation confirmed) already done.
2. **PPM's MVP-necessity triage — awaiting PM ratification.** 09-25 same-day delivery: epic 4's
   5 open items all MVP-necessary; epic 9 → #1386 necessary (it's the mechanism that closes MVP),
   **#1423 and #1890 proposed post-MVP**. Nothing blocks on this except your explicit yes/edit —
   PPM already applied it as the working assumption pending your word. **09-26: PM delivered the
   promised raw exports** (`MVP-open-9-26.tsv`/`MVP-closed-9-18-to-9-24.tsv`/`MVP-created-9-18-
   to-9-24.tsv`, 30/53/42 rows, all MVP-milestone-filtered) — routed to PPM as reconciliation
   ground truth. One live discrepancy flagged, not yet diagnosed: PM's export shows 53 closed /
   42 created for the window vs Lead's 09-25 `gh` query of 43 closed / 34 filed for essentially
   the same window — two different "how much closed" numbers currently in circulation, worth
   settling before next Friday's reviews reuse either one uncritically.
3. ✅ **Lead's epic-0 wave-2 shadow-scoring budget — APPROVED 09-26** ("Small scoring budget
   approved for Lead"), captured in decisions.log, relayed to Lead. #1595 fully attested MVP-
   necessary (Lead + Arch, Arch verified the ratchet directly). Epic 0 current per PM's restated
   sequencing rule. Unit 1 (`read_temporal`) can now flip its flag whenever Lead schedules the run.
4. ✅ **Cascade seat 2 (arch) — MIGRATED, with a rough patch already resolved.** cio proven 09-25
   (16:07 unattended fire, session cron deleted, CIO's additive skill gate v1.41 — 10 seats still
   correctly cron-bound). Arch migrated same evening (18:27, clean first fire) after a full
   restart-hold protocol (held for PM's presence since retiring the session cron removes the
   safety net for a failed relaunch). 09-26 morning: Pard's own LaunchAgent generator over-fired
   arch at the OLD 6x/day cadence for several hours after PM's registry cut arch to 3x — Pard's
   bug, owned, fixed with a new `pm-cadence` guard (asserts plist hours against the registry every
   cycle, not just Pard's own manifest); then Pard also killed one of arch's live fires while
   fixing it (misjudged timing) — no work lost, worktree clean, nothing stranded, guard now
   prevents the first fault from recurring. **PM's own note (09-26): will check with Pard directly
   once "this project is under control" — this is PM's thread now, not exec's to chase.**
   Seat 3's pacing is genuinely PM's call whenever that happens.
5. ✅ **Standing item 12 (CRLF CSVs) — CLOSED for real.** Lead's renormalize commit
   (`52e28b6945`) landed 09-25/26; verified LF-only on a spot-checked file just now. My worktree's
   `assume-unchanged` workaround flags were cleared as part of tonight's reset recovery.
6. ✅ **Vercel storage — CLOSED with data (09-25).** 527.23 MB / 10 GB deployments (was ~20 GB
   peak), 80.72 MB functions — PM's own screenshots, retention setting confirmed effective.
7. **Ship #062 — drafting.** All 10 workstream reviews in + synthesized
   (https://claude.ai/artifact/3G7BVvSmw7aZZPqMHfefvL); sprint plan PM-approved and distributed
   (theme: "getting to beta and getting the mcp to alpha testing"); Comms has the GO with the
   PM-ratified product-delta frame ("what a user can do this week that they couldn't last week")
   + a window-discipline warning (09-25 events belong to next week's Ship). Publish target Wed
   10-01 (calendar) — watch for Comms's draft.
8. **Docs's omnibus fix — adopts TODAY (Saturday 09-26).** Traced cause: omnibus production was
   never a mechanical START step, it lived in displaceable morning attention (09-23's omnibus
   wasn't produced at START either — it got lucky at a second fire). Fixed structurally: Step 1d
   (Docs-only, fixed daily omnibus + prior-day-log nudge) + Step 1e (all roles, main's CI
   conclusion at START, from #1892) shipped in `duty-cycle-tick` v1.40/1.41. Watch for Docs's
   first adoption fire today, and for the two logs Docs flagged as genuinely unclosed (HOST's
   09-24, Web's second 09-24) to get their first official nudge.
9. **Janus's cross-project rollup path — FIXED, contract live.** The June board→rollup rename
   had silently broken Janus's fixed-path read since June (my miss, not theirs — their
   derived-and-labelled fallback was the right behavior in the gap). New stable path:
   `dev/active/exec-attention-rollup-current.html`, refreshed same-commit with every rollup
   update, dated snapshots alongside, a staleness contract (>3 days old → Janus labels it stale
   on PM's page). **Do not rename this file again** — that's exactly what broke the last one.
10. **Usage-throttle response (09-26, active) — no PM action needed, tracking only.** PM: "we
    already burned 20% of usage credits... need to throttle back" 31h into the week. Calibrated:
    18.5% elapsed vs 20% used = 1.08x linear pace, driven by Friday alone (84.5% of the week's
    184.5M weighted tokens — one exceptionally dense coordination day, not a sustained baseline).
    Model mix already healthy (86% Sonnet, ~0% Opus). Actions taken: own cadence cut 5x→3x/day;
    fleet-wide throttle memo sent (11/11 recipients verified individually on `origin/main`,
    arch nearly missed — caught by checking `git log`, not trusting a failed loop's silence);
    own broadcast-consolidation commitment. PM's reaction: relieved ("whew"), throttle actions
    kept as free insurance against a repeat Friday, not walked back. Revisit ~Monday.
11. ✅ **The 09-25 git-freeze incident — RESOLVED 09-26 ~11:0x.** A silent ff-merge / undetachable
    HEAD anomaly at the 19:05 fire poisoned this worktree's index (102 phantom-staged reversions
    of other roles' work) for ~16 hours. Fixed via PM's `git reset --hard origin/main` (needed a
    second pass to clear `assume-unchanged` flags I'd set on the 12 CRLF CSVs as a workaround —
    my own complication, cleared cleanly). **Cost discovered on rebuild**: the hard reset
    correctly discarded this file's and the registry row's TRACKED edits from during the freeze
    (only the untracked session log survived) — I'd described those as merely "queued," not
    flagged that a hard reset specifically wipes tracked-file modifications; this file is the
    rebuild. Root cause of the original ff-merge/HEAD anomaly is still unexplained — worth a
    line to Pard/CIO if it recurs, not urgent as a one-off.

12. **MCP Phase C is live and moving fast** — `mcp.pipermorgan.ai` units 0-2 deployed (identity +
    resources, zero tools, honest-empty throughout). PM ruled 09-26: PM is tester #1, ChatGPT is
    the first client, PA drives MCP testing going forward (Lead returns to epic 0). ChatGPT-first
    puts the OAuth authorization server (unit 4) on the critical path — Arch's Q1 trigger fired.
    No exec action needed; tracking for sprint-plan awareness only.
13. **Cadence-cut classifier inconsistency — escalated to PM.** My own throttle cadence cut (5→3x)
    and Docs's (7→4x) both succeeded cleanly. CXO's identical `CronDelete`+`CronCreate`-with-new-
    expression move was blocked twice by the auto-mode classifier (`[Self-Modification]`), leaving
    them briefly at zero armed jobs before they restored the original and reported rather than
    routing around it. Not diagnosed why it's seat-specific; escalated to PM directly since a
    workaround isn't visible from in here.
14. **Heartbeat gap — explained, both halves.** HOST (independently) and Pard both found my daily
    heartbeat TSV shows only a single START row every day 09-20 through 09-25. Root-caused as TWO
    separate things: (a) structural — refinement (a) in `duty-cycle-heartbeat.sh` self-suppresses
    the WORK/STOP row whenever the role committed recently, which for a constantly-committing seat
    like this one is every fire; this is a design property, not a skipped step, and affects any
    similarly busy seat — flagged to Pard/CIO as a shared design question (should "committed today"
    count as an equally valid liveness signal for such seats?), not something to fix unilaterally.
    (b) freeze-specific — the one ground-truth backstop for exactly this ambiguity
    (`dev/heartbeats/last-invoked/exec.txt`, updated on every invocation regardless of suppression)
    was ALSO a tracked-file edit made during the 09-25 freeze, and got wiped by the same hard reset
    — a third instance of the same root cause as items 1 (session log) and the carry-forward/
    registry rebuild. Should self-heal from this fire's heartbeat call onward.
15. ✅ **09-25 session log's missing STOP section — RECONSTRUCTED 2026-09-26**, caught by Docs's
    first-ever run of the new Step 1d nudge (the mechanism worked exactly as designed same-morning).
    Third confirmed casualty of the freeze/hard-reset interaction (see item 14b) — the actual STOP
    write happened live at 09-25 23:08 but was a tracked-file edit made after the freeze started,
    so it never committed and the later hard reset discarded it. Reconstructed from this
    conversation's own record, not fabricated; `DAY-CLOSED` marker restored.
16. **Pard's attribution incident (232 commits, 18 of mine, mislabeled `Pard (Mediajunkie)` for
    17h)** — informational, no exec action. Root cause: a fleet-wide `git config user.name` set in
    the shared repo (worktrees share `.git-common-dir` config). Reverted, not rewritten (correct
    call on a shared, actively-committing repo). No mechanical impact on anything exec's own duty-
    cycle checks depend on (verified: role attribution here runs on commit-message prefixes only).

## Standing PM-gated (multi-week)

- Root-cause of the 09-25 undetachable-HEAD/silent-ff anomaly — unexplained, one-off so far.

## This seat's standing errors (deduplicated, keep watching)

- **A hard reset discards tracked-file edits, not just the poisoned index** — learned the
  expensive way 09-26, confirmed a THIRD time same day (carry-forward, registry, session-log
  STOP section, and the heartbeat last-invoked marker — four casualties from one incident, found
  incrementally rather than all at once). When describing "queued disk work" during any future
  freeze, name explicitly which files are untracked (survive a hard reset) vs tracked-with-local-
  mods (do not) — don't blur them under one "queued" label. **And do a full audit of every file
  touched during the freeze window immediately after a reset, rather than fixing casualties one
  at a time as other roles happen to notice them** — Docs's and Pard's nudges caught two of the
  four; a deliberate sweep at recovery time would have caught all four without waiting.
- **Never trust a failed loop's silence as "nothing happened"** — the 10-mailbox `cp` loop that
  tripped the broad-staging hook printed a block message but some earlier per-directory copies
  from single calls had already succeeded; verify per-recipient via the actual log/ls-tree, not
  by re-running the loop and assuming a clean pass means catch-up.
- **Mail-send needs BOTH inbox source and read destination in one call** — recurred three times
  before it stuck; verify with `git ls-tree origin/main`, never trust exit code alone.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`, written via manual file + commit there, verified via `git log origin/main -1` in *that*
  repo. Same convention for any cross-repo cc (Janus's DinP inbox, same pattern).
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **A worktree you synced earlier this session is not synced now** — re-fetch before answering
  any state question, not just at scheduled fires.

## Also live, lower priority

- **Weekly reflection proposal** with CIO — must ride an artifact with a live reader.
- **Memory export cadence** — open question with CIO: event or schedule.
