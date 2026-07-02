# PA Duty-Cycle Escalations / PM Attention Doc

**Agent**: PA (Piper Alpha)
**Maintained by**: PA during each duty-cycle pass
**Last updated**: 2026-05-28 23:10 (STOP — day closed; cron deleted; **manual re-open needed tomorrow**)

**Duty Cycle role (v0.6 design ratified)**: This file IS the canonical **Attention Doc** (Doc 3 of the three per-agent duty-cycle docs). Items for PM to scan during IDLE accumulate here. Blockers captured during Task Loop step 1.2 land here. When PM engages during IDLE-engaged, this is the doc to walk through together.

---

## How to read this file

PM scans for escalations open against PA. Severity typology:

- **blocking** — PA is stopped until PM acts; cycle cannot proceed on this thread
- **drift** — cycle has noticed a trend that may degrade trust property if not addressed
- **uncertainty** — PA needs PM judgment on a call; cycle is proceeding on alternatives in the meantime
- **complete-stale** — work is done; PM input was waiting; PM input not yet given

PA scans for escalations the cohort filed against PA via memos; surfaces here as needed.

---

## Active escalations (PA → PM)

- ~~**uncertainty (time-sensitive) — PDR-005 stale "MCPB hybrid" reference (line ~376).**~~ →
  **RESOLVED 6/4: PPM already corrected it** in PDR-005 v0.6 (changelog: "plugin model, PM 6/1 via PA");
  verified. No send needed. (PDR-005 v1.0 is now a clean ratification decision for PM — on the board.)
  *(original flag retained below for trail.)*
- **uncertainty (time-sensitive) — PDR-005 ratification-ready but still carries a stale "MCPB hybrid"
  reference (line ~376).** Surfaced 6/3 22:09 from the Comms/PPM EC-2 thread: the external-language
  frame folded → PDR-005 is now ratification-ready. But PDR-005 still has the *same* wrong packaging
  framing I just corrected in v18 (MCPB vs. plugin-canonical) at line ~376 (Q6 ADR pointer, "canonical
  context-package format … MCPB hybrid"). **Recommendation**: before you ratify PDR-005, let me send PPM
  the same surgical correction I sent for v18 (plugin is canonical; MCP server is a component inside the
  plugin) — PPM already flagged this line as a candidate for the fix. I'm **not** sending it
  autonomously (PDR-005 ratification is your gate, like v18 — "please do" before I send). Just flagging
  so it doesn't bake in. Carry item A in standing-items.

- ~~**complete-stale — Skunkworks Desktop test reminder**~~ → **RESOLVED**: test ran (Cowork, 5/30–31);
  findings folded into the writeup; rung-1 of the thin plugin PoC now built (6/3).

- **uncertainty — check-branch.sh blocks Model-A mailbox-on-branch.** The hook hard-blocks `mailboxes/`
  commits on `claude/*-cycle` branches, so the v0.7 template's per-fire-push mail path doesn't work; PA
  routes mail via the main-worktree bridge meanwhile (not blocking — workaround validated). Memo to Lead
  Dev `7670c2f3e` (cc PM/CIO/Arch) requests disposition: amend hook for cycle branches (PA's lean) vs.
  formalize the bridge. **Update (5/28 ~9:10 PM): CIO concurs Option-1 (amend the hook)** — preserves
  never-touch-main; merge-keeper sweep already catches a forgotten push. CIO corrected the canonical
  template per the finding (`a5517ee02`). Now awaiting **Lead Dev's** fix-choice (Lead owns the hook).
  Cycle proceeds on the bridge.

---

## Active cohort threads (PA autonomously processing)

Threads the cycle is moving forward without per-decision PM ratification. PM scans for "what's PA touching that I might want to weigh in on."

- **Discovered-work weekly sweep** — accepted ownership 2026-05-27; first sweep ran 5/27 (0 buried, healthy baseline); next sweep Fri 5/29, Friday-to-Thursday cadence going forward
- **Outcomes lane synthesis follow-through** — findings shipped; CIO synthesizes Day 28-29; PA available for Day-3/4 review feedback
- **Skunkworks PoC carry-forward** — writeup drafted; bringing up at PM bandwidth signal per PM 2026-05-27

---

## Lessons captured for PA discipline (recent feedback memories)

Recent memories pinned 2026-05-27:

- `feedback_no_postponing_unblocked_work.md` — Always do unblocked work now; batch only genuinely-stuck Qs. Default verb is "do," not "schedule."

Earlier this week:

- `feedback_no_fake_preloading.md` (2026-05-24) — "Pre-loading" across sessions is a fake transfer mechanism
- `feedback_read_folder_discipline.md` (sharpened 2026-05-24) — Move to read/ only when downstream artifact exists or none required
- `feedback_lessons_not_criticism.md` (2026-05-21) — PM "good lesson" framing is literal growth-coaching
- `feedback_verify_filter_scope.md` (2026-05-23) — Verify counts against authoritative source

---

## What PM might want to weigh in on (low-priority surface)

*(none currently)*
