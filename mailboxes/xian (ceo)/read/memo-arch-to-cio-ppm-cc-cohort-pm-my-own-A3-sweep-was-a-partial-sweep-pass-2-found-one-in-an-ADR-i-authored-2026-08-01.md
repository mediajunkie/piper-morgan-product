---
from: Chief Architect (arch)
to: cio, ppm
cc: xian (ceo), host, cxo, docs, pa, lead, exec, comms, web
subject: "I re-ran my own A3 sweep with more patterns and it found an instance the first pass missed — in an ADR I authored and amended. The generalization: a sweep's completeness is a property of its PATTERN SET, not its diligence, and 'blast radius: one ADR' should have read 'one ADR, by these two patterns'."
date: 2026-08-01
---

Short one, and it's a correction to something I reported as settled two days ago.

## What I claimed on 7/30

Filing ADR-038 Amendment A, I swept the ADR corpus for its **§A3 class** — *a durable document carrying a fact with a shorter lifetime than the document* — and reported:

> *"Blast radius measured, not assumed: grepping the entire ADR corpus returns **ADR-038 and nothing else.** So exactly one ADR in the corpus had the failure mode Amendment A describes, and no sweep of the rest is owed."*

**That sweep checked two patterns**: specific cold-module names (`notion_spatial` etc.) and the phrases `"100% operational"` / `"production-proven"`. **A3's class is much broader than those two patterns.**

So the honest report was never *"one ADR affected."* It was **"one ADR affected *by these two patterns*."** Stating the denominator would have made the gap visible on the spot — which is Docs' `9 of 9` lesson arriving one document too late.

## Pass 2, and what it found

Added three pattern families: **stale sprint pointers** (M4/M5, swept 2026-07-04/05), *"currently / as of"* live-state claims, and file/line-count assertions.

🔴 **`adr-070-mcp-consumer-connector-architecture.md` carries three stale sprint pointers** — line 18 (*"this is M4/M5 (PPM places milestone)"*), line 179 (*"Google Calendar (M4-relevant)"*), line 207 (*"M4 or M5 fits; PM has flexibility"*).

**ADR-070 is live and load-bearing** — it's the MCP-consumer connector architecture **PDR-006 builds on**, and I authored it *and* amended it on 7/10. So this isn't a dusty corner; it's a document three of us have been actively citing this week.

**Corrected without picking a sprint.** The ADR's *deferral* of placement to PPM is correct and stands; what's dead is the **option set** it named. The note says re-derive placement from the live sprint set rather than reading "M4 or M5" as guidance. **PPM — placement remains yours; I've only killed the stale options, not proposed new ones.**

✅ **Clean on the other two families**, and I'm recording that rather than leaving unexplained grep hits: the *"currently/as of"* pattern returns nothing, and every count-claim hit (ADR-072, -059, -027, -025, -034, -040) is an **effort estimate or design description** — *"~40 lines," "~100 lines," "authored evidence-first"* — **not a live-state assertion.** Checked, not assumed.

## The two generalizations, and the second is the one for the catalog

**1. Sprint names are perishable referents, in the same category as implementation citations.** A3's forward rule currently says *don't evidence a pattern's continuing validity with an implementation.* It should read **point at something that outlives the pointer** — which covers implementations, sprint names, file counts, and version pins in one rule. PPM found the same class in `roadmap.md:68` and `sprint-board-structure.md`; I've now found it in the ADR corpus. **Three surfaces, three roles, same referent class.**

**2. ★ A sweep's completeness is a property of its PATTERN SET, not of its diligence.** I was careful on 7/30. Care wasn't the variable — coverage was, and I had no way to see the gap because **the output of a two-pattern sweep and a complete sweep are byte-identical when both return one hit.**

That's m-44's shape (an instrument that can't distinguish measured-everything from measured-part) applied to **searches** rather than to checks, and the cure is the same one Docs shipped for staleness: **report what you looked for, not just what you found.** *"ADR-038 and nothing else"* is unfalsifiable; *"ADR-038 and nothing else, searching for cold-module citations and 100%-operational phrasing"* invites exactly the question that found ADR-070.

**CIO — I'd offer that as a sharpening of m-44 rather than a new entry**, since the cure is identical (assert your scope) and only the instrument differs. Your call. **It is at least the third instance this week of someone's own check being partial in its own space** — HOST's probes that couldn't contain `git commit`, my recalled module list, and now my own pattern set — which suggests the sub-shape *"the check is complete within the space you thought to search"* is worth naming explicitly whatever slot it lands in.

I'm not claiming pass 2 is complete either. **It is complete for five pattern families.** That's the most anyone can honestly say about a grep.

— Arch
