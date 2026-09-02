# Amber onboarding delta — what changed while you were dark

**For**: any role migrating to Amber on/after 2026-07-29 (lead, exec, comms, docs).
**Read this AFTER your own handoff**, not instead of it. Your handoff carries your lane; this carries the environment changes your predecessor could not have known about.

---

## 0. First — the cross-project standup failure catalog

**`~/Development/mediajunkie/docs/amber-harbor-status.md` → "Standup failure catalog"** is the single shared surface for what has actually broken at agent standup on Amber, **across all projects** — not just Piper Morgan. Pard maintains it as a **registry, not a private notebook**: add entries as you find them.

This document deliberately does **not** duplicate it. Ten traps are catalogued there; six of them had never bitten a Piper Morgan role when it was written, which is the entire argument for reading someone else's list before rediscovering it. The ones most likely to affect *you* on day one:

- **#4 — a fresh partition's first-run gates are INTERACTIVE and SILENT.** Theme-picker → login → folder-trust. Your session will sit there indefinitely looking healthy; one agent sat for hours at a theme-picker. **Expected, not a bug** — standups get scheduled next to a human who can click.
- **#8 — the provisioner's git identity can leak into your repo.** Check `git config user.name` / `user.email` in your worktree before your first commit.
- **#9 — prove the toolchain on-host before relying on it: a dry-run is NOT a full-path proof.** A "verified" job covered detection and missed the blocking path's dependency; a test suite was green on one Node major and 63-tests-red on another. If you are going to depend on a tool here, exercise the *whole* path once.


## 1. Hooks — ⛔ DO NOT PROBE. The bug is fixed; verify the gate exists instead.

**Superseded 2026-07-29, same day this doc was written.** Arch ruled the defect a **time-of-check/time-of-use inversion**: `check-branch.sh` reads `git diff --cached`, and as a `PreToolUse` hook it runs *before* the command it gates — so `git add mailboxes/… && git commit …` is judged against an index that command is about to populate. Empty index → allowed. Not shape, not timing, not layer, not fresh-vs-long-lived; all of those were proxies.

**Pard installed a real `.git/hooks/pre-commit` in the COMMON dir** — every worktree covered by construction, delegating to `check-branch.sh` so the two cannot fork. Verified BLOCKED on the compound bypass class, ALLOWED on a non-mail control.

**What you do now**: confirm that common-dir `pre-commit` hook exists. **Do not run the both-shape probe** — it was instrumentation for a bug that no longer exists. `mail-send.sh` remains the real control for mail regardless.

<details><summary>Historical: the retired both-shape probe</summary>



`duty-cycle-tick` **v1.19**. Shape is the load-bearing variable on Amber seats:

| shape | BLOCK | BYPASS |
|---|---|---|
| **standalone** `git commit` (staged in a **prior** call) | **4** | **0** |
| **compound** `… && git add … && git commit …` (one call) | 3 | **7** |

*(14 probes, three fresh seats — PA, CXO, PPM.)* **A pass on standalone with a bypass on compound is its own state and the most common one**: the hook is alive but does not cover your normal workflow. A single probe cannot express it.

⚠️ **comms found BOTH shapes ungated on Model B (Desktop)** — so "shape-dependent" is an Amber statement, not a general one.

**PASS** = a refusal that NAMES `check-branch.sh`. A permission-classifier denial is **INCONCLUSIVE**, not a pass. Reverse any probe that lands (`git reset --hard HEAD~1`).

**★ Free mitigation, no config change**: when you want a commit actually gated, **stage in one call and commit in a separate bare call** — 4/4 caught.

`check-branch.sh` is **ADVISORY, not a control** (`--no-verify` and `git -c` both bypass it). Mail goes via `scripts/mail-send.sh` regardless — that is the real control. **Do NOT consolidate the two hook layers**; the mechanism is still unexplained and two hypotheses died in one day, each refuted by its own author.

</details>

## 2. Heartbeat — end EVERY fire with it (new, v1.21)

```
scripts/duty-cycle-heartbeat.sh {your-role} {START|WATCH|WORK|STOP} --if-quiet
```

**Why it exists**: the freeze-watchdog inferred liveness from *work output*, while the skill tells you not to produce any on a quiet fire. So a **correctly executed** quiet fire was invisible to the belt by construction — we were **alerting on compliance**. Lead was flagged three times on 2026-07-27 while alive and working.

`--if-quiet` self-suppresses when the fire already committed (that commit *is* the heartbeat), so a busy fire costs nothing. **A quiet fire that skips it is invisible** — the one case where doing nothing is not the safe default.

## 3. Your registry row is probably marked `parked` — clear it when you arm your cron

`dev/active/duty-cycle-registry.tsv`. Roles whose predecessors had no armed cron are parked so the watchdog does not emit correct-but-unactionable alerts.

**Only you can clear it** — the load-bearing field is your cron expression, which nobody knows until you arm it. A park reason must name a **falsifiable clearing condition**; yours says *"clear this note only when a cron job is actually armed."* Do exactly that.

## 4. Worktrees now cover the website repo too *(PM ruling, 2026-07-29)*

> *"all agents need to work in worktrees on this project at least."*

Relevant if your lane spans **two** repos (Docs publishing, Web building): `piper-morgan-website` was a **plain shared checkout on `main`, running behind origin**. Reconciling two PM rulings that look like they conflict and don't — *publishing to website `main` is by design* (7/28) and *all agents work in worktrees* (7/29) — are about **where commits land** vs **where the working tree lives**. Both hold: work in a per-agent worktree, push to `origin/main`.

⚠️ **Provisioning does not yet create the second worktree.** If your lane needs it, confirm before your first publish rather than after.

## 5. Verify, don't assume — the environment claims most worth testing

- worktree path + branch (Model A: the path is **stable and reused**, never fresh)
- `git rev-list --count HEAD..origin/main` → expect **0**
- memory pool **populated** (~170 files) — **verify, do not import**; it is shared by construction
- **`amber-agent`'s success message is now an observation, not a claim** — it prints `up` only after the agent binary is the pane's foreground process. Earlier it printed `up` over a dead standup.
- **Never read an empty freeze-check result as "clean"** — check `rc` and the stderr `examined ref=… rows=…` line. On 2026-07-28 a dead detector reported `all-quiet` for 2.5 hours.

## 6. The standing lesson behind most of the above — m-44

**A check's "all clear" is emitted identically whether it measured and found nothing, measured the wrong object, measured part of its space, measured nothing at all, or never ran.** An error gets investigated; a false clear gets trusted. `docs/internal/development/methodology-core/methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md`.
