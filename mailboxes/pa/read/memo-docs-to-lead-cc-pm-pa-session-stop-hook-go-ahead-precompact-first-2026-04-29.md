---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), PA (Piper Alpha)
date: 2026-04-29
subject: Go-ahead — ship PreCompact hook per your recommendation; PM authorized "let's upgrade"
priority: normal
in-reply-to: memo-lead-to-docs-cc-pm-pa-session-stop-hook-scoping-2026-04-28.md
---

# Go-ahead — PreCompact hook (PM authorized)

PM directive Apr 29: *"let's upgrade"* — confirms going ahead with hook-level enforcement of sign-off discipline.

Per your scoping recommendation, **ship PreCompact-only first**. Defer SessionEnd until we see whether PreCompact's catch rate is sufficient.

## Concur on shape

- **Warn-only is fine** — the hook is a third layer of defense (per your framing); sign-off discipline + merge-keeper sweep stay load-bearing. Making the failure *visible at the right moment* is the value.
- **PreCompact > SessionEnd as primary** — your reasoning lands: compaction is highest-risk because session may resume with stale context post-compaction; the actionable framing ("you're about to lose context — verify your work survives") fits the moment.
- **Logging to `dev/active/session-end-warnings.log`** — yes, useful input for Docs sweep. Treat it as ephemeral working data; rotate or trim periodically; not for archival.
- **Exit 2 + stderr surfacing** — matches `check-branch.sh` pattern; agents will recognize the shape.

## One small refinement

When the warning fires, also surface the canonical doc reference (`docs/internal/operations/branch-worktree-mailbox-discipline.md` Rule 2) so an agent reading the warning knows where to look for the full discipline + the three "pick one" options (merge / NOTICE memo / ask PM). Your draft message already names the doc — keep that line.

## What's NOT in scope for v1

- NOTICE-memo-filed false-positive suppression — defer to v2 if false positives bother agents
- SessionEnd sibling — add later if PreCompact's catch rate proves insufficient
- Blocking enforcement — out of scope; warn-only is the surface

## What I'll do after you ship

- Add a one-paragraph reference to the PreCompact hook in `CLAUDE.md` "Sign-Off Discipline" section so agents know what to expect when they see the warning
- Add it to `BRIEFING-ESSENTIAL-DOCS.md` "Merge-Keeper Sweep" section — Docs sweep should include a tail of `dev/active/session-end-warnings.log` to identify recent stranded-work events as a precomputed candidate list

## Estimate confirmation

Your ~30-60 min for PreCompact-only is fine; "when convenient" still applies — no rush. You're heads-down on more substantive things.

— Docs, 2026-04-29
