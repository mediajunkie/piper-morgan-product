# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-08-01 STOP (~22:40 PT) — day closed, cron re-armed for Sunday
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

## ⚠️ SPRINT STRUCTURE — READ BEFORE ANY MILESTONE/SPRINT REASONING

**M4 and M5 DO NOT EXIST as sprints.** They were **swept 2026-07-04/05 — PPM's own work** — along
with M3-Quality/M3-Health/M3-Security/RECONNECT. Contents went either into the **Beta Blockers**
sprint or to the **Production** milestone.

- **Beta Blockers = the final pre-beta sprint.** The **MVP milestone IS the beta gate**: beta ships
  when every issue on `docs/internal/planning/beta-blockers.md` closes — not on a date.
- **Disposition rule**: anything in MVP that didn't meet the hard-gate bar → **Production**, to be
  addressed *during* beta. So **an issue sitting in Production is the rule working, not a defect.**

🔴 **Two "canonical" docs are STALE on this and will mislead you:**
- `docs/internal/planning/sprint-board-structure.md` — still lists M4/M5 as "next planned MVP sprint"
- `docs/internal/planning/roadmap/roadmap.md:68` — differentiator #4 still reads "(M4 territory)"

✅ **The accurate source is `docs/internal/planning/beta-blockers.md`** (see its lines 12 + 20).

**Cost of not knowing this (2026-07-30)**: I reasoned from the two stale docs and produced three
successive wrong readings of one roadmap line, then recommended moving **#1174 into M4** — a
dissolved sprint. PM caught it. **I had run the sweep myself and it was in no artifact I carried.**
Repointing the stale `(M4 …)`/`(M5 …)` references is owed work — do it as a class, not line-by-line.

## 🔴 FIRST THING SUNDAY (08-02)

**1. #1386 criterion 2 — QUALITY HALF still owed my signature.** Routing half **SIGNED 8/1**
(61/61, every category 100%, per-category regime cleared — [issue comment](https://github.com/mediajunkie/piper-morgan-product/issues/1386#issuecomment-5155623078)).
- ⏳ **Quality half withheld on measurement parity, not on quality.** Tonight's judge tier ran
  7 PASS / 15 MARGINAL of 22 under `claude-sonnet-4-6` + STRICT/PASS-only counting; Run 15 used a
  different judge (harness docstring says Gemini) and a different counting rule (23/25, MARGINAL
  separate). **Non-comparable.**
- **Lead runs the parity check in tomorrow's fresh session** — same judge config as Run 15, or
  Run 15's config documented and a new baseline declared. **Sign the quality half same-fire once a
  parity-checked number exists, whatever it says.**
- ⚠️ **Do not let routing-100% read as criterion 2 closing.** The regime's thresholds are stated in
  **Quality PASS**; routing is necessary, not sufficient. **Criterion 2 is partially satisfied.**

**2. Jake conversion — still on Exec's signal** (PM+CXO decision on synthesis §4). Same-day when it lands.

**3. Awaiting PM — down to ONE from two**: **#1462 milestone** (my read: Production). #1459 was set
to Production 8/1 ✅. Also still open: **`gh auth refresh -s project`** — six days, blocks board
reads for PPM and Sprint/Status writes for Lead.

**4. Watch, not drive**: #1467 (Q22 oscillator, Production, Arch-ratified N=3 stability criterion) ·
PA's Probe A (first arm 5/5 survived; PA says they tested the wrong thing — CXO has the verdict) ·
the keychain ACL issue (reads from non-authorizing binaries hang; Lead's seat is authorized).

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Ship #053** | ✅ Sent 2026-07-28 (window Jul 17-23), on time despite same-day kickoff | None |
| **Jul 19 log** | ✅ Retroactively closed 2026-07-28 (had no DAY-CLOSED marker, flagged by Exec's kickoff) | None |
| **#1386 gate run** | 🔴 **WINDOW LOCKED FRI 07-31** — Lead drives from ~06:17; CXO + PPM verify + sign off **on the issue** by noon. Closes criterion 2 + Scenario-B only, NOT the gate | See the FIRST THING FRIDAY block above |
| **Jake Krajewski alpha FTUX** | ✅ PPM lens sent 7/30 (4 of 4 in). **Exec synthesizes Friday first thing** | On Exec's signal → I file the issues same day, against the A/B/C bucket structure |
| **PDR-006 + Q2** | ✅ **RATIFY sent 7/30 — all three reviews in; PA sent it to PM for ratification**. CXO drafting the PDR-004 amendment (Layer-B decision ratification, my reframe accepted); rubric branch OPEN, PA running Probe A on Claude + GPT | Watch for PM ratification → **then I draft the implementation epic** (PDR still says "issue TBD") |
| **Spatial committed-theory** | ✅ Slice delivered 7/30; Arch + CXO concur **(b)**. L3-beyond-GitHub NOT promised → cold island disposes freely. **L4 substance stands**: #1174 OPEN/Production, zero implementation, and "earned proactivity" is differentiator 4 of 4. ⛔ **My "milestone split" finding was WITHDRAWN** — M4 was swept; #1174 in Production is CORRECT by rule. CXO owns #1174, taking option (i) — which needs **no milestone change at all** | Owed by me: repoint stale `(M4/M5)` refs in roadmap.md + sprint-board-structure.md **as a class** |
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
