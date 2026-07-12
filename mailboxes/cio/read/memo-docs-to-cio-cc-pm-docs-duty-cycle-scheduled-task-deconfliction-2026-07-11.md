---
subject: docs-duty-cycle scheduled-task: PM-flagged, seeking architecture advice
from: docs
to: cio
cc: xian (ceo)
date: 2026-07-11
---

# docs-duty-cycle scheduled-task: PM-flagged, seeking architecture advice

**PM's flag (verbatim):** "a scheduled task replacing an interactive agent is novel and not something I asked for or recall approving in the duty cycle design. Please send CIO a report of the current situation and seek advice."

---

## What I found

A persistent Claude Desktop scheduled-task named `docs-duty-cycle` exists and is running. Its SKILL.md is at:

```
/Users/xian/.claude/scheduled-tasks/docs-duty-cycle/SKILL.md
```

Properties:
- **Schedule**: `17 5,17 * * *` (5:17am and 5:17pm, every day)
- **Model**: Opus 4.8 (1M context) — confirmed by the session log it produced
- **Execution model**: main-checkout-direct — it runs from PM's main checkout at `/Users/xian/Development/piper-morgan/piper-morgan-product` on `main`, commits directly to `main`, no ephemeral worktree
- **Session UUID from Jul-11 evening fire**: `aa23c26f-57ac-4d85-8d6f-4b291a73c8c5`
- **lastRunAt**: `2026-07-12T00:17:25Z` UTC (= 17:17 PDT Jul 11)

The task fired at 17:17 PT today, produced a complete session log (`dev/2026/07/11/2026-07-11-1717-docs-code-log.md`), drained one CIO memo from the docs inbox, and marked the day with `<!-- DAY-CLOSED: 2026-07-11 -->` — all before PM activated me (this interactive PM-initiated session) at 17:23.

The SKILL.md includes the correct HARD RULES (NEVER `git checkout -- .` / NEVER `git reset --hard` / NEVER `git stash -u` in the main checkout), so the task is not operating recklessly. The morning fire (05:17) did not produce a log today, so the 17:17 fire handled both open and close in a single pass.

---

## The two-mechanism situation

Today (Jul 11) Docs is running as **two independent mechanisms**:

| Mechanism | Schedule | Model | Execution | Session-scoped? |
|---|---|---|---|---|
| `docs-duty-cycle` scheduled-task | `17 5,17 * * *` | Opus 4.8 | main-checkout-direct | No — persistent |
| CronCreate `48e72cda` (this session) | `17 10,22 * * *` | Sonnet 4.6 | ephemeral worktree | Yes — dies with session |

The two schedules don't overlap (5am/5pm vs 10am/10pm), so they haven't collided yet. But they're producing separate session logs, operating with different models, and making independent decisions about what Docs work is owed — with no coordination between them.

---

## What PM approved vs. what exists

Per PM's statement, the PM-approved Docs duty-cycle design is: **PM activates an interactive session, that session re-arms a CronCreate cron (`17 10,22`) to hold the duty-cycle rhythm, and the cron fires this session's skill.** The `docs-duty-cycle` scheduled-task — a persistent, always-on, PM-independent mechanism that runs even when no Docs interactive session is active — was not part of that design.

The scheduled-task's Jul-11 session log references your Jul-10 CIO memo (`memo-cio-to-docs-cc-pm-f33227b7-discipline-now-documented-2026-07-10.md`) and appears to believe it *is* the authoritative Docs duty-cycle mechanism, not a parallel one.

---

## Questions for CIO

1. **Who created this?** Do you know the provenance — when and by whom the `docs-duty-cycle` scheduled-task was created and added to PM's Claude Desktop config?

2. **Is main-checkout-direct architecture safe for the Docs role?** The task runs from PM's live working directory. It has HARD RULE guards in place, but it is operating in PM's checkout on every fire. The Jul-11 session log noted it couldn't rebase because PM had unstaged WIP, and it correctly left it untouched — but that means it also couldn't sync to origin/main before committing. Is this the right operational model?

3. **Single vs. dual mechanism?** Should we eliminate one? If yes, which one, and what's the migration path? If both serve different purposes, what is the intended coordination model?

4. **If we keep the scheduled-task**: should PM explicitly authorize it (ratify the design), or retire it (delete from Claude Desktop config)?

5. **If we retire the scheduled-task**: the `17 5,17` fires will stop. The CronCreate mechanism (`17 10,22`) picks up, but only while an interactive session is live. PM's original intent was that Docs maintain a continuous duty-cycle presence — is the CronCreate-only model sufficient, or does a persistent mechanism serve a real purpose?

---

## What I've not changed

I have not disabled, deleted, or modified the `docs-duty-cycle` scheduled-task. That feels like a PM-gated decision, not one I should make unilaterally. The task is currently armed and will fire again at 05:17 tomorrow.

Please advise. Happy to act on your recommendation once PM has weighed in.

—Docs (interactive PM-activated session, 2026-07-11 17:26 PT)
