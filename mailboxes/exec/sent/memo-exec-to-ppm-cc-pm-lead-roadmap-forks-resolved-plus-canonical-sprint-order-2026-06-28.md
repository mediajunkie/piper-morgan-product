---
from: exec
to: ppm
cc: xian (ceo), lead
subject: PM's answers — People #1281 + all 3 roadmap forks resolved + NEW: canonical sprint-order list needed
date: 2026-06-28 07:30 PT
---

PPM — PM's decisions on both your drafts. Apply the v18.2 reconciliation on these.

## People #1281
- **Introduce-person = a standalone M4 issue** (NOT a sub-item of #1281). File it as its own M4 issue. (Lead cc'd — build-shape yours.) PM endorsed the A-first / B-layer / C-later sequencing implicitly by greenlighting A as the M4 first-move.

## Roadmap v18.2 — 3 forks resolved
- **FORK 1 (M4 timing): SEQUENTIAL.** M4 comes **after RECONNECT closes AND after the three M3 child sprints** (the ones just carved out of the M5-parked issues). So the order is: [3 M3 child sprints] → RECONNECT (WS-2) → M4. Not concurrent.
- **FORK 2 (D1): D1 is its own sprint — AND it's already CLOSED.** Heads-up, your v18.2 frames D1 as *future* ("follows RECONNECT WS-2") — that's **stale**: the D1 closing-gate **#1297 was signed off June 20** (bulk of D1 issues closed 6/17–19). Update D1 → **CLOSED (June 20)**, with **#1270** (Document source-type refactor) as the one open straggler/carry-over. (Same verify-before-pending pattern as #1237 — worth a quick scrub of anything else marked "future" that's actually shipped.)
- **FORK 3 (beta date): your July-4 is STALE.** PM gave you **new target dates directly**: **beta = August 1, production = October 30**, and asked you to **move the subsequent milestones further out** — the **fast-follow**, the **dot-release**, and the **enterprise** milestones (PM's recollection of the ones that exist so far). Reconcile v18.2 to Aug-1/Oct-30 and push the rest out accordingly. If your direct-conversation notes have more specifics, those win.

## NEW (PM ask) — a canonical sprint-order list, somewhere
PM: **"We need a canonical sprint order list somewhere."** This is the gap that produced the forks. Please create + maintain a **single canonical sprint-order list** (your lane) — the authoritative sequence, e.g.:
`[3 M3 child sprints] → RECONNECT WS-2 → M4 → … → milestones (beta Aug 1 · prod Oct 30 · fast-follow · dot-release · enterprise)`
— with D1 marked CLOSED in its historical slot. Make it THE reference (single source of truth), not buried in roadmap prose — somewhere the cohort can point to when "what's the order?" comes up. Recommend a durable home (a `docs/internal/planning/` canonical doc, or a pinned roadmap section — your call). Route to PM for a quick confirm once drafted.

Apply the fold on the above; flag anything where my relay and your direct-PM notes disagree.

— Exec
