---
type: adr
number: 80
title: "LLM decides meaning; code decides permission, checks meaning against real data, and shows before it acts"
status: "ACCEPTED"
valid_from: "2026-10-06"
last_updated: "2026-10-06"
---

# ADR-080 — LLM decides meaning; code decides permission, checks meaning against real data, and shows before it acts

**Status**: **ACCEPTED (2026-10-06)**. Arch-authored; **PM confirmed the division** on 2026-10-06 (via Exec): *"I agree with the division Arch laid
out, wish we'd stated this a year ago (live and learn) and want it baked into our architectural design docs, domain models, dependency diagram, etc."*
**Author**: Chief Architect (arch)
**Deciders**: PM (direction); Architect (author); Lead (the args flip and binder retirement); CXO (the confirm and disclosure copy).
**Related**: **ADR-059** (workflow-dispatcher rail; floor-first) · **ADR-077** (routing integrity) · **ADR-078 D4** (the classifier/router is stateless) ·
**ADR-079** (owner-scoping) · **#1595** (epic 0, the Inversion) · **#1943** (router args for complete_todo and the clear family) · **#1942** (one Intent
shape across paths) · **#1190** (destructive confirm) · **#1509/#1510** (consent gate) · **#1677** (write allowlist). Source memo:
`docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-2026-10-05.md`. Standing procedure: the "Deletion and rail procedure"
section of `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

---

## Context

For a year, two different kinds of deterministic code grew around the LLM and were discussed as one thing. **Permission code** decides what is
*allowed* and makes it safe: identity, data ownership, consent and confirmation, a single dispatch path, honest refusals, CI and deploy gates.
**Interpretation code** decides what the user *meant*: regexes that guess which action, which items, which verb sense, which trailing noun is a
project name.

The 10-05 live round on alpha v169 showed the cost. Every interpretation failure came from interpretation code ("the first three" bound by a
single-position regex; a clear-family request completing a todo called "it"; "list my repos on github" read as a project named "github").
Meanwhile the router already extracted the right arguments on every turn into `context["inversion_args"]`, which nothing read. Epic 0 had moved
*which action* to the LLM (the pre-classifier ceiling fell 567 → ~120) but not *which things the action applies to*. PM: *"It sometimes feels like
we are mostly just encumbering an LLM with a bunch of limitations that are not providing any visible value."*

This ADR states the division once, so each new handler, rail entry and review can be judged against it.

## Decisions

**D1 — The LLM decides meaning.** Which operation the user wants, which items it applies to (ordinals, ranges, names, exceptions), which sense of
an ambiguous verb applies, and whether a turn answers a pending question or is a new ask: these are the router's to extract, carried as
structured args on the Intent. **New deterministic interpretation (a regex, keyword list or substring sniff that guesses user meaning) is not
added.** The default answer to a new failing phrasing is a corpus row and a description change, not a pattern (the extraction-ratchet corollary in CLAUDE.md).

**D2 — Code checks meaning against real data.** Before acting, code resolves the LLM's interpretation against the user's actual state: do those
items exist, are they the caller's, is the set unambiguous. This is **lookup, not guessing**. Anything that doesn't resolve is *asked about*, never
guessed and never silently dropped. An unparseable arg is an unresolved arg.

**D3 — Code decides permission.** Identity and owner-scoping (ADR-079), the effect class of each rail entry (one entry per effect class), the
#1509 consent gate, the #1190 confirm for destructive changes, the #1677 write allowlist, the live flag, and CI and deploy gates stay deterministic.
**The LLM is never asked whether something is allowed.**

**D4 — Code shows before it acts.** Any change touching more than one item, carrying an exclusion, or being destructive is confirmed with an
**enumeration of exactly what will and won't be touched** ("Complete A, B, C? Leaving D."). The confirm is what makes it safe to trust the LLM with
meaning: a misreading costs the user one "no" instead of a silently wrong action. After acting, the reply names what was done.

**D5 — Statelessness stays where it is (ADR-078 D4).** The router sees the message and the catalog, not session state. Anything that depends on what
was just shown (which list "the first three" refers to; the scope of a numbered list) is resolved by code in D2, from state code records.

**D6 — The interpretation layer only shrinks, mechanically.** The pre-classifier extraction ceiling (`TestExtractionPatternRatchet`) and the
floor-internal binder counts (`todo-floor-binding`, `reminder-clear-binding`, 26 at introduction on 2026-10-05) only go down. Each args flip
retires the binders it replaces in the same lane.

## Consequences

- **Handlers** consume `inversion_args` (resolved per D2) instead of re-parsing the message. The 1-item case may act directly; 2+, exclusions or
  destructive effects go through the enumerating confirm (D4).
- **Verb-ambiguous families** (e.g. "clear") become a router operation shaped as a **resolver entry**: it mutates nothing, resolves the verb (ask,
  or the user's stored default), and re-enters the rail as the concrete op, so that op's own permission gates apply (D3).
- **"Ready to test"** means a live probe of real user phrasings asserts the **served answer**, not the route.
- **Every catalog change** (new rail entry, changed description) is scored on the full corpus in the same lane, because meaning is chosen from the whole catalog.
- **What stays deterministic, permanently**: D2's resolution, D3's permissions, D4's confirmations, honest-refusal copy, and the gates. These are
  boundaries, and they are cheap to keep.

## How to apply this ADR (review checklist)

1. Does this change add code that guesses what the user meant? → Not allowed (D1). Use a corpus row plus a router description, or args.
2. Does a handler act on an interpretation without resolving it against real data? → Add D2 resolution, and ask on anything unresolved.
3. Does a multi-item, excluding or destructive change act without an enumerating confirm? → D4.
4. Is the LLM being asked a permission question? → Move it to D3 code.
5. Does the change make the router depend on session state? → D5; resolve it in code.

## Open questions

- Which write operations follow complete_todo and the clear family, and in what order, is sequenced in #1595's scope doc, not here.
- Whether the #1631 prose floor on answer turns retires per carrier once that carrier's answers carry structured args (Arch's 10-05 (b): yes, per carrier, not before).
