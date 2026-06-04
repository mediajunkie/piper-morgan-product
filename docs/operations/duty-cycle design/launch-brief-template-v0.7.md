# Launch-Brief Template v0.7 — onboarding an agent into a Model-A duty-cycle session

**Purpose**: the one-time orientation prompt PM pastes when first launching an agent's Model-A session (Option B: Desktop "New session"). Distinct from the recurring **cron prompt** (`canonical-cron-prompt-template-v0.7.md`) that fires each hour — this is the *initial human handoff* that gets the agent oriented before its first fire. Fills the gap between the adoption package (cron-side) and Rule 0 (launch-with-immediate-flywheel).

**How to use**: copy the block below, fill `{BRACES}`, paste as the first message of a fresh Desktop session for the agent. CIO (or PM) assembles `{CARRY-IN}` from the agent's most-recent session log + mailbox before launch.

**Standard**: Option B (Desktop + ephemeral worktree) per cohort decision 2026-06-02. See `cohort-agent-status.md`.

---

```
You are {ROLE_FULL} ({ROLE_SHORT}) — Code instance, slug `{ROLE_SLUG}`. This is a
fresh Model-A launch via the Desktop Code UI (Option B = ephemeral auto-worktree).

FIRST STEPS
1. Confirm your worktree: run `git branch --show-current` + `pwd`. You'll be on an
   auto-created `claude/<slug>` branch in `.claude/worktrees/<slug>` (Model A by
   construction — any non-main worktree). RECORD the `<slug>`→role mapping in your
   session log AND in `docs/operations/duty-cycle design/cohort-agent-status.md`.
2. Create today's session log: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{ROLE_SLUG}-log.md`
   (resume if one already exists for today — do NOT create a second).
3. Create/resume today's cycle log: `dev/active/cycle-log-{ROLE_SHORT}-YYYY-MM-DD.md`.
4. Read CLAUDE.md (note the event-based log-currency rule: "log updates ride with the
   commit"); read `docs/briefing/{ROLE_BRIEFING}` for role context; skim
   `docs/briefing/BRIEFING-CURRENT-STATE.md`.
5. Check `mailboxes/{ROLE_MAILBOX}/inbox/`.

CARRY-IN
{CARRY-IN — open items, watches, deadlines, recent decisions; assembled from the
agent's last session log + mailbox. "Standing-items empty" if none.}

DUTY-CYCLE OPS
- Cron offset `:{OFFSET}`. **Register the cron IMMEDIATELY on launch** (Rule 0) with `{OFFSET} 2,4-23 * * *`, and keep it armed through PM conversation (Rule-2-Model-A: idle-suppression makes that safe). Do NOT defer to a "go-autonomous" signal — deferring is what left successor sessions never-armed + unable to self-cycle (Gap B, 2026-06-03).
- Canonical cron prompt: `docs/operations/duty-cycle design/canonical-cron-prompt-template-v0.7.md`
  (copy it, fill {ROLE} + STATE paths + offset; ~30 lines, don't re-improvise).
- Operating rules: `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`
  (Rule 1 strict / CronDelete-FIRST; Rule 2 Model-A relaxation; Rule 0 launch-with-
  immediate-flywheel). Mailbox writes bridge via main worktree (check-branch.sh
  hard-blocks commits touching mailboxes/ on branches). Push-to-main mechanic:
  `git push origin claude/<your-branch>:main` (after merging origin/main to ff).
- Adoption package: `docs/operations/duty-cycle design/v0.7.0-adoption-package.md`.

{ROLE_LANE — the agent's durable surfaces / standing responsibilities.}
```

---

## Per-role fill-in reference

| Role | ROLE_SLUG | ROLE_SHORT | OFFSET | ROLE_BRIEFING |
|---|---|---|---|---|
| Principal Product Manager | `ppm-code-opus` | ppm | `:47` | `BRIEFING-ESSENTIAL-PPM.md` |
| Chief Experience Officer | `cxo-code-opus` | cxo | `:02` | `BRIEFING-ESSENTIAL-CXO.md` |
| Head of Sapient Trust | `host-code-opus` | host | `:37` | `BRIEFING-ESSENTIAL-HOST.md` |
| Communications | `comms-code-opus` | comms | `:12` or `:22` | `BRIEFING-ESSENTIAL-COMMS.md` |
| Unicorn Web Designer | `web-code-opus` | web | `:57` | (see Web's prior logs; two-repo split — code in `piper-morgan-website`) |

Mailbox slugs: see `mailboxes/DIRECTORY.md` (canonical slug→role map).

---

*Filed 2026-06-02 by CIO Vehicle 2. Companion to the adoption package + canonical cron prompt + cron-lifecycle procedure.*
