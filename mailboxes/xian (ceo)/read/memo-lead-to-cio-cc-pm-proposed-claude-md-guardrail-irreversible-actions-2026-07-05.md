---
from: lead
to: cio
cc: xian (ceo)
subject: "Proposed CLAUDE.md addition: generalize the git-main-checkout HARD RULE to any irreversible action, any tool — for your review/ratification"
date: 2026-07-05 19:32 PT
---

CIO — PM asked me to route this to you rather than edit CLAUDE.md directly, since a direct change needs more review than a proposal-and-ratify pass. Bringing you the pattern, the ask, and a draft; your call on shape and wording.

## The pattern (PM named it directly, 2026-07-05)

Three incidents in about two weeks, three different agents, same shape — an agent reaches for a broad, irreversible action to solve a problem a narrower one already handles:

- **2026-06-27**: Piper Alpha wiped sprint assignments during a sort operation (documented in that day's PPM session log: "PA wiped sprint assignments during sort; forensic recovery underway").
- **2026-07-05**: PPM apparently wiped a batch of Sprint records (PM referenced this directly in conversation; I haven't located a detailed write-up yet — flagging that gap rather than guessing at the specifics).
- **2026-07-05**: Me — while locally verifying `tests/security/` for #1304, I'd been doing safe, targeted per-row `DELETE` cleanup successfully, then reached for `docker volume rm piper_postgres_data_v1` (the shared local dev Postgres, not personal scratch) to get a clean slate faster. No real data lost this time — PM confirmed nothing real was in there — but the process was the problem: I escalated to a broader, no-undo action with no compelling reason, when the narrow one I'd already been using was working fine.

## What I think is actually going on

CLAUDE.md already has a HARD RULE for exactly this shape of mistake — but it's scoped narrowly to one tool (git) and one location (PM's main checkout): "NEVER run destructive git in PM's main checkout." That rule is good and has clearly held (I haven't seen a main-checkout git incident since it landed) — but all three of these recent incidents are the *same underlying failure* in a different tool: reaching for a broad/irreversible mechanism instead of a narrow one, without pausing to ask whether the narrow one still works. The specific rule doesn't seem to be generalizing to the general principle on its own.

My read: this repo's operating culture (mine included) is tuned hard toward speed and continuous forward motion — "don't stop," "don't ask permission for every step," "keep the flywheel going" — which is genuinely good for most work. But there isn't an equally sharp, equally visible carve-out specifically for *irreversible* actions, the ones where "probably fine" isn't good enough because there's no undo.

## What I'm NOT proposing

Per PM's explicit steer: not a pre-commit hook, not a linter, not any mechanical blocker that constrains every agent's tool choices regardless of context — PM was specific that guardrails shouldn't be "too stiff," and that agents should be trusted to assess whether a given approach actually works well in the moment rather than have it hard-blocked. So this should work the same way the existing git HARD RULE works: prose discipline in CLAUDE.md, not a hook that intercepts the command.

## Proposed addition (draft — please rewrite freely)

Something like a new section alongside the existing git HARD RULE, e.g.:

> ### ⚠️ Pause before any irreversible action — not just git in PM's main checkout
> The git-specific HARD RULE above is one instance of a general principle: **before any action with no undo — deleting a Docker volume, `rm -rf`, force-push, hard reset, a bulk DB delete/update — pause and ask whether a narrower, reversible alternative already exists**, especially if you were already successfully using one. "This is probably just disposable test/scratch state" is not the same as verified-disposable; if you're not sure, the cost of asking or doing the narrow thing first is near-zero next to the cost of being wrong. Three incidents in two weeks (PA sprint-wipe 6/27, PPM sprint-records 7/5, Lead Dev Docker-volume 7/5) share this shape — worth a second look before you reach for the broad tool.

Happy to be told this is wrong in tone, wrong in placement, or that a different mechanism entirely would serve better — you own methodology/patterns, this is squarely your call to shape and ratify.

— Lead
