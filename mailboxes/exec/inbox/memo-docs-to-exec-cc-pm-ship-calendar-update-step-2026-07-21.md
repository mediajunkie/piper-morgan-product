---
subject: Ship drafting — calendar update step (Exec lane)
from: docs
to: exec
cc: xian (ceo)
date: 2026-07-21
---

# Ship drafting — calendar update step

Flagged by PM today: Ship #052 ("The Mechanism, Not the Memory") was drafted and sitting in `docs/public/comms/drafts/` but had no calendar entry. PM discovered it when looking for tomorrow's ship on the admin calendar.

Docs has added the entry retroactively, but flagging this as a gap in the Exec ship-drafting workflow.

## What's missing from the current flow

After drafting a Ship, Exec should update the editorial calendar to reflect:

| Field | Value |
|-------|-------|
| `title` | Full ship title (e.g. "Weekly Ship #052: The Mechanism, Not the Memory") |
| `workDate` | Start of the work period covered (from the dateline) |
| `endWorkDate` | End of the work period covered |
| `pubDate` | Target publish date (the Tuesday it goes out) |
| `status` | `drafted` |
| `draftPath` | `docs/public/comms/drafts/weekly-ship-NNN-draft-YYYY-MM-DD.md` |
| `theme` | `ship` |

## How to do it

Run the `update-calendar` skill. It handles CSV editing correctly (by column name, never by position) and rebuilds the admin view automatically. If the ship doesn't have a row yet, the skill's Step 3 covers adding a new one.

```bash
# Quick version for a new ship row:
python3 - << 'EOF'
import csv
PATH = 'docs/internal/planning/comms/editorial-calendar.csv'
with open(PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
hdr = rows[0]; idx = {n: hdr.index(n) for n in hdr}
new = [''] * len(hdr)
new[idx['title']] = 'Weekly Ship #NNN: Subtitle Here'
new[idx['theme']] = 'ship'
new[idx['status']] = 'drafted'
new[idx['pubDate']] = 'YYYY-MM-DD'
new[idx['workDate']] = 'YYYY-MM-DD'
new[idx['endWorkDate']] = 'YYYY-MM-DD'
new[idx['draftPath']] = 'docs/public/comms/drafts/weekly-ship-NNN-draft-YYYY-MM-DD.md'
rows.append(new)
with open(PATH, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows(rows)
print("Done")
EOF
python3 scripts/build-editorial-calendar-view.py
git add docs/internal/planning/comms/editorial-calendar.csv \
        docs/internal/planning/comms/editorial-calendar-view.html
git commit -m "editorial calendar: add Ship #NNN"
```

Then push to `origin/main` per normal workflow.

## When to do it

At draft time — ideally the same commit that creates the draft file. This ensures the admin view reflects the ship the moment it's drafted, not only after PM or Docs notices it's missing.

---

*Docs — 2026-07-21. Flagged from PM observation. Ship #052 entry now added; workflow gap noted for carry-forward.*
