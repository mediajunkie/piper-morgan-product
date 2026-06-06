# CIO thin cron prompt (thin-job-prompt PoC, 2026-06-06)

The replacement for the ~40-line fat DUTY CYCLE TICK prompt. Carries ONLY the irreducible per-agent constants; the durable procedure lives in the `duty-cycle-tick` skill, and the transient carry-forward lives in `cio-carry-forward.md`. This is the string passed to CronCreate.

---

```
DUTY CYCLE TICK (CIO). Autonomous loop fire; no human driving. Run the **duty-cycle-tick** skill and follow it.

CONSTANTS: role=CIO (slug cio) · worktree=/Users/xian/cool/piper-morgan/piper-morgan-product-cio-cycle (claude/cio-cycle, Model A — cwd anchors here; NOT shared main) · cron=`7 2,4-23 * * *` (offset :07; STOP 11pm→silent→WATCH 2am→START 4am→hourly day).

CARRY-FORWARD: read dev/active/cio-carry-forward.md + the cycle-log tail (dev/active/cycle-log-cio-<today>.md) + cio-standing-items.md. Rewrite cio-carry-forward.md at end of any substantive fire.

Hold the discipline; holistic-not-tactical. If the skill is unavailable for any reason, fall back to docs/operations/duty-cycle design/procedures/ (cron-lifecycle / watch / stop / start).
```

---

**Note the fallback line** — the one real PoC risk is whether a cron-injected one-line prompt reliably triggers skill-loading (vs. the old self-contained fat prompt). The fallback to the procedures docs makes a mis-fire safe: if the skill doesn't load, the agent still has the pointer to the full procedure. Watch the first few fires for whether the skill actually loads + is followed.
