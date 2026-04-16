# The Closing Sprint

<!-- image: 'ai-finish.png' -->
<!-- alt: 'A runner crosses a finish line on a newly solid track while ghostly alternate paths converge behind them, guided by glowing, translucent AI companions assembling the final pieces in midair.' -->
<!-- caption: '"Almost there!"' -->

*March 20–22*

Pouring coffee on a Friday morning. The architecture was facing the right direction. The floor was routing as expected. The dispatcher was consolidating offers. The briefings were accurate. The mail was flowing.

Now we had to finish the sprint.

M1 had been organized into four tiers: architecture, quality, capabilities, and PM-led decisions. The first two tiers were done. Tier 3 — the capability gaps that actual users would notice — was next.

The sprint had quadrupled in length during build and testing. It had led to a literal revolution in the architecture. Now it felt like we had finally rounded the corner.

## Five sources of truth

The Lead Developer's first audit Friday morning surfaced a problem we hadn't seen coming. Piper was telling users it could do things it couldn't actually do.

The root cause: five disconnected systems were each describing Piper's capabilities. PIPER.md listed 28 capabilities. The soft invocation detector knew 7 workflow types. The dispatcher registry had exactly 1 — meetings. The context assembler had its own capability list. And the canonical handler set implied yet another.

None of them coordinated. So when a user asked about project setup, the LLM — drawing from PIPER.md — would offer to help. The user would accept. And then nothing would happen, because the dispatcher had no handler registered for project setup.

The fix was registry-driven reconciliation: if it's not in the dispatcher registry, don't offer it. One source of truth, enforced at the earliest detection point. PIPER.md was updated to reflect runtime reality. The soft invocation detector was gated on the registry. The context assembler was made registry-aware.

Five sources of truth became one. The Lead Developer filed and closed #923 the same session.

It's hard enough to keep these critters honest without confusing them with mismatched and incorrect info!

## The 75% pattern, four times in a row

Saturday was Tier 3 capability day. Four issues. Each one followed the same pattern.

GitHub issue close/reopen (#902): handlers existed, pre-classifier existed, fuzzy matching existed, 34 tests existed. What was missing? The MCP adapter didn't have an `update_issue()` method — an AttributeError at runtime — and there was no confirmation UX. Two gaps in a 95% complete feature. Forty-four tests after the fix.

Todo completion (#904): fully implemented with 23 tests passing. Never formally closed. No code changes needed. Verified and closed.

Reminders (#903): the database already had a `reminder_date` field, indexed. The todo CRUD was complete. The time parsing library was in requirements. What was missing was the wiring — five integration points connecting the pre-classifier to the time parser to the handler to the action mapper to the greeting surfacing. Thirty-two new tests.

Lazy workflow deferral (#883): six dispatch methods were pre-creating workflow objects that no handler ever used. One hundred percent wasted work. The fix was `workflow = None` — let handlers create workflows when they actually need them. Zero new tests needed because the behavior was invisible to existing tests.

Four issues. Each one 75-95% complete before anyone touched them. The audit-first approach — checking what exists before assuming what's missing — identified the 5-10% gap instead of reimplementing the whole feature.

I know some of the 75%-complete problem is endemic to LLM coding agents these days and some of it is a natural consequence of modularity in which you can't really finish till all the parts are wired up, and this always requires an additional pass. In some ways the unique part of doing this with AI is the frequent astonishment the agents appear to experience when they rediscover partially completed work.

## The gate

M1 needed a formal gate — a defined set of criteria that must pass before the sprint can close. Like M0's gate #779, but informed by everything we'd learned since.

The Lead Developer filed #926 with four verification areas: conversation quality, task lifecycle completeness, architectural integrity, and bug debt. Then asked the CXO and PPM to independently review and refine the criteria.

They converged without coordinating. Both recommended fresh-account testing — spin up a new user and verify the full experience, not just individual features. Both recommended integrating the Colleague Test rubric — the CXO's "would a knowledgeable colleague respond this way?" heuristic, now formalized with a three-dimension scoring system and worked examples.

The gate grew from 5 smoke queries to 9. A Colleague Test score threshold of 7+. Canonical retest target of 85% or above. Capability registry verification. Offer system precedence check. Multi-turn integration test.

## The experience philosophy

While the Lead Developer closed capability gaps and the gate took shape, the PPM resolved a thread that had been carried for ten days. Product concept decisions for #717 — what IS a Product in Piper's domain model, how does it relate to Projects, what lifecycle states does it have.

But the bigger deliverable was PDR-004: Experience Philosophy. Four principles distilled from ten days of product decision-making:

The Session Belongs to the User. Offer-First Activation. Piper Coordinates Understanding. The LLM Floor Guarantee.

These weren't aspirational statements. They were extracted from actual decisions — the workflow escape commands and timeout mechanisms that ensure the user's session is always theirs, the offer-first pattern that replaced the onboarding wizard's session capture, the context assembler's role in closing the gap between what participants think they know and what's actually true, and the floor-first guarantee that Piper is always at least as good as a well-prompted LLM with context. The philosophy was already in the code. The PDR just named it.

## Where the sprint stands

By Sunday evening, M1 Tiers 1 through 3 were complete. The architecture was floor-first. The dispatcher was consolidating offers. The capability registry was gating promises. GitHub close/reopen, todo completion, reminders, and lazy workflow deferral were all shipped and tested. The gate was defined and independently reviewed.

Tier 4 — the PM-led decisions, the product concept work, the collaborative discovery sessions — remained. But the engineering was done. The foundation sprint was living up to its name.

And the first E2E smoke test was already running through `/api/v1/intent`, testing a full task lifecycle from the outside. Not unit tests checking internal behavior. An actual simulated user, typing actual queries, getting actual responses.

Seems like we must be close, right?

---

_This is Part 6 of a series about the M1 sprint. The series began with [Ten Roles, One Day](https://pipermorgan.ai/blog/ten-roles-one-day/) and tracked through an architectural inversion, a floor that wasn't, a foundation rebuilt, and nine voices finding their first chord. The sprint isn't over. But the floor is under our feet. Next on Building Piper Morgan, "The Migration," in which a series of seismic tooling shifts require us to sort out all of my projects and agents and migrate the entire team to new digs._

_When has your team reached the point where the engineering was done but the product questions remained? What did you do with that moment?_
