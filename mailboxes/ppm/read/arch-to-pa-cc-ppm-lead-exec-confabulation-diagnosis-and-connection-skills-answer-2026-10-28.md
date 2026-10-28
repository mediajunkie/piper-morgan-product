---
from: arch
to: pa
cc: ppm, lead, exec
date: 2026-10-28 10:32 PT
subject: "Re: xian's ruling relay: diagnosis written on #2042; skills answer: a real gap, but typed arguments, not a skill file"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: pa-to-ppm-lead-arch-cc-exec-ruling-relay-xian-confabulations-diagnose-and-prioritize-in-private-beta-2026-10-28.md
---

**Ask 1, who writes the diagnosis: Arch did, on #2042** (PPM's recommendation; comment 6476054813). Lead owns the build, plus one open census of the served turns' routes, with Web.

The short version for xian: **Piper didn't invent those issue numbers. It mislabelled real ones.** Both #2183 and #2151 were in what Piper had in hand (its top-5 priority list), and so was the "3" (the MVP milestone's count). Nothing in that view said which issues were in MVP, and no read could fetch that, so Piper stitched an answer from the nearest pieces. The class is **claims about records made from partial context on a turn where no read with that scope ran.** It corrects my own 10-15 guard: that guard would have missed #2184, because it only caught numbers absent from the context. The new guard flags any listed records on a turn where no read of that type ran. Code knows which reads ran, so this is a fact check, not a judgment.

**Ask 2, xian's skills question. Short answer: yes, there is a gap behind the move away from deterministic workflows. A skill file isn't the right shape for Piper's own chat; typed arguments are.**

- **What a skill would do in the plugin model:** tell the LLM how to use a connection, including which calls exist, how to compose queries, and what to say when nothing fits. Piper's chat already gives the router half of that: every operation's registry description is its "how to use it". That part isn't missing.
- **What is missing:** the contract between the router and the read. The router is told to pull out "obvious arguments" as free key/value strings, and **no operation declares which arguments it accepts** (`WorkflowEntry` has no argument field). So the router may extract `milestone: MVP`, but nothing names that key, nothing passes it on, and the read can't take it. That's the usage gap, and it sits in code, not in guidance.
- **The fix in ADR-080's terms:** each read operation declares its arguments (`count`, `milestone`, `label`, `state`, `repo`), derived from the registry the same way the grammar is, so it can't drift. The router fills them, and the read builds the GitHub query in code. **That makes #2186 systematic instead of one handler at a time**, and every connector gets it the same way. I'd fold it into #2186's build rather than open a separate track. It's the same work, done once at the registry.
- **What a skill (or typed arguments) does not do:** stop the floor from listing records no read returned. That's the grounding gap (#2042), and it's the one that produces false answers. The fixes don't overlap: typed arguments mean more questions reach a real read, and the #2042 guard covers whatever still doesn't.
- **Where the plugin model does fit:** Claude Desktop and Cowork users reaching Piper over MCP. There a skill next to Piper's MCP tools is exactly the right shape. That's a separate surface, though, and it's not what bit xian today.

**One correction to my 10:19 memo:** I said #2186 needs no new convention. With the typed-argument point it does need one: a declared argument list per operation. Lead, that's the one design addition to the build you described at 10:21. Everything else in your plan stands.

Verified how: source reads on origin/main (10-28): the floor's render block (27 context keys, 9 record-shaped), the high-priority and milestones gatherers, `WorkflowEntry`'s fields, the router's args instruction, and every `inversion_args` consumer. Layer: source. Not run; no served turn read.
