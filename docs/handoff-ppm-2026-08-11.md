# PPM handoff — 2026-08-11 (Amber reboot, macOS 26.6)

**Role**: Principal Product Manager (PPM) · slug `ppm-code`
**Worktree**: `~/Development/piper-morgan-worktrees/ppm` (Model A) · branch `claude/ppm-cycle`
**Cron at stand-down**: `25f1a782` — `52 6,9,12,15,18,21`, six fires/day. **Session-only; it does NOT
survive the reboot.** ⚠️ **On resume, `CronList` will show ZERO — re-arm immediately (Gap-C self-heal)
and note it in the fire entry.** The prompt text to restore is reproduced in §6.

**Written for the case where resume fails for me specifically.** A cold start can pick up from this
file plus `dev/active/ppm-carry-forward.md`.

---

## 1. Where things stand — nothing is in flight

**No work is half-done.** 2026-08-10 closed cleanly at 22:20 with its `DAY-CLOSED` sentinel; six clean
fires, fourth clean day running. **No 08-11 session had started when the notice arrived** — so there is
no open log for today and nothing parked mid-task.

**At last verification (08-10 STOP): working tree clean, 0 unpushed, 0 behind, inbox 0.**

---

## 2. 🔴 Open for PM — the only things actually waiting

1. **Bless the merged first-contact criterion** — `docs/internal/product/first-contact-criterion-merged-2026-08-10.md`. **Three items, not four.** ⛔ **Bless neither §7a as written nor #1536's ACs as written** — both had holes; the merged list is the artifact. All three items now stand on their own (item ③'s architectural block was discharged by Arch on 08-10).
2. **The (a)/(b) fork on #1510** — *does the user DEMONSTRATE the working model (inferred, months) or TELL Piper (declared, an afternoon)?* ⚠️ **Now has at least THREE consumers**: #1510 itself, #1511's standup preference, and the standup invitation's persistence. **Arch established the declared surface is safe to build under either answer**, so the fork blocks only the expensive half.
3. **Surface 1 in the 1.0 five**, and **name-or-strike Surface 3** — Surface 3 has exactly one corpus mention (`PDR-005:84`) and no name, doc, ADR or build lane. A "5 of 7" scope claim with one unidentifiable member.

---

## 3. Lanes and their state

| lane | state |
|---|---|
| **Jake FTUX conversion** | ✅ **COMPLETE.** #1536→MVP+Beta Blockers; #1537–#1540→Production/PUB (PM ruled 08-10). Register: `dev/active/jake-ftux-item-register-2026-08-08.md` — **4 filed → 9 filed, 1 held (row 5, pending Arch on tool-catalog naming), 2 preference-holds, 0 unfiled** |
| **#1511 two standups** | Spec filed on the issue; **Lead shipped the MVP slice 08-10** (name-addressable interview). **Production half** = first-run fallback + preference — ⛔ **must ride #1510's declaration surface, not grow its own store** |
| **Standup invitation design** | CXO's three properties adopted (report first/complete · invitation after and cheap to decline · **declining changes nothing else**). **My addition, sent 08-10 22:30**: the **EMPTY standup** is the exception PM named — *demonstrate-then-ask has nothing to demonstrate*, so honest-failure takes over. **Boundary caution: "empty" = genuinely nothing, NOT thin** |
| **Understanding-layer inversion** | My per-category ratchet input was **amended into Arch's ruling**. Watching only |
| **BYOC task force** | Lane taken: **a listing is honest at #1440's contract, not at a connector count.** ⚠️ **Slack cannot be listed while PM's #1481 hold stands** |
| **#1462 / PDR-006** | Production / PUB sprint (PM). CXO's #1463 retest gate is blocked on `services/mcp/server/` — **unbuilt, not undeployed** |

---

## 4. ⚠️ Standing corrections a cold start must not re-derive

- **The web UI is NOT going away.** The modeled UX is holistic, expressed per surface (phone, Slack, web, other-chat, **CLI all maintained**). *"Which surface survives"* is a **false question** — my sort key on that axis was withdrawn 08-08 after PM corrected it. **This error has been made twice; do not make it a third time.**
- **Milestone sequence**: **MVP → Production → Fast Follow.** *"Not MVP"* NEVER defaults to Fast Follow. **Production = required for PUBLIC beta**, worked in the PUB sprint. *"Out of alpha" = the PUBLIC beta.*
- **Beta moved back a month on 2026-08-08.** ⛔ **Do not carry a beta date in any prompt** — it has been wrong twice. The date is PM's.
- **Counts**: never a total without its parts. Use `scripts/sprint-truth.py` verbatim. ⚠️ **It is milestone-scoped — unmilestoned work is invisible to it by construction.** Report not-started AS not-started.
- **Proxies**: safe when the remainder is **ROUTED**, dangerous when merely **IMPLIED**. Say **"gateable fraction"**, never *"shadow"* — shadow implies substitution.
- **`mail-send.sh` can fail silently** — a transient `fetch origin/main failed` leaves the memo unsent with no other signal. **Read the tail of every send.**
- **Before re-asking PM anything: check GitHub.** Items have twice been answered by **action** rather than by answer.

---

## 5. Files a cold start should open, in order

1. `dev/active/ppm-carry-forward.md` — **the live state; read this first**
2. `dev/2026/08/10/2026-08-10-0722-ppm-code-log.md` — most recent full day
3. `docs/internal/product/first-contact-criterion-merged-2026-08-10.md` — awaiting PM
4. `dev/active/jake-ftux-item-register-2026-08-08.md` — the Jake lane, countable
5. `docs/briefing/ROLE-PORTFOLIO-PPM.md` — the portfolio §2 goals table

---

## 6. Cron prompt to restore on resume

Re-arm `52 6,9,12,15,18,21` with the prompt currently in `25f1a782`. Its load-bearing clauses:
**heartbeat first (clock-checked, not tick-order)** · **no standing owed item, and delete any owed
block the fire it completes** · **stacked ticks = one wake; CronList before diagnosing** · **Step 0
verifies the PRIOR day's sentinel** · **delete-then-create at STOP, CronList-verify exactly one** ·
plus the standing lines in §4 above (dates, milestone sequence, surfaces, counts, audit bias, general
contracts, proxies, mail-send).

---

## 7. Registry note

`dev/active/duty-cycle-registry.tsv` ppm row carries the 08-10 day-close. ⚠️ **If the reboot window
crosses a scheduled fire (06:52 or 09:52), the freeze-watchdog may see a genuine silence.** **That
silence is the reboot, not a stall** — this file is the referent.

---

**Stood down with nothing in flight.** — PPM, 2026-08-11
