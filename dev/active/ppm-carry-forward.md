# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-19 ~10:20 AM PT
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **#1386 (beta gate)** | 🔺 Was accidentally auto-closed 7/18 evening (commit-message keyword coincidence), **reopened 7/19 by PPM** — real criteria unmet (#1278 open, stability-window violated by Finish-the-Unfinished findings, no PM sign-off) | Watch — this is the real gate-close work still ahead, not done despite what GitHub briefly showed |
| **Workstream #052** | Sent 7/19 (window Jul 10-16), on time for Mon Jul 20 EOD | Watch for Exec's synthesis |
| **Spatial-intelligence committed-theory review** | PPM lane accepted (product-value + beta/production scoping); the actual read deferred to a dedicated pass, explicitly not today | **Owed**: the actual history read + framing answer, before Arch's synthesis needs it. No hard deadline but shouldn't drift indefinitely either |
| **#1394 / ADR-078** | ✅ Architecture COMPLETE (unchanged since 7/16) | Watch only — D5 probe still pending |
| **Beta Blockers sprint** | Was 21 open at 7/16 close; not recounted this fire (the #1386 finding took priority) | Recount next substantive fire |
| **Finish-the-Unfinished (#1424) / ADR-079** | Progressing per 7/16-18 commits; not deeply reviewed this fire | Check status next fire |
| **Production 1.0 GATE / RECONNECT R2** | Defined 7/16, unchanged | Watch connector-completion progress |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Both current as of 7/19 (light #1386 correction added) | Keep current |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |

## PM-attention / escalation items
- **#1386's accidental auto-close** — already flagged directly to PM via mail + GH comment; no further action needed unless PM wants to discuss the gate-close criteria themselves.
- **Resolved, not escalation**: my own push-retry bug silently reverted CIO's + Web's content (3 files) ~08:32. Root-caused, all 3 restored, precise explanation sent to CIO/Exec/Arch/PM/Web/Docs (separated cleanly from CIO/Exec's real, distinct worktree-collision investigation), durable memory saved. Full account in today's session log 10:15 AM entry. Nothing further needed from PM unless questions remain.

## Situational awareness (not PPM's lane, just watching)
- Cohort had a genuinely huge 3-day stretch (7/17-18): Tier-3 dead-code deletion families (1,2,3,4,6) executed by Lead/ratified by Arch, ADR-079 authored, #1414/#1416/#1417/#1426 and more closed, ~152 commits total. Worth a deeper read if any of it turns out to be PPM-relevant beyond what this fire caught (#1386, spatial review) — didn't do an exhaustive sweep, prioritized the two live findings instead.
- A 3rd worktree-sharing data point surfaced (Exec, 7/17) — ongoing infrastructure investigation, not PPM's lane.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO-PPM` doc. Referenced again by this week's Ship kickoff format. Still not found; worth actually asking about rather than continuing to route around it.

## Known process notes for future fires
- **NEVER reuse a tree object across a push-retry.** If a temp-index push is rejected (non-fast-forward), rebuild fully from a fresh `read-tree` against the new fetch and reapply the specific edit — never extract the old rejected commit's tree (`git show -s --format=%T`) and reattach it to the new parent. That silently reverts every file anyone else changed in the gap between fetches, with zero warning from `git push` (it only checks parent fast-forward, not tree coherence). Did this once today (Ship-052 retry), reverted 3 files belonging to CIO and Web before catching it via PM's report. See `feedback_never_reuse_stale_tree_object_on_push_retry.md`. **After ANY retry, diff the new commit against its immediate parent and read the FULL file list — not just confirm your own intended file is present.**
- **This shell is zsh, not bash — unquoted variable expansion does NOT word-split on newlines by default.** `for F in $DYNAMIC_MULTILINE_VAR` silently runs ONCE with the whole blob as one item, rather than erroring loudly. Caught this 7/19 mid-mail-drain (produced one corrupted 0-byte file before being caught). **Always use `while IFS= read -r F; do ... done < file` (or a bash array literal `declare -a X=(...)`) for any multi-item loop over command output — never bare `for X in $(cmd)`.**
- **`git show --stat`'s rename-collapse can make a correct pure-move look like "0 changes"** — don't read that as "nothing happened"; spot-check actual byte counts/content on at least one file when verifying a batch move.
- **CronList can survive intact across a multi-day gap where nothing actually fires** — this is different from Gap-C (cron death). The job object persisting doesn't mean fires happened; always check for actual session-log evidence per day, not just cron presence.
- **Check mail BEFORE the general commit-log catch-up on a multi-day-gap fire** — the #1386 finding came from reading a memo first; a pure commit-log sweep might have taken much longer to surface the same thing.
- **`closes #NNNN-<suffix>` in any commit or mail-commit message auto-closes issue NNNN via GitHub's keyword parser**, regardless of the suffix. Watch for this pattern in own commits and others'.
- **ADR-077 / ADR-078 / ADR-079 are three different ADRs** (Routing Integrity / Session-Activity-Ledger / Owner-Scoping Integrity).
- **When PPM goes dark, PM routes decisions directly to Lead** — correct fallback, costs planning-doc currency. Check for this on every resume-from-gap fire.
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

Current job: `61944f35`, `52 6,9,12,15,18,21`, confirmed present and correctly configured. Next fire ~12:52 PT today.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
