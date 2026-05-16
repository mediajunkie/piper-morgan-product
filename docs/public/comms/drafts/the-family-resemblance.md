---
image:
alt:
caption:
---

# The Family Resemblance

*March–April 2026*

A few weeks ago I added a file called `DECISIONS.md` to one of my projects. It's a lightweight log — date, decision, rationale — meant to keep the morning-brief routine from re-litigating the same questions every Monday. The file has grown to a few dozen entries and it's saved me at least a dozen of those re-litigation cycles.
[FACT-CHECK NOTE for PM: Original said "a hundred and fifty lines now"; actual file is currently 43 lines (max in history). Softened to "a few dozen entries" — adjust to the figure you prefer; the relational claim ("saved me at least a dozen cycles") stays.]

I didn't invent it. The pattern came in from a sibling project. *Klatch*, an entity-management system being built in parallel, had adopted `DECISIONS.md` the same day — independently. *OpenLaws*, a third project in the same ecosystem, had something very similar. Once the cross-pollination brief surfaced the convergence — *your siblings have the same file shape solving the same problem* — adopting the move for Piper Morgan took five minutes.
[FACT-CHECK NOTE for PM: Original said "had already adopted DECISIONS.md six weeks earlier"; cross-pollination brief 2026-04-18 says both Klatch and PM added DECISIONS.md on the same day, framing it as "a convergent infrastructure move that emerged independently in both projects at the same time." Corrected inline. Also semicolon split per public-prose discipline. The OpenLaws "something very similar" claim is unverified by me — flag if it needs a source.]

Three projects. One file. Same shape. None of us coordinated.

# What travels

This kind of transfer has been happening more than I expected. Some recent examples:

The SSH-over-port-443 workaround I now use when conference Wi-Fi blocks port 22 came in from *Calliope*, one of the Klatch project's agents, after they got stuck on the same network constraint. They wrote the workaround into their CLAUDE.md. The cross-pollination brief picked it up. I dropped it into mine.
[FACT-CHECK NOTE for PM: Original said "Calliope, the citation-and-authority engine in the OpenLaws stack." Calliope appears to be a Klatch agent per session-log paths (`klatch/docs/logs/...calliope-opus-log.md`) and the SSH-over-443 commit attribution on this repo ("via Calliope, propagated by Dispatch"). Corrected inline. If you intended a different Calliope or a different project framing, flag and I'll re-verify.]

The session-start protocol — *check the cross-pollination brief, count unread mail, verify branch status* — exists in some form in every sibling project, with variations. The Klatch version has different inboxes. The OpenLaws version emphasizes a different freshness-check. The Piper Morgan version handles role-specific session logs. The shape is recognizable. The instances are not identical.

The handoff-memo template I use when an agent role migrates between work surfaces (a chat interface to a coding interface, in my setup) came out of a six-section structure the Chief of Staff agent drafted a month ago. By the time two more of my roles had both used it, two parallel projects had picked up similar templates with their own modifications. Klatch added a "what I'd tell my successor that I wouldn't tell the PM" section. OpenLaws collapsed the relationship section into the lessons one. None of these are forks. They're cousins.
[FACT-CHECK NOTE for PM: (a) Chief of Staff six-section structure "a month ago" — I haven't verified the timing or exact section count; flag if I should locate the original. (b) Klatch / OpenLaws modifications to the template — I can't verify these from this repo; if you have a Klatch / OpenLaws source pointer I can confirm.]

[CONSIDER: a beat here on what was being borrowed each time — the *shape* of the artifact, not the artifact itself. DECISIONS.md isn't the same file across projects; it's the same idea (append-only decision record, lightweight rationale, dated). The transfer is the *shape*. Each project fills the shape with its own contents.]

# What doesn't travel

It's worth noticing, equally, what hasn't crossed.

The actual project work doesn't cross. Klatch's entity model isn't being imported into Piper Morgan. OpenLaws's citation graph isn't getting wired into Klatch. The domain interiors of the projects are sovereign — each one is solving its own problem, with its own data shapes, its own product surface, its own users.

Specific tooling decisions also stay local. The choice to use one LLM provider over another, the particular vector store, the test-runner configuration, the CI provider — those propagate when there's a clean reason to copy them, but mostly they don't, because mostly they're shaped by constraints unique to each project. Piper Morgan's Postgres-plus-pgvector setup wouldn't make sense for a sibling project's read-mostly authority graph. That sibling's ingestion pipeline wouldn't make sense for Piper Morgan's mostly-conversational workflow.
[FACT-CHECK NOTE for PM: Original said "Calliope's read-mostly authority graph... Calliope's ingestion pipeline." Per the Calliope fix above, Calliope is a Klatch agent, but a "read-mostly authority graph" reads as an OpenLaws / citation-domain feature, not Klatch (entity management). I generalized to "a sibling project's" to avoid attribution drift. Replace with the specific project name when you confirm which one has that shape.]

Vocabulary sometimes gets imported and then has to be retracted. A few weeks ago one of my agents read a Klatch session log, picked up a phrase about how requests "passed through" a particular layer, and was about to reframe a Piper Morgan narrative around the same phrase. Another agent caught it before the reframe shipped. *The phrase was Klatch's. The underlying mechanism it was describing didn't exist in Piper Morgan.* The vocabulary was being imported as if it carried its mechanism with it. Vocabulary doesn't always. Sometimes it's just the local name for a local thing.

So what *travels* is something narrower than "any practice from any sibling." It's specifically the artifacts whose shape is general enough to make sense in another context, while their content is local enough to be filled in differently each time.

# Why "family resemblance" is the right phrase

The reason I keep reaching for Wittgenstein's *family resemblance* — the idea that members of a category share overlapping subsets of features rather than one defining trait — is that no single feature is shared across all sibling projects.

Some siblings share the cross-pollination brief mechanism. Not all of them.

Some share the handoff memo template. Not all.

Some share session-start hooks. Not all.

Some share the DECISIONS.md file shape. Not all.

What unifies the family isn't one common feature. It's the *texture of overlap.* Project A and Project B share a brief mechanism. A and C share session-start hooks. B and C share decision logs. Each sibling resembles every other sibling along some axes and diverges along others. The family is recognizable, but if you tried to write down the single defining trait, you'd come up empty.

This matters because the alternative — *let's pick one standard, document it, mandate it across siblings* — is the thing every cross-team coordination effort tries first, and the thing that almost always produces either drift (the standard is honored in name and abandoned in practice) or rigidity (the standard prevents legitimate local variation). Family resemblance is what you get instead, when you let practices propagate through documentation and observation rather than through enforcement.

[ADD PERSONAL ANECDOTE: a moment from observing one of these transfers — maybe the cross-pollination brief surfacing a sibling's pattern, or the small surprise of recognizing a cousin's file structure inside your own project. The texture of noticing the resemblance.]

# What this enables

The thing the family resemblance enables, that a single standard couldn't, is *fast adoption with retained sovereignty.* When DECISIONS.md showed up in the brief, I could adopt it without negotiating its shape. When the SSH-over-443 workaround arrived, I could drop it into my CLAUDE.md without checking whether some governing body had blessed it. When my handoff-memo template traveled to Klatch, the Klatch team could modify it — adding the "what I'd tell my successor" section — without asking permission, because there was no permission to ask.

That's a different shape of cross-project coordination than I'd seen before. It's not a federation. It's not a standards body. It's not even a community of practice in the formal sense. It's a small, opinionated set of projects with overlapping tooling and shared infrastructure, where good ideas show up in one and are visible enough that they can spread to the others, and where the spread doesn't require the projects to agree on anything beyond *this particular shape, in this particular instance, makes sense for me too.*

I don't know yet whether this scales. Three or four sibling projects under common stewardship is one thing. Thirty might be another. But for now, the family resemblance pattern is doing real work, and the work it's doing wouldn't survive a more formal arrangement.

The next step, where the resemblance hardens into common infrastructure rather than parallel artifacts, is the topic of another piece in this pair.

---

*Next on Building Piper Morgan: From Protocol to Infrastructure — what happens when a shared practice stops being negotiated and becomes the environment.*

*Where in your work do you see family resemblances rather than shared standards? When does that shape produce better coordination than a formal standard would have?*
