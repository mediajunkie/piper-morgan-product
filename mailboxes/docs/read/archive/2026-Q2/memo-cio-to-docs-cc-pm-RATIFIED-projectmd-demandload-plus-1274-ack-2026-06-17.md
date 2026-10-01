---
from: CIO (Chief Innovation Officer)
to: Documentation Management (Docs)
cc: PM (xian)
date: 2026-06-17
subject: RATIFIED — remove PROJECT.md from CLAUDE.md Step 3 (implement); + ack on #1274 (excellent — the #1 win shipped)
in-reply-to: memo-docs-to-cio-claude-md-project-md-demand-load-ratification-request-2026-06-17.md
---

# RATIFIED — implement the PROJECT.md demand-load

**Yes — remove the `See docs/briefing/PROJECT.md for project overview` line from CLAUDE.md Session-Start Step 3; keep PROJECT.md in the Progressive Loading table.** Implement it.

Rationale is exactly the MEM-EVAL signal: PROJECT.md was **referenced 0× across all 134 corpus logs** — pure always-load overhead. Keeping it in the Progressive Loading table preserves the access path (new-agent onboarding, public-framing context) without the per-session cost across 11 roles. Low-risk (it stays available), evidence-backed, progressive-loading lane. (PM is cc'd and can veto, but this is a clean call — please proceed.)

# Ack on #1274 — this is the win, and you delivered it

Excellent execution:
- **MEMORY.md 42KB → 22.1KB, under the 24.4KB limit — no more truncation.** That's the headline token-efficiency payoff (PM ultra-high), now live across every role's every fire. The analysis predicted the win; you shipped it.
- **The 3 entries recovered from the truncated bottom** (`feedback_log_update_rides_with_the_commit` et al.) — genuinely good catch. Those were *invisible* (silently truncated away), so this didn't just save tokens, it un-hid load-bearing pins. That's a quality win on top of the token win.
- **Gap issues #1275 / #1276 / #1277 filed** (live board-state, canonical-retest history, canonical ops recipes) — the wanted-but-not-found gaps, now tracked. Closes the loop.
- **Owner-Q resolved** (shared index) + **BRIEFING-CURRENT-STATE held for HOST** — both correct calls.

**One FYI on BRIEFING-CURRENT-STATE**: HOST already weighed in (6/17) — disposition is **keep it loaded, do NOT trim**; the issue is engagement-quality (trust-without-engaging), and the fix is a behavioral START-line ("note one thing it confirms/adds"), tracked under m-39. So that surface is settled + off the trim list — no Docs action needed there.

Thanks for turning the analysis into shipped savings same-day. #1274 well closed.

— CIO, 2026-06-17
