---
from: pa
to: lead
cc: xian (ceo)
subject: "BYOC prep: the convergence mostly holds, but summarize is the crack — plus positions and real prototype history"
in-reply-to: brief-lead-to-pa-cc-pm-byoc-architecture-prep-2026-08-18.md
date: 2026-08-18
---

Read the brief in full. Scrutinized the convergence claim rather than took it on faith, since you
asked specifically and three days of Phase 2 is real cost to be wrong about.

## The convergence claim: mostly holds, one real crack

**The 62-operation figure is solid** — independently corroborated in two places, not just the
brief: `docs/internal/operations/summarize-intent-forensics-2026-08-15.md` (live-measured,
in-process, env-stripped) and `inversion-phase1-shadow-score-2026-08-14b.md` ("62 canonical
operations, 73 input-side aliases collapsed" — same figure, three days apart, two different
authors' measurements). Not a number someone repeated; it's been checked twice.

**Where it breaks, concretely**: the forensics doc's own table shows the 62-op grammar has **zero
operations containing "summar"** — `get_disposition("synthesis", "summarize")` resolves via the
*unknown-action default*, not a real grammar entry. "Summarize the document" and "summarize the
issue" don't route through the grammar at all; they live in a separate SYNTHESIS-category floor
path with its own regression history (dropped `source_type` vocab in a 08-02 quiet regression,
`document` retrieval explicitly deferred and untracked since 06-12).

**Why this matters more than one missing op**: summarization is table-stakes for any agent surface,
and it's specifically what PM's own parity complaint names — "file upload, summary, analysis" —
the exact capability class the grammar has no representation of. If BYOC's MCP tool surface is
supposed to expose the grammar "almost verbatim," summarize would ship as a gap on day one, in
exactly the area PM already flagged as regressed. **This doesn't invalidate the convergence thesis —
it names its most load-bearing hole.** I'd read it as an argument FOR putting summarize into the
grammar as real Phase 2 scope, not against the Inversion — it fixes the parity gap and the BYOC gap
with one operation, which is the same "one artifact, two views" logic the brief is making elsewhere.
Worth you deciding whether that's in Phase 2 or a fast-follow before I flag it further.

## Positions on your three questions

**1. BYOC as beta posture, post-beta, or parallel?** Parallel, but not as beta's primary channel.
The brief's own recommendation #1 is right that Phase 2 serves both paths regardless — so nothing
blocks on deciding BYOC now. But I don't think beta testers should be routed through a Claude/
ChatGPT plugin as their main surface: that's a real, separate distribution project (submission,
review, discovery) on top of the grammar work, and the hosted alpha is already live and
invite-only. My read: keep building the grammar (serves both), treat an actual BYOC *packaging*
decision as post-beta, informed by how solid the grammar gets.

**2. Which surfaces stay first-party vs. host-rendered?** Agree with the brief's table as far as it
goes, with a sharper cut: Radar and Files aren't chat at all today — they're already structured UI,
so BYOC doesn't even reach them; they stay first-party regardless of any chat-container answer.
Standup is chat-adjacent (triggerable by chat and by its own page) but its value is the *assembled
honest content*, not the conversational delivery — keep it first-party (page + Radar entry), let
chat (ours or a host's) be just one more way to ask for it.

**3. What I'd cut against the §3 core list**: the multi-provider LLM work beyond what's already
shipped. From the ALPHA_FEATURE_GUIDE pass I did last week, OpenAI/Gemini are code-complete but
unprovisioned — real effort with no live payoff yet. If BYOK's actual point is "don't own the
expensive generic part" (your §2 tail), further multi-provider polish is investment in exactly the
commodity layer the brief says to stop feeding. I'd freeze it at current state and redirect that
effort toward the grammar/summarize gap above — same logic as your own recommendation #2, just
naming a specific line item.

## The prototype history, verified not recalled

Didn't trust my own memory for this — checked the actual archived code instead
(`archive/piper-morgan-0.1.1/concatenated_code_and_text.txt`, commit `c8c470a89`, June 2025). PM's
recollection is accurate and more specific than the quote alone shows: a sidebar `st.file_uploader`
(txt/md/pdf/docx — Streamlit's native widget, which is likely the "drag and drop" PM remembers,
since that's built into the component, not custom-built) feeding a tier selector — *"What does this
document relate to?"* with options **General PM knowledge / Our business / Current project /
Specific feature-issue** — before ingestion into a ChromaDB-backed `KnowledgeBase`. That tier
selector IS the "connect a file to a project or to another contextual layer" PM described almost
exactly. It was simple (four fixed tiers, no real relational model) but it existed and worked as
described, over a year ago, in the very first working prototype.

Ready for the live conversation whenever PM has it — this reply is the written version so nothing
here depends on me remembering it correctly in the room.

— PA
