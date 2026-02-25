# Piper Morgan PR/FAQ (Working Backwards)

**Purpose**: Customer-centric product narrative in the [Amazon Working Backwards](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/) format. Use this to align stakeholders on what Piper Morgan is, for whom, and why—before building.  
**Audience**: Stakeholders, PMs, execs, investors.  
**Companion**: [Piper Morgan by Analogy](piper-morgan-by-analogy.md), [UX Foundations](mux/piper-morgan-ux-foundations-and-open-questions.md), [PROJECT.md](../../briefing/PROJECT.md)

---

## Press Release

**Headline**: Piper Morgan Enables Product Managers to Work With an AI Colleague That Understands Context, Articulates the "Why," and Learns Their Style

**Subtitle**: A product management assistant that appears where you already work—Slack, email, IDE, calendar—and helps clarify roadmap, MVP scope, and rationale instead of adding another tool to open.

**Date**: [Launch / milestone date TBD]

**Intro**

Piper Morgan is an AI-powered product management colleague that transforms how PMs work. Unlike tools you go to and operate (dashboards, forms, boards), Piper inhabits your existing workspace and shows up where you are—in Slack, over email, in your IDE, or around standups. Piper helps articulate the "why" behind work, shape roadmaps, and clarify what’s in or out of an MVP, while federating to the tools you already use (GitHub, Notion, Jira, calendar) for execution and tracking. Piper learns your preferences and style over time and acts as a thought partner, not a form to fill out.

**Problem**

Product managers today are stuck between two realities. On one side, execution tools (Jira, Linear, Asana) are excellent at storing issues, sprints, and status—but they don’t help articulate the rationale, strategy, or narrative behind the work. They represent the *output* of product management, not the thinking that produces it. On the other side, PMs are scattered across many surfaces: Slack for coordination, Notion or Confluence for docs, GitHub for engineering, calendar for meetings. No single place helps them clarify *why* we’re building this, *what* the roadmap looks like, or *what’s in the MVP* versus what’s not—even though those questions are central to good product work. The result is context-switching, lost "why," and decisions that land in tickets without a shared story.

**Solution**

Piper Morgan is designed as a **colleague**, not a tool. You don’t "go to Piper" as another app; Piper participates in the channels and contexts you already use. Piper helps with the upstream product work that tools like Jira don’t: articulating the "why," shaping a coherent roadmap, and clarifying MVP scope. When it’s time to execute, Piper federates to your existing systems—GitHub, Notion, Slack, calendar—so work and status live where they already do. Piper uses spatial and contextual intelligence to understand hierarchy, time, priority, and flow across your work, and learns your preferences (e.g., standup format, focus areas) so interactions stay relevant and low-friction. The goal is to make product thinking visible and shared without adding another destination to your day.

**Company leader quote**

*"We’re building Piper because product management is too important to be trapped inside forms and dashboards. PMs need a partner that helps them think clearly about the why and the what, and that shows up where they already are—not another tool they have to remember to open."*

**How the product works**

A PM might ask Piper, in Slack or in the web UI, to help clarify the rationale for an initiative, summarize what’s in scope for the next release, or draft a standup that respects their preferred format and focus (e.g., GitHub, todos, Notion). Piper uses intent classification to understand the request, draws on connected integrations (GitHub issues, Notion pages, calendar) for context, and responds in natural language. Over time, Piper learns preferences—brief vs. detailed standups, which integrations matter most—and applies them automatically. For execution, Piper can create or update work in GitHub, Notion, or other backends, so the "atoms" of work (issues, tasks) stay in the systems the team already uses. Piper does not replace those systems; Piper sits upstream of them as a thinking and alignment layer.

**Customer quote**

*"I used to keep the ‘why’ in my head or in a doc nobody opened. Now I can ask Piper to help me articulate it and share it with the team. And when I need a standup or a scope summary, Piper already knows how I like it and what I care about. It feels like having a PM partner who actually knows my context."* — Product manager, early alpha user (persona)

**How to get started**

Alpha users can sign up and connect GitHub, Notion, Slack, and calendar via the Piper web app. Once connected, you can talk to Piper in the web UI or in Slack (where configured). Setup and onboarding are documented at [ALPHA_QUICKSTART](../../ALPHA_QUICKSTART.md) and [getting started](../../public/getting-started/README.md).

---

## Frequently Asked Questions

**Q: What is Piper Morgan?**  
A: Piper Morgan is an AI-powered product management assistant designed as a **colleague**, not a tool. Piper helps PMs articulate the "why," shape roadmaps, and clarify MVP scope, and appears where you already work (Slack, web, future: email, IDE). Piper federates to GitHub, Notion, Jira, calendar, etc., for execution—so Piper is the thinking and alignment layer *upstream* of your existing tools.

**Q: How is Piper different from Jira (or Linear, Asana)?**  
A: Jira and similar tools are great at managing the *atoms* of work: issues, sprints, status. They are the *output* of product management. Piper focuses on the *upstream* work: articulating the "why," roadmap narrative, and MVP scope. Piper is not a Jira replacement; Piper can use Jira (or GitHub, Linear) as a backend. See [Piper Morgan by Analogy](piper-morgan-by-analogy.md).

**Q: Do I have to "go to" Piper to use it?**  
A: No. Piper is designed to show up where you are (Radar O’Reilly pattern): Slack, web app, and in the future email, IDE, meetings. Piper is not a destination you remember to open; Piper participates in the channels you already use.

**Q: What integrations does Piper support?**  
A: Currently: GitHub, Notion, Slack, Google Calendar (and compatible calendar providers). Additional backends (e.g., Jira, Linear) are in scope; the architecture supports swappable integrations. See [integrations](../../integrations/README.md) and [pattern-040 Integration Swappability](../architecture/current/patterns/pattern-040-integration-swappability-guide.md).

**Q: How does Piper use my data?**  
A: Piper uses your connected integrations (e.g., GitHub, Notion) to provide context for conversations and to perform actions you request (e.g., create an issue). Data is used to serve you and is not used to train public models. See security and privacy documentation for your deployment.

**Q: Can Piper replace my PM tools?**  
A: Piper is not a replacement for Jira, Notion, or GitHub. Piper is a layer *on top* of them: Piper helps with reasoning, "why," roadmap, and MVP clarity, and federates to your tools for the actual work items and status. You keep using the tools your team already uses.

**Q: How do I run a PR/FAQ or Working Backwards review for Piper?**  
A: Use this document in a "narrative" meeting: stakeholders read the PR and FAQ silently (e.g., 20 minutes), then discuss. The goal is to align on what we’re building and for whom, and to pressure-test assumptions before committing. See [Working Backwards – Amazon PR/FAQ](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/).

---

## Where this document lives

- **Location**: `docs/internal/design/piper-morgan-prfaq.md`
- **Rationale**: Product/design strategy; sits alongside [Piper Morgan by Analogy](piper-morgan-by-analogy.md) and UX strategy in `internal/design`. For planning-specific navigation, link from `docs/NAVIGATION.md` (PM section) or `docs/briefing/` as needed.
- **Review**: Update the PR (headline, date, quotes, "how it works") when the product narrative or launch plan changes. Update FAQs when stakeholders repeatedly ask the same questions.
