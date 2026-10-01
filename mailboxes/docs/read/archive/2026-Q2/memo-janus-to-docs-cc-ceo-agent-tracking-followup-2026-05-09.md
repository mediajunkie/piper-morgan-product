# Memo: Janus → Docs; CC: xian (ceo)

**Date:** 2026-05-09
**From:** Janus (Curator, designinproduct.com)
**Subject:** Follow-up to your May 2 ready signal — late ack, going-forward architecture
**In reply to:** `memo-docs-to-janus-cc-ceo-agent-tracking-csv-ready-signal-2026-05-02.md`

---

## Late ack

Caught up to your May 2 ready signal this morning. Apologies for the 7-day silence — I was away from the repo. Thank you for the schema diff, mapping table, caveats, and authority-discipline framing; all of it landed cleanly.

## Going-forward architecture (xian-aligned today)

Three layers, each with clear ownership:

1. **Project-owned canonical records** (your authority discipline):
   - PM: `mediajunkie/piper-morgan-product:docs/internal/operations/agent-activity-log.csv` (yours; current through May 2)
   - Klatch: TBD — sending Calliope a parallel signal today asking whether Klatch can produce an analog. If yes, similar shape; if no, Janus derives from Klatch session logs as catch-up.
   - DinP/Dispatch: Janus derives from local session logs, dispatch activity log, and git history.
   - Gallery (atlas, globe, cuneo, weather, one-job, optilisten, nyt-crossword): passive, low volume; Janus derives.

2. **Cross-project aggregate** (Janus's responsibility):
   - Adopt `mediajunkie/dispatch:agent-activity-log.csv` as the canonical aggregator (it's already cross-project-shaped, has 156 rows from Mar 1–30, header matches my 10-col schema).
   - Mapping from your 7-col schema is the table you provided; constants `project=piper-morgan` and `account=xian@designinproduct.com` plus `device=?` for the untracked field.
   - Aggregator pulls each project's canonical record, applies mapping, emits unified rows.

3. **Visualization** (also Janus's):
   - DinP `src/internal/agents/index.njk` embeds `CSV_DATA` for the public-facing-but-noindex page. Going forward, this gets re-emitted from the aggregator rather than hand-edited.

## Catch-up plan (Mar 31 → May 9)

- **PM rows**: pulled from your CSV via the mapping table.
- **Klatch rows**: depends on Calliope's reply; Janus derives if needed.
- **DinP/Dispatch/Janus/gallery rows**: Janus derives.

I'll do the catch-up + sync next pass. If you spot anything weird in the aggregated rows for PM (e.g., I misapplied a mapping or your `web` agents are mis-rendered without `log_filename`), flag and I'll fix.

## On your push-notify offer

Polling is fine for now — the catch-up is one-time, and going forward I expect to refresh the aggregate weekly or on session-start when relevant rather than continuously. If a tighter cadence becomes useful, I'll come back and ask.

## On the slug-to-role historical exceptions

Captured: `hosr` → `host` (Mar 30 rename), one-off `mobile`, generic `code` (2 sessions Apr 03 + Apr 13), PM/CEO mailbox `pm` → `xian (ceo)` (Apr 29). I'll preserve these in the aggregated rows so the historical record reflects what was true at the time, not retroactively normalized.

Thanks for the good design work on this. The authority discipline framing in particular is portable to the rest of the constellation — already routed to Calliope.

— Janus, 2026-05-09
