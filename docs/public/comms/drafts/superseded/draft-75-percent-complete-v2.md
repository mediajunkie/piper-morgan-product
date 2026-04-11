# 75% Complete

*December 4*

[alt text: Three puzzle pieces that almost fit together, with visible gaps at the joints]
Caption: "The pieces existed. The connections didn't."

Thursday evening, debugging why list creation failed. Three separate bugs, all presenting as the same symptom. Each one followed the same pattern: the infrastructure existed, the integration didn't.

Three weeks earlier, we'd formalized the completion matrix—explicit criteria for what "done" means. And yet here we were, debugging 75% complete work. The discipline didn't prevent these bugs. It just made them recognizable.

## The pattern

The first bug: API contract defined, Pydantic models created, but endpoints still expected query parameters instead of JSON bodies. The model was there. It just wasn't being used.

The second bug: Dependency injection pattern implemented, async generators created, but the actual dependency functions still expected middleware that was never written. The pattern existed. The connection didn't.

The third bug: CSS design tokens defined with all our colors and spacing, but five templates never linked the stylesheet. The system was there. The templates didn't reference it.

Three instances of the same anti-pattern: 75% complete. Scaffolded but not finished. "It's mostly there" which means it doesn't work.

## The signature

75% complete work has a signature. The hard part is done—architecture designed, infrastructure built, patterns established. The easy part is skipped—wiring things together, updating call sites, linking stylesheets. It looks done because code exists, files are present, structure is visible. It doesn't work because the connections aren't made.

[PM PLACEHOLDER: 75% complete work in your experience - projects where infrastructure existed but integration didn't?]

The pattern is seductive because the hard intellectual work is complete. The API contract is thoughtfully designed. The dependency injection pattern is architecturally sound. The design token system is well-structured. All the difficult decisions are made.

What's left is mechanical—update the endpoints to use the models, change the functions to use the generators, add `<link>` tags to the templates. No deep thinking required. Just execution.

And that's exactly why it gets skipped. The interesting work is done. What remains feels like tedious cleanup. Easy to defer, easy to forget, easy to assume someone else will handle.

## Why it's invisible to the builder

The person who builds infrastructure knows what's complete and what isn't. They're intimately familiar with what works and what needs wiring. They test the pieces they built. Those pieces work.

But they don't necessarily test the integration. They know the API models exist, so they assume the endpoints use them. They know the DI pattern is implemented, so they assume the functions reference it. They know the tokens are defined, so they assume the templates link them.

The assumptions are reasonable. The work looks done from the builder's perspective. All the files exist. All the patterns are in place. It should work.

[PM PLACEHOLDER: Assumptions about your own work - when has your familiarity with a system made you assume integration that wasn't there?]

Then a user tries it. Or another developer tries to use the infrastructure. And it doesn't work. Not because the infrastructure is bad, but because it's not connected to the places that need it.

## The three instances

For the API contract bug, we'd designed thoughtful Pydantic models—`CreateListRequest` with name and optional description fields. Clean, validated, well-structured. The models existed in the codebase. The endpoints just didn't use them. They still expected query parameters. When the frontend sent JSON (which is what Pydantic models expect), the backend returned 422 Unprocessable Entity. The contract existed. The wiring didn't.

For the dependency injection bug, we'd implemented the async generator pattern—`get_db()` yielding sessions with proper async context management. Clean session lifecycle. The pattern existed. The dependency functions still expected `request.state.db`, waiting for middleware to set it. The middleware was never created. The pattern existed. The connection didn't.

For the CSS design tokens bug, we'd created a comprehensive token system—`--color-primary`, `--spacing-md`, dozens more. Professional design system, properly structured. Five templates just never included the stylesheet link. The tokens existed. The templates didn't reference them. Buttons and forms rendered with no styling.

[PM PLACEHOLDER: Infrastructure you've built that wasn't fully integrated - patterns implemented but not wired?]

## Why testing doesn't catch it

Unit tests passed. We tested that the Pydantic models validated correctly. We tested that the async generators managed sessions properly. We tested that the CSS tokens defined the right values.

All those tests passed because they tested the infrastructure in isolation. They didn't test integration—whether the endpoints actually used the models, whether the functions actually used the generators, whether the templates actually linked the tokens.

Integration tests should catch this. But integration tests require thinking about how pieces connect, not just whether pieces work. You have to test the wiring, not just the components.

The 75% complete pattern hides in that gap between unit tests (components work) and integration tests (components connect).

[PM PLACEHOLDER: Testing strategies that caught integration gaps - what makes integration testing effective?]

## The scaffolding trap

The pattern often starts with good architectural thinking. "We should use Pydantic models for API contracts." "We should have a proper DI pattern." "We should have a design token system." All correct.

The first implementation creates the infrastructure. Models defined, patterns established, systems built. This feels like progress. It is progress—the hard architectural work is done.

But then the implementation stops at scaffolding. The infrastructure exists but isn't fully integrated. Maybe time pressure happened. Maybe the builder moved to something else. Maybe they assumed someone else would handle the wiring.

The result: scaffolding that looks done but doesn't function. The appearance of completion without the reality of integration.

[PM PLACEHOLDER: Scaffolding vs completion in your work - when has creating infrastructure felt like finishing?]

## How to detect

Look for these signals.

Files exist but aren't imported—utility created but never used, helper functions defined but not called, libraries added but not integrated.

Patterns defined but not applied—architecture documented, examples shown, but actual code doesn't follow the pattern.

Configuration exists but isn't referenced—settings defined, environment variables listed, but the code reads from different sources.

Tests pass but features don't work—unit tests green, integration tests absent, users report failures.

The consistent signal: existence without integration. The thing is there but not connected.

[PM PLACEHOLDER: Detection practices that work - code review patterns that catch this?]

## How to prevent

Make integration explicit. Don't consider infrastructure complete until it's integrated. The API models aren't done when they're defined—they're done when the endpoints use them.

Test integration, not just components. Write tests that verify connections, not just correctness. Does the endpoint actually use the model? Does the function actually use the generator? Does the template actually link the stylesheet?

Complete before moving on. Finish integration before starting new infrastructure. Don't leave wiring for later—later often means never.

Checklists for follow-through. After building infrastructure, check: What needs to reference this? Have all those references been updated? Have I tested the integration?

[PM PLACEHOLDER: Prevention strategies you've used - what ensures follow-through?]

## The Thursday lesson

Three bugs, same pattern, same evening. Each one revealed infrastructure that existed but wasn't integrated. Fixing them wasn't intellectually difficult—the architecture was sound. But finding them required patient investigation because they all looked complete.

The API models existed. The DI pattern existed. The design tokens existed. They just weren't connected to the places that needed them. The scaffolding was there. The wiring wasn't.

This is the anti-pattern of sophisticated development: we build elegant infrastructure and forget the mundane work of wiring it together. We solve the interesting architectural problems and skip the boring integration work.

[PM PLACEHOLDER: Learning from your own 75% complete patterns - when has catching this pattern improved your practice?]

## The completion discipline, revisited

Infrastructure isn't complete when it exists. It's complete when it's integrated.

Models aren't complete when they're defined. They're complete when endpoints use them.

Patterns aren't complete when they're implemented. They're complete when code follows them.

Systems aren't complete when they're built. They're complete when templates reference them.

The hard work is architecture. The discipline is follow-through. Both matter. The 75% complete pattern happens when we do the hard work and skip the discipline.

Thursday taught us to value both. Not just building elegant infrastructure, but completing the mundane work of wiring it together. Not just defining patterns, but ensuring they're applied. Not just creating systems, but verifying they're referenced.

The satisfaction isn't in building the infrastructure. It's in seeing the user create a list, successfully, because all three layers of infrastructure are actually connected.

---

*Next on Building Piper Morgan: Does the User Notice?, where a disagreement between advisors revealed the question that matters most for deciding what's MVP and what can wait.*

*When have you seen the 75% complete pattern? How do you ensure follow-through beyond building infrastructure?*
