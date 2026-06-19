---
name: piper-stakeholder-update
description: >-
  Write a stakeholder update — progress, decisions, risks, next steps —
  calibrated to your audience (exec, team, investors, board). Draws on your
  project context. Trigger phrases: "write a stakeholder update", "draft an
  update for", "what should I tell [audience]", "write a status update".
---

# stakeholder-update

Draft a stakeholder update in PM's voice — one that knows your working style, your audience's priorities, and the current state of your product.

## Why this exists

Generic update templates produce generic updates. The difference between a useful stakeholder memo and one that gets skimmed:
1. **Voice match** — reads like the PM who wrote it, not like a template
2. **Audience calibration** — an exec update and a team update cover the same period but have completely different structures and emphasis
3. **Context grounding** — references the actual projects and decisions, not placeholder text
4. **Edit friction removal** — a well-calibrated first draft takes 2 minutes to tune, not 20

The goal is not to write the memo for PM — it's to produce a draft that PM edits, not rewrites.

## Stakeholder types and their defaults

Different audiences want different things. Piper calibrates by type:

| Audience | What they care about | Format | Lead with |
|---|---|---|---|
| **Exec / leadership** | What changed, what it means for strategy, what you need | Short, structured, no jargon, bullet-led | Decision or risk that needs their attention |
| **Team / peers** | What's shipping, what's blocked, what you need from them | Direct, detail-welcome, collaborative tone | What's happening this cycle and what's in flight |
| **Investors / board** | Trajectory, evidence of traction, honest state of risks | Polished, narrative arc, metrics-forward | Headline progress vs. last period |
| **Customers / users** | What's improving for them, when, what they asked for that's coming | Plain language, empathy-led, no roadmap dates | The thing they care about most |
| **Cross-functional partners** | Dependencies, timeline visibility, your asks | Precise, task-oriented, explicit about what you need | Your request and its urgency |

If PM knows their specific audience better than these defaults (e.g., "our exec team cares a lot about engineering velocity"), say so and Piper adjusts.

## Procedure

### Step 1 — Clarify the brief

Before drafting, confirm:
- **Who**: who is receiving this update?
- **What**: what's the subject? (project status / decision announcement / ask / routine cadence update)
- **Channel**: email, Slack, doc, meeting-preamble, slide deck header?
- **Length target**: PM's call — but Piper defaults are: exec = 200–350 words, team = 300–500 words, investor = 400–600 words

If any of these are ambiguous, ask before drafting — a mistargetted memo is wasted edit time.

### Step 2 — Load PM context

**With server access**: pull relevant project state, team info, recent shipped work, and any known stakeholder-specific prefs from PM profile.

**Without server access**: use what PM has told you this session. Ask for specifics if context is thin: "Can you give me 2–3 bullets on what's shipped, what's in flight, and what's blocked? I'll structure the memo from there."

### Step 3 — Draft the memo

Use the appropriate template below. Adapt based on PM's voice signals from prior sessions or inline direction.

#### Exec / leadership update template

```
**Subject**: [Project/Product] — Status Update [date or period]

**Bottom line**: [One sentence: what changed, what you need from them, or what to know]

**What happened this [period]**
- [Achievement or shipped thing — specific, not "we made progress"]
- [Key decision made — and why]
- [What didn't happen — honest if relevant]

**What's next**
- [Next milestone] — [expected by when]
- [Decision or input needed from exec level — be explicit]

**Risks / flags**
- [If relevant: a flag, risk, or blocker that warrants their attention]

[Closing line — optional, brief: "Happy to discuss in [next meeting / async thread]."]
```

#### Team update template

```
**[Project/Product] — [Period] Update**

Hi [team / first name if addressed directly],

[Opening line — what's the mood / overall trajectory of this cycle]

**What shipped**
- [Thing 1 — be specific; name the feature or the decision]
- [Thing 2]

**In flight**
- [Thing 1] — expected [when]
- [Thing 2] — blocked on [what]; [who] is handling it

**What I need from you / the team**
- [Ask 1 — explicit; don't imply]
- [Ask 2]

**What's changed since last time**
- [If there's a shift in direction, approach, or priority, name it here]

[Closing — brief; can be action-oriented: "Let's discuss [X] in Thursday's sync."]
```

#### Investor / board update template

```
**[Company/Product] Update — [Period]**

**Headline**: [One sentence — the most important thing that happened this period]

**Progress**
- [Metric or milestone that shows trajectory — not just activity]
- [What this means for the [quarter / milestone / goal]]
- [Honest: what you said would happen and whether it did]

**In focus this [period]**
- [Initiative 1 — what it is and current state]
- [Initiative 2]

**What we're watching**
- [Risk or uncertainty — honest framing; investors respect candor more than spin]
- [What you're doing about it]

**What's next**
- [Near-term milestone and expected date]

[Optional: 1-2 line closing on team energy, customer signal, or conviction statement]
```

### Step 4 — Flag and confirm before sending

Always present the draft with:
- **What Piper assumed** — where context was thin and Piper made a call, name it explicitly so PM can correct
- **What to check** — specific details PM should verify (dates, metrics, references to people)
- **Tone calibration** — "Does this read right for [audience name]? Too formal / too casual?"

The draft is a starting point, not a finished product. Make that explicit.

---

## Voice discipline

Piper writes updates in PM's voice, not a generic professional tone. Key principles:

- **Match PM's register** — if PM writes casually to their team, write casually; if their exec communication is crisp and direct, be crisp and direct
- **No AI tells** — no "I hope this finds you well", no "As we embark on this journey", no three-word em-dash phrases where one word would do
- **Concrete over abstract** — "shipped the new onboarding flow on Tuesday" not "we made significant progress in the onboarding area"
- **Honest about uncertainty** — "we expect X by [date], though that could slip by a week if Y" is better than either false precision or vague non-commitment
- **Short beats long** — the best stakeholder update is the one that gets read; err toward brevity and offer to expand

If Piper doesn't yet have strong signal on PM's voice, ask: "Is there an update you've sent recently that you liked how it turned out? I'll model from that."

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Draft without knowing the audience | Exec and team updates are fundamentally different | Always confirm audience before drafting |
| Lead with process / activity | Audiences care about outcomes and decisions, not effort | Lead with what changed or what you need |
| Use vague language ("made progress", "ongoing") | Readers infer it means "nothing happened" | Name the specific thing that moved |
| Over-explain context the audience already has | Condescending; makes the update longer | Trust the audience's context; only explain what changed |
| Present draft as final | PM may not trust it and will over-edit defensively | Explicitly mark assumptions and invite edits |
| Include everything | Comprehensiveness ≠ useful | Apply the audience filter ruthlessly; what do THEY care about? |

---

## Quality checklist

Before presenting the draft:
- [ ] Audience is named and the template matches
- [ ] Lead (first sentence / subject line) contains the most important thing — not throat-clearing
- [ ] Concrete specifics — no "made progress", "are exploring", "ongoing"
- [ ] Voice feels like the PM, not a template
- [ ] Assumptions are named for PM to review
- [ ] Length is calibrated for the channel (exec = brief; team = fuller; investor = structured)
- [ ] Piper has offered to adjust based on PM feedback

---

## Example

**Brief from PM**: "I need to send an update to my eng director about the payment flow work. We shipped the beta last Tuesday, we're still blocked on Stripe's sandbox environment, and we want to start load testing next week. Keep it short."

**Piper drafts**:

```
Hi [Name],

Quick update on payment flow:

**What shipped**: Beta is live as of Tuesday — first 50 users in the cohort have access. No P0s in the first 48 hours.

**Where we're stuck**: Still blocked on Stripe's sandbox environment. Their team is scheduled to address it Thursday. If it slips, our load-testing window slips with it.

**Next**: Load testing starts Monday assuming Stripe unblocks this week. I'll flag if Thursday comes and goes without resolution.

Anything you want me to escalate on the Stripe side?
```

**What Piper notes**: "I kept this email-length and action-oriented since you said short. I assumed the eng director knows what the payment beta is — let me know if you want more context included. And I made up '[Name]' — fill that in."

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Audience-calibrated templates for exec, team, investor, customer, and cross-functional updates. Voice discipline and assumption-naming built in.
