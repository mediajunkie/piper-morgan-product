# Four Roles, Ninety Minutes

*March 23*

Monday evening. Nine-twenty. A question had been sitting in the Lead Developer's inbox all day: how should products relate to projects in the data model?

This sounds like an implementation detail. It wasn't. It was a product philosophy question disguised as a database schema decision. The answer would shape navigation, user mental models, and how Piper thinks about the relationship between what you're building and who you're building it for.

[ADD PERSONAL DETAIL — why this issue had been open for a while, what had kept it from being resolved]

The Lead Developer needed input from three other roles before writing a single line of code. So memos went out: one to the Chief Architect for schema validation, one to the CXO for navigation design, one to the PPM for product model confirmation.

## The disagreement

The Architect responded first. Two schema changes approved — a one-to-many relationship between products and projects (simpler than the many-to-many in the original design record), and a bridge table for features. Clean migration path if we needed the complexity later. Cascade behavior specified. Done.

The CXO responded next, and disagreed with the PPM's proposed navigation.

The PPM had recommended Option A: products as first-class navigation items, on equal footing with projects. The CXO chose Option B: products as a section within projects. The rationale was direct — our own product decision record said "products emerge from projects, not the other way around." Navigation should reflect how users think, not how the database is organized.

[CONSIDER — the PDR-003 callback, where a document the team wrote months earlier resolved a live disagreement]

## The synthesis

The PPM read both responses and did something I didn't expect. Instead of defending Option A or accepting Option B, the PPM reframed the question.

Both mental models are valid. Sometimes a PM starts with a project and a product emerges from it — the CXO's bottom-up model. Sometimes a PM has a product vision and organizes projects to build it — the PPM's top-down model. Different workflows, different starting points, same system.

The revised design: products appear as a section within projects (respecting the emergence model), but with a clickable header that opens a product detail view (supporting the orchestration model). Neither privileged. Both accessible.

[ADD PERSONAL DETAIL — reaction to watching this unfold through memos rather than a meeting]

## The consolidation

The Lead Developer received five memos over ninety minutes. Architect validation. CXO recommendation. PPM's revised synthesis. Confirmation of all five product model decisions. One remaining design question routed back to the CXO on header prominence.

By 10:15, the Lead Developer had written a comprehensive design document — entity definition, relationships, lifecycle states, database schema, navigation design, cascade behavior, and a note documenting where the implementation deliberately diverged from the original PDR with a migration path back.

Issue #717 closed with evidence. Product concept fully specified for M2.

## What made it work

Four roles. Five memos. Two productive disagreements. One design document. Ninety minutes.

No meeting. No shared screen. No real-time back-and-forth where the loudest voice wins or the first suggestion anchors the conversation. Each role read the question, thought about it from their domain, and wrote a considered response. The disagreement between CXO and PPM produced a better answer than either had alone.

[ADD PERSONAL DETAIL — reflection on the memo system vs meetings, what this says about async multi-agent coordination]

The memo system isn't fast. It requires a human to route messages between inboxes. It requires patience — you send a question and wait for responses rather than demanding real-time engagement. But it produces something that real-time conversations rarely do: considered input from multiple expert perspectives, each one written rather than spoken, each one complete rather than interrupted.

Ninety minutes from question to closed issue. Not because anyone rushed. Because nobody wasted time.

---

*Next on Building Piper Morgan: The Migration — when the infrastructure underneath you changes, and everything has to keep running.*

*When was the last time a disagreement between colleagues produced a better outcome than consensus would have?*
