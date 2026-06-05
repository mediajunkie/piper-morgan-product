---
image: ai-guide.png
alt: 'A mountain guide and three hikers study a trail map at a trailhead while, in the distance, another hiking party encounters a series of avoidable problems including a broken bridge, a wrong turn, and a difficult cliff climb.'
caption: 'One party brought a map.'
---

# Be Prepared

*December 9, 2025*

Tuesday afternoon. The T2 Sprint (Test Polish) was complete — 602 smoke tests marked, test infrastructure production-ready, six GitHub issues closed. A full epic, finished by noon.

The S2 Sprint (Security Polish) sat waiting. Encryption at rest. Sensitive user data protection. AES-256-GCM, HKDF key derivation, GDPR compliance, SOC2 requirements. We estimated forty-two hours of implementation work across six phases.

We could have started coding immediately. The encryption libraries were installed. The fields needing protection were identified. The implementation pattern was clear enough. Just start with the FieldEncryptionService, build out the ORM integration, write the migration scripts.

Instead, we spent five hours on preparation. No code written. No features implemented. Just thinking, documenting, and creating the conditions for implementation to succeed.

# What those five hours bought

By evening, we had:

**A comprehensive review package for Ted Nadeau** (our computer-science advisor):
- Thirteen specific questions about the architectural approach
- Five Whys analysis for every major decision
- GDPR and SOC2 compliance mapping
- Test strategy and performance baselines

**A 42-hour implementation gameplan**:
- Six phases with detailed breakdown
- Daily work estimates
- Acceptance criteria for each phase
- Code patterns and examples
- Quick reference commands

**Four GitHub issue templates** for deferred S3 work:
- Email encryption
- Search on encrypted fields
- KMS migration
- Key rotation automation

**Infrastructure verification**:
- Confirmed cryptography library support
- Identified all fields requiring encryption
- Validated no existing encryption conflicts

Five hours of preparatory work. Zero lines of production code.

# The implementation that didn't happen yet

Here's the interesting part: as of writing this, we still haven't implemented the encryption. The S2 Sprint prep is complete, and technically we're waiting for Ted's cryptographic review before we start coding.

So we can't point to the implementation and say "look how smoothly it went because we prepared." We can't measure the bugs we avoided or the refactorings we didn't need.

And, honestly, I don't need this for the MVP yet. To get from beta to production, yes, but to get to beta? No.

But we can imagine two timelines:

**Timeline A** (preparation first):
Five hours of upfront work. Ted reviews the architectural decisions. He spots potential issues before any code exists. We adjust the approach. When we start implementing, every major decision is already made. The questions are answered. The compliance requirements are mapped. The test strategy is clear.

**Timeline B** (implementation first):
Start coding immediately. Build the FieldEncryptionService. Integrate with the ORM. Write some tests. Hit a question about key rotation. Stop and research. Hit a question about GDPR compliance. Stop and research. Realize the initial approach doesn't quite work. Refactor. Get partway through and need cryptographic review. Ted identifies architectural issues that require significant rework. Back up, redesign, reimplement.

I have lived through versions of Timeline B. It is not fun.

The five hours we spent upfront doesn't get added to the implementation time. It replaces time we would have spent stopping, researching, backtracking, and reworking during implementation.

# The question you can't un-ask

The thirteen questions we prepared for Ted aren't optional questions. They're questions the implementation will force us to answer one way or another.

Questions like:
- How do we handle key rotation without breaking existing encrypted data?
- What's our strategy for GDPR right-to-erasure on encrypted fields?
- How do we balance searchability with encryption requirements?
- What's the migration path to KMS once we're past alpha?
- How do we test encryption without exposing plaintext in logs?

We can answer these questions before we write any code, with Ted's expert review, making deliberate architectural decisions.

Or we can answer them during implementation, under time pressure, while code is half-built, making expedient tactical choices that become technical debt.

The questions exist either way. Preparatory work just changes *when* and *how* we answer them.

# The architectural review that saves days

Ted's review of our S2 prep package will probably take an hour or two of his time. He'll read through the architectural decisions, check our Five Whys analysis, validate the cryptographic approach, flag any issues.

If he finds problems — and he probably will, that's why we asked for review — we adjust the gameplan before any code exists. Changing a design document takes minutes. Changing code that's half-implemented takes hours or days.

Every issue caught in the review package is an issue that doesn't derail implementation. Every question answered upfront is a decision that doesn't block progress later.

This is why preparatory work isn't overhead. It's front-loading the decisions, concentrating the architectural thinking, creating clear answers before the implementation pressures start.

# The gameplan that prevents scope creep

The 42-hour implementation gameplan breaks the work into six phases:

**Phase 0**: Investigation & Setup (4 hours)
**Phase 1**: FieldEncryptionService (8 hours)
**Phase 2**: ORM Integration (8 hours)
**Phase 3**: Data Migration (6 hours)
**Phase 4**: Performance Validation (4 hours)
**Phase 5**: Testing & Documentation (8 hours)
**Phase 6**: PM Handoff (4 hours)

Each phase has specific deliverables. Each phase has acceptance criteria. Each phase has test cases defined upfront.

This isn't a detailed step-by-step plan — those never survive contact with reality. It's a framework. A way to know if you're on track or drifting. A way to recognize when you're solving problems that weren't in scope.

When you start implementing without a gameplan, every technical decision feels equally important. Every potential optimization seems worth pursuing. Every edge case demands attention.

With a gameplan, you can ask: "Is this in scope for Phase 1, or does it belong in Phase 3?" You can defer. You can sequence. You can make conscious decisions about what to solve now versus later.

The gameplan prevents the implementation from expanding to fill all available time. It prevents "while we're at it" feature creep. It prevents solving tomorrow's problems instead of today's.

# The S3 templates that prevent future debates

The four GitHub issue templates for S3 (post-alpha work) might seem like pure overhead. We're not implementing those features now. Why document them?

Because right now, in the preparation phase, we can think clearly about what's in scope and what's deferred. We can make conscious decisions about the MVP boundary. We can document why certain features aren't in S2.

Three months from now, when someone asks "why doesn't this support encrypted search?", we won't have to reconstruct the reasoning. We won't have debates about whether it should have been included. We'll point to the S3 template that explains exactly why encrypted search is complex, what approaches we considered, and why we deferred it to post-alpha.

The templates turn future debates into non-debates. The decisions are already documented. The scope is already clear.

# What counts as "real work"

There's a persistent belief in software development that code is the only real work. That time spent not-coding is time spent not-working.

By that measure, the five hours we spent on S2 preparation produced zero value. No features shipped. No bugs fixed. No tests written. Just documents and plans.

But measure differently:

- Questions answered before they block implementation: 13
- Architectural issues caught before code exists: Unknown, but >0
- Scope creep prevented by clear gameplan: Hard to quantify, but real
- Future debates prevented by S3 templates: Several
- Implementation time saved by having clear answers: Days

The preparatory work *is* the work. It's not something you do before the real work starts. It's not overhead that delays shipping. It's the architectural thinking, the decision-making, the scope-setting that determines whether implementation goes smoothly or becomes a death march.

# When preparation becomes procrastination

There's a line. You can absolutely overthink things. You can absolutely use "preparation" as an excuse to avoid the hard work of implementation.

Some warning signs:
- You're rewriting the gameplan for the third time
- You're researching tools instead of making decisions
- You're creating process documents about how to create process documents
- You've been "preparing" for weeks without starting

The preparation phase should feel uncomfortable in its brevity. You should feel slightly underprepared when you finish. You should have open questions and known unknowns.

For S2, five hours felt right. We answered the major questions. We identified the phases. We created the review package. But we didn't design every function signature or plan every test case. That would be overthinking.

The heuristic: prepare until you know what you're building and why, then start building. You'll discover details during implementation — that's normal. But the architecture, the scope, the major decisions — those should be clear.

# The alternative to heroics

Without preparatory work, complex implementations require heroics. Brilliant developers making split-second architectural decisions under pressure, pivoting when approaches don't work, debugging their way through unanticipated edge cases.

Sometimes this works. Sometimes you get lucky. Sometimes the developer is experienced enough to make good decisions on the fly.

But it's exhausting. It's error-prone. It's not sustainable. And it makes the implementation dependent on having someone brilliant and experienced available at every decision point.

Preparatory work replaces heroics with clarity. The brilliant thinking still happens — but it happens during the preparation phase, with time to consider alternatives, consult experts, and make deliberate choices.

The implementation becomes execution rather than invention. Still challenging, still requiring skill, but without the constant cognitive load of major architectural decisions.

That's what the five hours bought us. When we start implementing S2, we won't need heroics. We'll need careful execution of a well-thought-out plan.

And if we encounter problems we didn't anticipate? We'll have Ted's review to fall back on. We'll have the gameplan to revise. We'll have the architectural thinking already documented.

The preparatory work doesn't eliminate all problems. It just ensures the problems we encounter are novel ones, not problems we could have anticipated with a few hours of careful thinking.

---

*Next on Building Piper Morgan: [tease pending — set after PM↔Comms slate decision].*

*How do you distinguish productive preparation from procrastination in your own work? What signals tell you it's time to stop preparing and start building?*
