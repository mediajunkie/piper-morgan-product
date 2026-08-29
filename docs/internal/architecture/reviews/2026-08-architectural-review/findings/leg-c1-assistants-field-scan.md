# Leg C1 — Personal AI Assistants Field Scan (fully blind researcher)

*Filed verbatim 2026-08-29. Researcher had NO knowledge of Piper Morgan — pure outside view, per
Exec's vocabulary-blind refinement. Citations are URLs; researcher flagged vendor-listicle bias
explicitly and used independent anchors (Wikipedia, TechCrunch, a16z, security researchers, arXiv).*

---

## Headline findings (Arch's filing note — the report's own words below)

- **Winners' minimal spine (5 pieces)**: conversation loop on channels users already have (no custom
  UI) · tool calling against a small set of real accounts (email/calendar first) · plain-text memory
  files as source of truth (both AutoGPT and OpenClaw converged here, one by painful removal) · a
  dumb scheduler driving one proactive surface (the daily brief) · a swappable frontier model via API.
- **The retention moat is accumulated memory** ("context compounding") — 68% ChatGPT paid retention
  at month 12; only 9% of consumers pay for more than one assistant. The sticky jobs are mundane:
  inbox triage, scheduling, meeting prep, daily brief. Lindy charges $49.99–$199.99/mo for exactly
  that after abandoning its agent-builder platform.
- **OpenClaw** (Steinberger): WhatsApp piped to Claude Code built in ~1 hour, weekend hack →
  ~300K users / ~247K+ GitHub stars in under three months, zero funding. Explicitly declined: vector
  DB as source of truth, custom UI, orchestration framework, multi-agent management plane. Memory =
  Markdown files on disk with a disposable SQLite index over them.
- **The dominant cause of death is overbuild, not underbuild.** Four failure shapes, each with
  multiple bodies: hardware-before-habit (Humane $230M/<10K units; Rabbit R1 mass returns;
  Limitless→Meta acquihire/product death) · autonomy-before-reliability (AutoGPT v1 "infinite loops
  and runaway API bills"; OpenAI Operator 38.1% OSWorld, retired to supervised mode) ·
  model/companion-before-wedge (Inflection Pi: $4B valuation, no job-to-be-done, reverse-acquihired)
  · hosted-infrastructure-before-economic-engine (Khoj Cloud sunset April 2026).
- **The success case's own bill**: OpenClaw's minimalism externalized security — 42K–180K
  internet-exposed instances (counts disagree by methodology), auth-bypass conditions in 93.4% of a
  verified sample, malicious skill-marketplace exfiltration, 4 CVEs. The one thing minimal spines
  chronically skip and must not: secure defaults at the network boundary from day one.
- **Field's one-sentence verdict** (researcher's closing): "the assistant is a loop, a mailbox, a
  text file, and an alarm clock — everything else is either the moat (memory) or the overbuild
  (everything else)."
- **Most common category error**: building the *platform* for assistants instead of *an assistant* —
  orchestration framework, agent marketplace, custom device, multi-agent architecture, autonomy
  engine. Every major failure is a variant of shipping generalized capability before proving one
  daily habit; both biggest successes collapsed a general platform into one assistant doing boring
  jobs proactively.

## Key products surveyed (with the report's caveats)

**Open/self-hosted**: OpenClaw (dominant; governance now a Foundation, Steinberger joined OpenAI
Feb 2026), Khoj (~35K stars; hosted cloud sunset 2026-04-15, self-host-only now), Vellum Assistant
(real but self-ranked #1 in own marketing), AutoGPT (pivoted from autonomy to workflow builder).
**Commercial**: ChatGPT (agent mode absorbed Operator; Pulse proactive briefs), Gemini (+300% YoY
Pro), Claude (+200% YoY paid US), Lindy (pivoted Feb 2026 from builder platform to pre-assembled
EA), Martin (SMS/WhatsApp EA, "drafts rather than acts" per reviewers), Alexa+ (GA Feb 2026 after
year-long throttled ramp, Amazon itself called the tech "primitive" mid-rollout).

## Per-section "proves possible / proves unnecessary" pairs (verbatim)

1. Leaders: possible = solo dev's self-hosted assistant reaching 300K users in <3 months competing
   with billion-dollar incumbents; unnecessary = venture funding, proprietary model, custom
   hardware, dedicated app UI.
2. Spine: possible = competitive assistant fits in one process and one directory; unnecessary =
   vector DBs as primary memory, custom chat UIs, orchestration frameworks, multi-agent
   architectures — "every one of these was built and then removed or declined by the category's most
   successful projects."
3. Speed: possible = first-user in one hour riding existing channels + existing agent runtime;
   unnecessary = stealth periods, hardware, platform-first phases — "every extra month between
   prototype and first user in this dataset correlated with worse outcomes."
4. Failures: possible = dying with $230M in the bank while a $0 weekend hack wins your market;
   unnecessary = custom devices, autonomous multi-step ambition, build-the-platform-first. NOT
   unnecessary: security-by-default at the network boundary.
5. Retention: possible = charging $50–200/mo for email+calendar+morning-brief done proactively with
   memory; unnecessary = breadth — "the paying user keeps one assistant, for a handful of boring
   jobs, because switching means abandoning accumulated context."

## Source-quality note (researcher's own)

Vendor listicles (alfred_, Vellum, Saner.AI, Carly) all rank themselves first — treated as
marketing. Independent anchors: Wikipedia (OpenClaw), TechCrunch (Alexa+ rollout), a16z consumer-AI
reports (retention/consolidation data), Securonix/Hive Security/CSA/arXiv (OpenClaw security),
MMNTM (AutoGPT retrospective), digitalapplied/Layer3Labs (hardware postmortems). Star-count and
exposed-instance figures disagree across sources; the report flags each disagreement rather than
picking a number. Field disagreement flagged: vendor claims specialized EAs retain better vs. a16z
data showing consolidation onto ONE general assistant — no published cohort data resolves it.
