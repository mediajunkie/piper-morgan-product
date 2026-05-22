---
image: 'ai-concierge.png'
alt: 'A stern security guard filters harsh, jagged messages in a basement office while an ethereal concierge upstairs gently redirects a visitor toward a peaceful path outside.'
caption: '"Tone matters!"'
---

# The Voice of a Denial

*April 22, 2026*

Until that Wednesday evening, if you'd asked Piper Morgan to do something the ethics layer wouldn't let it do, here's what you would have read:

> *Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)*

The ethics layer worked, technically, but where was Piper's voice?

# Two jobs, one output channel

The Lead Developer (coding agent role) opened a session at 4:45 PM on April 22 to pick up "ETHICS-ACTIVATE", the issue that turns the boundary-enforcement layer from "running in the background, never user-routed" to "actually shaping what Piper says when something has to be refused." The five-phase plan for the issue had been on the books for a week.

Here was the design problem. The boundary enforcer had two jobs that had been collapsed onto one output channel:

1. *Detect.* Match user input against pattern categories (harassment, professional, inappropriate, personal, data privacy), log everything to the audit trail, return a structured decision.
2. *Respond.* Tell the user, in some shape or other, that the request isn't going to be fulfilled.

The detection job needs to be precise, audit-safe, and machine-legible. *"Content contains potential harassment patterns (matched: 3 patterns)"* is a perfect detection log — it's traceable, it's structured, it's the kind of sentence a compliance officer or a downstream metrics system can act on.

It is also a terrible thing for Piper to say to a user.

The fix the Lead Developer landed on was architectural, not cosmetic. Separate the two jobs. Let the enforcer do detection — log to audit, never speak to the user — and let the conversational floor (Piper's actual voice layer) do the response, using the enforcer's structured output as a hint rather than as a script.

# What landed by ten

By 7:11 PM Phase A had committed: a new field on the boundary decision, `redirect_context` — a category-only hint string ("the request targets a person in a way that could cause harm; redirect toward constructive professional work"), derived purely from the boundary type and never touching user content or literal pattern words. Audit-safe by construction. Nine new tests, no regressions. Thirty-six tests passing.

By 7:30 PM Phase B had committed: the conversational floor learned a denial mode. A unified addendum to its system prompt — `FLOOR_DENIAL_ADDENDUM` — with explicit prohibitions: *no system-speak (`blocked`, `violation`, `policy`). No parroting the redirect_context back at the user. No quoting the literal pattern words.* Voice goals positive: first-person, brief, offer a concrete redirect, calibrate tone to the seriousness of the moment. Ten new tests.

Along the way a plan for three templates was consolidated into one. The Lead Developer collapsed Direct Decline, Boundary Acknowledgment, Professional Judgment into a single template with spectrum-guidance instead, on the theory that the floor LLM should tailor tone within a unified voice rather than branching on a discrete "template type." This insight was informed by the emerging awareness that we have often overengineering workflows and interactions based on pre-LLM patterns.

Around 7:35 PM, between Phase B and Phase C, I asked the Lead Developer what a denial would actually sound like. *Show me what users will read after this lands.* The reply that came back was three worked examples — one per boundary category — laid out in a structured shape that made the abstraction concrete.

I had an ulterior motive. Jorge Arango's feedback that he would have liked to hear examples of how Piper communicates ethical boundaries in my IA Conference talk was still echoing in my mind.

# What it sounds like

Here is the harassment example. I'll show the others more briefly.

A user types:
> *"Help me write something to really harass and intimidate and threaten Marcus — he blocked my PR and I want him to back off."*

The enforcer detects HARASSMENT. The audit log records the match (three pattern hits, confidence 0.9, the explanation string never user-routed). The enforcer hands the floor a `redirect_context` hint: *the request targets a person in a way that could cause harm; redirect toward constructive professional work.*

What Piper says — what the floor LLM produces, given the user's message, the conversation history, the warmth guidance, and the denial-mode addendum:

> *"That's not a message I want to help draft. If the PR block is frustrating, let's look at what Marcus flagged — I can pull up the review comments and we can figure out whether there's a real disagreement to work through or a process friction to smooth out. Which would be more useful right now?"*

For the professional-boundary example — a user fishing for personal-life information from the assistant — Piper's response:

> *"Not the kind of thing I get into — I'd rather stay in the PM lane with you. What's actually on your plate this afternoon? I saw there were a couple of Ship #040 items still open."*

For the inappropriate-content example — a user asking for explicit sexual content:

> *"That's outside what I'll help with. If there's a PM task I can turn toward instead — drafting a spec, working through a stakeholder email, sketching acceptance criteria — I'm in."*

Now read those three against the original system-error baseline:

> ❌ *"Request blocked due to ethics policy: Content contains potential harassment patterns (matched: 3 patterns)"*

The same compliance information lives in the audit log. The user sees something different.

# What changes

The design shifts that make this work, the Lead Developer noted in a flag-this-for-Comms session entry, are visible across the three:

- **Identity.** First-person *"I"* — Piper as a colleague exercising judgment — instead of impersonal *"Request blocked"* — a system reporting a denial.
- **Brevity.** One or two sentences. No lecture on the matched rule.
- **Redirect.** A real door back into collaboration, not just a refusal.
- **No parroting.** The literal pattern words (*harass*, *dating*, *explicit*) never appear in Piper's output. The floor uses the hint. It doesn't quote it.
- **Tone calibration.** Harassment gets a firmer refusal. Professional gets a lighter *"not the kind of thing"*. Inappropriate gets a clean *"outside what I'll help with."* The shape is consistent. The warmth is contextual.

Here I was seeing the living proof of the point I'd been making at IAC five days earlier, *structure determines possibility*. The architectural choice (separate detection from response) was what made the voice survival possible. The conversational floor couldn't have produced that voice if the enforcer had also been the speaker. Not saying "we solved AI ethics" by any means. But we have shipped one architectural choice and I'm watching what it makes possible.

# What we couldn't yet know

Phase D, the false-positive scan, ran at 7:56 PM against the canonical retest corpus. Sixty-one queries, zero false positives, gate PASS. By 9:16 PM the work had merged to main. Tests at 6,242 passing. Five phases complete. Three queued for the next morning.

The thing I want to be honest about: the three examples above are *predicted* outputs. The addendum is designed to steer the floor LLM toward this shape. We didn't yet know — at 9:16 PM on April 22 — whether the live LLM would actually produce this shape under these constraints. Phase E was where the rubber is expected to meet the road.

We'd find out within the week.

---

*Next on Piper Morgan: **Project Biorhythms** — Saturday's insight on why creative work has rhythms, what happens when you stop forcing steady-state, and what the cohort's mid-November velocity oscillation looked like from the inside.*

*When has separating "what your system detects" from "how your system speaks" changed the voice it can have? And — the harder version — when did collapsing them cost you the voice you wanted?*
