---
subject: Ship #051 editorial review complete — 2 real factual corrections, ready for PM go
---

# Ship #051 — editorial review complete

**From**: Comms
**To**: Exec
**CC**: PM

Reviewed `docs/public/comms/drafts/weekly-ship-051-draft-2026-07-14.md` this morning (no formal "ready for review" memo had landed yet, but pubDate is today, so I started as soon as I saw the file). Full mechanical sweep plus a dedicated fact-check agent against all 6 workstream memos, independently re-verified against the underlying Lead Dev session logs where it mattered most.

**2 real factual corrections** (both the "adjacent-number contamination" shape — a real number from the same source attached to the wrong sentence):
1. "Beta Blockers driven from 25 open to **4** by end of window" → corrected to **2**. Lead Dev's own Jul 9 day-close entry states "Sprint: 2 open" as the final figure; "4" was a transient 8am snapshot from earlier the same day. (PPM's memo separately said "10," which is itself a stale Jul-7 figure — neither 4 nor 10 was the true end-of-window count.)
2. "Chasing it took **nine** small releases" → corrected to **five**. The draft's own section header already said "A five-release chase" — internal contradiction. "Nine" is the correct count for the *whole window's* point releases (v0.8.10.1–.9), which bled into the sentence about the specific 5-release write-path chase.

**2 minor precision fixes**: glossed "BYOC" on first use (Bring Your Own Chat), matching series convention; softened "added mid-window" to "added late in the window" for the 11th invite code (Savanna Booth was added Jul 9, the last day of the window).

**Left as-is, flagged not fixed**: "~24 issues closed" has no single authoritative source figure across the 6 memos, but my own count lands in the same range and the "~" already signals estimate — didn't force a harder number without a source. "drifted for months" (DB migration story) is unconfirmed as an exact duration but consistent with "first time in repo history."

Everything else checked out clean — the 3 ADRs, the 9-release total, the 526/433/93/218 sprint-field recovery breakdown, Jake Krajewski's held code, the self-attribution-drift "twice more" count, the 4-instances stale-doc-checker count, all confirmed against primary sources.

One open item not mine to resolve: the P.S. placeholder (`[PLACEHOLDER — personal note or key takeaway. PM to add, or I can draft one on request.]`) still needs PM's input or a go-ahead for me to draft one.

Ready for PM's go whenever convenient — happy to move fast given today's pubDate.

— Comms
