---
image:
alt:
caption:
---

# The Family Resemblance

*March–April 2026*

A few weeks ago I added a file called `DECISIONS.md` to one of my projects. It's a lightweight log — date, decision, rationale — meant to keep the morning-brief routine from re-litigating the same questions every Monday. The file has grown to a few dozen entries and it's saved me at least a dozen of those re-litigation cycles.
[FACT-CHECK NOTE for PM: Original "a hundred and fifty lines now" is off. Actual current file (`/Users/xian/Development/piper-morgan/piper-morgan-product/DECISIONS.md`) is 43 lines. Softened to "a few dozen entries" — adjust to the figure you prefer.]
[SOURCE NEEDED for PM: "saved me at least a dozen of those re-litigation cycles" is a relational claim that lives in your memory of the morning-brief routine. No project-source evidence for the specific count. Keep as written, soften, or ground in one or two concrete examples?]

I didn't invent it. The pattern came in from a sibling project. *Klatch*, an entity-management system being built in parallel, adopted `DECISIONS.md` the same day, independently; a new project I'm doing at work for [OpenLaws.us](https://openlaws.us/) quickly adopted something very similar. Once the cross-pollination brief surfaced the convergence — *several sibling projects have the same file shape solving the same problem* — adopting it for Piper Morgan took five minutes.
[FACT-CHECK NOTE for PM: Original "six weeks earlier" contradicted by the cross-pollination brief 2026-04-18, which says: "Both Klatch and PM added `DECISIONS.md` files today" and frames it as "a convergent infrastructure move that emerged independently in both projects at the same time." Corrected to "the same day, independently."]
[SOURCE NEEDED for PM: OpenLaws "quickly adopted something very similar" — no cross-pollination-brief entry I could find records the OpenLaws DECISIONS.md adoption. Likely PM-memory or sibling-project-internal. Want a concrete timing tied to the OpenLaws side, or stay at the relational "quickly adopted"?]

Three projects. One file. Same shape. No pre-planning or mandated coordination.

# What gets across

This kind of transfer has been happening more than I expected. Some recent examples:

The SSH-over-port-443 workaround I now use when conference Wi-Fi blocks port 22 came in from my primary assistant on Klatch, Calliope, after one of their agents got stuck on the same network constraint. They wrote the workaround into their CLAUDE.md. The cross-pollination brief picked it up. We added it to this project's.
[SOURCE NEEDED for PM — IMPORTANT ATTRIBUTION CHECK: The April 18 omnibus log in this repo records the attribution chain as "the workaround … was contributed via Calliope **(OpenLaws)** and propagated by Dispatch." So the project-side primary source ties Calliope to OpenLaws here, not Klatch. Three possibilities: (a) Calliope works across both projects and you're framing this as the Klatch instance; (b) the omnibus log got the project-tag wrong; (c) "primary assistant on Klatch" should be "primary assistant on OpenLaws" or "primary assistant across the siblings" for the post. As written, this would contradict the repo's own log if a reader cross-referenced. Want me to (i) keep "Klatch" with a footnote/sentence acknowledging Calliope works across both, (ii) swap to "OpenLaws," or (iii) rephrase as project-agnostic ("my primary assistant, Calliope")?]

The session-start protocol — *check the cross-pollination brief, count unread mail, verify branch status* — exists in some form in every sibling project, with variations. The Klatch version has different inboxes; the version for work emphasizes a different freshness-check; the Piper Morgan version handles role-specific session logs. The shape is recognizable. The instances are not identical.
[SOURCE NEEDED for PM: Piper Morgan side is verifiable — CLAUDE.md §"Session Start Protocol" + SessionStart Hook + role-specific session-log convention are all in repo. Klatch + OpenLaws specifics ("different inboxes," "different freshness-check") aren't sourceable from this repo. Sibling-project memory or your direct knowledge. Stay general ("with variations") and drop the specifics, or supply the sibling-project details?]

The handoff-memo template I use when a Chat-based agent role migrates to Code came out of a five-section structure my head-of-sapient-relations agent (HOST) drafted back in March. By the time HOST and chief innovation officer (CIO) roles had both used it, two parallel projects had picked up similar templates, with their own modifications: Klatch added a "what I'd tell my successor that I wouldn't tell the PM" section (omg, I love this so much). For work, a more no-nonsense context, we collapsed the relationship section into the lessons one.
[FACT-CHECK NOTE for PM: Corrections from `knowledge/handoff-notes-template-v1.md`: (a) template has **five** sections, not six — (1) What Changed, (2) What's Pending, (3) What Surprised You, (4) What Your Successor Should Know, (5) Briefing Update Candidates; (b) attribution: filename header says "HOSR" — possibly the earlier name for what's now HOST? Unified to "HOST" in body, but flag if HOSR/HOST is a distinction you want to preserve; (c) filed **March 13, 2026**, so "back in March" is more accurate than "a month ago" (it's been about two months). Also corrected "Chief of Staff" → HOST (the actual template author per the file), since the Chief of Staff role is exec, not HOST. Also fixed typos: "roless" → "roles", "conetxt" → "context".]
[SOURCE NEEDED for PM: The HOST-and-CIO both-used-it claim — I couldn't trace specific HOST or CIO session logs / memos applying this exact template. Want me to dig further for handoff-memo applications, or rely on your memory of when each used it?]
[SOURCE NEEDED for PM: Klatch's "what I'd tell my successor that I wouldn't tell the PM" section and the work-project collapse of relationship-into-lessons — both are sibling-project changes not recorded in this repo's cross-pollination briefs. PM-memory or sibling-side evidence. Keep, or rephrase as illustrative-without-specifics?]

# What doesn't get leaked

It's worth noticing, equally, what hasn't crossed.

The actual project work doesn't cross. Klatch's entity model isn't being imported into Piper Morgan, OpenLaws's business info isn't getting shared at all. The domain interiors of the projects are sovereign — each one is solving its own problem, with its own data shapes, its own product surface, its own users, it's own posture in terms of private, confidential, public, open, and so on.

Specific tooling decisions also stay local. The choice to use one LLM provider over another, the particular vector store, the test-runner configuration, the CI provider — those propagate when there's a clean reason to copy them, but mostly they don't, because mostly they're shaped by constraints unique to each project. Piper Morgan's Postgres-plus-ChromaDB setup wouldn't make sense for Calliope's read-mostly authority graph; Calliope's ingestion pipeline wouldn't make sense for Piper Morgan's mostly-conversational workflow.
[FACT-CHECK NOTE for PM: Original "Postgres-plus-pgvector" is off. `docker-compose.yml` confirms Postgres 15 + **ChromaDB** as the vector store, not pgvector (which is a Postgres extension). Corrected to "Postgres-plus-ChromaDB."]
[SOURCE NEEDED for PM: "Calliope's read-mostly authority graph" / "Calliope's ingestion pipeline" — this couples to the earlier Calliope attribution question. "Read-mostly authority graph" reads as an OpenLaws / citation-domain shape; if Calliope is OpenLaws (per the April 18 omnibus), this is internally consistent. If Calliope is Klatch (your earlier framing), the tech-shape doesn't match what Klatch is for. Whichever way the earlier Calliope attribution resolves, this paragraph should match.]

Vocabulary sometimes gets imported and then has to be retracted. A few weeks ago one of my agents read a Klatch session log, picked up a phrase about how requests "passed through" a particular layer, and was about to reframe a Piper Morgan narrative around the same phrase. PA caught it before the reframe shipped. *The phrase was Klatch's; the underlying mechanism it was describing didn't exist in Piper Morgan.* The vocabulary was being imported as if it carried its mechanism with it. Vocabulary doesn't always; sometimes it's just the local name for a local thing.
[VERIFIED for PM: The PA-catching-a-Klatch-vocabulary-import incident is sourced in the April 16 omnibus log: "PA corrects PPM memo after PM feedback — 'Klatch Step 10 = BYOC' was a vocabulary import error, not a genuine mechanism map; retracted two reframes, kept only 'backend has rich data' diagnostic." The "passed through" phrasing in the post is a paraphrase / generalization of that incident rather than a direct quote — if you want, I can swap the paraphrase for the actual phrase ("Klatch Step 10 = BYOC"), but the paraphrase reads better and the underlying incident is real.]

So what *travels* is something narrower than "any practice from any sibling." It's specifically the artifacts whose shape is general enough to make sense in another context, while their content is local enough to be filled in differently each time.

# Why "family resemblance" is the right phrase

The reason I keep reaching for Wittgenstein's *family resemblance* — the idea that members of a category share overlapping subsets of features rather than one defining trait — is that no single feature is shared across all sibling projects.

Some siblings share the cross-pollination brief mechanism. Not all of them.

Some share the handoff memo template. Not all.

Some share session-start hooks. Not all.

Some share the DECISIONS.md file shape. Not all.

What unifies the family isn't one common feature. It's the *texture of overlap.* Project A and Project B share a brief mechanism; A and C share session-start hooks; B and C share decision logs. Each sibling resembles every other sibling along some axes and diverges along others. The family is recognizable, but if you tried to write down the single defining trait, you'd come up empty.

This matters because the alternative — *let's pick one standard, document it, mandate it across siblings* — is the thing every cross-team coordination effort tries first, and the thing that almost always produces either drift (the standard is honored in name and abandoned in practice) or rigidity (the standard prevents legitimate local variation). Family resemblance is what you get instead, when you let practices propagate through documentation and observation rather than through enforcement.

[ADD PERSONAL ANECDOTE: a moment from observing one of these transfers — maybe the cross-pollination brief surfacing a sibling's pattern, or the small surprise of recognizing a cousin's file structure inside your own project. The texture of noticing the resemblance.]

# What this enables

The thing the family resemblance enables, that a single standard couldn't, is *fast adoption with retained sovereignty.* When DECISIONS.md showed up in the brief, I could adopt it without negotiating its shape. When the SSH-over-443 workaround arrived, I could drop it into my CLAUDE.md without checking whether some governing body had blessed it. When my handoff-memo template traveled to Klatch, the Klatch team could modify it — adding the "what I'd tell my successor" section — without asking permission, because there was no permission to ask.
[SOURCE NEEDED for PM: "When my handoff-memo template traveled to Klatch" — same status as the earlier Klatch-modifications claim. Not traceable in this repo's cross-pollination briefs. Sibling-project evidence or your direct knowledge. Want me to dig further if you have a brief entry I missed, or accept as PM-memory and let it ride?]

That's a different shape of cross-project coordination than I'd seen before. It's not a federation. It's not a standards body. It's not even a community of practice in the formal sense. It's a small, opinionated set of projects with overlapping tooling and shared infrastructure, where good ideas show up in one and are visible enough that they can spread to the others, and where the spread doesn't require the projects to agree on anything beyond *this particular shape, in this particular instance, makes sense for me too.*

I don't know yet whether this scales. Three or four sibling projects under common stewardship is one thing. Thirty might be another. But for now, the family resemblance pattern is doing real work, and the work it's doing wouldn't survive a more formal arrangement.

The next step, where the resemblance hardens into common infrastructure rather than parallel artifacts, is the topic of another piece in this pair.

---

*Next on Building Piper Morgan: From Protocol to Infrastructure — what happens when a shared practice stops being negotiated and becomes the environment.*

*Where in your work do you see family resemblances rather than shared standards? When does that shape produce better coordination than a formal standard would have?*
