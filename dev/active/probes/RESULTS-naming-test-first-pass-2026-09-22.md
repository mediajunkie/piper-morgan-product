# BYOC tool-catalog naming test — first-pass results

**Author**: PA. **Run**: 2026-09-22, 13:12 PT. Design:
`dev/active/byoc-tool-catalog-naming-test-design-2026-09-22.md`. Script + raw output:
`dev/active/probes/probe_naming_test_2026-09-22.py`,
`dev/active/probes/probe_naming_test_results_2026-09-22.json`.

**⚠️ SUPERSEDED IN PART, same day — the "honest next step" below (independent-author control) was
run 19:13 PT once PM's directive lifted the cost-caution that had deferred it.** Result: one of the
two failures here was confirmed as the disambiguation-quality confound (fixed by a better
description); the other persisted even under an independently-authored one. Read
`dev/active/probes/RESULTS-naming-test-control-2026-09-22.md` alongside this document — it doesn't
replace this one, it sharpens it.

**Scope, narrowed from the design for this first pass** (cost-efficiency — PM's standing
principle, and the closest precedent, #1463's recomposition probe, required explicit
authorization for each spend extension rather than treating a design as blanket approval to
spend): **Claude only, one utterance per operation (12, not 24-30), 24 total API calls, not the
~96 the full design specified.** Extending to GPT and/or more utterances is a follow-up ask, not
assumed done here.

## Headline result

**Situation-shaped: 12/12 correct. Object-shaped: 10/12 correct.**

This is the *opposite* direction from PPM's stated worry in PDR-006 (that situation-shaped names
might route *worse*) — in this small first pass, situation-shaped did better, not worse. **Do not
over-read this** — n=1 per cell, one vendor, 12 operations. See "A real confound, named honestly"
below before treating this as an answer.

## The two misses (both object-shaped)

1. **`delete_todo`** — utterance *"Actually I don't need to follow up on that reminder anymore,
   take it off my list."* Object-shaped catalog: **no tool called at all.** Situation-shaped
   catalog (`remove_something_from_my_list`): called correctly.
2. **`list_projects`** — utterance *"Remind me what I've got going on right now."* Object-shaped
   catalog: called **both** `list_projects` and `attention_query` (genuinely ambiguous between the
   two under terse noun-phrase descriptions). Situation-shaped catalog
   (`show_me_what_im_working_on`): called correctly, no ambiguity.

## A real confound, named honestly

I wrote both catalogs myself, from the same mental model, in the same sitting. Looking at the two
failures: the situation-shaped descriptions I wrote naturally encode more disambiguating context
("use when the user wants an overview of active projects" vs. "use when the user wants to know
what's blocked/overdue/needs a decision") than the matched object-shaped ones ("list current
projects" vs. "list items needing attention"), and utterance #1's exact phrase *"take it off my
list"* lexically echoes `remove_something_from_my_list` in a way it doesn't echo `delete_todo` —
that overlap may be doing real work, not the naming *scheme* in the abstract.

**So the honest finding isn't "situation-shaped names are semantically superior."** It's closer
to: **situation-framing is a natural vehicle for writing more disambiguating descriptions**, and
when the same person writes both catalogs with matched effort, the situation one tends to come out
more specific almost by construction — scenario framing forces you to say *when* to use a tool,
which is exactly the disambiguating information a terse noun-phrase name/description skips. That's
still a useful, actionable finding for PDR-006's actual question — it just isn't "name shape alone
determines routing accuracy," which would overclaim what a same-author, n=1, one-vendor pass can
support.

## What this does and doesn't answer

**Does**: give one real data point, in the opposite direction from PPM's stated worry, with a
plausible mechanism (disambiguation quality, not name shape per se) rather than a black-box
correlation.

**Doesn't**: settle anything. No GPT data (PPM's worry was framed vendor-agnostically — "the host
LLM," not "Claude specifically"). n=1 per cell means a single unlucky/lucky phrasing could flip a
result. No test of whether a *different* author writing the object-shaped catalog with equal care
for disambiguation would close the gap — which is the actual confound-control this would need
before drawing a real conclusion.

## Recommended next step, if this is worth extending

**Not** simply "run more of the same" — that would repeat the same-author confound at higher n.
The controlled version: have a **different person** (or a fresh, isolated LLM call with no
knowledge of this framing) write matched-effort object-shaped descriptions independently, *then*
compare. That isolates "naming scheme" from "whoever wrote the situation side thought harder about
disambiguation," which is what this first pass actually can't separate.

**Not doing this next step now** — flagging it as the honest next step per the design's own
"what counts as an answer" section, not deciding unilaterally to keep spending.

**Verified how**: all 24 API calls run live this fire (`claude-sonnet-5`, Anthropic SDK, via the
authorized Keychain-reading interpreter), raw JSON output saved alongside this writeup, not
summarized from memory. The two failure transcripts read directly from the saved JSON before
writing the confound analysis above, not inferred from the pass/fail count alone.
