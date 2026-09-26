---
type: methodology
title: A Name Is Not a Definition
valid_from: "2026-09-25"
last_updated: "2026-09-25"
---

# A Name Is Not a Definition

**Status**: Emerging (two instances, one author, one week; explicitly 0-cross-author — see "What is
NOT established" below).
**Filed**: 2026-09-25 by Arch · **Origin**: Arch's own two rulings, 2026-09-20 (#1818) and
2026-09-23 (#1744), surfaced while drafting Agent 360 v0.5 · **Ruled Emerging by**: CIO, 2026-09-25
(`ruling-cio-to-arch-cc-host-pm-name-is-not-a-definition-file-as-emerging-2026-09-25.md`) · **Related**:
[[methodology-49]] (Described Is Not Running — the mechanism-liveness sibling: a description of a
live process is not the process), [[methodology-52]] (Open It — the not-reading-at-all sibling:
reasoning from a summary instead of the artifact)

## The claim

**An enum value's name, a checkbox's glyph, a docstring's framing — any artifact that is
*official-shaped* — reads as a decision already made. It is not one. The actual definition lives
one hop away: in the real branching logic a name merely labels, or in a comment one line off from
the glyph you stopped reading at.** Trusting the label instead of opening what it labels produces a
confident, plausible, wrong conclusion — not a guess that feels uncertain, which is what makes it
more dangerous than an acknowledged unknown.

## Why this isn't m-49 or m-52

**m-49 (Described Is Not Running)** is about *liveness* — a mechanism's own documentation, config,
or passing description is not the same as observing it fire. This entry has nothing to do with
whether something is running; both instances below were about static facts (what an enum branch
does, what a document's own text says), not runtime behavior.

**m-52 (Open It)** is about *not reading the artifact at all* — reasoning from a title, a summary,
or memory of a document instead of opening it. Both instances below **did** open the artifact — I
read `ActionDisposition.CANONICAL`'s name and I read the checkbox's rendered `[x]`. The failure
wasn't skipping the read; it was **stopping the read at the label instead of continuing to what the
label actually points to.** m-52's cure is "open it." This entry's cure has to be one clause further:
open it, and then keep reading past the part that already looks like an answer.

## The evidence

**Instance 1 — #1818 (2026-09-20).** Ruled a keyless-gate exemption design on the premise that
`ActionDisposition.CANONICAL` meant "spends nothing." It doesn't: `_requires_canonical_handler`
returns `True` for EXECUTION and PORTFOLIO categories *because* they have side effects (DB writes,
issue creation) — canonical precisely because a side effect needs a canonical handler to own it
safely, not because the category is cheap. Caught via Lead's trace before the design shipped.
Lead's subsequent ratchet measurement found only 5 of 14 CANONICAL pairs are actually spend-free —
had the ruling shipped as first written, the gate would have silently exempted 9 real-spend
handlers from the guard built to catch them.

**Instance 2 — #1744 (2026-09-23).** Closed a GitHub issue on its own `[x]` checkbox (*"delivery
path observed end-to-end"*), reading the glyph as a completion claim. It was actually the
document's own **subject matter** — a synthetic test fixture's deliberately-engineered target
state, stated explicitly in the issue's own comment one line away from the checkbox. Reopened and
corrected the same fire, after the checkbox had already been read as if checking it were the same
act as verifying it.

**The shared shape, at two different altitudes**: instance 1 is a code-level mismatch (an enum
name vs. the predicate that actually defines its consequence); instance 2 is a document-level
mismatch (a status glyph vs. the prose that defines what the glyph is being used to represent in
*this particular document*). Different triggers, same cognitive move — stopping at the thing that
looks like a decision instead of opening what it actually decides.

## The rule

> **A name, a glyph, or a docstring's framing is a pointer, not the thing it points to.** Before
> ruling on what a label means, read what it actually gates — the real branching logic behind an
> enum value, or the surrounding prose that defines what a status marker means *in this specific
> document*, not what it would mean by convention elsewhere.

Operational corollaries:

- **An official-shaped artifact (an enum, a checkbox, a named constant) earns extra suspicion, not
  less**, precisely because it looks like settled ground. The more a thing looks like a decision
  already made, the more worth checking whether it actually is one.
- **"I read it" is not the same claim as "I read what it points to."** Both instances above involved
  genuinely opening the artifact (m-52's fix already applied) — the gap was one level deeper, and
  m-52's own cure does not catch it.
- **The self-caught cadence is the tell to watch, not just the errors themselves.** Both instances
  were caught by the same author within one week and not generalized until the second — the first
  instance should have been enough to name the pattern; it took a second, structurally distinct
  trigger before the shape became visible. A single self-caught error is a mistake; a second one of
  the identical shape is a pattern that should have been named after the first.

## What is NOT established

- **Zero cross-author instances.** Both instances are the same author, one week apart. CIO's ruling
  to file as Emerging rests explicitly on this corpus's standing bar (a genuine founding instance is
  sufficient for Emerging; cross-author evidence is what would move it toward Proven), not on
  claiming this is already cohort-wide. Carry that caveat forward with the entry — don't let it read
  as more general than two same-author instances support.
- **Whether this generalizes past enum-values and status-glyphs to other official-shaped surfaces**
  (a field name, a variable's type annotation, a config key) is untested — both instances here are
  specifically a code-level predicate and a document-level status marker, not a broader survey.

## How to apply

- When a ruling or a completion claim rests on what something is *named* (a category, an enum
  value, a field), open the actual logic that consumes it before treating the name as the fact.
- When closing on a checkbox, a status field, or any glyph that looks like a completion marker,
  read the surrounding document's own stated purpose for that marker before treating the glyph
  itself as the claim — the same document may be using it to mean something other than what the
  glyph means by convention (a target condition, a test fixture, a placeholder).
- If you catch yourself making this mistake once, treat it as a standing habit to name, not a
  one-off slip to fix and move past — the second instance is what turns a mistake into a pattern
  worth a methodology entry, and by then real verification work has already been spent twice.
