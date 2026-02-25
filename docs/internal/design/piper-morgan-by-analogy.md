# Piper Morgan by Analogy: Similar to and Different from Jira

**Purpose**: Clarify how Piper Morgan relates to tools like Jira—same domain, different paradigm.  
**Audience**: Stakeholders, architects, PMs.  
**Companion**: [UX Foundations and Open Questions](mux/piper-morgan-ux-foundations-and-open-questions.md), [ADR-000 Meta-Platform](../architecture/current/adrs/adr-000-meta-platform.md)

---

## Same Domain

Piper Morgan and Jira (and Linear, Asana, etc.) all support **product and work management**:

- **Work items**: Issues, tasks, stories, epics
- **Projects and structure**: Backlogs, sprints, roadmaps
- **Status and flow**: Backlog → In Progress → Review → Done
- **Priority and assignment**: Who, when, how important
- **Integrations**: GitHub, Slack, calendar, docs (Piper federates; Jira has plugins)

So **by domain**, Piper is "like" Jira: both help PMs and teams manage work.

---

## Different Paradigm: Colleague vs Tool

**Jira (and similar)**: A **tool** you go to. You open Jira, fill forms, run reports, manage boards. The tool is the destination; you operate it.

**Piper Morgan**: A **colleague** who inhabits your workspace. You don’t "go to Piper" as the only way to get PM work done; Piper shows up where you already are (Slack, email, IDE, meeting) and helps. You collaborate with Piper; you don’t "use" Piper like a form.

From [UX Foundations](mux/piper-morgan-ux-foundations-and-open-questions.md):

- Piper is **not a destination** ("go to Piper to do PM work")
- Piper is **not a form to fill out** ("input your requirements here")
- Piper is **not a report generator** ("here's your dashboard")
- Piper is **not a command interface** ("type /standup to begin")

Jira is all of those: destination, forms, dashboards, and (in some setups) slash commands. Piper is the opposite by design.

---

## What Jira Is and Isn’t

Jira is a **great** tool to manage some of the *atoms* of Product Management—issues, sprints, backlogs, status. But it is really a tool to **manage software development**, not to **develop** Product Management itself. Jira represents the **output** and **instantiation** of a Product Management process; it is where decisions land, not where "why" and roadmap and scope get clarified.

**Jira is not particularly good at:**

- **Articulating the "why"** — the rationale, strategy, and narrative behind the work
- **Articulating a roadmap** — coherent narrative over time (it can *store* one; it doesn’t *clarify* it)
- **Clarifying or determining what is in the MVP and what is not** — though it is a **repository for the answer** once someone has decided

**Jira (by itself) doesn’t facilitate:**

- **Demo / mock-up** — though it could manage the *development* of them (tickets, assignments, status)

**Jira is not a design-decision-discussion repository** — something like Atlassian Confluence might fill that role. *(Nor perhaps is Piper Morgan; we aim for "why," roadmap, and MVP clarity, but design-decision-discussion is a distinct capability we don’t claim by default.)*

This framing helps: Piper aims to sit *upstream* of where Jira shines—helping articulate why, shape roadmap, and clarify MVP—while federating to Jira (or GitHub, Linear) for the atoms of work and execution.

---

## How Piper Is "Better" (Where We Aim to Differentiate)

| Aspect | Jira (typical) | Piper Morgan |
|--------|-----------------|--------------|
| **Interaction** | Go to app; forms and boards | Conversational; natural language; appears where you are (Radar O'Reilly pattern) |
| **Context** | You bring context (clicks, filters) | Spatial intelligence: 8 dimensions (hierarchy, temporal, priority, flow, etc.); federated view across tools |
| **Intelligence** | Rules, automation, reports | LLM + orchestration: understands intent, suggests, summarizes, learns from feedback (composting) |
| **Place** | One app (or many separate tools) | Inhabits your existing places (Slack, web, CLI); can federate GitHub, Notion, calendar, future Jira/Linear |
| **Trust** | Tool reliability | Colleague metaphor: trust gradient (apprentice → associate → PM); systematic kindness; ethics as infrastructure |

So Piper is "better" **where** we want: less "operate a tool," more "work with a colleague who knows your work and your tools."

---

## Where the Analogy Helps

- **"What is Piper?"** → Same *domain* as Jira (work and product management), different *paradigm* (colleague, not tool).
- **"Why not just use Jira?"** → Jira is where work is *stored* and *tracked*; Piper is who you *talk to* to create, prioritize, and understand that work across Jira, GitHub, Slack, etc.
- **"Is Piper a Jira replacement?"** → No. Piper can *use* Jira (or GitHub, Linear) as a backend. Piper is the conversational, spatial, and learning layer *above* issue trackers and project tools.

---

## References

- **Colleague metaphor, Radar, what Piper is not**: [UX Foundations and Open Questions](mux/piper-morgan-ux-foundations-and-open-questions.md)
- **Meta-platform (practitioner, demonstrator, enabler)**: [ADR-000 Meta-Platform](../architecture/current/adrs/adr-000-meta-platform.md)
- **Spatial intelligence and performance**: [Spatial Intelligence Competitive Advantage](../architecture/current/spatial-intelligence-competitive-advantage.md)
- **Integration swappability (e.g. GitHub vs Jira backend)**: [Pattern-040 Integration Swappability](../architecture/current/patterns/pattern-040-integration-swappability-guide.md)
- **Learning and preferences (e.g. "Not Jira, Linear")**: [Composting & Learning Architecture](../architecture/current/composting-learning-architecture.md)
