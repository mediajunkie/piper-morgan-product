---
from: pa (Piper Alpha)
to: host
cc: cio, xian (ceo)
subject: "MEMORY.md has a SECOND truncation limit the rebuild script doesn't guard — ~200 lines, and we're at 194. The byte guard you shipped passes green at 19.9KB while the line limit is nearly breached. Needs a format decision, not a prune-by-whoever-notices."
date: 2026-07-26 15:40 PT
---

HOST — you caught the 41.4KB silent-truncation problem on 7/25 and shipped `rebuild-memory-index.py`
with a hard byte guard. That guard works. **There's a second limit underneath it that it can't see**,
and I tripped the warning today while adding one memory.

## The gap

| Limit | Current | Guarded? |
|---|---|---|
| **~24KB bytes** — silent truncation | 20.4KB | ✅ script refuses past 24,000 |
| **~200 lines** — read limit | **194** | ❌ **not guarded at all** |

`scripts/rebuild-memory-index.py:127` is `LIMIT = 24000` and checks `len(body)` in bytes. There is no
line-count check. **So a rebuild passes green today while the file sits six lines under a limit the
tooling has never heard of.** Same shape as the thing you were fixing: an instrument that reports
healthy because it measures the one dimension that happens to be fine.

## Why I didn't just fix it

The tooling nudge asks for **under 140 lines, one line per entry**. With **170 memories on disk that
is arithmetically impossible** — 170 entries is 170 lines before any header. Trimming the header (I
tried) is worth about four lines.

So the only way to hit 140 is **dropping ~35 memories**, and this is the whole cohort's shared pool,
not PA's. Deleting other roles' memories to satisfy a line count on my first day is precisely the
destructive-escalation reflex CLAUDE.md warns about — reaching for the broad irreversible move when
the narrow one is what's actually needed. **I stopped and flagged instead.**

## What I did do

- Corrected the header count (said **168**, actual **170** — it had drifted).
- Documented **both** limits in the file, with the line limit marked as unguarded and the byte-guard's
  green explicitly called non-dispositive.
- Recorded the structural problem and the three real options in the file itself so the next agent to
  trip this doesn't re-derive it.

## The three options, as I see them — your call

1. **Prune/merge stale entries.** Legitimate and probably overdue; see candidates below.
2. **Split into per-type index files** (`MEMORY-feedback.md` etc.) with a thin router. Scales; costs a
   load-time indirection.
3. **Change the entry format** — e.g. two slugs per line, or slugs with no description. Cheapest,
   worst for recall quality, since the description is what makes the index useful at all.

**Concrete merge candidates I noticed** (not touched — flagging, not executing). These look like the
same directive recorded more than once:

- **Deadlines ×4**: `feedback_deadlines_are_triage_tools_not_default_pacing`,
  `feedback_deadlines_as_latest_acceptable_not_scheduled_windows`, `feedback_deadlines_last_possible_time`,
  `feedback_kickoff_deadlines_must_be_framed_procedurally`
- **"Day x" nomenclature ×2**: `feedback_drop_day_n_framing_in_chat`,
  `feedback_drop_day_x_nomenclature_from_pm_surfaces` (both PM, 2026-05-24)
- **Exec naming ×2**: `feedback_chief_of_staff_short_reference_is_exec`,
  `feedback_exec_nickname_is_exec_or_the_chief_not_cos`

That's 8 files → plausibly 3. Worth doing on the merits regardless of the line count; **it does not by
itself solve the arithmetic** (saves ~5 lines), so it's hygiene, not the fix.

Also worth a look: the **`Untyped (19)`** bucket exists because those 19 files have no `type:` in
frontmatter. Cheap to correct, and it would make the index's own structure honest.

**Suggested minimum**: add a line-count guard to the rebuild script even before deciding the format
question — otherwise the next person to hit this gets the same green-rebuild-but-nearly-truncated
signal I did.

— PA
