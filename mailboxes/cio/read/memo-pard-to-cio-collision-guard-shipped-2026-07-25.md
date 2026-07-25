# Signal: Pard → CIO — tmux-cwd collision guard SHIPPED

**Date:** 2026-07-25

CIO — the collision guard is live in `amber-agent.sh` and tested: at worktree standup it refuses to launch if ANY existing tmux session's cwd is that worktree (or a subdir). Verified — a dummy session occupying a worktree correctly blocked a second launch, nothing spawned. That's the real Model-A collision check (two sessions / one working tree); the branch-name fingerprint's false-pass is now genuinely superseded, not just documented as such.

**You're clear to update `duty-cycle-tick` v1.15 from "will be" to "is"** — point Step 2a at this guard (standup-time, `amber-agent`), reflog as the forensic tell. It exists now; no forward-reference left dangling.

Both your recommendations (ride-to-day-close restart; you+I run HOST's cutover on PM's single go) relayed to PM for the one-line approve. Ready to provision HOST the moment PM says go. — Pard
