# Cohort attention rollup — let's design how you'd want to own it

**To:** Exec (Chief of Staff)
**From:** PA (Piper Alpha)
**CC:** xian (CEO/PM)
**Date:** 2026-06-06
**Re:** Handing off the attention-dashboard prototype — collaboratively, not as a drop

---

Hi Exec —

PM and I just talked through a clean division of labor: you oversee the team and assist xian as CEO;
I'm his *product* assistant, helping him be a better product lead. The **cohort attention rollup** — the
single-glance HTML board of what across the cohort needs his decision vs. is drift vs. is clean — sits
more naturally in your lane than mine. It's org-attention synthesis, same family as the Weekly Ship
synthesis you already drive. So PM suggested I hand it to you.

I'd rather **co-design the handoff than drop a spec on you.** Here's what I've got and where I think the
real choices are; tell me how you'd want to shape it.

## What exists right now

1. **A skill** — `cohort-attention-rollup` (`.claude/skills/cohort-attention-rollup/SKILL.md`, on main).
   It captures the procedure I'd been running ad-hoc: gather the per-role `duty-cycle-escalations-*.md`
   docs → **live-state verification pass** → triage into 🔴 Decision / 🟡 Drift / ⚪ Clean / ✅ Resolved →
   render a self-contained HTML page → deliver to PM with a clickable path.
2. **A worked example** — `dev/active/pa-cohort-attention-rollup-2026-06-03.html` (the one PM said he
   *loved*). That's the visual + structural target.

## The one part that's load-bearing

If you take nothing else from the prototype, take **the live-state verification pass.** The whole value
is that the board reflects *now*, not a concatenation of stale role-docs. The 6/3 example caught a
decision (PDR-005) that a role's doc still listed "open" but PM had already ratified that day — without
verification it would have shown a phantom decision in his queue. Budget the time to check each
"decision awaiting you" against actual GitHub state / ratifications before listing it.

## Where I think the real design choices are (your call, genuinely)

- **Cadence.** I ran it on-demand + on duty-cycle fires. Does it fit your cycle as a daily compile during
  active weeks, or purely on PM request? Your oversight rhythm should drive this, not my prototype's.
- **The "On your plate (non-cohort)" section.** In my version that surfaced *my own* PA threads to PM.
  For you it might become org-level items, or just disappear. Probably doesn't transfer as-is.
- **Automation.** The verification pass is manual today. There's a real future where CIO + you wire
  auto-stale-flagging + live-GitHub-verify so it's mechanical. Worth a conversation with CIO if you want
  to pursue it — I flagged it in the skill's footer notes.
- **Anything about the format itself** — I'm not attached to my section order or styling. If a different
  shape serves your synthesis better, change it.

## What I'm proposing

You adapt the skill into your working approach however fits — rename sections, change cadence, restructure
freely. I'll stay available as the original builder if you hit anything that doesn't make sense, and I'm
happy to pair on a first run if useful. No rush; PM and I are deep in the BYOC skunkworks, and this is a
"when it fits your cycle" handoff, not an urgent one.

What would you change first? Or if it's easier, run it once your way and tell me what felt off about the
prototype's assumptions.

— PA
