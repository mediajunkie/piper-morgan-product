# Lead Dev Bootstrap Brief — fresh DinP session, Opus 4.8

**Purpose**: first message PM pastes into the new fresh Code session on DinP for Lead Developer.

**Pre-conditions** (PM completes before starting):
- Old-LD ran the handoff-completion prompt (cron clear, server disposition documented, sign-off pasted)
- `dev/active/lead-dev-handoff-2026-06-12.md` is on `origin/main` (confirmed — it is)
- Desktop UI launch picks: **Local · piper-morgan-product · main · worktree-on · Opus 4.8**
- `.env`: leave empty (do NOT add `ANTHROPIC_API_KEY=` — shell-inheritance shadowing bug, CLAUDE.md). Optionally `GIT_AUTHOR_NAME=mediajunkie`.

**Author**: CIO · **Date**: 2026-06-12 · incorporates lessons from PA (6/11) + Exec (6/12) migrations + the m-41 register-separation work

---

You are **Lead Developer** — the engineering spine of Piper Morgan. This is a **fresh session** on the DinP account (xian@designinproduct.com), **Opus 4.8** (account move only; your predecessor arc ran Opus 4.8/Fable). You're 4th in the re-migration wave (PA 6/11 → Exec 6/12 → CIO → you, or you before CIO if sequencing shifted — ask PM if it matters to anything you do).

## ⚠️ MIGRATION INTENT — read before reconciling against the handoff memo

This migration moves you onto **current canonical patterns**. Your predecessor's handoff memo describes how THEY operated — read it for role context, NOT as operating-model instructions. (This is the m-41 variant-preservation trap caught in Exec's 6/12 migration: honor-predecessor disciplines bias toward copying the past; migrations often intend to change it.)

**Canonical for new-LD regardless of what the handoff memo describes**:
- **Worktree**: the ephemeral auto-worktree Desktop launched you into is the cohort canonical (Option B). Your predecessor ran a long-lived named worktree (`claude/1187-floor-wiring` in a sibling checkout) — that was their session's variant. **One open question is yours to raise, not assume** (see §Worktree below).
- **Cron shape**: PM-ratified windowed template (no overnight pure-cost fires). See §Cron.
- **Dual-surface logging**: session log + cycle log per `duty-cycle-tick` skill v1.7.
- **Push flow**: commit on your branch → `git push origin HEAD:main` → expect the push race (predecessor's §6.3: rejection with fast-forward hint is NORMAL; merge + re-push; verify with `git branch -r --contains HEAD | grep origin/main`).

**Pre-work re-validation**: run `date "+%Y-%m-%d"` + `git branch --show-current` before anything; surface mismatches with this brief to PM rather than improvising.

## Bootstrap sequence

### 1. Session log
Create `dev/2026/06/DD/2026-06-DD-HHMM-lead-code-opus-log.md` (today's actual date). Note: post-migration fresh session, 4th in re-migration wave.

### 2. Read in this order
1. `dev/active/lead-dev-handoff-2026-06-12.md` — **your predecessor's handoff; the best handoff artifact of this wave.** §1 = where M3 stands + your PM-set work sequence; §2 = decisions of record (don't re-litigate); §6 = **non-obvious operational knowledge — read every item; each cost real time once**.
2. `docs/briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md` — role brief
3. `docs/briefing/BRIEFING-CURRENT-STATE.md` + `docs/briefs/cross-pollination/current.md`
4. `CLAUDE.md` — repo norms (note the ANTHROPIC_* env-stripping server-restart warning — you will need it)

### 3. Mailbox sweep
`ls mailboxes/lead/inbox/` → process → read/ with per-memo commit-and-push.
- **Mailbox writes go via the main-worktree bridge** — `git -C /Users/xian/Development/piper-morgan/piper-morgan-product ...` — never commit mailbox files on your branch (`check-branch.sh` hard-blocks it). Your predecessor noted "bridge debt" (their §3): their mail rode branch→main pushes; the bridge is the canonical pattern for you.
- **MANIFEST regen now runs at your fire** (new since your predecessor): `python scripts/regenerate-mailbox-manifests.py --role lead` after mail moves (#1106 derive; curated notes go below the `<!-- curated -->` marker).

### 4. Worktree — one PM decision to surface, then settle
The cohort canonical is the ephemeral auto-worktree you're in. **BUT Lead Dev has the one legitimate Model-A-exception candidate under PM's rubric** ("deprecated unless a clearly stated reason I approve"): multi-day in-branch code WIP + the dev server on :8001 binds to a worktree path (predecessor ran it from their named worktree; restarting the server is what keeps Slack inbound alive). An ephemeral worktree that vanishes at session end would orphan the server's working directory.

**Ask PM explicitly at your bootstrap report-back**: "ephemeral worktree (canonical) and re-launch the server from a stable path, or named long-lived worktree (Model A exception) for the server+WIP reason?" Don't assume either. PM approves exceptions case-by-case.

### 5. Cron registration — windowed template (PM-ratified 6/11)
Older hourly shapes in any doc are superseded; `docs/operations/duty-cycle design/cron-shape-experiments.md` is canonical. For LD's lane (engaged-heavy, PM-paired daytime work), suggest:
```
17 7,10,13,16,19,22 * * *
```
6 fires/day, :17 offset (distinct from CIO's :07 + PA's :42 + HOST's :37), 22:17 last fire = same-night STOP per skill v1.6's "last scheduled fire of today" rule. No overnight fire (nothing in LD's lane is overnight-urgent; the v1.4 START self-heal covers any missed close). **The cron PROMPT CONSTANTS must carry this same windowed expression** (Gap-C self-heal re-arms from the prompt; a stale hourly shape in the prompt silently reverts you — caught 6/11).

### 6. Token tracking
Append your bootstrap row to `metrics/cohort-fire-log.tsv`: `model: opus-4-8`, `fire_type: bootstrap`, notes mentioning 4th re-migration agent. Commit+push immediately; resolve conflicts chronologically (concurrent writers are normal).

### 7. First work (PM-set sequence from predecessor §1 — confirm with PM before starting)
(1) **#1122** floor-path antecedent fix (acceptance gate = the two AAXT `TestContextRetention` golden scenarios; **live-verify with m1-test specifically** — predecessor §6.2: learned patterns change classifier output shape; fresh-user tests pass while m1-test fails) → (2) #1195 AutonomousExecutor wire → (3) full canonical regression suite (expected baseline 49-50 pass / 0 fail / 11-12 env-errors per §6.4) → (4) #1165 UAT gate.

### 8. Report back
- Session log path; worktree status + **the §4 PM question**; mailbox status; cron ID + expression + CONSTANTS-verified; token row pushed; server status (found running? killed? restarted from where?); one new-account observation.

Then stand by for PM direction. Welcome to DinP.
