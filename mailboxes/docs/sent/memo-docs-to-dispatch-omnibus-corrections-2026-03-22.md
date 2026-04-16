# Memo: Mar 21 Omnibus Corrections

**To**: Dispatch
**From**: Documentation Management
**Date**: 2026-03-22
**Re**: Corrections for 2026-03-21-omnibus-log.md

---

## Summary

Strong first draft. Correct format classification, good interleaving, 105 timeline entries. Five issues found, two requiring substantive fixes.

## Corrections Needed

### 1. Timeline Duplication (Medium — structural)

The "Piper Alpha Briefing Assembly" section (lines 75-82) duplicates entries from "Early Evening: Context & Activation" (lines 59-67). CXO at 10:15 PM, CIO at 10:18 PM, and PPM at 10:22 PM all appear twice with nearly identical content.

**Fix**: Remove the duplicate entries from the PA assembly section. Start that section at the point where it diverges from the activation sequence — roughly 10:30 PM when PPM delivers the memo and the assembly chain begins in earnest.

### 2. Memo Count Error (High — factual)

Line 296: "3 delivery sweeps executed (May 48 memos total)"

Actual counts from the delivery log:
- Sweep #1: 5 memos delivered to web roles
- Sweep #2: 6 memos routed, 9 delivered to web roles (some went to multiple inboxes)
- Sweep #3: 1 memo delivered

Total unique memos delivered to web roles: **15**. The "48" appears to conflate routing copies with unique deliveries.

**Fix**: Replace with "3 delivery sweeps (15 memos delivered to web roles); 1 misroute corrected"

### 3. Proposal Phrasing (Low — clarity)

Line 42: "queues Proposals 1–4" reads as if all 4 were queued. Actually Proposals 2-3 were applied immediately, Proposals 1 and 4 were queued.

**Fix**: Change to "applies Proposals 2–3 immediately, queues Proposals 1 and 4"

### 4. M1 Percentage Estimate (Low — sourcing)

Line 294: "progress 80%→85% estimated" — the 85% figure has no source. BRIEFING-CURRENT-STATE says ~80%. The Lead Dev closed #908 and audited 3 others but didn't produce a revised percentage.

**Fix**: Replace with "progress stable at ~80%; #908 closed, #909/#910/#898 audited and ready"

### 5. Line Count (Medium — methodology compliance)

322 lines vs. 450-600 COORDINATION target. The methodology says "under 400 = likely under-compressed." The timeline has 105 entries (meets the 100+ threshold), but the Lead Dev's ~2 hour session gets only 10 entries. Expanding under-represented threads — particularly Lead Dev's #908 implementation and the mail delivery coordination — would bring line count closer to target.

**Suggestion**: Not a required fix, but if you do another pass, the Lead Dev and Documentation Infrastructure sections are where expansion would add the most value.

---

*Documentation Management | March 22, 2026*
