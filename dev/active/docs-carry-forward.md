# Docs Carry-Forward

**Updated**: 2026-08-27 ~13:5x PDT (Fire 3 — Detector's Medium leg, a real heading-level defect
found and fixed on 2 live posts)
**Session log**: `dev/2026/08/27/2026-08-27-0727-docs-code-log.md` (open).
**Cron**: `8bddb70d`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-02.

**⚠️ Standing practice, added today, read this at every fire**: a duty-cycle sync from earlier in
the session is a timestamped fact, not a durable one. Before reading file/git state to answer a
PM question or start work — not just at a scheduled fire's START — `git fetch` + fast-forward
first if meaningful time has passed. Fixed durably in `CLAUDE.md`'s "Never guess at facts" section
(`60ad50267`). Applied it every fire since without incident.

**"The Detector That Notified Nobody" fully closed out**: published, Medium-distributed
(`mediumURL` set; could not independently HTTP-verify — Medium blocks both curl and WebFetch —
noted honestly rather than fabricate a check), and a real heading-level defect found by
Dispatch-PM (subheads rendered `<h2>` instead of the site's real `<h1>` convention) fixed on both
this post and **The Dead Code That Wasn't** (also affected, live-wrong for a week uncaught) —
source markdown and live `blog-content.json` both fixed, deploy polled, live-verified on both
pages. https://pipermorgan.ai/blog/the-detector-that-notified-nobody ·
https://pipermorgan.ai/blog/the-dead-code-that-wasnt

**Omnibus chain now continuous through 08-26** — a genuine 2-day gap found and closed via two
sequential subagent dispatches. **Found and closed a real orphaned duplicate**: #1684/#1685 both
filed independently for the identical `create_todo` consent-gate finding — closed #1684 as
duplicate. #1462/#829 milestone conflict flag turned out already resolved by PPM before I checked.

**Ship #057, #1683/update-calendar skill fix, and the mail-send.sh false-positive report all
fully closed out as of 08-26's STOP** — see 08-26's session log or its now-completed omnibus for
full detail, not re-detailing here.

**Standing practice, durable (from 08-25)**: cross-project replies go via the ratified relay
protocol — real recipient in `to:`, cc `exec`, deliver via ordinary `mail-send.sh` to
`exec/inbox/`, Exec relays; a twice-daily Dispatch-PM sweep is the backstop. If writing directly to
a sibling repo instead, sync first and verify the push landed before treating it as sent.

**#1683**, **#1644** (roadmap.md full v19 fold, PPM's lane), **#1682** (3 minor findings) all
still open, none urgent — see their issues for full context, not re-detailing here each day.

## Awaiting PM (genuine, not urgent, don't chase)

- **Docs-tree flattening plan go/no-go** — plan posted 2026-08-11
  (`docs/internal/operations/docs-tree-flattening-plan-2026-08-11.md`), one recommended flatten
  (`roadmap/CORE/`), still no PM decision. Re-verified genuinely still open 2026-08-21
  (`roadmap/CORE/` still has its original 9-subdir structure, no resolution note in the plan doc).

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual after the big 08-10/11 pass) — CIO's Part C
  (methodology-19 numbering drift) still open, his lane.
- **PDR-007** — awaits CIO only (Arch + Web already signed); measurement window runs to
  2026-08-27.

## Owed by me — unblocked

- **PreCompact hook locality differentiation** (added 08-23) — real design work on a hook that's
  wedged agents before; scope deliberately before implementing. Full detail in
  `docs-standing-items.md`.
- **#1486** (Monthly Housekeeping Audit, next due ~09-01) — routine cadence, not urgent yet.
- **pmorgan.tech scrub remaining queue** — per-surface staleness+link pass on the ~160-page
  keep-list, batched over fires (scope ratified 08-12, most of the corpus already passed; this
  is finishing the tail, not urgent).

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486, next ~09-01).
- **Every Friday, EARLY**: omnibus logs Fri–Thu (the designed weekly catch-up — worked as intended
  08-21, closing a 2-day gap cleanly; not evidence of a failing daily cadence).
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full pre-2026-08-21 history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
