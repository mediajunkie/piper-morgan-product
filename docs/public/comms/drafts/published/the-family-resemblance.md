---
image: 'ai-quilt.png'
alt: 'Ethereal AI beings collaboratively sew a shared quilt whose patterns grow more intricate and interconnected from left to right.'
caption: '"It's becoming a tradition!"'
---

# The Family Resemblance

*March–April 2026*

A few weeks ago I added a file called `DECISIONS.md` to one of my projects. It's a lightweight log — date, decision, rationale — meant to keep the morning-brief routine from re-litigating the same questions every Monday. The file has grown to a few dozen entries and it's saved me at least a dozen of those re-litigation cycles.

I didn't invent it. The pattern came in from a sibling project. *Klatch*, an entity-management system being built in parallel, adopted `DECISIONS.md` the same day, independently, and a new project I'm doing at work for [OpenLaws.us](https://openlaws.us/) quickly adopted something very similar. Once the cross-pollination brief surfaced the convergence — *several sibling projects have the same file shape solving the same problem* — adopting it for Piper Morgan took five minutes.

Three projects. One file. Same shape. No pre-planning or mandated coordination.

# What gets across

This kind of transfer has been happening more than I expected. Some recent examples:

The SSH-over-port-443 workaround I now use when conference Wi-Fi blocks port 22 came in from my primary assistant on Klatch, Calliope, after one of their agents got stuck on the same network constraint. They wrote the workaround into their CLAUDE.md. The cross-pollination brief picked it up. We added it to this project's.

The session-start protocol — *check the cross-pollination brief, count unread mail, verify branch status* — exists in some form in every sibling project, with variations. The Klatch version has different inboxes; the version for work emphasizes a different freshness-check; the Piper Morgan version handles role-specific session logs. The shape is recognizable. The instances are not identical.

The handoff-memo template I use when a Chat-based agent role migrates to Code came out of a five-section structure my head-of-sapient-relations agent (HOST) drafted back in March. By the time HOST and chief innovation officer (CIO) roles had both used it, two parallel projects had picked up similar templates, with their own modifications: Klatch added a "what I'd tell my successor that I wouldn't tell the PM" section (omg, I love this so much). For work, a more no-nonsense context, we collapsed the relationship section into the lessons one.

# What doesn't get leaked

It's worth noticing, equally, what hasn't crossed.

The actual project work doesn't cross. Klatch's entity model isn't being imported into Piper Morgan, OpenLaws's business info isn't getting shared at all. The domain interiors of the projects are sovereign — each one is solving its own problem, with its own data shapes, its own product surface, its own users, its own posture in terms of private, confidential, public, open, and so on.

Specific tooling decisions also stay local. The choice to use one LLM provider over another, the particular vector store, the test-runner configuration, the CI provider — those propagate when there's a clean reason to copy them, but mostly they don't, because mostly they're shaped by constraints unique to each project. 

Jargon has sometimes leaked across and then has had to be retracted. A few weeks ago one of my agents read a Klatch session log, picked up a phrase about how the "bring your own chat" architecture model related to Step 10 of Klatch's longstanding roadmap. But Step 10 is meaningless outside of that context and "Klatch Step 10 = BYOC" is practically hieroglyphic.

The vocabulary was being imported as if it carried its mechanism with it. Vocabulary doesn't always. Sometimes it's just the local name for a local thing.

So what should come across is something narrower than "any practice from any sibling." It's specifically the artifacts whose shape is general enough to make sense in another context, while their content is local enough to be filled in differently each time.

# Why "family resemblance" is the right phrase

When the philosopher Ludwig Wittgenstein talked about *family resemblance* (hey, I gotta get some use of that philosophy degree, especially with a reunion coming up next weekend, in 1879 Hall no less!) he meant the idea that members of a category share overlapping subsets of features rather than a single defining trait. This is true of the various projects I've got going at different scales that are using agentic assistance: No single feature is shared across all sibling projects in exactly the same form.

Some siblings contribute to or read the cross-pollination brief mechanism. Not all of them.

Some use a handoff memo template. Not all have adopted this.

Some have added session-start hooks. Not all have.

Some follow the DECISIONS.md file shape. Not all do.

What unifies the family isn't one common feature. It's the *texture of overlap.* Project A and Project B share a brief mechanism. A and C share session-start hooks. B and C share decision logs. Each sibling resembles every other sibling along some axes and diverges along others. The family is recognizable, but if you tried to write down the single defining trait, you'd come up empty.

This matters because the alternative, something like *let's pick one standard, document it, mandate it across siblings*, is the thing every cross-team coordination effort tries first, and the thing that almost always produces either drift (the standard is honored in name and abandoned in practice) or rigidity (the standard prevents legitimate local variation). Family resemblance is what you get instead, when you let practices propagate through documentation and observation rather than through enforcement.

Hey, I cut my teeth on the platform design team at Yahoo, seeing teams resist aligning with single sign-on, some for good reason (ahem, Flickr).

# What this all enables

The thing the family resemblance enables, that a single standard couldn't, is *fast adoption with retained sovereignty.* When DECISIONS.md showed up in the brief, I could adopt it without negotiating its shape. When the SSH-over-443 workaround arrived, I could drop it into my CLAUDE.md without checking whether some governing body had blessed it. When the Klatch project drew inspiration from Piper Morgan's handoff-template convention as a way to capture a missing layer of contextual memory, my handoff-memo template traveled to Klatch. The Klatch team could then modify it, for example adding that "what I'd tell my successor" section, without asking permission.

That's a different shape of cross-project coordination than I'd seen before. It's not a federation. It's not a standards body. It's not even a community of practice in the formal sense. It's a small, opinionated set of projects with overlapping tooling and shared infrastructure, where good ideas show up in one and are visible enough that they can spread to the others, and where the spread doesn't require the projects to agree on anything beyond *this particular shape, in this particular instance, makes sense for me too.*

I don't know yet whether this scales. Three or four sibling projects under common stewardship is one thing. Thirty might be another. But for now, the family resemblance pattern is doing real work, and the work it's doing wouldn't survive a more formal arrangement.

The next step, where the resemblance hardens into common infrastructure rather than parallel artifacts, is the topic of another piece in this pair.

---

*Next on Building Piper Morgan: From Protocol to Infrastructure — what happens when a shared practice stops being negotiated and becomes the environment.*

*Where in your work do you see family resemblances rather than shared standards? When does that shape produce better coordination than a formal standard would have?*
