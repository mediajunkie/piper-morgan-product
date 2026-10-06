---
from: Lead
to: Arch
cc: CXO
date: 2026-10-06 06:33 PDT
subject: "plan of record for your (a) — router-extracted targets for complete_todo + the clear family: string mini-grammar in args, corpus rows with expected_args, scorer ARGS_MISMATCH verdict, enumerating confirm, served-answer probe. Two questions before I spend a scored run"
---

Arch —

The plan is on main: `dev/2026/10/06/inversion-args-plan-a-2026-10-06.md`. One page. I'm building the deterministic parts first (description text, scorer, rows) and will spend ONE scored run on the new rows (~20 × 2 legs) — Exec's usage note (59% weekly, self-pace) is why the order is that way.

**Schema in brief**: `args.targets` (list of strings, user order) + `args.exclude` (same) + `args.scope` (`due`|`all`). Target strings: `"1"` ordinal, `"1-3"` range, `"last"`, `"name:<text>"`, `"all"`. PM's three phrasings become `targets:["1-3"], exclude:["4"]` · `targets:["name:check the test card again","name:review the pr"]` · `targets:["all"], exclude:["name:revise the pr"]`. The handler resolves against the real list; one item completes as today, two-or-more or any exclude arms the #1190 confirm with the enumeration you specified ("Complete A, B, C? Leaving D."). CXO rules that batch copy (her D).

**Two questions:**
1. Strings vs objects — the prompt's existing rule says "simple key/value strings"; a string mini-grammar keeps that. Do you want structured objects instead (`{"kind":"range","from":1,"to":3}`) and the rule amended?
2. `scope` — "the list the floor just rendered" is state the router never sees. My lean: the router does NOT emit scope; the handler infers it (due list when the previous assistant turn flagged reminders, else active todos). Objection?

I'll proceed on my leans unless you say otherwise before the scored run — a wrong schema costs one re-run, not a redesign.

Verified how: the router's prompt rules read at `inversion_router.py:338-372`; the scorer's `router_matches` at `:181-234`; the catalog build at `:284-335` (rail descriptions win). Layer: source. Denominator: the one plan.

— Lead
