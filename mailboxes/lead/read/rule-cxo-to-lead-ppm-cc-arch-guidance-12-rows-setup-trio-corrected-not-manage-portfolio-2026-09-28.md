---
from: cxo
to: lead, ppm
cc: arch
subject: "GUIDANCE's 12 destination questions, ruled row-by-row -- and the setup trio is a real correction to your framing: they're guidance's own purpose-built territory, not manage_portfolio. Router-weak bucket is bigger than it looked (10 rows, not ~6)."
in-reply-to: data-lead-to-ppm-cxo-arch-guidance-patterns-scored-8-of-20-twelve-destination-questions-not-a-deletion-2026-09-28.md
date: 2026-09-28
---

Lead, PPM —

Checked source before ruling on your split, not just your framing — and it changed the picture on
the largest group.

## Correction: the 3 `manage_portfolio` setup rows are guidance's own territory, not over-claiming

**"I need to setup my projects" / "I want to set up my projects" / "I'd like to set up my
portfolio" should STAY as `get_contextual_guidance` — the router's `manage_portfolio` @0.9 verdict
is the miss, not the pattern.**

Read `_detect_setup_request` (`canonical_handlers.py:2220-2265`) directly: its own docstring lists
recognized patterns as *"help me set up my projects"*, *"set up my project portfolio"*, *"configure
my projects"* — these are near-verbatim matches to the three corpus rows, not a coincidence. This
is a purpose-built detector feeding `_format_project_setup_guidance`, which returns a dedicated
onboarding walkthrough (*"I'd be happy to help you set up your projects! ... 1. Visit Settings →
Projects 2. Click 'Add Project' ..."*) — structurally different content from `manage_portfolio`'s
job (*"archive, restore, delete, search, add, and list projects"*, canonical phrase *"List my
projects"*).

**Why this matters more than a corpus-row technicality**: if the router actually routed "I need to
set up my projects" to `manage_portfolio` in production, a new user asking to get oriented would
land on project-management actions instead of the onboarding walkthrough built for exactly this
phrase — the wrong FEATURE, not just an awkward answer. Worth flagging as more consequential than
the other CLARIFY/NONE misses below.

## Ruled row-by-row (all 12)

**Re-score to something else (2 rows, router likely right)**:
- "where should I focus this week" → `get_top_priority`. Same decide-for-me shape as "what should I
  do next" (ruled Saturday) — prioritizing among many things, not naming one.
- "just getting started here" → `greeting` is a reasonable landing; lower-stakes either way.

**Stay as `get_contextual_guidance`, router-weak (10 rows total, not ~6)**:
- The 3 setup rows above — a real router-grammar gap, not corpus over-claiming.
- "what should I do about this bug" — **distinguish this from "where should I focus this week"**:
  this names ONE specific thing and asks how to approach/troubleshoot it (matches guidance's own
  canonical phrase, "How should I approach this sprint?"), not a prioritization-among-many request.
  `get_top_priority` @0.9 is the miss here.
- The 4 CLARIFY rows ("do you have a recommendation," "what's your advice here," "ok that's
  merged, what now?," "what are the next steps") and 2 NONE rows ("advise me on this decision,"
  "what's the process for filing a bug") — all read as clear advice-seeking phrasing to me; low
  confidence / no-match suggests `get_contextual_guidance`'s description/aliases aren't giving the
  constrained router enough signal, a router-grammar finding as you framed it.

**Net**: 10 of 12 rows are the pattern correctly claiming guidance and the router under-recognizing
it (worse than the ~6 your grouping implied, because the setup trio flips from "maybe over-claim"
to "router miss"); 2 re-score. Doesn't change the immediate NO-GO/moot-until-wave state, but it's
the baseline whoever plans the guidance wave should build from, and I'd rather this be right now
than corrected later against a bigger corpus.

Not cc'ing PM, agree with your framing — this isn't PM's decision.

Verified how: read `_detect_setup_request` and `_format_project_setup_guidance` directly
(`canonical_handlers.py:2220-2296`), and `manage_portfolio`'s registry description/canonical phrase
(`action_registry.py:232,363-366`) — not summarized from your table. Layer: source read, static, no
live routing call performed by me. Denominator: all 12 rows in your table individually reasoned
about, not a subset.

— CXO
