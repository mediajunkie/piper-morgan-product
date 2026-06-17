---
name: synthesize-feedback
description: Distill themes from raw user feedback — interviews, support tickets,
  surveys, reviews, research notes — into prioritized themes with evidence, severity,
  and roadmap recommendations grounded in your actual product. Trigger phrases: "synthesize
  this feedback", "what are users saying", "analyze these interviews", "themes from
  this research", "what should we build based on this".
scope: cross-role
version: 1.0
created: 2026-06-15
---

# synthesize-feedback

Turn a pile of raw user feedback into prioritized themes with evidence and actionable recommendations — grounded in your actual roadmap, not generic PM advice.

The difference from just asking Piper: this skill produces a **consistent output shape** (themes with frequency, severity, product position, and recommendation for each), **distinguishes signal from noise** (volume ≠ severity), and **grounds recommendations in what you're already building** rather than treating the roadmap as a blank slate.

## When to Use

- You have a body of raw feedback to make sense of: user interviews, support tickets, survey responses, app store reviews, research session notes, Slack/Discord messages from users
- PM asks "what are users actually asking for?" or "what should we prioritize based on this?"
- You want to close a research spike with a deliverable that can drive roadmap decisions
- You're preparing for a planning session and need to translate user signal into concrete inputs

**Not for**: a single piece of feedback (just respond to it directly). Not for internal team feedback (different dynamic — use a retro or `sprint-wrap`). Not for quantitative analytics (different skill — `metrics-review`).

## The Core Insight

**Volume ≠ severity.** The loudest signal in user feedback is rarely the most important one. Many users mentioning something means it's visible — it doesn't mean it's blocking, painful, or worth building. The synthesis has to distinguish:
- **Frequency**: how many users raised this
- **Severity**: how much does it hurt when it happens
- **Scope**: is this niche (power user only) or universal

A single user unable to do their job because of X is a higher-severity signal than ten users requesting a nice-to-have. Both matter; neither should be lost; they need different responses.

## Procedure

### Step 1 — Receive and orient to the source material

Before synthesizing, understand what you're working with:

**Source type** shapes what you can and can't conclude:
| Source | Strength | Limitation |
|---|---|---|
| User interviews (structured) | Rich context, can probe why | Small N; interviewer bias |
| Support tickets / email | Real pain, self-selected urgency | Over-represents power users + failures |
| Survey (open-ended) | Broader N; less prompted | Shallow; hard to probe |
| App store reviews | Unfiltered sentiment | Negative-skewed; no context |
| Research session notes | Behavioral + attitudinal | Requires careful reading |
| Slack/Discord | Spontaneous; community signal | Noisy; vocal minority |

Note the source type in your synthesis — it affects how much weight each theme should carry.

**Ask PM if not obvious:**
- What decision is this synthesis feeding? (roadmap prioritization? go/no-go? scope a feature?)
- Is there a milestone or sprint this needs to inform?
- Are there themes you already expect to see? (avoids confirmation bias in the other direction)

### Step 2 — Read all source material before coding any themes

**Read everything first. Code nothing yet.**

This is the most important discipline in synthesis. If you start labeling themes in the first pass, you anchor on the first things you read and miss patterns that only become visible across the full corpus. Read, mark interesting passages, hold themes loosely — then name them in Step 3.

For large corpora (>20 items), do a first-pass skim to understand the shape, then a second-pass read for coding.

### Step 3 — Identify and name themes

After reading the full corpus, cluster the signals you noticed into themes. Good themes are:
- **Named with a verb-noun**: "Can't find X", "Wants Y to work like Z", "Confused by W"
- **Distinct**: minimal overlap between themes (if two themes keep appearing together, they may be one theme)
- **Grounded**: supported by at least 2 independent data points
- **User-facing**: about what users experience, not about what you'd build

Typical theme count: 4–8 for a healthy corpus. Fewer than 4 suggests you may be lumping; more than 8 suggests you may be splitting.

For each theme, capture:
- Representative quote(s): exact or near-exact language from source material
- Frequency: how many sources raised it (rough count or %)
- Severity: high (blocks core task) / medium (causes friction) / low (nice-to-have)
- Who: any notable pattern in which users raise this (segment, tenure, use case)

### Step 4 — Load Piper's product context

Before writing recommendations, check what you know about the current product:
- What's already in the roadmap (MVP, Fast Follow, Post-MVP)?
- What features already exist that might address this?
- What's in flight that PM may not have mentioned?

If running with server access: pull Piper's product profile + current sprint state.
If running natively: use conversation context. Note what you couldn't verify.

This step exists so recommendations say "this is Fast Follow scope, already tracked" instead of "we should build this" when it's already planned.

### Step 5 — Write the synthesis

Use the template below. Every section is mandatory.

```markdown
# Feedback Synthesis: [Source description] — [Date]

**Source**: [What was synthesized — e.g., "8 user interviews, April–May 2026"]
**Synthesized by**: Piper
**Decision this feeds**: [e.g., "Q3 roadmap prioritization" or "feature scope for WEEKLY-DIGEST"]
**Confidence**: [High / Medium / Low — see §Signal Quality]

---

## Executive Summary

[2–3 sentences. Top 2–3 themes, their severity, and the single most important recommendation.
Write this last.]

---

## Themes

### Theme 1: [Verb-noun name]

**Frequency**: [N of M sources / ~X%]
**Severity**: [High / Medium / Low]
**Who**: [Any segment pattern — or "across all users"]

**What users say** (representative quotes):
> "[Exact or near-exact quote from source material]"
> "[Second quote if available]"

**Pattern**: [2–3 sentences synthesizing what's underneath the quotes. Why does this happen? What's the user trying to do when they hit this?]

**Current product position**: [Does Piper already handle this? Is it in the roadmap? Where?]
- [Already exists in: X feature] OR [In Fast Follow scope: #N] OR [Not currently tracked]

**Recommendation**: [One of: File issue | Accelerate existing work | Update roadmap | Investigate further | Park — no action now]
- [Specific next step: e.g., "File as P1 Fast Follow — this blocks the core weekly review workflow"]

---

### Theme 2: [Verb-noun name]

[Same structure as Theme 1]

---

[Repeat for each theme, ordered by severity × frequency — highest impact first]

---

## Signal Quality

[Be honest about what this synthesis can and can't conclude.]

| Dimension | Assessment |
|---|---|
| Source diversity | [Did feedback come from multiple independent sources, or one channel?] |
| Sample size | [N = X — large enough to trust? Or directional only?] |
| Recency | [When was this collected? Is it still current?] |
| Interviewer/selection bias | [Any known skew in who provided feedback?] |
| Confidence | [High: clear signal, multiple sources, consistent severity / Medium: directional, warrants investigation / Low: one data point, needs validation] |

---

## Recommended actions

[Prioritized by urgency × impact. Be specific.]

| Priority | Action | Theme | Owner | Notes |
|---|---|---|---|---|
| 1 | [File issue / Accelerate #N / etc.] | [Theme name] | [PM / Lead Dev / etc.] | [Why this priority] |
| 2 | [Action] | [Theme] | [Owner] | |
| 3 | [Action] | [Theme] | [Owner] | |

---

## What to file

[Issues or roadmap items this synthesis recommends creating or updating. Use `draft-issue` for each.]

- [ ] [New issue: SLUG — brief title — Priority and milestone]
- [ ] [Update existing issue #N: add evidence from this synthesis]
- [ ] [Or: "No new issues recommended — existing roadmap addresses findings"]

---

## Signals not synthesized into themes

[Things that came up but didn't rise to theme level — single mentions, outliers, or out-of-scope items. Don't discard them; park them here so they're findable.]

- [Item] — [Source] — [Why not a theme: single mention / out of scope / already tracked as #N]

---

## Open questions

[What would you need to know to be more confident in these recommendations?]

- [Question] — [How to answer it]
```

### Step 6 — Show PM the synthesis and proposed actions

Walk PM through:
- The top theme and why you ranked it highest
- Any theme where your confidence is low (where you'd want more data before acting)
- The recommended actions — PM confirms, reprioritizes, or parks them

Then use `draft-issue` to file any issues PM approves.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| List quotes without synthesis | Quotes ≠ themes; PM still has to do the sense-making | Name the pattern, then support with quotes |
| Treat all themes as equally important | Not all feedback deserves equal response | Order by severity × frequency; be explicit about relative weight |
| Recommend building something already planned | Wastes PM's attention; creates false sense of new signal | Check the roadmap first (Step 4); say "already in scope at #N" |
| Conflate volume with severity | 10 nice-to-haves < 1 job-blocker | Report frequency and severity separately |
| Skip the Signal Quality section | Synthesis without epistemic humility is overconfident | Always note source limitations |
| Skip the "not a theme" section | Single mentions get lost; they may matter later | Park them explicitly |
| Write the Executive Summary first | You don't know what the top themes are yet | Write it last |

---

## Quality checklist

Before showing the synthesis to PM:
- [ ] Read all source material before coding themes (no first-pass anchoring)
- [ ] Themes are verb-noun named and distinct
- [ ] Each theme has at least 2 data points
- [ ] Frequency and severity are reported separately for each theme
- [ ] Roadmap context is checked — no redundant "we should build this" recommendations
- [ ] Signal Quality section is honest about limitations
- [ ] "Signals not synthesized" section captures outliers
- [ ] Executive Summary was written last

---

## Example

**Input** (from PM):
> "Here are notes from 5 interviews I ran with PMs who tried Piper last month. Can you tell me what's coming up and what we should do about it?"

**Source material** (paraphrased):
- Interview 1: "I kept asking it things and it would give me these general answers. I wanted it to know that I'm working on a B2B SaaS product, not a consumer app."
- Interview 2: "The first time I used it, I didn't know what to ask. Like, what does this thing do? I needed examples."
- Interview 3: "Once I figured out the right questions to ask, it was great. But it took me like a week to get there."
- Interview 4: "I wanted to connect it to my GitHub but I couldn't figure out how. So I just gave up and use it for general questions."
- Interview 5: "I use it every Monday to plan my week. I wish it would just send me something — like a digest — instead of me having to remember to open it."
- Interview 1 (second quote): "It forgot what I told it last time. I had to re-explain my product again."
- Interview 3 (second quote): "I connected GitHub but then when I asked about my sprint it didn't seem to use it."

**Synthesis output**:

```markdown
# Feedback Synthesis: 5 PM interviews (May–June 2026) — 2026-06-15

**Source**: 5 user interviews, PM personas, May–June 2026
**Synthesized by**: Piper
**Decision this feeds**: Wave 1 priorities + onboarding design
**Confidence**: Medium (small N; same PM type; no quantitative validation)

---

## Executive Summary

Three themes dominate: PMs don't know what to ask Piper (onboarding gap), context doesn't persist across sessions (memory gap), and connectors are hard to wire (setup friction). The highest-severity finding is context loss — PMs who invest in explaining their product feel burned when they have to repeat it. Onboarding and connector setup are the practical preconditions. Recommended: accelerate `meet-piper` connector step (already in Wave 1) + file an issue for in-session context examples.

---

## Themes

### Theme 1: Context doesn't persist — "I had to re-explain my product"

**Frequency**: 3 of 5 sources
**Severity**: High — directly undermines the "colleague who knows you" value prop
**Who**: All three are multi-session users (have used Piper more than once)

**What users say**:
> "It forgot what I told it last time. I had to re-explain my product again."
> "I kept asking it things and it would give me these general answers. I wanted it to know that I'm working on a B2B SaaS product."

**Pattern**: Users expect Piper to carry context across sessions — that's the core promise. When it doesn't, they feel like they're starting over. This isn't a feature gap so much as a trust break: they invested in telling Piper about their world, and that investment disappeared.

**Current product position**: meet-piper stores a profile server-side (MVP). Gaps: the profile isn't being surfaced back to users on re-engagement, and GitHub context isn't persisting from the connector step.

**Recommendation**: Accelerate existing work
- meet-piper connector step (Wave 1) addresses the GitHub gap
- File issue: `CONTEXT-RECAP` — on re-engagement, Piper opens with a one-line context recap ("You're working on [product] with [team]. Last week...") to signal memory is working

---

### Theme 2: Onboarding — "I didn't know what to ask"

**Frequency**: 3 of 5 sources
**Severity**: Medium — causes abandonment before users discover value
**Who**: All three are first-week users

**What users say**:
> "The first time I used it, I didn't know what to ask. Like, what does this thing do? I needed examples."
> "Once I figured out the right questions to ask, it was great. But it took me like a week to get there."

**Pattern**: Piper's value is gated on knowing how to prompt it well. First-time PMs don't have that mental model yet. A week is a long time to invest in learning before seeing value — most will churn before they get there.

**Current product position**: meet-piper runs an interview but doesn't proactively teach question patterns. No in-product examples or starter prompts.

**Recommendation**: File issue
- `STARTER-PROMPTS` — after meet-piper, Piper offers 3 example questions tailored to what PM just shared ("Based on what you told me, you might ask..."). P2 Fast Follow.

---

### Theme 3: Connector setup is invisible and opaque

**Frequency**: 2 of 5 sources
**Severity**: Medium — blocks enrichment-dependent features; users give up and work around
**Who**: Two users who attempted GitHub connection

**What users say**:
> "I wanted to connect it to my GitHub but I couldn't figure out how. So I just gave up."
> "I connected GitHub but then when I asked about my sprint it didn't seem to use it."

**Pattern**: Two separate failure modes: (1) can't find the connection flow at all, (2) connected but no visible feedback that it's working. Both produce the same outcome: user stops relying on enrichment.

**Current product position**: connect-piper is Wave 1 scope. The "connected but not working" symptom is the consult-piper enrichment gap (Cowork: no GitHub; Code: payload error).

**Recommendation**: Accelerate existing work
- connect-piper (Wave 1) addresses setup
- File issue: `CONNECTOR-FEEDBACK` — after connecting, Piper confirms with a live test ("Connected. Here's one thing I just pulled from your GitHub...") so PM knows it's working.

---

### Theme 4: Proactive delivery — "I wish it would just send me something"

**Frequency**: 1 of 5 sources
**Severity**: Low for now (one user); Medium-high for the long game (weekly digest is the recurring touchpoint that drives engagement)
**Who**: Single power user; Monday-morning planning workflow

**What users say**:
> "I use it every Monday to plan my week. I wish it would just send me something — like a digest — instead of me having to remember to open it."

**Pattern**: The most engaged user is the one who wants Piper to be proactive. This is a leading indicator of what engaged PMs want once they're past onboarding.

**Current product position**: WEEKLY-DIGEST is a draft spec (2026-06-15); not yet in the roadmap formally.

**Recommendation**: File issue
- `WEEKLY-DIGEST` — P2 Fast Follow; add to roadmap. The single mention is directionally consistent with product strategy (proactive + trust gradient). Don't over-index; single data point.

---

## Signal Quality

| Dimension | Assessment |
|---|---|
| Source diversity | Single channel (PM interviews); all recruited similarly — likely similar PM profile |
| Sample size | N=5 — directional only; don't make high-conviction roadmap bets from this alone |
| Recency | May–June 2026; current |
| Selection bias | All tried Piper voluntarily; non-adopters not represented; success bias likely |
| Confidence | Medium — consistent themes across 5 sources, but small N and single channel |

---

## Recommended actions

| Priority | Action | Theme | Owner | Notes |
|---|---|---|---|---|
| 1 | Accelerate meet-piper connector step | Context loss + Connector setup | Lead Dev | Already Wave 1; this synthesis confirms urgency |
| 2 | File `CONTEXT-RECAP` issue | Context loss | xian | In-session signal that memory is working; P1 |
| 3 | File `CONNECTOR-FEEDBACK` issue | Connector setup | xian | Confirmation UX after connecting; P2 |
| 4 | File `STARTER-PROMPTS` issue | Onboarding | xian | Post-meet-piper examples; P2 Fast Follow |
| 5 | Add WEEKLY-DIGEST to roadmap | Proactive delivery | xian | P2 Fast Follow; already specced |

---

## What to file

- [ ] `CONTEXT-RECAP` — Piper opens re-engagement sessions with a one-line context recap — P1 MVP
- [ ] `CONNECTOR-FEEDBACK` — Confirmation + live test after connecting a connector — P2 Fast Follow
- [ ] `STARTER-PROMPTS` — Post-meet-piper: 3 suggested questions tailored to PM's profile — P2 Fast Follow
- [ ] Update `#WEEKLY-DIGEST` spec: add interview quote as evidence

---

## Signals not synthesized into themes

- Interview 5 mentioned wanting Piper on mobile. Single mention, out of scope for current platform decisions. → Park.
- Interview 2 mentioned wanting team features (shared context). Out of scope for single-PM MVP. → Park; relevant to enterprise roadmap.

---

## Open questions

- Does context loss happen because the profile isn't surfaced, or because it's not being used? Would need a session with a user + live session replay to distinguish. — PA to investigate with Lead Dev.
- Are the two "connected but not working" users on Cowork or Code? The enrichment failure mode differs. — Lead Dev action item.
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Wave 1 PM skill #4. Distinguishes volume from severity as the core synthesis discipline. Deployment: Native + Plugin.
