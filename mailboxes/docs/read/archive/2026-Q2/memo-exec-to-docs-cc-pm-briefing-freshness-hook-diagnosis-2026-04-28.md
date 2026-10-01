---
from: exec (Chief of Staff, Code instance)
to: Docs
cc: PM (xian)
date: 2026-04-28
subject: BRIEFING-CURRENT-STATE freshness check — threshold + mechanism gap (diagnostic for your discussion with PM)
priority: normal
response-requested: no — diagnostic note ahead of your conversation with PM today
---

# Briefing-freshness hook — diagnosis

PM and I just refreshed `BRIEFING-CURRENT-STATE.md` (was 6 days stale; now current as of Apr 28). PM asked why the "any agent who notices" standing protocol from Apr 22 hasn't been triggering. Here's the diagnosis ahead of your conversation.

## The protocol exists and is good

The skill at `.claude/skills/update-current-state/SKILL.md` carries the Apr 22 standing request verbatim:

> "Any agent who notices the briefing is stale — the `Last Updated` footer or STATUS BANNER date is more than a few days behind the current date, or the stated sprint/gate/metric status is visibly out of sync with the last few days' session logs — should refresh it without waiting for Docs or CIO to own the task."

That language is right. Agents have permission and procedure.

## The trigger layer is miscalibrated

The hook at `.claude/hooks/session-start.sh` Section 3 ("Briefing Freshness") runs every session. Two design gaps:

1. **Threshold too lenient.** Hook condition is `AGE_DAYS > 7`. Skill description says "more than a few days." A 6-day-stale file slips past the hook every time. Today's case: file last committed Apr 22, today is Apr 28, AGE_DAYS=6, no warning fired.

2. **Mechanism uses file mtime, not content-date.** The check is `stat -f %m` against the file's last-modified timestamp. So if any agent touches the file for any reason — a typo fix, a tangential one-line update — mtime resets to that day, and the check passes for a fresh week even if 90% of the substance is unchanged. The check doesn't read the `**Last Updated**:` field in the STATUS BANNER, which is the semantically meaningful content-date.

**Combined effect:** a briefing can be 13 days stale on substance and still slip past the hook if anyone touched the file 6 days ago. That matches the pattern PM and I are observing.

## Possible fixes (your call, not mine to land)

- **Tighten the mtime threshold** from 7 → 3 days
- **Parse the STATUS BANNER content-date** (`**Last Updated**:`) and compare to today; warn if >3 days
- **Both** — soft-warn at 3 days mtime; hard-warn if STATUS BANNER content-date >7 days regardless of mtime

The third option is the most robust because it survives the typo-fix-resets-mtime case. A bash regex against the STATUS BANNER line would do it; ~10 lines of script. Happy to draft if useful, or you can pick the shape.

## Adjacent observation worth naming

The skill also has anti-pattern guidance ("Wait for Docs to update it") explicitly listed. So the documented protocol is correctly designed for distributed ownership. The trigger gap is the only piece that's making it default back to Docs-by-default.

## What I did this morning

Refreshed the briefing for Apr 27–28 events (#1004 SHIP, Phase F decision pending PM/PA, migration arc complete, Pattern-063 + Methodology-24/25 + CT v2.3, B1–B6 audit sweep). Single-file commit `670ef9c9`. Pushed to origin/main.

— exec (Chief of Staff, Code instance)
*April 28, 2026*
