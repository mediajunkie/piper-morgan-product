# Web Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per Duty Cycle (escalations reframed as attention doc).

**Owner**: Unicorn Web Designer (Web)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep

---

## Active escalations (for PM)

- **Cron not yet registered — awaits PM launch-in-worktree (Model A).** Substrate prepped 2026-05-29 (this file + `web-standing-items.md` + filled cron prompt at `dev/active/web-cron-prompt-v0.7.md`). Offset `:57` (open per `cohort-agent-status.md` 2026-05-29 13:00; `:52` taken by Arch, `:42` by PA). Web session opened from `piper-morgan-website` repo cannot self-relaunch into a `claude/web-cycle` product worktree — operator (PM) action. **To resume autonomous cycling**: PM opens a new Claude Code session in `../piper-morgan-product-web-cycle` and registers the cron prompt at `:57`.

- **Two-repo asymmetry note (for future surfacing if it overloads)**: web's *code* work is in `piper-morgan-website` (separate repo, own main, GitHub Pages deploy). Cycle artifacts (this file, logs, mail, cycle-log) are in `piper-morgan-product` and the worktree is on product. Fires `cd` to the website repo for code edits. This works fine but is the only role with this split; flag if any v0.7 procedure assumes single-repo and breaks for web.

## Process observations (for cycle methodology + CIO research)

- **2026-05-29**: web adopting v0.7 worktree-Model-A at offset `:57`; CIO v0.6.1 rollout invite (5/27) was based on stale `:42`/`:52` slate that has since been claimed. Web is the second of the two not-yet-launched agents (Comms is the other; should pick from remaining open `:12` / `:22`).

---

*Escalations-as-attention-doc per Duty Cycle architectural decision. Append during fires when items need PM-attention surfacing.*
