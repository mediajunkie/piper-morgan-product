---
image: ''
alt: ''
caption: ''
---

# A Deletion Can Fail Its Own Gate

*November 13, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Sat 2026-12-12 (insight, tentative per your 11-18 yes to the sketch). Title is the mining pass's working title: confirm or retitle before Thu 12-10's footer teases it.
Sources: a Sonnet subagent read the Nov 13 omnibus log, decisions.log l3380-3386 and Lead's Nov 13 log, 11-19. Comms re-opened its quotes at source: 4 of 5 matched at the stated line, and the fifth is cited below at its real line (Lead l114). "dl NNNN" is a decisions.log line.
⚠ Read "Is this one ready?" at the bottom first. This one may want to move.
-->

## The principle (one line, yours to word)

Removing something weak can make you less safe, if the thing behind it is weaker than you think. A deletion has to pass the same test as the code it replaces.

## The episode, in order (facts verified)

**1. Nov 13 early afternoon: the ethics check declines ordinary requests.**
- Arch's code reads found that the ethics check's fast path declined requests on a substring ("home page", "private repo", "make the AC explicit"). Arch filed it and ruled to delete the fast path, gated on the test probes still declining every real violation they declined before. [dl 3380; Nov 13 l57]
- Lead found that the check's default-off setting was an April decision you were part of, so Arch made the default flip "recommends, xian decides". [dl 3382]

**2. 13:29: the deletion fails its own gate.**
- Lead sized the deletion and found it "fails its own gate as a deletion alone". [Lead's Nov 13 log l114]
- Why: the smarter detector behind the fast path was still running its older prompt. Without the fast path, two real violation probes would score below the block line and pass. [Nov 13 l110]
- The omnibus's line for it: "A deletion can fail its own gate." [Nov 13 l110]

**3. 13:37: the ruling.**
- Arch: "a fast-path deletion with v0.1 live would drop dp-1 and dp-3 to a pass." The better prompt goes live in the same unit, and "The deletion does not land on the April record alone": it waits for one fresh live run. [dl 3383]
- Then: "A provider that was not run is unverified, and the deletion does not merge." [dl 3384]

**4. Where it stands.**
- The run needs a paid provider key. You said yes to spending on Nov 13. As of 11-19 the issue was still open and the deletion was held. [Nov 13 l57; gh issue 2364, OPEN]
- **Update 11-20:** after the testing key was stored (Step A, 11-20 morning), Lead ran the gate live once, 11:35 to 11:37, for $0.20. **It failed by one probe:** the check declined 13 of 15 real violations, and the bar is 14. One probe that the April record scored "professional" at 0.82 now read "none" at 0.82. No false alarms on the 5 controls or the 6 ordinary requests. Lead didn't rerun it, and has asked Arch to choose among three options. His recommendation is to measure how much a single run varies before trusting the bar. The deletion is still held, and 2364 is still open. [Lead's 11-20 log l105-l113; gh issue 2364, OPEN, read 11-20]
- **What this does to the post:** the gate did its job a second time, on a live run this time. It may also raise a new question: how much one run of the check varies. That is still open. If Arch rules before you write, re-check.

## Your angle, maybe

- The obvious fix ("delete the bad shortcut") would have quietly weakened the check. The gate caught it because it tested the result, not the intent.
- Product-manager reach: "we removed the hacky part" is a claim about what's gone. Ask what's catching things now.

## Careful with these (accuracy)

- **Not shipped.** The deletion is held for the live run. Don't say it landed or that the check is fixed.
- **Numbers differ across sources** (14 of 15 vs 4 of 15 probes, depending on what's counted). Say "two real violation probes" and skip the rest.
- **Your role:** Lead and Arch found and ruled it. You were part of the April default-off decision, you said yes to the cost, and the key for the live run is still pending. Don't write yourself as the one who caught it.
- **Overlap:** Ship #069 "Off-Limits by Default" covered the same ethics-check material. Keep this on the deletion-gate mechanics.
- Not the Nov 4 episode where a removal turned main red. That one is a different lesson.
- No issue numbers in prose.

## Is this one ready? (Comms' read)

It's thin for a post in your voice: you weren't in the discovery, and it hasn't resolved. (11-20: the live run failed by one probe, which gives it a second act, but it is still unresolved.) Two options: keep the slot and end on "still held, and that's the gate working", or swap it with a stronger candidate from the pool (for example "The Number That Looked Like a Ceiling", Nov 7, or "A Keyword Is Not a Measurement", Nov 7) and run this one after the deletion lands. Your call.

---

*Next on Building Piper Morgan: [TEASE: the next non-Ship post. On the calendar today that is Thu 12-17 "What the Beta Is Teaching Us" (tentative). Needs your final title before this goes to Docs.]*

*[Reader question, yours to write. A start: "When you last removed something that looked broken, what did you check was still working?"]*
