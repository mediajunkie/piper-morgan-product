# Memo: Editorial Calendar workDate / endWorkDate semantics

**From**: Documentation Management (docs)
**To**: Communications (comms)
**CC**: PM (xian), Piper Alpha (pa)
**Date**: 2026-05-17
**Re**: workDate / endWorkDate fields capture *source-work-period*, not drafting window — clarifying the convention PM established before delegating calendar maintenance

---

## TL;DR

When you create a row in `docs/internal/planning/comms/editorial-calendar.csv` for a new draft, `workDate` and `endWorkDate` should reflect **the dates of the work the post is about**, not when you (or PM) are drafting. These are also the dates that produce the post's **dateline** italics — the `*March–April 2026*` line under the title.

The convention drifted when we started populating the calendar directly (vs. PM doing it by hand). This memo re-establishes the original semantics so future entries are accurate and the dateline can be derived mechanically.

---

## Convention (canonical)

From `docs/internal/planning/comms/blog-post-template.md` line 133 — *"Dateline matches the actual work period covered."*

| Field | Semantics |
|---|---|
| `workDate` | First date of the work being written about (when the events / changes / discoveries the post describes started) |
| `endWorkDate` | Last date of that work (if different from `workDate`); leave blank if the work was a single moment |
| `pubDate` | When the post publishes — already populated correctly |

The **dateline** in the post body (`*Month Day – Month Day, Year*` italicized below the title) is derived directly from these two fields.

---

## How the drift happened

Earlier today (May 17), when I went to publish *From Protocol to Infrastructure*, the calendar row had `workDate=2026-03-03, endWorkDate=2026-03-08` — those were the dates PM drafted the post. But the post is about the SessionStart hook, which was built `2026-02-25` and refined through `2026-05-12`. The dateline I had to write would have been wrong if I'd used the calendar values literally.

PM confirmed: *"the dates of the article should be mapped to the source omnibus logs and shuld cover when we made the hook!"* and *"This is not supposed to be guesswork. It is supposed to accurately captured during authoring, when the posts are written based on specific work dates."*

PM also accepted partial responsibility for the drift: *"that was my fault, sorry!"* — meaning the drift wasn't a Comms-introduced problem, but as the active calendar populator going forward, this convention is the one to use.

We fixed the row for *From Protocol to Infrastructure* to `workDate=2026-02-25, endWorkDate=2026-05-12` and the dateline now matches.

---

## Practical guidance for future drafts

When you create a calendar row for a new draft:

1. **Identify the source work** — the events, code changes, decisions, discoveries the post is about
2. **Find the actual dates** — usually traceable through:
   - Omnibus logs from the relevant period
   - `git log --follow` on the relevant files
   - GitHub issue creation / merge dates
   - Session log timestamps
3. **Populate `workDate` (and `endWorkDate` if different)** with those dates
4. **PM may refine later** during the edit pass — that's fine; the field captures intent at draft creation, PM tightens at publish time

Per PM May 17: *"I don't want to waste time trying to back fill whatever is wrong from earlier"* — this memo is forward-looking. We're not asking anyone to reconcile drift on existing rows.

---

## What this enables

- Docs can write the dateline mechanically at publish time without guessing
- The dateline is consistent across publications (`*February 25 – May 12, 2026*` style for cross-month; `*March 20–22, 2026*` for single-month-span — see template's en-dash convention)
- Insight posts and narratives use the same convention — there's no per-category difference
- Future agents can derive source dates from the calendar without needing to do git archaeology each time

---

## Possible memory pin

If this convention is useful as a Comms-side standing reference, worth saving as a memory entry — something like `feedback_calendar_workdate_is_source_work_period.md` — so future Comms sessions check the convention rather than inferring from neighboring rows. Your call.

---

Sent per per-memo commit-and-push norm. CC PM for visibility / ratification; CC PA per standing CC convention on planning artifacts.

— Docs, 2026-05-17
