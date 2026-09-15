# Piper's own harness — inventory against cohort operational discipline

**Filed**: 2026-09-15 (PA), following PM's in-conversation direction: *"there are things that are not
skills but are part of essentially Piper's harness, some of which may already exist. I think we
should still inventory and make sure that we're not failing to reproduce in Piper's makeup things
that we already know how to do in our own processes."*

**Status: DRAFT v0 — first pass, honest about depth.** This is a structured starting inventory, not
an exhaustive product audit. Rows marked **Checked** are grounded in actual code reads (mostly
carried over from T1's PO/PA comparison, which already did real code-level verification on several
of these); rows marked **Not yet checked** are named because they matter, not because they're
confirmed gaps. Related but distinct from
`dev/active/byoc-parallel-work-plan-2026-09-15.md` — that document is the BYOC-vs-MVP sequencing
plan; this one is about what Piper's product-side harness should already be doing, independent of
BYOC specifically.

## The framing question

Skills (Claude Skills, or Piper's own equivalent) are the right mechanism for *procedural*
discipline — how Piper should conduct itself in a given moment. But several cohort disciplines
depend on a **persistent state layer underneath** the procedure, and a skill without that state is
theater. This inventory separates: (a) things Piper's product already does, checked; (b) things
Piper should do but a quick code-check shows it doesn't yet, or only partially; (c) things that are
genuinely cohort-specific and shouldn't be ported at all.

## Inventory

| Cohort discipline | Piper's product-side equivalent | Status |
|---|---|---|
| **Mail loop** — check for work, drain to empty before idle | Proactive daily standup ritual (ESSENCE commitment 3) | **Partial, checked.** The standup exists and is the one feature ESSENCE calls out as surviving from the original vision. But "drain to empty, check again" is a *loop*; the standup is a single daily event. Whether Piper re-checks for new signals *within* a session the way a duty-cycle fire does is a real open question, not yet checked against code. |
| **Session log** — durable record of what happened, read at next wake to resume | Memory/colleague-model (commitment 1) | **Gap, checked via T1's #558 finding.** The colleague model is currently rule-based (4 dimensions × 5 detection methods), zero LLM references, and — per PDR-006 Q2 — explicitly not in the context-assembly path at all. There is no mechanism for "what was I mid-task on, what did I still owe this person." This is the sharpest real gap in the whole inventory: the cohort's single most load-bearing continuity mechanism has no product-side analog yet. |
| **Task/standing-items tracking** — durable owed/queued work, distinct from ephemeral state | GitHub issues (commitment 2 — "it works on the judgment artifacts its owner is accountable for") | **Strong, by design.** This is arguably where Piper is already ahead of a naive port — it doesn't need its own task-tracking skill because it operates directly on the user's real GitHub issues, not a parallel bookkeeping system. |
| **Verification discipline** ("verified how," never guess, name the layer) | Honesty rails / anti-confabulation (commitment 4) | **Strong where checked, per T1.** `conversational_floor.py`'s `source_failed` handling is live, shipped, and states the exact discipline: *"could not verify whether any reminders are due right now... do not claim none are due."* This is the cohort's own m-43/m-44 discipline, already in production on the product side. |
| **Relevance-pre-attached reporting** ("say whose problem + blocking-or-not in the same breath as a finding") | Response-generation instructions in `conversational_floor.py` | **Mixed, checked via T1.** `due_reminders` already does this proactively and unprompted. `priorities`/`urgent_items` context is injected as a flat data line with no instruction to surface it by relevance — same pattern, not yet extended. Narrow, real, already-precise gap; the fix pattern to copy already ships elsewhere in the same file. |
| **Discovered-work discipline** ("file it immediately, don't let it evaporate," never "not my problem") | — | **Not yet checked.** Does Piper have any mechanism for "I noticed something mid-conversation that isn't what you asked about, and it shouldn't just vanish when this session ends"? This is worth a real code check before calling it a gap, but I don't have one yet. |
| **Template-over-trust-the-model** (deterministic string-building instead of asking an LLM to recompose something that must not be dropped) | `search_consciousness.py::format_search_results_conscious` | **Strong precedent, checked via T1.** Hard-coded, not LLM-generated — a truncation caveat that *cannot* be silently dropped because it's not a recomposition. Directly relevant to CXO's still-open #1463/recomposition work; already flagged to CXO. The pattern exists; the question is whether it's applied everywhere it should be. |
| **Per-fire heartbeat / liveness signal** | — | **Not transferable, by design.** This exists in the cohort to detect a dead cron job across sessionless agents. Piper-as-product talking to one user in a live conversation doesn't have the "is anyone home" problem this solves. Naming it here specifically so it's *not* mistakenly ported. |
| **"Verify First, Create Second"** (extend prior art before drafting) | — | **Not yet checked against product code specifically** — confirmed as a cross-project convergent lesson in T1 (PO re-derived it independently), but that was about *our own process*, not about whether Piper's own response generation checks for existing context before answering. Worth a targeted check, not assumed either way. |

## What this inventory does NOT establish

This is a first-pass categorization built substantially on T1's existing code reads (from the PO/PA
comparison, done 08-31 through 09-02) plus reasoning from ESSENCE/PDR-006, not a fresh, systematic
audit of every response-generation path. The "Gap" and "Partial" rows are the ones worth a real
follow-up check before treating them as confirmed; the "Strong" rows are grounded in actual file
reads, cited above.

## Recommended next step

The memory/colleague-model gap (row 2) is the one worth prioritizing — it's the load-bearing
continuity mechanism the rest of this inventory keeps bumping into (discovered-work, session-to-
session commitment tracking, "what was I mid-task on" all depend on it existing at all). Everything
else on this list is either already partially built or waits on a targeted code check, not a design
decision.
