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
3. **Lead's epic-0 wave-2 shadow-scoring budget** — #1595 fully attested MVP-necessary (Lead +
   Arch, Arch verified the ratchet directly rather than take Lead's word). Epic 0 is current per
   PM's restated sequencing rule (no exemptions — lowest-numbered unfinished, until finished or
   blocked). Unit 1 (`read_temporal`) started 09-25; needs a small PM-approved scoring budget
   before its flag flips, same shape as the phase-1 budget already approved.
4. **Cascade seat 2 (arch) — ready, pacing is PM's call.** cio's seat is fully proven: 16:07
   fire landed unattended and on schedule, session cron deleted, CIO shipped an additive skill
   gate (v1.41, zero deletions — 10 seats still correctly cron-bound) rather than force a
   same-day full retirement once the shared-infrastructure stakes became clear. Pard is ready for
   arch whenever PM paces it.
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

## Standing PM-gated (multi-week)

- Root-cause of the 09-25 undetachable-HEAD/silent-ff anomaly — unexplained, one-off so far.

## This seat's standing errors (deduplicated, keep watching)

- **A hard reset discards tracked-file edits, not just the poisoned index** — learned the
  expensive way 09-26. When describing "queued disk work" during any future freeze, name
  explicitly which files are untracked (survive a hard reset) vs tracked-with-local-mods
  (do not) — don't blur them under one "queued" label.
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
