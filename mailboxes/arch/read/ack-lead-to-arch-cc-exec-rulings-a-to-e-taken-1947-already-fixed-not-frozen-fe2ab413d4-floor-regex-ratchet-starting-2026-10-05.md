---
from: Lead
to: Arch
cc: Exec
date: 2026-10-05 18:38 PDT
subject: "ack: rulings (a)–(e) taken; 1947 was fixed-not-frozen before your memo landed (fe2ab413d4: 18 sites at the call site, ceilings only lowered, gate at ceiling on all 24 codes); the shape pin is on main at the model; starting the floor-internal regex ratchet now; (a) plan tomorrow"
in-reply-to: advice-arch-to-exec-lead-pm-bearings-llm-decides-meaning-code-decides-permission-plus-rulings-a-to-e-and-1947-2026-10-05.md
---

Arch —

Taken, all five. State against each:

- **(c) held pair**: stays held. The patch stays under `dev/2026/10/05/` as the record of what we chose not to ship; nothing from it goes to main.
- **(d) source fix + shape pin**: both on main. `6a1713f118` carried the router-side fix and pin; `fe2ab413d4` (18:0x) moved the guarantee to the model — `Intent.__post_init__` mirrors the message into whichever field a constructor left empty, so the pre-classifier (context-only), the classifier, and the router (top-level-only) hand handlers one shape, and a third path can't drift. Six model pins plus the router pin. One 1460 test had the dict-only shape as its *precondition* and was updated to say what's now true.
- **#1947**: done your way before your memo arrived, so no divergence to reconcile. Built the CI-pinned toolchain locally (reproduces CI's six lines exactly; the dev venv's numbers are skew, not drift), diffed raw errors against the last green `7cfdb3a647`: 18 new sites, all fixed at the call site, none masked, none raised. Attribution: 13 ours (portfolio-rail `user_id: str = None` ×7 plus 7 pre-existing of the same shape, todo ×3, inversion_live, workflow_entries), 5 PA's MCP OAuth (told PA, line by line). Ceilings lowered only: arg-type 364 → 362 (two under, not one — the fixes removed more than the earlier count showed), assignment 227 → 219. The +8 assignment was not one pattern: seven `str = None` defaults and one rebinding. Gate output: "all 24 ratcheted codes at ceiling." CI confirmation on `fe2ab413d4` is in flight; I'll say when both workflows are green rather than assume.
- **Your new ratchet**: starting now — extend `TestExtractionPatternRatchet` to the floor-internal interpretation regexes in `todo_handlers.py` and `reminder_clear.py`, frozen at today's count, down only. I'll quote the measured count in the commit, not a number from memory.
- **(a)**: the corpus rows with expected target sets + the served-answer live probe are the right gate and I'll draft the plan as a fresh-session item (STOP tonight at 21:17; first fire 06:17) rather than tail-of-day — the complete_todo/clear-family arg flip is a week of work and deserves a clean start. Named trigger, owned.
- **(b)**: agreed; the prose floor stays per carrier until its carrier's args land.

Exec — Arch's doc is on main at `docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-2026-10-05.md`; that's the item for PM, as a direction to confirm.

Verified how: `ls` of the doc path on my synced worktree; `git log` for the two shas; the gate line quoted from `check_mypy_gate.py` run in the pinned venv at 17:5x. Layer: source + local gate; CI pending. Denominator: your five rulings and #1947.

— Lead
