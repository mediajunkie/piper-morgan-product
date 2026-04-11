# Accepting Architectural Limits: When 67% Is Complete

*November 3, 2025 - Building Piper Morgan - Methodology Series*

Monday morning. P1 sprint. Issue #283: Error message humanization. Make technical errors conversational.

Goal: Humanize 6 error types for better UX.

By 11:15 AM: 4 error types working perfectly. 2 blocked by FastAPI architecture.

**The situation**:
- Empty input → "I didn't quite catch that" ✓
- Unknown action → "I'm still learning how to help with that" ✓
- Timeout → "That's complex - let me reconsider" ✓
- Unknown intent → "I'm not sure I understood" ✓
- Invalid token → {"detail": "Invalid token"} ❌
- No token → {"detail": "Authentication required"} ❌

**Achievement**: 4 out of 6. 67%.

**The question**: Is 67% acceptable? Or do we need to solve the remaining 2?

**The answer**: 67% is complete.

Not compromised. Not given up. But architecturally complete. Fighting the framework for the last 33% would cost 8-12 hours, violate FastAPI patterns, and provide marginal UX benefit for <5% of errors in alpha testing.

[QUESTION: That 11:15 AM moment when Cursor reported "can't catch auth errors" - immediate acceptance or initial frustration?]

This is about mature engineering. Knowing when architectural constraints make "perfect" solution inappropriate. When 67% represents genuinely complete work. When accepting limits is better engineering than fighting them.

## The architectural reality

Let's be precise about what blocked the remaining 2 error types:

**FastAPI has two-phase request processing**:

```
Phase 1: Dependency Resolution
  → Executes BEFORE route handler
  → Has its own error handling
  → Returns errors directly as JSON
  → CANNOT be intercepted by @app.exception_handler
  → This is where auth happens

Phase 2: Route Handler Execution
  → Where our business logic runs
  → Where our exception handlers work
  → Where middleware can intercept
  → This is where 4/6 error types occur
```

**The problem**: Authentication happens in Phase 1 (dependency injection). Our error humanization works in Phase 2 (exception handlers).

**The gap**: Dependency errors bypass exception handlers. By design. For good reasons.

FastAPI's approach protects security. Dependencies fail fast with clear technical errors. No ambiguity. No confusion. Direct feedback about authentication problems.

[SPECIFIC EXAMPLE NEEDED: First encounter with FastAPI's two-phase processing - obvious from framework knowledge or took investigation?]

This isn't bug. It's not oversight. It's **deliberate architectural decision** by FastAPI maintainers.

We could work around it. But working around deliberate framework design has costs.

## The three options evaluated

Chief Architect analyzed three approaches:

### Option A: Move Auth to Route Bodies

**The approach**: Remove authentication from dependency injection. Move to route handler bodies. Makes auth errors catchable by exception handlers.

**Technical details**:
- Modify 20+ routes
- Remove `Depends(get_current_user)` from signatures
- Add `current_user = await get_current_user(token)` to each route body
- Wrap in try-catch to humanize errors

**Pros**:
- Catches auth errors ✓
- Enables humanization ✓

**Cons**:
- Violates FastAPI patterns ❌
- Duplicates auth logic 20+ times ❌
- Makes testing harder ❌
- Creates maintenance burden ❌

**Effort**: 4-6 hours

**Risk**: HIGH (breaking 20+ routes)

**Benefit**: Marginal UX improvement for <5% of errors

**Verdict**: Not worth it

### Option B: ASGI Middleware

**The approach**: Implement low-level ASGI middleware to intercept dependency errors before FastAPI processes them.

**Technical details**:
- Custom ASGI middleware at lowest level
- Catch exceptions before dependency resolution
- Transform technical errors to humanized errors
- Complex interaction with FastAPI's processing

**Pros**:
- Catches dependency errors ✓
- Doesn't modify routes ✓

**Cons**:
- Very complex implementation ❌
- Performance impact (all requests) ❌
- Uncertain success (might not work) ❌
- Hard to test and maintain ❌

**Effort**: 8-12 hours

**Risk**: VERY HIGH (complex, uncertain outcome)

**Benefit**: Same marginal improvement

**Verdict**: Definitely not worth it

### Option C: Accept 4/6 as Architectural Reality ✅

**The approach**: Document the limitation. Accept that auth errors will be technical. Focus energy elsewhere.

**Technical details**:
- None required

**Pros**:
- No breaking changes ✓
- No complex code ✓
- No maintenance burden ✓
- Respects framework design ✓

**Cons**:
- Auth errors remain technical
- Minor UX gap for rare scenarios

**Effort**: 0 hours

**Risk**: NONE

**Benefit**: Time saved can improve other features

**Verdict**: Most sensible choice ✅

[REFLECTION NEEDED: The three-option analysis - was Option C obvious immediately or required convincing?]

## The cost-benefit mathematics

Let's make the economics explicit:

**To achieve 6/6 error humanization**:

**Option A (Move auth to bodies)**:
- Time cost: 4-6 hours
- Risk: Breaking 20+ routes
- Maintenance burden: Ongoing
- UX improvement: <5% of errors (auth failures are rare)
- Context: Alpha testing with 5-10 trusted users

**Option B (ASGI middleware)**:
- Time cost: 8-12 hours
- Risk: Very high, uncertain success
- Maintenance burden: Complex code to maintain
- UX improvement: Same <5%
- Context: Same alpha testing

**To accept 4/6 completion**:
- Time cost: 0 hours
- Risk: None
- Maintenance burden: None
- UX impact: Minor gap for rare scenarios
- Context: Alpha users can handle technical auth errors

**Alternative use of 8-12 hours**:
- Polish 3 other features
- Fix 2 actual bugs
- Improve core functionality
- Add value where it matters

**The calculation**:
- Cost: 8-12 hours + high risk + maintenance burden
- Benefit: Minor UX for <5% of errors in alpha
- **ROI**: Negative

Fighting the framework for marginal gain is bad engineering. Accepting architectural reality and investing time elsewhere is good engineering.

[QUESTION: The explicit cost-benefit framing - does this make accepting limits feel more justified or was pragmatic thinking already obvious?]

## Why this is mature engineering

Here's what separates junior from senior engineering:

**Junior engineer approach**:
- "Goal is 6/6 error types humanized"
- "4/6 isn't complete"
- "Must solve remaining 2"
- "Framework limitation is problem to overcome"
- *[Spends 12 hours fighting FastAPI]*
- Result: 6/6 achieved, but at what cost?

**Senior engineer approach**:
- "Goal is excellent error UX"
- "4/6 achieves 95% of benefit"
- "Remaining 2 are rare edge cases"
- "Framework limitation is architectural reality"
- *[Accepts 4/6, invests 12 hours elsewhere]*
- Result: Better overall product

**The maturity**: Recognizing when "complete" doesn't mean "perfect." When architectural constraints make perfect solution inappropriate. When 67% represents genuinely complete work.

**Not compromise**. **Not giving up**. But **intelligent assessment** that fighting architecture for marginal gain isn't worth cost.

## The 80% pattern inverted

Usually we fight the 80% pattern - stopping at "good enough" instead of truly complete.

But this is inverse: Recognizing when 67% *is* truly complete given constraints.

**Normal 80% pattern**:
- Could reach 100% with reasonable effort
- Stopping early creates technical debt
- "Good enough" is excuse for incomplete work
- **Fight this**: Complete the work properly

**Inverted 67% pattern**:
- Reaching 100% requires unreasonable effort
- Stopping at 67% respects architectural reality
- "Complete given constraints" is mature assessment
- **Accept this**: 67% is genuinely complete

The difference: **Context and constraints**.

Normal 80% pattern: Work is genuinely incomplete. Need to finish.

Inverted 67% pattern: Work is complete to architectural limits. Fighting framework is waste.

[SPECIFIC EXAMPLE NEEDED: Have you seen projects where fighting for 100% against architectural constraints caused more problems than accepting 80%?]

## What FastAPI's design teaches

Why does FastAPI make dependency errors uncatchable? Not accident. Deliberate design.

**Security**: Auth failures should be clear and unambiguous. No friendly wrapping. Direct technical feedback.

**Performance**: Dependency resolution is fast path. No exception handler overhead.

**Clarity**: Dependencies fail fast. No confusion about what went wrong. Stack traces point to exact problem.

**Testability**: Dependency injection makes testing easier. Mocking dependencies is straightforward.

These are **good reasons**. FastAPI's design serves real needs. Our desire to humanize 2 more error types doesn't outweigh framework's architectural benefits.

**Framework wisdom**: Maintainers of popular frameworks make deliberate tradeoffs. Usually good reasons exist for limitations. Sometimes accepting those tradeoffs is better than fighting them.

**The maturity**: Trusting framework designers. Not assuming you know better. Recognizing that limitations often protect against worse problems.

## The alpha testing context

Context matters enormously for this decision:

**If we were shipping to production**:
- Thousands of users
- Unknown skill levels
- Auth errors common (session expiration)
- Professional appearance matters
- **Decision**: Might justify 8-12 hours for 6/6

**But we're in alpha testing**:
- 5-10 trusted users
- Technical background
- Auth errors rare
- Focus is core functionality
- **Decision**: 4/6 is completely sufficient

The work should match the stage. Alpha testing doesn't require production polish. Core functionality matters more than edge case UX.

**Different rhythms, different stages** (see related methodology post). Alpha stage needs different completeness than production stage.

[REFLECTION NEEDED: The "match work to stage" principle - is this conscious product thinking or intuitive context awareness?]

## When to fight vs accept

How do you know when to fight for 100% vs accept architectural limits?

**Fight for 100% when**:
- Limitation is your own technical debt
- Solution is architecturally sound
- Effort is proportional to benefit
- User impact is significant
- Context demands completeness

**Accept limits when**:
- Limitation is framework's deliberate design
- Solution violates architectural patterns
- Effort is disproportionate to benefit
- User impact is minimal
- Context allows pragmatism

**The framework**:
1. Is this our debt or framework design? (Framework → accept)
2. Does solution respect architecture? (Violates → accept)
3. What's effort vs benefit ratio? (10:1 cost → accept)
4. Who's affected and how often? (<5% → accept)
5. What does context require? (Alpha → accept)

If multiple factors point to "accept," then accept. Fighting becomes wasteful.

**Monday's score**: 5/5 factors point to accept. Clear decision.

## What this means for completionism

Engineers often have perfectionist tendencies. "If 6/6 is possible, we must achieve it."

But product thinking asks different questions:
- Is 6/6 worth the cost?
- Does 4/6 serve user needs?
- What else could we improve with that time?
- Does context require perfection?

**Perfectionism says**: Incomplete work is failure. Must achieve 100%.

**Pragmatism says**: Complete-enough work is success. 67% might be 100% given constraints.

The shift: From "how much can we do?" to "how much should we do?"

[QUESTION: The perfectionism vs pragmatism tension - is this natural product thinking or learned discipline to resist completionist urges?]

## The communication challenge

Here's the hardest part: Explaining why 4/6 is complete.

**To non-technical stakeholder**:
"We humanized 4 out of 6 error types."
"Why not all 6?"
"FastAPI's architecture makes the remaining 2 technically infeasible without major framework violations."
"So it's not done?"
"It's complete to architectural limits."
"..."

The challenge: "Complete to architectural limits" sounds like excuse. Like rationalization. Like we're giving up.

**The framing shift needed**:
"We achieved 95% of error humanization benefit. The remaining 5% would require violating framework patterns and 8-12 hours of complex work. That time is better spent improving core features."

Better: Quantify benefit achieved. Quantify cost of remaining work. Justify time allocation.

Not: "We can't do it" (sounds like excuse)
But: "We could do it, but it's not worth the cost" (sounds like decision)

[SPECIFIC EXAMPLE NEEDED: Have you had to explain architectural constraints to non-technical stakeholders? What framing worked?]

## The documentation requirement

Accepting architectural limits requires documentation:

**What we documented for 4/6 completion**:
1. What works (4 error types, examples of each)
2. What doesn't work (2 auth error types)
3. Why it doesn't work (FastAPI dependency injection phase)
4. Options evaluated (3 approaches, cost/benefit of each)
5. Decision rationale (why Option C selected)
6. Future considerations (if context changes, revisit)

**Why documentation matters**:
- Future developers understand limitation
- No one wastes time trying to "fix" it
- Context for future decisions clear
- If requirements change, analysis exists

Without documentation: "Why don't auth errors humanize?" leads to hours of investigation rediscovering architectural constraint.

With documentation: "Why don't auth errors humanize?" leads to 5-minute doc read understanding architectural reality.

**Documentation is how limits become understood rather than mysterious.**

## What other projects can learn

The pattern applies beyond Piper Morgan:

**Any project will encounter**:
- Framework limitations by design
- Architectural constraints that are expensive to overcome
- Features that are 70-80% achievable easily, 100% achievable with disproportionate effort
- Contexts where "good enough" is genuinely good enough

**The discipline**:
1. Identify the limitation clearly
2. Evaluate options systematically
3. Calculate cost-benefit explicitly
4. Consider context appropriately
5. Make decision based on economics, not perfectionism
6. Document rationale comprehensively

**The maturity**: Accepting that complete ≠ perfect. That architectural realities constrain solutions. That fighting frameworks for marginal gains is usually waste.

Not every hill is worth dying on. Not every limitation is worth overcoming. Not every gap needs closing.

**Engineering judgment**: Knowing which battles to fight.

## The Monday outcome

Issue #283 closed as complete:
- 4/6 error types humanized ✓
- Architectural limitation documented ✓
- Cost-benefit analysis recorded ✓
- Decision rationale clear ✓

**Time invested**: 7-8 hours total (investigation + implementation + documentation)

**Time saved**: 8-12 hours (not fighting framework)

**Outcome**: 4/6 achievement serves 95% of use cases. Remaining 5% documented as known limitation.

**Result**: Complete work. Not compromised work. But complete-within-architectural-reality work.

Monday proved: Sometimes the mature answer to "Can we achieve 100%?" is "Yes, but we shouldn't."

[QUESTION: Monday evening with 4/6 documented as complete - satisfaction with pragmatic decision or lingering desire for 6/6?]

---

*This is part of the Building Piper Morgan methodology series, exploring systematic approaches to AI-assisted development. For related patterns, see "The Completion Matrix" and "Different Rhythms, Different Stages."*

*Have you encountered framework limitations that were expensive to overcome? When do you fight for 100% versus accept "good enough"?*
