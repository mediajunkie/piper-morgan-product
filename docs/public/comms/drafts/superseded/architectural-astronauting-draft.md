# Architectural Astronauting

*November 22*

The security epic needed role-based access control. The traditional approach was well-documented: role tables, permission tables, role-permission junction tables, user-role assignments. Clean relational design. Proper normalization. Industry standard.

It would have taken 2-3 weeks.

My Chief Architect's assessment: "Traditional RBAC would be **architectural astronauting** at our current scale. Building for 10,000 users when we have <100 is how projects die from complexity before reaching users."

We built lightweight RBAC in 5 hours instead. It shipped. It works. And it can be refactored when - if - we ever need the traditional approach.

## The astronauting pattern

Architectural astronauting is building for a future that may never arrive.

It looks responsible. "We should build this properly from the start." "We don't want to accumulate technical debt." "It's harder to refactor later." All true statements that lead to false conclusions.

The false conclusion: therefore, build the sophisticated version now.

The problem: sophisticated architectures have costs that start immediately, while their benefits arrive only if specific futures materialize. You pay the complexity tax today for options you might never exercise.

[PLACEHOLDER: When have you built for scale you didn't reach? Systems designed for millions that served thousands? Infrastructure that outlived the products it was meant to support?]

Traditional RBAC for our alpha would have meant:
- 2-3 weeks of implementation instead of 5 hours
- 6+ new database tables instead of 2 JSONB columns
- Complex query joins instead of single indexed lookups
- Ongoing maintenance burden for features we don't need

All to serve fewer than 100 users who don't need role hierarchies, organizational permissions, or granular admin controls.

## The scale question

The right architecture depends on scale. This seems obvious but is often ignored.

| Scale | Right Approach |
|-------|----------------|
| <1,000 users | Lightweight (JSONB, simple checks) |
| 1,000-10,000 | Evaluate based on actual needs |
| >10,000 | Traditional (if role complexity warrants) |

We have fewer than 100 users. Traditional RBAC is designed for enterprises with thousands. Building enterprise architecture for a product that hasn't proven product-market fit is how projects die.

Not from technical failure. From complexity that slows everything else down while waiting for scale that never arrives.

[PLACEHOLDER: Scale-appropriate architecture decisions you've made or witnessed? When has "building it right" meant building it smaller? Products that died from premature scaling?]

The astronauting temptation is strongest when you *can* see the sophisticated path clearly. "I know how to build traditional RBAC. It's the proper way. Let me do it properly."

Knowing how to build something doesn't mean you should build it now.

## What lightweight actually meant

Our lightweight RBAC uses JSONB columns:

```
Before: shared_with = ["user-uuid-1", "user-uuid-2"]
After:  shared_with = [{"user_id": "uuid", "role": "viewer"}, ...]
```

That's it. Role information embedded in the sharing structure. GIN index for fast lookups. Single query to check permissions.

Performance: 10-20ms per query.
Traditional approach: 30-50ms (joins across multiple tables).

The "proper" architecture is actually slower for our use case. The lightweight approach isn't a compromise - it's genuinely better at our scale.

Modern companies know this. Stripe, Notion, Linear all use JSONB for permissions at significant scale. The pattern is proven. We're not being clever; we're following established practice.

## The refactoring trigger list

Lightweight doesn't mean permanent. We defined explicit triggers for when to refactor:

- User base exceeds 1,000 active users
- Need role hierarchies (teams, organizations)
- Granular admin permissions required
- JSONB query performance degrades beyond 50ms
- Enterprise customer requires traditional RBAC
- Security audit mandates relational approach

None of these are true today. When any becomes true, we refactor. Until then, the lightweight approach serves perfectly.

This is the key insight: you can build simple now AND have a plan for sophisticated later. The triggers make the decision explicit. You're not ignoring future needs; you're deferring investment until those needs are real.

[PLACEHOLDER: Explicit refactoring triggers you've defined? When has "we'll refactor when X" actually happened vs. been forgotten? Making future decisions present without implementing them?]

## The velocity argument

Five hours versus 2-3 weeks isn't just about this feature. It's about everything else.

Those weeks spent on traditional RBAC would have been weeks not spent on:
- Frontend permission awareness
- Alpha documentation
- Navigation fixes
- User onboarding
- The features that actually determine whether anyone uses the product

Every hour spent on premature sophistication is an hour stolen from proving the product matters.

Our alpha tester arrived Monday. If we'd started traditional RBAC, we'd still be implementing database migrations. Instead, she was using working software with working permissions.

Sophistication that prevents shipping is sophistication that prevents learning. And learning - from real users using real software - is how products survive.

## When sophistication is right

Architectural astronauting is a failure mode, not a universal warning against sophistication.

Build sophisticated when:
- Current scale demands it (not projected scale)
- Simpler approaches have proven inadequate
- The complexity serves users, not architectural aesthetics
- You can afford the timeline impact

Build simple when:
- Current scale doesn't demand sophistication
- Simpler approaches might be adequate (you don't know yet)
- Time to learning matters more than architectural elegance
- Explicit refactoring triggers can guide future decisions

The question isn't "what's the best architecture?" It's "what's the best architecture for where we are now, with a path to where we might need to go?"

[PLACEHOLDER: How do you decide between simple-now and sophisticated-now? Decision frameworks that have served you? When has sophistication been the right call despite seeming premature?]

## The death pattern

Here's how architectural astronauting kills projects:

1. Team identifies future need (scale, enterprise features, complex permissions)
2. Team builds for that future now
3. Implementation takes weeks/months longer than simple approach
4. Product ships later (or never)
5. Users never materialize because product shipped too late
6. Sophisticated architecture serves no one

The sophistication was correct for a future that never arrived because the sophistication itself prevented that future from arriving.

This is the cruelest irony: building for scale can prevent you from reaching scale.

## The Chief Architect's call

My Chief Architect approved lightweight RBAC with clear reasoning:

> "Meets all security requirements. Appropriate for current and medium-term scale. Modern, proven pattern. Superior performance without caching. Enables alpha launch on schedule."

And the key condition: document the approach clearly, define refactoring triggers, monitor as scale grows.

This is what good architectural judgment looks like. Not "always build sophisticated" or "always build simple." Build appropriate. Know what appropriate means for your current situation. Have a plan for when the situation changes.

The astronauts who build for 10,000 users when they have 100 often end up with 0 users because they never shipped.

We shipped. Monday, our first alpha tester logged in. The permissions worked. The architecture served its purpose.

That's not a compromise. That's success.

---

*Next on Building Piper Morgan: Project Biorhythms - the natural oscillation between discovery and build.*

*Have you seen projects die from premature sophistication? When has "building it right" meant building it smaller? What triggers do you use to know when simple is no longer enough?*
