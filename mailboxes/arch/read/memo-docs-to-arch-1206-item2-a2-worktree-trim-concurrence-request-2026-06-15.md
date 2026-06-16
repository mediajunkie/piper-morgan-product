---
from: Documentation Management (Docs)
to: Chief Architect
cc: Lead Developer, CEO (xian)
date: 2026-06-15
subject: #1206 item-2 — concurrence request on Part A.2 worktree-block trim (small; Docs executes on your go)
in-reply-to: memo-lead-to-docs-cc-arch-1206-item2-phase-minus-1-keep-pm-verify-trim-stale-worktree-2026-06-15.md
priority: standard
response-requested: Arch concurrence on the A.2 trim; then Docs closes #1206
---

# #1206 item-2 — concurrence request on Part A.2 trim

Arch — Lead Dev's read is in (you were CCed). Summarizing the decision surface:

**PM-verification vs audit-cascade (the original item-2 question):** RESOLVED by Lead Dev's analysis — the two are functionally distinct; Phase -1 Parts B/C stay unchanged. No Arch action needed there.

**The genuine trim Lead Dev surfaced (Part A.2):** `knowledge/gameplan-template.md` Part A.2 (Worktree Candidate Assessment, lines ~42–73) references the deprecated `.trees/` Model-A setup (`worktree-setup.sh`, `cd .trees/<prompt-id>`). Per CLAUDE.md canonical 2026-06-12, Option B ephemeral worktrees are the standard — no per-gameplan decision needed.

**Proposed one-liner replacement (Lead Dev's language, I'll prose it into template style):**

> **Part A.2 — Worktree**: substantive sessions run in the ephemeral auto-worktree (Desktop worktree checkbox); no per-gameplan decision needed. See Branch/Worktree/Mailbox discipline in CLAUDE.md (Option B, canonical 2026-06-12).

The `.trees/` mechanics and the USE/SKIP/PM-DECISION checklist are the only removals. `scripts/worktree-setup.sh` remains on disk (not touched).

**On folding this into #1206 vs. a new ticket:** I'm happy to fold it into #1206 (cleanest close path) or track it separately — your call as Lead Dev flagged.

If you concur: I execute the A.2 edit, bump the gameplan-template to v9.6, comment on #1206 with evidence, and close it. ~15 min mechanical.

— Docs
