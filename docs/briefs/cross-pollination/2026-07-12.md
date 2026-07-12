# Cross-Pollination Brief — July 12, 2026

Piper Morgan's Comms role hit the same source-verification failure mode twice in a single session: a real number from the primary source, attached to the wrong story. Standard "verify against primary sources" discipline doesn't catch this — the number is there, just describing something adjacent. The fix is a narrower check. Klatch quiet this window; all secondary sources quiet.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### "Verify against primary sources" doesn't catch a number that's real in the source but belongs to an adjacent story

**From:** Piper Morgan, Comms role (`dev/2026/07/11/2026-07-11-1331-comms-code-log.md`, July 11)

**Relevant to:** Any team that reviews agent-produced content against session logs or internal working documents before publishing — especially when multiple incidents or incidents share quantitative data. Klatch (Calliope blog posts from session logs); DinP (Janus curation from working notes); One Job (Coral blog beat production from internal design docs).

During review of two sequential blog posts in one session, the same failure mode appeared twice with identical shape: a specific, plausible-sounding number existed in the primary source but described a different story nearby.

**Instance 1 — Pattern-073 instance count:** A blog post attributed its opening story to "Pattern-073 instance #14." The CIO's own methodology ruling for that same incident explicitly assigned the "#14" label to a different finding within the same incident — and named the blog's actual opening story a *separate* finding, NOT Pattern-073. The number "14" was real; it was in the same ruling document. But it described an adjacent categorization, not the claim being fact-checked.

**Instance 2 — Recovery duration:** A second post claimed "the recovery took me ninety minutes." Ninety minutes does appear in the primary source log — but in an entry describing a May 10 workstream-review incident. The crash recovery the post was actually about (May 23) has no such duration figure anywhere in the same log.

Both cases passed a "does this number appear in the primary source?" check. Both failed a "does this number specifically describe *this* event?" check.

**Why this happens:** Rich session logs and omnibus documents accumulate many incidents with overlapping shapes — multiple crashes, multiple multi-hour investigations, multiple numbered methodology instances. Proximity bias and pattern-matching make an adjacent figure feel like confirmation when it isn't. The more your source documents are narrative records of similar recurring events, the higher the risk.

**The more exacting standard:** When verifying a specific factual claim — especially a number, count, or duration — the check is not "is this figure somewhere in the source?" It's: *"Does this specific figure, in this specific sentence of the source, describe this specific event?"* That narrowing is often the difference between a correct attribution and a plausible-but-wrong one.

**Suggested action:** In any content-review checklist that includes "verify against primary sources," add the narrower version as a sub-step for quantitative claims: trace the specific number to the specific sentence in the source that describes the specific event being asserted. If the number appears nearby but describes something else, treat it as not-found.

## Sources Read

- **Klatch** — git log (48h): brief delivery commits only. No new methodology; one `.gitignore` commit from Jul 9 already covered.
- **Piper Morgan** — git log (48h): Comms blog-production pipeline (three editorial rounds on "When the Documentation Drifts," published live; preliminary review of Jul 12 post), HOST alpha-invite operational close, Docs duty-cycle deconfliction memo filed to CIO. One transferable finding above; rest operational or continuation of July 10–11 findings.
- **atlas, globe, cuneo, optilisten, mediajunkie** — no commits in 48h window; skipped.
- **weather, one-job, nyt-crossword** — brief delivery or automated status commits only; skipped.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*