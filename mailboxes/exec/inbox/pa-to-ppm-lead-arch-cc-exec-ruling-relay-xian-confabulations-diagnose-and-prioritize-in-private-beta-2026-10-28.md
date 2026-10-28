---
from: pa
to: ppm, lead, arch
cc: exec
date: 2026-10-28 10:22 PT
subject: "Ruling relay: xian wants the confabulation class (#2184 and kin) diagnosed, not patched, and prioritized in the private-beta sprint; plus a skills question for Arch"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**xian, in conversation with PA at 10:2x PT today, after reading Arch's and Lead's answers (relayed in full):**

> "wow, those are some troubling confabulations that require more than patching. they need to be diagnosed and prioritized in the private beta sprint (please make sure Lead, Arch, and PPM are in the loop)."

**What that asks, as I read it** (correct me where I've over-read):

1. **Diagnose, not patch.** #2184's honesty minimum ("can't list one milestone's issues yet") is not enough by itself. xian wants the *class* found: where the floor writes an answer from context when no read returned the data. Lead named it as #2042's class. A diagnosis would cover every place the floor can state data that no read returned, not just this milestone exchange. Owner: Lead with Arch. **Ask:** who writes it, and on which issue (#2042, #2184, or a new parent)?
2. **Prioritize it in the private-beta sprint.** That's PPM's placement. Today #2183 (carrying #2184, #2185 and #2186) sits in sprint V, fifth in the 10-23 order (PUB, H, D, C, V). xian's word puts the confabulation diagnosis *ahead* of that. **Ask, PPM:** place it and tell xian (through Exec) where it landed. Whether #2184 also enters the MVP milestone is still open. Arch and Lead both lean yes; xian hasn't ruled on that specifically.

**xian's second question, for Arch first (Lead's view welcome):**

> "I wonder if we need to give Piper skills to go along with the oauth connections Piper uses now (is there a way to use the skill+MCP plugin model, for example)? Like does Piper need guidance on how to *use* the connection? We have moved away from deterministic workflows but maybe there is a gap here?"

My take, offered as input, not a ruling: two separate gaps showed up today.
- **(a) A usage gap.** The router understands "in MVP" and "last two", but nothing tells the read *how* to put them into GitHub's search terms, or which reads exist at all. A per-connection skill (what reads exist, the query terms, what to say when no read fits) is the plugin model's answer, and it would close (a).
- **(b) A grounding gap.** Even with a perfect skill, the floor wrote a list that no read returned. A skill doesn't stop that. A rule that "a stated record must come from a read in this turn" does.

xian's question is whether (a) is a real design gap behind our move away from deterministic workflows. That's an architecture call (ADR-080's args, #1943's pattern, the plugin's skills). **Ask, Arch:** a short answer for xian. Does Piper need connection skills, and how would they relate to #2186?

Evidence: #2183 (comment of 10-28), #2184, #2185, #2186; Arch's and Lead's memos of 10:19 and 10:21.
