---
image: 'ai-log.png'
alt: 'Glowing ethereal beings amending a giant ledger book, reintegrating missing pages into the official record while the book appears to point out its own omissions'
caption: '"Not so fast!"'
---

# The Log That Fact-Checked Itself

*April 22, 2026*

The Piper Morgan methodology fixed itself last month. My Documentation Management again (Docs) opened a session a little after eleven AM on April 22 with a mundane task on the agenda: the Apr 17–21 omnibus logs (the synthesized daily logs we make by interpolating each agent individual session log) were overdue, and we needed to walk the source materials together before synthesis. No drama expected. A catch-up sweep, an hour or two of work, then back to the active week.

I asked Docs to do a horizontal pass instead — list every agent's session logs across the missing days in a single CSV, role by role, day by day, so we could verify the source set was complete before any omnibus got written. The CSV was an export of a spreadsheet I had started to track daily sessions and make sure I got all the logs, but I realized I don't want to have to do this myself anymore, especially now that all the agents write their logs directly to disk.

# The case of the missing logs

The CSV took about half an hour to assemble. When we read it together, something stopped us.

The April 16 omnibus log — synthesized three days earlier on April 19 — listed six source sessions in its footer. Lead Developer. CXO. Docs. Piper Alpha. The Chief Architect. Comms. Six agents, six logs, one omnibus.

The CSV showed nine session logs for April 16. Lead Dev, CXO, Docs, PA, Architect, Comms — *plus* my Principal Product Manager (PPM) at 5:00 PM, plus my Chief Innovation Officer (CIO) at 4:23 PM, plus my Head of Sapient Trust (HOST) at 4:56 PM. The Architect log in the footer had also turned out to be a partial 1,965-byte snapshot; a complete 2,652-byte version was sitting in another directory.

Three sessions missing entirely. One sitting in partial form. The omnibus from three days earlier had been built on roughly two-thirds of the actual day. We'd been treating it as canonical.

# The cost of mmemory drift

I'll spare you the inventory, but it wasn't trivial. The CIO's missing session held the morning's [Excellence Flywheel](https://github.com/mediajunkie/piper-morgan-product) reformulation decisions — three structural layers, five practices including the new "Audit the composition" promotion of Pattern-062, the CLAUDE.md Option B vote. The PPM's missing session held the pathological-tagging memo to Lead Dev that quietly reshaped how we were going to score the next round of canonical retests. HOST's missing log held a twelve-role health check whose worst finding (`team-structure.md` 103 days stale) had been waiting unread for three days.

None of those threads were *lost* — the artifacts existed, just not in the synthesis. But the synthesis was what other agents would read when they wanted to know what April 16 had been. Three days into being canonical, our canonical record was missing a third of its sources.

I felt the small irritation that comes from noticing a drift you should have seen earlier. *This drift worries me*, I told Docs. *I'm still a little disappointed our methodology doesn't include common sense noticing of missing logs when there are often clues and responses in other logs from the day.*

# The fast fix and the slow one

The literal fix was straightforward. Docs amended the April 16 omnibus log: sessions count from six to nine, three previously-missing sources integrated, the partial Architect log replaced with the complete version, the executive summary expanded to absorb the new content. The amendment was an explicit annotation rather than a silent rewrite — *this omnibus was originally synthesized 2026-04-19 from incomplete source set; amended 2026-04-22 after PPM/CIO/HOST 4/16 logs downloaded.* Provenance preserved.

The methodological fix took a little longer. Docs added a new mandatory step to the create-omnibus skill — Step 2.5, *Cross-Reference Gate.* Before any omnibus gets synthesized, the skill now runs a regex against each source log looking for mentions of other agent roles ("CXO sent...", "Architect responded...", "PA flagged..."). It compiles the union of mentioned roles. It compares that union to the source set. Any role that appears in someone else's log without having a corresponding source in the omnibus footer triggers a STOP — go fetch the missing log, or document the gap explicitly. Never silently paper over.

In the omnibus footer for April 22 (the day this all happened), Docs noted that the Step 2.5 gate had been written *and tested in the same session* — my Chief of Staff agent's (Exec's) own April 22 log surfaced as missing from the initial source set, got fetched, and the gate re-evaluated PASS. The methodology had caught its own first test case on the day it was written.

# Recursion increases...

What made the morning feel like a methodology moment, rather than just a housekeeping one, was the timing.

Five days earlier — April 17, the day of the IAC talk and the M1 methodology audit — the CIO had promoted [Pattern-062 (Assembly Assumption)](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/current/patterns/pattern-062-assembly-assumption.md) to be the fifth practice of the Excellence Flywheel: *audit the composition.* The pattern was already in our catalog. The promotion to a Flywheel practice was the formal recognition that "individually-correct components composing into collectively-incomplete outcomes" is a *kind of failure* the methodology has to actively guard against, not just notice when it happens.

Five days later, the practice's first major test case turned out to be an omnibus log we'd produced ourselves. The Apr 16 omnibus had been individually-correct in every line — every claim verifiable, every quote sourced — and collectively incomplete because the source set itself had been wrong. Pattern-062 at the synthesis layer.

So meta!

Good reminder that nothing immunizes a discipline against the failure mode it names. The discipline can help you catch its own failures more quickly, at least.

The fix wasn't that we became *better* at noticing. The fix was that we made the noticing *mandatory at a specific gate*. The skill now runs the cross-reference check whether the human or the agent would have thought of it or not. The discipline got moved from attention into infrastructure.

# The mote in one's own AI

The interesting question isn't whether a discipline can prevent its own failure mode. (It can't.) The interesting question is whether, when the failure mode shows up *on its own work*, the discipline is honest enough to catch it and durable enough to fix the fix.

That morning was a yes on both.

---

*Next on Building Piper Morgan: The Voice of a Denial — what happened that same Wednesday evening, when the ethics-enforcement work shipped its first four phases and showed us what it sounded like when Piper actually had to refuse something.*

*When has your team's discipline caught its own failure mode? And — separately — when did you confuse "we have a principle for that" with "the principle is operating"?*
