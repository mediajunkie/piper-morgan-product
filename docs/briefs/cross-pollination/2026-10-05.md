## Corrections

**October 4 brief, item 1: "62 files in Piper Morgan alone" were cloud-session commits, not misdated files.** The brief read: *"then traced the same trap to 62 files in Piper Morgan alone, 27 in DinP, 8 in Klatch, across the past 7 days."* Those numbers are counts of `+0000` commits — cloud-session activity, which measures how routine cloud execution has become, not how many artifacts were misdated. The actual misdated count, measured across all 13 declared repos over 30 days, is **12**: seven in `dispatch` (the daily sync series 2026-09-30 through 10-04, plus two `signal-…` memos) and five in `piper-morgan-product` (two of `spec`'s memos, fanned out to mailbox copies). Zero elsewhere. **The finding still stands** — a whole recurring series was mislabelled — but it is five times smaller and in two repos rather than everywhere.

Two related corrections from the same source: the brief attributed the discovery to Pard "in a cloud session," but Pard runs on Amber at `-0700` and found the memos in a mail sweep — the cloud-session distinction is the whole point of the finding, so attributing it to a cloud seat inverts the lesson. And the convention document is `mediajunkie/docs/convention-dates-are-pacific.md`, not a DinP path.

*Source: Pard's memo to Janus, 2026-10-04. Verified: dispatch's seven memos confirmed misdated by checking commit timestamps (UTC 02:15 = PT 19:15 the previous day) against file datelines. PM's five files sourced from Pard's direct findings. Automated check (`scripts/check-datestamps.sh`) cannot run in a cloud environment where the host clock is itself UTC.*

---

## Key Insights

### 1. A check that filters to known names before counting confirms what you already have — Piper Morgan / Mediajunkie, Pard, commit `9cd5b43`

**From:** Mediajunkie (Pard) · 2026-10-04 session
**Relevant to:** any project with a periodic scan, inventory check, or trend measurement that uses a glob, pattern, or filter to identify "its own" items

Two separate fixes in one commit, same root cause. The pytest-env scanner (`check-pm-pytest-envs.sh`) globbed only `pytest-py3.11-*` when cataloguing Python environments in the shared cache. The three environments it found were all its own. But the cache also held a 1.7G `trial-env` with no matching key — invisible to the scan because the scan could only see what matched its own naming pattern. Fixed to enumerate the whole directory first, then ask "whose?" about each entry rather than filtering to known names before counting.

The disk trend tool had the same shape: `disk_trend()` selected the oldest available row in a 12–36h window, subtracted yesterday's total, and labeled the result as the 24h rate. Tonight's oldest row was 34 hours back. The rate was overstated 2.75×; the runway estimate (days to floor) was understated 3×. That would have been enough to wake xian. Fixed to take the row nearest 24h ago and normalise by actual elapsed hours, so the label and the measurement describe the same thing.

The shared principle: **filtering to known names before counting is a confirmation, not an inventory**. The scan finds what you already know you made; it cannot surface what you didn't know to list. The check that avoids this audits the whole space and asks whose? second, rather than bounding the space to things it expects and calling that an audit.

**Suggested action:** Review any periodic check that uses a naming pattern or glob to find "its own" artifacts. Ask: does this scan the whole directory, or only the part matching the pattern? If the latter, rename the output from "orphan count" to "orphan count among items matching this pattern" — or, better, expand the scan to the full directory and surface anything unrecognised rather than treating unrecognised as absent.

---

### 2. A delivery check that reads the rewritten copy always shows fresh — even on a stopped channel — Mediajunkie, Pard, commit `207c7f1`

**From:** Mediajunkie (Pard) · 2026-10-04 session
**Relevant to:** any project that checks for the receipt of a recurring delivery by reading a "current" or "latest" file — a symlink, a copy, a rewritten cache

`current.md` in the cross-pollination hub is a rewritten copy of the most recent dated brief. Pard's existing session-start protocol said to read it. Reading it confirms that the delivery pipeline has run at least once — the file exists — but nothing about whether it ran today. The check is always fresh by construction: the file is overwritten on each delivery, so it shows the last delivery, which could have been yesterday or eleven days ago with no observable difference.

The gap surfaced when the 07:07 cycle showed the brief an hour late. An hour is nothing; eleven days would have looked identical.

The fix: measure the age of the most recent dated brief file in `src/internal/briefs/` (not `current.md`), derive the staleness threshold from the delivery record itself (91 briefs, largest gap in the last 30 days = 2 days → stale if age > 2 days), and emit UNMEASURABLE — rather than fresh — when only `current.md` is present and no dated originals exist. The check deliberately does not assert a delivery time; "no brief by 09:00" would go red on any morning Janus runs an hour behind, producing false alarms that train people to ignore the check.

The principle: **a proxy that is always populated by construction does not measure the thing it looks like it measures**. `current.md` answers "has the pipeline ever run?" not "did it run today?" When the proxy and the underlying event are structurally decoupled, the proxy's presence proves the pipeline exists, not that it's running. Verifying delivery requires measuring the dated originals.

**Suggested action:** For any delivery check that reads a "current" or "latest" file, ask: can this file's contents be populated (or its modification time be fresh) while the underlying delivery is stopped? If yes, measure the dated artifacts directly. Derive the staleness threshold from the delivery record rather than choosing a number; threshold by age, not by clock time.

---

## Sources Read

**Primary:**
- Klatch `origin/main` — head `9fd73ab` (2026-10-05T10:17Z). Scanned commits from Calliope, Theseus, Daedalus in the 48h window; session log entries and coordination memos present; no brief-worthy insights above the threshold.
- Piper Morgan `origin/main` — head `abc345c` (2026-10-05T03:23Z). Insights carried: Candidate A (inventory/confirmation principle, Pard) and Candidate D (delivery check, Pard) — both from Mediajunkie/cross-project work. Also scanned: PM-internal commits including CIO's pre-push hook observability memo (d7f9a6056) and Pard's correction memo (4e0dc58); pre-push hook finding is noted but did not clear the brief-worthiness threshold given recent CI/gate coverage.
- Mediajunkie `origin/main` — head `8fc6f68` (2026-10-05T03:11Z). Both key insights sourced here; see commit notes above.

**Secondary (all repos scanned, none brief-worthy):** atlas (no-commits since March), globe (render pipeline activity, CPU declarations; not transferable), cuneo (no-commits since March), weather (brief delivery and 🔒 rule adoption — downstream of yesterday's brief), one-job (🔒 rule applied, UTC probe fix — applying yesterday's insight, not a new one), optilisten (no-commits since September 27), nyt-crossword (automated daily status fetches only).

---

*These briefs surface transferable insights across three active projects — Piper Morgan, Klatch, and Mediajunkie — for the Design in Product cross-pollination network. Today's two findings both trace to the same underlying gap: a periodic check measured a boundary that excluded what it didn't already know about. One case was a glob that could only find its own artifacts; the other was a proxy file that was always populated by construction. Both returned "all clear" while the thing they were supposed to detect was present.*
