# Leg C3 — AI PM-Copilot Category Scan (vocabulary-blind researcher)

*Filed verbatim-condensed 2026-08-29. Researcher had no project context. Source-typing used:
vendor docs vs. practitioner reports vs. aggregators, flagged throughout; self-reported user counts
marked as marketing claims.*

## Category map

**Standalone independents**: ChatPRD (flagship — "AI CPO" anchored on PRD/doc generation; claims
100k+ PMs, bootstrapped, founder + "nine AI employees," $15–29/seat) · Squad AI (strategy layer;
self-reported claims, comparison pages explicitly written to game LLM categorization) ·
BuildBetter.ai (~$770K ARR est.) · Spinach AI (standup agent, YC/Zoom/Atlassian-backed) · Enterpret
($25M raised; Canva/Notion/Linear customers; the strongest surviving feedback-lane independent).

**Suite incumbents**: Productboard Spark (dedicated PM agent; entire pricing rebuilt around it) ·
Atlassian Rovo/Agents-in-Jira (GA Feb 2026; bought Cycle.app for feedback in JPD) · Linear (opposite
tack: became the VENUE where agents work — agents as first-class assignable users; by Jul 2026
triage rules delegate issues to agents with no human) · Notion 3.0/3.3 agents (20-min unsupervised
runs; custom agents on schedules) · airfocus-by-Lucid (relaunched around "bidirectional MCP") ·
Amplitude (absorbed Kraftful) · Reforge (absorbed Monterey AI).

**Open-source**: nothing venture-shaped — OSS energy went to *skills/prompts for general agents*
(PM frameworks packaged for Claude Code/Codex), not standalone apps. "Mirrors the coding-agent
world circa 2024: OSS value concentrates in methodology-as-context."

## The irreducible core — five anchors, different fates

| Anchor | Who | Outcome |
|---|---|---|
| PRD/document generation | ChatPRD, Squad | Best traction-per-dollar; 100k users on document-writing alone |
| Feedback triage / VoC | Kraftful, Cycle, Monterey, Zeda, Enterpret | **Bloodbath: 4 of 5 dead as standalones in 18 months**; only enterprise-scale Enterpret survives |
| Roadmap/strategy synthesis | Squad, airfocus | No standalone winner |
| Meeting/standup synthesis | Spinach, BuildBetter | Viable niche, modest scale, constantly compressed by general note-takers |
| Whole-PM-job suite agent | Spark, Rovo, Notion | The incumbent play — anchored on OWNING THE CONTEXT, not one JTBD |

**The correlation (verbatim)**: traction accrues to anchors where the output is a *durable artifact
the PM is judged on* (PRD, spec, ticket) rather than an *intermediate synthesis* (feedback themes).
Feedback triage was the most-funded anchor and the most-dead one — it produces input to judgment,
not the judgment artifact, so it was absorbable as a feature by whoever owns the analytics or
ticketing system. Document generation survived independently because the artifact is portable
across whatever stack the PM's company runs.

## Integration surface: native APIs → MCP, visibly, in one year

- Atlassian remote MCP server: beta May 2025 (Claude first partner), GA Feb 2026 (OAuth 2.1,
  Jira/Confluence/Compass read-write to Claude/ChatGPT/Cursor/VS Code).
- **ChatPRD consumes Linear and Atlassian via THEIR MCP servers** rather than maintaining its own
  API clients; Atlassian admins may need to allowlist ChatPRD's domain — governance of third-party
  AI access has moved to the platform side.
- Productboard Spark: MCP connectors for Slack/Linear/Amplitude/Notion + custom, while its legacy
  Jira integration stays classic field-mapped sync — old and new models coexist in one product.
- **The pattern**: every serious player does BOTH directions — publishes an MCP server and consumes
  others'. Bespoke point-to-point survives mainly for deep field-mapped sync. "The maintenance
  burden of connectors shifted from the copilot vendor to the system-of-record vendor — which is
  precisely why being a copilot with no system of record got structurally cheaper to be, and
  simultaneously less defensible."

## Trust stack — now a checklist, not a differentiator

1. Act-as-user permission inheritance (Rovo agents can't touch what the invoking human can't; newer
   Agent Accounts give scoped agent identity).
2. Per-tool-call audit logging, org-queryable.
3. **Tiered HITL gates, not blanket confirmation** — auto for reversible low-stakes, human gate for
   irreversible; preview/zero-writes modes. "The market rejected both extremes."
4. Normative conduct rules (Linear's Agent Interaction Guidelines: agents disclose they're agents,
   show state, stop immediately when told; "final responsibility always remains with a human").
5. Bounded autonomy windows (Notion's ~20-min cap) — time-boxing as a trust primitive.
6. Positioning retreat from autonomy: the suite with the most data (Spark) chose ASSISTIVE framing
   for judgment work ("humans are in charge… guiding you").

**The autonomy frontier as shipped**: the ONE fully-autonomous PM action that shipped and stuck is
Linear triage-rule delegation — routing, the most reversible, lowest-judgment action. Nobody ships
autonomous stakeholder messaging.

## Failure pattern

Casualties 2025–26 are almost entirely **feedback-triage standalones**: Kraftful (→Amplitude, shut
Aug 2025), Cycle.app (→Atlassian, sunset Oct 2025), Monterey (→Reforge), Zeda.io
(probable-but-unconfirmed wind-down; only detailed source is a competitor's blog — flagged),
airfocus (capitulation-to-consolidation sale). Context: one tracker counts 285 AI tools shut down
or acquired by Aug 2026 — "vertical AI absorbed by enterprise platforms."

**The structural position that dies (verbatim)**: every casualty sat BETWEEN the data sources and
the system of record, doing synthesis that (a) LLM commoditization made cheap and (b) the
system-of-record owner could replicate natively with better data access. Survivors are at the two
poles: artifact generators with no data dependency (ChatPRD) and enterprise-depth data platforms
(Enterpret).

## Closing synthesis (verbatim key lines)

Must nail: (1) **anchor on the judgment artifact, not the input stream**; (2) ride the MCP rails in
both directions; (3) the trust stack is the price of entry (act-as-user, audit, tiered gates,
self-disclosure, instant stop); (4) respect the autonomy frontier where it actually is — judgment
work ships human-led everywhere, including at the incumbent with the most data.

Most commonly overbuilt: feedback-ingestion pipelines (most-funded, most-dead) · integration
breadth ("100+ integrations" was a 2024 moat; MCP made it a weekend) · full autonomy (no evidence
of demand; market rewarded calibrated gates, punished nothing for lacking autonomy) · **a
destination UI** ("the standalone hub-you-visit is the structurally doomed shape" — winners live
inside the system of record or produce portable artifacts consumed elsewhere).

One line: **"own the artifact or own the record system — everything in between is acquisition
inventory, and trust plumbing plus MCP connectivity are the price of entry, not the product."**
