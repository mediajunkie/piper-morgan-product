# CITATIONS.md

**Project**: Piper Morgan - AI-Powered Product Management Assistant
**Last Updated**: September 2, 2026 (Docs) — targeted review, not a full pass: verified the
"8-Dimensional Spatial Intelligence" claim is still live in code post the 2026-08-15 spatial
cold-island disposal (confirmed via `services/integrations/spatial/github_spatial.py`); fixed the
MCP section's platform list, which named Linear/CI/CD/GitBook — none of which are live MCP
integrations — instead of the actual current set (GitHub/Google Calendar/Notion/Slack); checked
orchestration-related citations against the codebase, none tied to the deleted
`services/orchestration/`/`methodology/coordination` packages, no changes needed. **Not checked
this pass**: whether recent architecture (MUX Object Model/ADR-055, Understanding-Layer Inversion,
the PDR-006 hosted-MCP distribution pivot) warrants new citations — that needs a real research
pass, not a mechanical check, flagged rather than guessed at. Prior: March 3, 2026.
**Purpose**: Comprehensive attribution of ideas, frameworks, and research that inform our work

> "We proudly acknowledge we build on the work of others while trying to contribute what we can to the common weal."

## Theoretical Foundations

### Embodied Cognition & Spatial Intelligence

**Radical Embodied Cognition**
- **Alva Noë** - "Action in Perception" (2004)
- **Francisco Varela, Eleanor Rosch, Evan Thompson** - "The Embodied Mind" (1991)
- **Andy Clark** - "Being There: Putting Brain, Body and World Together Again" (1997)
- **Mark Johnson** - "The Meaning of the Body" (2007)
- *Applied in: PM-068 Embodied Architecture, 8-dimensional spatial intelligence framework*

**Spatial Cognition in AI**
- **Barbara Tversky** - "Mind in Motion: How Action Shapes Thought" (2019)
- **Dedre Gentner** - Structure mapping and analogical reasoning research
- **Douglas Hofstadter** - "Fluid Concepts and Creative Analogies" (1995)
- *Used in: Spatial metaphors for Slack integration, workspace navigation*

**Geoffrey Hinton's Contributions**
- **Capsule Networks** - Spatial relationships in neural networks (2017)
- **Forward-Forward Algorithm** - Alternative to backpropagation (2022)
- **Early work on distributed representations** (1986)
- *Influenced: Spatial representation approaches in Piper's architecture*

**Knowledge Graph Extraction Challenges**
- **Yáñez Romero** - "Knowledge Graph Extraction Challenges" (Medium, January 2026)
- LLMs produce fragmented KGs: treat extraction as generation rather than classification
- Coreference problem ("Party A" vs "the aforementioned party" = separate nodes) maps to entity extraction challenges
- Asserted vs. augmented graph distinction maps to trust/provenance architecture
- Pipeline error propagation (90% × 90% = 81%) relevant to multi-stage learning pipeline design
- *Flagged for: Architect consideration when learning system reaches entity extraction stage*

**Attention Mechanisms**
- **Vaswani et al.** - "Attention Is All You Need" (2017) - Transformer architecture
- **Bahdanau et al.** - Neural machine translation with attention (2014)
- *Applied in: Attention model for Slack events, priority scoring algorithms*

---

## Proprietary Systems & Methodologies

### Pattern Sweep Process (Piper Morgan Original)
- Automated pattern detection across 10,000+ files
- Confidence scoring and categorization
- Integration with TLDR for test acceleration
- Self-improving methodology patterns
- *Enables: Compound learning acceleration*

### Systematic Verification Methodology (Piper Morgan Original)
- "Check first, implement second" principle
- Pattern examination before code writing
- Backward compatibility as primary constraint
- *Delivered: 100% first-implementation success rate*

---

### Agent Design & Orchestration

**Rahul Vir - "The Agentic PM's Guide: From an AI Partner to Autonomous Agents"** (2025)
- Agent Core Charter Definition framework
- Architecture Complexity Mapping (single vs. multi-agent decisions)
- API vs. GUI Interaction Model Selection
- Human-Centric Automation Matrix
- PM Lifecycle Integration patterns
- *Used in: Agent Charter v1.0, Multi-agent architecture decisions*

**Stanford HAI - 4-Axis Evaluation Model**
- Technical, Human-Centered, Temporal, and Contextual evaluation dimensions
- Comprehensive metrics beyond pure technical performance
- *Used in: Success metrics framework, validation methodology*

**Steve Yegge - Beads** (December 2025)
- Git-backed memory system for AI coding agents
- JSONL + SQLite architecture for persistent agent state
- Solves the "50 First Dates" problem (agents losing context across sessions)
- https://github.com/steveyegge/beads
- *Studied for: Agent memory architecture, inspired beads implementation*

**Steve Yegge - Gas Town** (January 2026)
- Multi-agent orchestration framework for parallel AI coding
- GUPP (Gas Town Universal Propulsion Principle): "If there is work on your hook, YOU MUST RUN IT"
- Throughput-first philosophy with durable Git-backed workflows
- https://github.com/steveyegge/gastown
- *Analyzed for: Multi-agent patterns; philosophy deliberately differs (quality over throughput)*

**Jesse Vincent - Agent Conflict Alert Pattern** (2025)
- Technique for LLMs to signal when they feel overly conflicted
- Suggested phrasing: "I think we're not in Kansas anymore, Dorothy"
- *Adapted as: Time Lord Alert pattern for quality-over-time-constraint signaling*

**Jesse Vincent - Engineering Notebook** (Prime Radiant, February 2026)
- Automated ingestion of Claude Code JSONL transcripts → LLM summarization → browsable views (journal, project, calendar)
- Convergent evolution with Piper's omnibus log system — same underlying problem (agentic work generates too much output for humans to track)
- Our system ahead on cross-agent coordination and strategic decisions; his ahead on automation and open-source availability
- *Analyzed for: Omnibus system automation potential, lower-layer transcript ingestion supplement*

**Ethan Mollick - Spans of Control in Multi-Agent Systems** (One Useful Thing / Substack, February 2026)
- Boundary objects, coupling tradeoffs, and middle management agents in AI orchestration
- Validates empirical discoveries in Piper's multi-agent coordination patterns
- *Referenced in: CIO innovation analysis (Feb 16, 2026); methodology-product convergence discussion*

### Prompting & Efficiency Techniques

**Chain-of-Draft (CoD) Prompting**
- Linhui Ye, Chong Wang, et al. "Chain of Draft: Thinking Faster by Writing Less" (arXiv:2502.18600v1, February 2025)
- 5-word maximum reasoning steps
- 68-92% token reduction techniques
- *Used in: Inter-agent communication patterns, token optimization strategy*

**Chain-of-Thought (CoT) Prompting**
- Wei et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022)
- Foundation for reasoning approaches
- *Referenced in: CoD comparison baseline*

**Tree-of-Thoughts (ToT)**
- Yao et al. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" (2023)
- Exploration of solution spaces with backtracking
- *Considered for: Complex decision-making patterns*

**Skeleton-of-Thought (SoT)**
- Ning et al. "Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation" (2023)
- Parallel processing patterns
- *Applied in: Multi-agent parallel execution strategies*

---

## Architectural Patterns

### Model Context Protocol (MCP)
**Anthropic** (2024-2025)
- Standardized JSON-RPC 2.0 communication
- Tool federation patterns
- Resource discovery and management
- *Used in: connector integration (GitHub, Google Calendar, Notion, Slack — `services/mcp/consumer/`);
  corrected 2026-09-02, the prior platform list (Linear, CI/CD, GitBook) no longer matched the
  live integrations*

### Domain-Driven Design (DDD)
**Eric Evans** - "Domain-Driven Design: Tackling Complexity in the Heart of Software" (2003)
- Ubiquitous language
- Bounded contexts
- Repository pattern
- *Used in: Service architecture, domain modeling*

### Test-Driven Development (TDD)
**Kent Beck** - "Test-Driven Development: By Example" (2002)
- Red-Green-Refactor cycle
- Test-first methodology
- *Used in: Development methodology, quality assurance*

---

## Multi-Agent Systems Research

**Anthropic - Multi-Agent Research System** (2024)
- Lead agent with specialized subagents pattern
- Token economics in multi-agent systems
- 90.2% performance improvements over single-agent
- *Referenced in: Multi-agent orchestration patterns*

**Microsoft - Magentic-One** (2024)
- Orchestrator with specialized agents (WebSurfer, FileSurfer, Coder, ComputerTerminal)
- Task decomposition strategies
- *Studied for: Agent specialization patterns*

**LangChain - LangGraph** (2023-2024)
- Graph-based agent orchestration
- State management in multi-agent systems
- *Evaluated for: Orchestration architecture options*

---

## Evaluation & Verification

**Wild Claim Verification Protocol** (Piper Morgan Original, August 2025)
- Mathematical proof requirements for >100x claims
- Empirical validation methodology
- Distinguishing test vs. production metrics
- *Created in response to: Pattern analysis discoveries*

**Token-Budget-Aware LLM Reasoning (TALE)**
- Zhang et al. "Token-Budget-Aware LLM Reasoning" (arXiv:2412.18547v1, 2024)
- Dynamic budget estimation
- Token elasticity concepts
- *Informed: Token budget management strategies*

---

## Methodology & Process

**Excellence Flywheel** (Piper Morgan Original, 2025)
- Systematic Verification First
- Test-Driven Development
- Multi-Agent Coordination
- GitHub-First Tracking
- *Note: The "flywheel" metaphor originates with Jim Collins (see below); our specific framework is original*
- *Core methodology: All development work*

**Jim Collins - "Good to Great"** (2001)
- The Flywheel Effect: cumulative momentum from consistent effort
- "Good to great comes about by a cumulative process—step by step, action by action"
- The Doom Loop (anti-pattern): seeking single breakthrough moments
- *Origin of: Flywheel metaphor now widespread in business/product contexts*

**Architectural Decision Records (ADR)**
**Michael Nygard** - "Documenting Architecture Decisions" (2011)
- Lightweight architecture decision capture
- Context-Decision-Consequences format
- *Used in: All architectural documentation*

### Root Cause Analysis

**Five Whys** (Toyota Production System, 1950s)
- **Taiichi Ohno** - Iterative interrogative technique for root cause identification
- Ask "why" repeatedly (typically 5 times) to trace symptoms to root causes
- *Used in: Bug investigation methodology, Cascade Investigation pattern (Pattern-060)*

**Swiss Cheese Model**
- **James Reason** - "Human Error" (1990)
- Accident causation theory: failures occur when holes in multiple defense layers align
- *Applied as: Debugging methodology — "layers work, alignment fails"*

### Strategic Analysis

**Wardley Mapping**
- **Simon Wardley** - Strategic positioning through component evolution (2008-ongoing)
- Maps components across Genesis → Custom → Product → Commodity evolution
- *Used in: CXO strategic analysis, component positioning decisions*

**Jobs-to-be-Done Framework**
- **Clayton Christensen** - "Competing Against Luck" (2016)
- Understanding what "job" customers hire products to do
- *Applied in: Canonical query analysis, identifying feature gaps*

### Decision-Making Principles

**Chesterton's Fence**
- **G.K. Chesterton** - "The Thing" (1929)
- Principle: Don't remove something until you understand why it was put there
- *Applied in: Refactoring decisions, methodology reflection*

**Antifragile**
- **Nassim Nicholas Taleb** - "Antifragile: Things That Gain from Disorder" (2012)
- Systems that improve under stress rather than merely surviving
- *Influenced: Error handling philosophy, learning from failures*

### Reliability & Leadership

**High Reliability Organization (HRO) Principles**
- **Karl Weick & Kathleen Sutcliffe** - "Managing the Unexpected" (2007)
- Preoccupation with failure, reluctance to simplify, sensitivity to operations
- *Referenced in: Leadership patterns, executive coaching*

**Mission Command / Commander's Intent**
- Military doctrine for decentralized decision-making
- Clear objectives with freedom in execution
- *Applied in: Agent delegation patterns, leadership coaching*

**The Checklist Manifesto**
- **Atul Gawande** (2009)
- Distinguishing "do-confirm" vs. "read-do" checklists
- *Referenced alongside: HRO principles for procedural reliability*

---

## AI Safety & Alignment

**Constitutional AI**
**Anthropic** - Bai et al. "Constitutional AI: Harmlessness from AI Feedback" (2022)
- Principle-based AI training
- Self-critique and revision
- *Influenced: Ethical guidelines, human-in-loop protocols*

**Human-Compatible AI**
**Stuart Russell** - "Human Compatible: AI and the Problem of Control" (2019)
- Uncertainty about human preferences
- Beneficial AI principles
- *Informed: Human-centric automation philosophy*

---

## Software Engineering Practices

**Clean Architecture**
**Robert C. Martin** - "Clean Architecture: A Craftsman's Guide to Software Structure and Design" (2017)
- Dependency inversion
- Layer separation
- *Applied in: Service architecture*

**The Pragmatic Programmer**
**Andrew Hunt & David Thomas** (1999, 2019 20th Anniversary Edition)
- DRY principle
- Orthogonality
- Tracer bullet development
- *Influenced: Development practices*

---

## Product Management Domain

**Inspired: How to Create Tech Products Customers Love**
**Marty Cagan** (2008, 2017 Second Edition)
- Product discovery techniques
- Empowered product teams
- *Informed: PM domain modeling*

**The Lean Startup**
**Eric Ries** (2011)
- Build-Measure-Learn cycle
- Validated learning
- *Applied in: Iterative development approach*

**Radical Focus**
**Christina Wodtke** (2016, 2nd ed. 2021)
- OKRs (Objectives and Key Results) methodology
- Weekly commitment and celebration cadences
- One of four people who shaped modern OKRs (with Doerr, Grove, Drucker)
- *Referenced in: Goal-setting patterns, celebration practices*

---

## UX & Human-AI Interaction Research

### Frameworks & Practitioners

**Cindy Chastain - "Experience Themes"** (Boxes and Arrows, 2009)
- Using narrative themes from user research to guide UX design
- "An Experience Theme encapsulates the value and focus of the experience from users' point of view"
- Presented at IA Summit 2009
- https://boxesandarrows.com/experience-themes/
- *Applied in: Podcast preparation, leadership lessons framework*

**Dan Saffer** (CMU HCII)
- "Designing with AI" methodology
- Matchmaking AI capabilities to design problems
- *Referenced in: UX research reconnaissance (November 2025)*

**Greg Nudelman** (UXforAI.com)
- 35 AI projects documented with systematic practitioner patterns
- Most comprehensive practitioner pattern work in AI UX
- *Referenced in: UX research reconnaissance*

**Jakob Nielsen** (UX Tigers)
- "Articulation barrier" concept
- Insight: Prompt engineering is a UX failure, not a user failure
- *Influenced: Recognition interface design philosophy*

**Victor Dibia** (Microsoft AutoGen)
- Agent UX framework with four principles
- *Referenced in: Agent design research*

**Andrew Hinton**
- Context definition: "An agent's understanding of relationships between elements in their environment"
- *Crystallizing insight for: Architecture and context modeling*

### Academic Research

**Zhang et al.** - Trust Calibration Research
- Finding: Confidence scores help calibrate trust, but local explanations (feature importance) had no effect
- *Informed: Transparency and trust design decisions*

**Adam et al.** (2024) - System-Initiated Delegation
- Finding: When AI offers to take over (vs. user asking), users feel "self-threat" and resist more
- *Influenced: Proactive assistance design philosophy*

**IDEO Research** - AI Collaboration Study
- Finding: 56% more ideas with AI-generated questions, 28% decrease with AI-generated example ideas
- Key insight: "Questions scaffold; examples constrain"
- *Applied in: Conversational scaffolding approach*

---

## Standards & Specifications

**WCAG 2.1 / 2.2 Level AA** (W3C)
- Web Content Accessibility Guidelines
- Contrast requirements, ARIA labels, keyboard navigation
- *Compliance target for: MUX accessibility sprint*

**PEP 420** - Python Namespace Packages
- Implicit namespace package specification
- *Used to resolve: Shadow package conflicts in test infrastructure*

**NIST Cryptographic Standards**
- AES-256-GCM + HKDF encryption approach
- *Referenced in: S2 Sprint encryption implementation*

---

## Infrastructure & Technologies

### Web Technologies
- **WebSockets** - Real-time bidirectional communication
- **Webhooks** - Event-driven architecture patterns
- **ngrok** - Secure tunneling for local development
- **JSON-RPC 2.0** - Remote procedure call protocol (used in MCP)
- *Note: While these are established technologies, their specific orchestration pattern in Piper is novel*

### Database & Storage
- **PostgreSQL** - Relational database with JSON support
- **Redis** - In-memory data structure store for caching
- **ChromaDB** - Vector database for embeddings
- **SQLAlchemy** - SQL toolkit and ORM
- *Applied in: Multi-layer persistence strategy*

### Development Tools
- **Docker & Docker Compose** - Containerization and orchestration
- **GitHub Actions** - CI/CD automation
- **pre-commit hooks** - Code quality enforcement
- **pytest-asyncio** - Asynchronous test support
- **Serena MCP Server** (oraios/serena) - Symbolic code analysis via MCP
  - Language Server Protocol (LSP) integration for semantic code understanding
  - Supports: find_symbol, search_for_pattern, get_symbols_overview operations
  - *Recommended by: John Phamvan (Kind Systems CEO)*
  - *Integrated: October 2025*
  - *Used in: Token-efficient project briefings (79% reduction), symbolic code navigation*
  - *Enables: Live codebase queries replacing static documentation*
- *Enables: Consistent development environment*

---

### Python Ecosystem
- **FastAPI** (Sebastián Ramírez): Web framework
- **SQLAlchemy** (Mike Bayer): ORM
- **Pydantic** (Samuel Colvin): Data validation
- **pytest** (Holger Krekel et al.): Testing framework

### AI/ML Libraries
- **LangChain** (Harrison Chase): LLM application framework
- **ChromaDB**: Vector database
- **OpenAI Python SDK**: API integration
- **Anthropic Python SDK**: Claude integration
- **Google Generative AI SDK** (google-generativeai): Gemini model integration (October 2025)

### Additional Python Libraries
- **keyring** (Jason R. Coombs): OS-level keychain integration for secure credential storage
- **Rich** (Will McGugan): Terminal UI formatting and rich text display
- **asyncpg**: High-performance PostgreSQL async driver
- **ONNX Runtime** (Microsoft): Cross-platform ML model inference
- **scipy**: Scientific computing algorithms

### MCP Tools
- **Context7**: Documentation lookup service for library APIs
  - *Integrated: October 2025*
  - *Used in: Package compatibility verification, API documentation queries*

### Mobile Development
- **Expo / React Native**: Cross-platform mobile development framework
  - *Used in: Mobile skunkworks PoC (December 2025)*

---

## Acknowledgments

### Direct Collaborators
- Chief Architect sessions providing strategic guidance
- Lead Developer implementing core features
- **John Phamvan** (Kind Systems CEO) - Tool recommendations and technical guidance
- Community feedback shaping requirements

### Advisors

**Ted Nadeau** - Advisor + Alpha Tester
- Why-Molecule Framework (Intent Specification DSL)
- ADR-046, ADR-050 contributions
- Micro-format architecture proposal
- Comprehensive Windows testing and bug documentation
- *Collaborating since: December 2025*

**Sam Zimmerman** - Ethics Advisor
- Three-layer ethics model: Inviolate boundaries / Adaptation mechanism / Ethical style
- "Relationship-first ethics" framing
- *Contributions: November-December 2025*

**Cindy Chastain** - Advisor + Collaborator
- Experience Themes framework application (see UX section for published work citation)
- Documentary/podcast approach to storytelling
- *Collaborating since: January 2026*

### Indirect Influences
- The broader AI safety research community
- Open source maintainers whose work we depend on
- Product management practitioners sharing experiences

---

## Our Contributions

While building on these foundations, Piper Morgan contributes:

1. **Excellence Flywheel Methodology**: Systematic approach to AI-assisted development (flywheel metaphor from Collins; specific framework original)
2. **Wild Claim Verification Protocol**: Empirical validation framework
3. **8-Dimensional Spatial Intelligence**: Novel PM context understanding
4. **Debate-Driven CoD Pattern**: Multi-agent consensus at 5% token cost
5. **Enhanced Autonomy Protocols**: 4h 45m unsupervised operation patterns
6. **Time Lord Alert**: Pattern for signaling quality-over-time-constraint conflicts (alert mechanism adapted from Jesse Vincent)
7. **Cascade Investigation Pattern** (Pattern-060): Systematic multi-layer debugging methodology
8. **Cathedral Thinking Application**: Long-term purpose orientation (using folk parable tradition, not Raymond's open-source usage)

### Inspirational Quotations (Folk Attributions)

We use two quotations whose attributions are well-known to be approximate:

- **"Cathedral Builder" parable** - Commonly attributed to Christopher Wren; first documented in Bruce Barton's "What Can a Man Believe?" (1927). The story is likely apocryphal but the concept of long-term, purpose-driven work is authentic to our usage.

- **"Teach them to long for the endless immensity of the sea"** - Commonly attributed to Antoine de Saint-Exupéry; actually a folk paraphrase inspired by *Citadelle* (1948). First appeared in modern form circa 1995; attributed to Saint-Exupéry around 2007. See also: "Play it again, Sam" and "Lead on, Macduff" for similar folk-attribution patterns.

---

## License Note

This project respects all original licenses and attributions. Where we adapt or modify existing work, we maintain attribution chains and comply with original licensing terms.

---

## Maintenance Process

To ensure comprehensive attribution, we follow this systematic process:

### 1. Regular Audits
**Weekly Pattern Sweep** (using TLDR/Pattern Sweep tools)
- Scan codebase for new patterns or techniques
- Identify external influences in recent implementations
- Document any new frameworks or methodologies adopted

### 2. Session Log Mining
**End-of-Session Review**
- Extract any referenced papers, articles, or frameworks
- Note informal influences mentioned in discussions
- Capture "inspired by" references even if not directly used

### 3. Dependency Tracking
**Quarterly Dependency Audit**
```bash
# Python dependencies
pip list --format=freeze > requirements-audit.txt

# JavaScript dependencies (if any)
npm list --depth=0

# Check for new libraries or version updates
git diff requirements.txt
```

### 4. Knowledge Graph Maintenance
**Categories to Track**:
- Theoretical foundations (papers, books)
- Frameworks and methodologies
- Code libraries and tools
- Infrastructure and platforms
- Informal influences (blog posts, discussions)
- Internal innovations and patterns

### 5. Attribution Triggers
**Add citations when**:
- Implementing a pattern from external source
- Adapting a framework for our use
- Building on theoretical concepts
- Using significant code libraries
- Inspired by blog posts or articles
- Learning from other projects

---

This document is maintained as new influences are incorporated. Each significant framework adoption or pattern inspiration should be added with:
- Source attribution
- Date of incorporation
- How it's used in our project
- Any modifications or enhancements we've made

---

*"If I have seen further, it is by standing on the shoulders of giants."* - Isaac Newton (acknowledging Bernard of Chartres)
