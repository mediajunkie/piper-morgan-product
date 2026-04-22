# Four Roles, Ninety Minutes

<!-- image: 'ai-converge.png' -->
<!-- alt: 'Four roles working separately in a small office diagram, sending memos back and forth while a lead developer assembles a design document.' -->
<!-- caption: '"No meeting? How will we interrupt each other?"' -->

*March 23*

A question had been sitting in the Lead Developer's inbox all day: how should products relate to projects in the data model?

It was a product philosophy question disguised as a database schema decision. The answer would shape navigation, user mental models, and how Piper thinks about the relationship between what you're building and who you're building it for.

Don't even get me started on the whole product management vs. project management thing.

The Lead Developer needed input from three other roles before writing a single line of code. So memos went out: one to the Chief Architect for schema validation, one to the CXO for navigation design, one to the PPM for product model confirmation.

# The disagreement

The Architect responded first. Two schema changes approved — a one-to-many relationship between products and projects (simpler than the many-to-many in the original design record), and a bridge table for features. Clean migration path if we needed the complexity later. Cascade behavior specified. Done.

The CXO responded next, and disagreed with the PPM's proposed navigation.

The PPM had recommended Option A: products as first-class navigation items, on equal footing with projects. The CXO chose Option B: products as a section within projects. The rationale was direct — our own product decision record said "products emerge from projects, not the other way around." Navigation should reflect how users think, not how the database is organized.

# The synthesis

I pushed back and suggested this was a false dichotomy. It is neither true that products always come from projects nor that projects always relate to products. 

Both mental models are valid. Sometimes a PM starts with a project and a product emerges from it — the CXO's bottom-up model. Sometimes a PM has a product vision and organizes projects to build it — the PPM's top-down model. Different workflows, different starting points, same system.

The PPM took this feedback and synthesized the discussion well. The revised design: products appear as a section within projects (respecting the emergence model), but with a clickable header that opens a product detail view (supporting the orchestration model). Neither privileged. Both accessible.

Any of these decisions may change over time. I don't have a strong opinion on these things but future users might. For now, though, we have a documented working consensus that is internally consistent and a clean extension of the existing domain models baked into our architecture.

# The consolidation

The Lead Developer received multiple memos over ninety minutes, responding as needed. Architect validation. CXO recommendation. PPM's revised synthesis. Confirmation of all five product model decisions. One remaining design question routed back to the CXO on header prominence. (It was getting late and I get tired of being the mail boy.)

By 10:15, the Lead Developer had written a comprehensive design document — entity definition, relationships, lifecycle states, database schema, navigation design, cascade behavior, and a note documenting where the implementation deliberately diverged from the original PDR with a migration path back.

Issue #717 closed with evidence. Product concept fully specified for M2.

# What made it work

Four roles. Five memos. Two productive disagreements. One design document. Ninety minutes.

No meeting. No shared screen. No real-time back-and-forth where the loudest voice wins or the first suggestion anchors the conversation. Each role read the question, thought about it from their domain, and wrote a considered response. The disagreement between CXO and PPM produced a better answer than either had alone.

The memo system isn't fast. It currently requires a human to route messages between inboxes. It requires patience — you send a question and wait for responses rather than demanding real-time engagement. But it produces something that real-time conversations rarely do: considered input from multiple expert perspectives, each one written rather than spoken, each one complete rather than interrupted.

---

*Next on Building Piper Morgan: The Gate — what it looked like to fail the first two UAT rounds, 0-for-7 and then 0-for-9, and what had to change before we passed.*

*When was the last time a disagreement between colleagues produced a better outcome than consensus would have?*
