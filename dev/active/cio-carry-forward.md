# CIO carry-forward — rewritten 2026-08-08 STOP

**Cron**: `4f1515cc` · `7 10,16,22` LEAN · re-armed 2026-08-08 STOP · **auto-expires ~2026-08-15**.
**Three silent cron deaths**: session exit · 7-day expiry · **context compaction**. `CronList` at every fire *and immediately after any compaction*.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## ⏸ AWAITING PM

1. **Memory-index hybrid packing** — today's blank-line fix bought headroom **6 → 18** and that is the *entire* "for now." **PM's chosen option ① does not relieve the binding limit** (lines, not bytes). The measured structural fix: pack the **127 of 175 self-describing slugs** at 4/line, keep the **48 terse ones described** → **182 → 87 lines, headroom 113**. **Lead has offered to build the generator change on PM's ruling.** Trades recall for capacity on the shared pool, so it is PM's call.
2. **Innovation agenda §6** — building mechanisms vs protecting a property. **Today added the strongest instance yet**: our own `CLAUDE.md` endorsed the command that destroyed work, and what caught it was Arch self-reporting a casualty *their own remediation* caused.
3. **Short-period cron experiment** — the only way to decompose the ~30-min dispatch latency (jitter term saturates at 15 min on all eleven seats). ~3 extra fires on my seat.

## Owed / in flight

- **Freeze detector still has no caller.** `cohort-freeze-detect.sh` verified 3 ways; HOST closed the *waking* half (skill Step 1b). **The *during* half needs Pard to land the 4-line patch** to `freeze-watchdog-amber.sh` — sent 08-08 with a tested diff, **not yet landed** (checked at STOP: 0 references). Only a real crontab can watch a frozen cohort.
- **Recurring-instrument self-firing (PM 08-07)** — Role Health has a working workflow (I fixed its 14-min boundary bug); **Agent 360 + skill-candidates have NO workflow.** Copy the now-correct pattern; **verify by step-level conclusions, not the green tick.**
- **`cio-standing-items.md`** carries: memory-index option ① (generator change), Exec's mail-protocol fixes (**check duplication against my 08-07 Step-3 restoration first**), and **PM's chess-board idea** — *"agents have a move log and no position."* Still the most interesting item on the board; **needs a real design pass, not a tail-of-fire one.**

## Watch

- **`docs` inbox 149+** — the cohort's one real mail backlog, four days growing.
- **Merge-drop**: rule shipped, **no tooling built on purpose** (one incident, one seat). **If a second seat trips it after the rule is in place, that earns a guard.**
- **Heartbeat emitters** swing 3→9 across a day; both readings are correct (`--if-quiet` suppresses when a commit exists). Not a signal by itself.

## Standing corrections to myself

- **m-47 applies to claims about MY OWN work too** — Lead attributed a merge-drop guard proposal to me that I never made. Checked my log and sent mail before accepting it.
- **A correction that stops at the mailbox has not happened.**
