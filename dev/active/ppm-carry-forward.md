# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-30 ~17:40 PT (Fire 1, Amber, cron live)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Environment note — CURRENT as of 2026-07-30

**This role is on Amber, Model A**: `~/Development/piper-morgan-worktrees/ppm`, branch
`claude/ppm-cycle`, 0 behind `origin/main`. **Cron is ARMED and firing.**

*(Superseded: the prior note here described a 7/28 session running from the old pre-Amber worktree
`pensive-kepler-02a0f6`. That was accurate then and is not now. Rewritten rather than left to be
inherited — this file has already caused one four-session error by being read as current state.)*

**PPM went dark twice** (7/20-25, 7/27-28) and was resumed by PM both times; a third interruption
(overload error, 7/29-30) was also PM-resumed. In all three the carry-forward + mail were the only
continuity — never a clean STOP. **The environment question the 7/28 session raised is now answered
by fact rather than by ruling: PPM runs on Amber.**

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Ship #053** | ✅ Sent 2026-07-28 (window Jul 17-23), on time despite same-day kickoff | None |
| **Jul 19 log** | ✅ Retroactively closed 2026-07-28 (had no DAY-CLOSED marker, flagged by Exec's kickoff) | None |
| **#1386 gate run** | Unblocked since 7/20 (beta v25 carries both Scenario-B fixes per 7/26 log). **TOP ITEM per the Amber session's own priority call** | Schedule with Lead + CXO directly (~half a day) |
| **Jake Krajewski alpha FTUX** | ✅ **PPM roadmap lens sent 7/30** — 4th of 4, unblocked Exec's synthesis. Bucket-sort by which surface survives PDR-006; #1386 cannot fail for what Jake reported | Await Exec synthesis → **I file the issues same day** |
| **PDR-006 + Q2** | ✅ **PPM review RATIFY sent 7/30** — was the last outstanding (Arch ✅, CXO ✅). Ratification unblocked | Watch for ratification; I owe the implementation epic (PDR says "issue TBD") once it lands |
| **Spatial committed-theory** | ✅ **PPM slice delivered 7/30** — concur (b). L3-beyond-GitHub NOT promised (roadmap classes connectors "indoor plumbing (commodity)"); **L4 IS promised — #1174 OPEN/Production + differentiator 4 of 4, zero implementation** | 3 options to PM; on PM's pick I make the roadmap qualifier + #1174 re-scope |
| **Hooks** | ✅ **SETTLED.** Defect was TOCTOU (PreToolUse fires before the gated command, so a compound `add && commit` is judged against an empty index). Pard installed a real `.git/hooks/pre-commit` in the **common dir** — covers all worktrees by construction. **Do NOT probe** (v1.22 retired the probe apparatus); verify the hook file exists | Closed for PPM |
| **#1394 / ADR-078** | ✅ Architecture COMPLETE (unchanged since 7/16, reconfirmed OPEN-pending-D5-probe by 7/26 session) | Watch only |
| **Beta Blockers sprint recount** | Not possible — `gh` token lacks `read:project` scope (found by 7/26 session). Last real count: 21 open at 7/16 close | Needs `gh auth refresh -s read:project` — PM's call |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Current as of 7/19 only — 9+ days stale now given everything since | Needs a real refresh once the above items settle, not urgent today |
| **Docs-tree audit** | Plan delivered 7/13, still PM-gated as of last check | Watch |

## PM-attention / escalation items
- **Environment question** (see note above) — not blocking, but worth PM's call if a future session hits the same ambiguity.

## Mail status (2026-07-30)
**Inbox ZERO.** 50 memos triaged to `read/` at Fire 1, MANIFESTs regenerated. Deep-read: everything addressed *to* PPM + everything gating owed work. Triaged-not-deep-read: hook/m-44 cross-traffic where PPM is cc'd (now settled in CLAUDE.md).

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found
- ~~A canonical `ROLE-PORTFOLIO-PPM` doc. Flagged by two prior PPM sessions now (7/19, 7/26). Worth actually asking PM rather than a third session routing around it again.~~
  ✅ **RESOLVED 2026-07-29 — IT EXISTS AND ALWAYS DID.** `docs/briefing/ROLE-PORTFOLIO-PPM.md`, 118 lines, **self-authored by PPM**, commit `d9be35bbf`, `last_updated: 2026-06-27`. Sits with eleven sibling portfolios in the default briefing directory. Found by one `find . -iname "*ROLE-PORTFOLIO*"`.
  ⚠️ **Read this as a process finding, not a filing correction.** *Four* PPM sessions recorded it missing (7/19, 7/26, 7/28, and the predecessor's handoff) because each inherited this line instead of re-running the check — and the line gained confidence as it propagated, which reads as diligence and is actually the error compounding. It is the predecessor's own lesson #3 ("records that look authoritative are only as good as the discipline keeping them synced; checking costs less than it feels like") landing on the carry-forward itself.
  **Rule earned**: a "wanted but not found" entry is a **claim with a timestamp**, not a standing fact. It decays exactly like a status claim. Date it and re-check it, or don't inherit it.

## Predecessor handoff (Sections 4 & 6) — now durable
- `dev/active/handoff-ppm-predecessor-2026-07-28.md`. The predecessor's own lessons + load-bearing/commodity read — the content CIO's orientation note correctly flagged as the one thing artifacts couldn't supply.
- ⚠️ It arrived as **session-message text only**. The path the predecessor reported writing it to did not exist, and no copy existed on disk or on `origin/main`. Committed 7/29 from the message text; had that message not been relayed, it was gone. `mail-send.sh` refusing it was correct behavior (mailbox paths only) — the gap is that **there is no equivalent durable-delivery path for non-mailbox handoff artifacts**, and the fallback was "leave it uncommitted in the main checkout," which is exactly where it evaporated.

## Known process notes for future fires
- **NEVER reuse a tree object across a push-retry** — rebuild fully from a fresh `read-tree`. See `feedback_never_reuse_stale_tree_object_on_push_retry.md`.
- **This shell is zsh — unquoted multi-line variables don't word-split in `for X in $VAR`.** Use `while IFS= read -r`.
- **`git show --stat`'s rename-collapse can hide a pure move as "0 changes"** — spot-check byte counts.
- **A dark PPM session leaves no explanation of its own gap** — twice now (7/20-25, 7/27-28), the carry-forward + mail were the only continuity, never a clean STOP. Don't assume a gap means nothing happened elsewhere — 985 commits landed cohort-wide during the first gap alone.
- **Check Ship kickoff memos for exact window boundaries** — Exec's #053 kickoff explicitly warned against folding post-window material in; read the window dates literally.
- **ADR-077 / ADR-078 / ADR-079 are three different ADRs.**
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

**ARMED** — job `85981d52` (rearmed each fire), `52 6,9,12,15,18,21`, six fires/day.
⚠️ **Session-only + auto-expires after 7 days** — it is NOT a durable daemon. If this session ends
the cycle stops silently while the registry row still claims watched coverage. Flagged to PM 7/30.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
