# Priority Is Not Pace

*December 4*

My Lead Developer was debugging an alpha testing failure. The PM - me - was blocked, waiting for the fix. The pressure to rush felt legitimate. Get it working so the PM can continue testing. Ship something, anything, fast.

Then we stopped and reframed. Priority indicates what to work on next. It doesn't dictate how to work on it. The work should remain deliberate, craft-focused, systematic. Urgency signals sequencing, not approach.

This distinction - priority versus pace - became what we now call the Time Lord Doctrine. It crystallized under pressure, during the kind of moment where teams usually skip steps and accumulate technical debt.

## The cultural conflation

In most work cultures, "priority" implicitly means "rush." Someone says "this is high priority" and everyone understands: cut corners, skip investigation, ship something quickly. The semantic slippage happens automatically.

This makes sense in genuine emergencies. Production is down, customers can't access the service, revenue is at risk. Rush. Fix it now. Move fast.

But most work isn't emergencies. Most "high priority" work is just: this matters, do it next. The situation doesn't require compromised craft. It requires focused attention on the right thing.

[PLACEHOLDER: Work cultures where "priority" meant "rush" - have you experienced this conflation? Times when urgency contaminated approach? The cost of that pattern?]

The confusion creates problems. When priority always means rush, teams develop antibodies to prioritization. Product managers learn not to call things priorities unless they want shoddy work. Engineers learn to push back on urgency because it correlates with technical debt. The communication breaks down.

## The moment of reframing

Thursday midday, debugging the dialog component issue. I'd been about to implement a quick fix - just swap components, make the error disappear, move on. Michelle was waiting. The PM was blocked.

Then I caught myself. What's the broader pattern here? Not just "how do I make this error go away" but "what does this error tell us about how we're building?"

The pressure felt real. But the pressure was contaminating my approach. I was about to skip investigation because someone was waiting. That's how you ship code that passes tests but doesn't solve problems.

[PLACEHOLDER: Moments when you caught yourself rushing - times when external pressure influenced your approach? The discipline of stopping to recalibrate?]

I stopped and checked with the PM. Is this actually an emergency requiring compromised craft? Or is this important work that deserves thorough investigation?

The answer: important, not emergency. The PM being blocked signaled sequencing (work on this now, not something else). It didn't signal approach (skip steps, compromise investigation, accumulate technical debt).

## Priority as sequencing signal

Priority answers: What should I work on next?

In a queue of possible tasks, priority indicates order. Work on the auth bug before the documentation update. Work on the integration issue before the UI polish. This task, not that task. Next, not later.

This is valuable information. Without prioritization, engineers work on whatever seems interesting or familiar or easy. With prioritization, effort aligns to impact. But the prioritization is about sequence, not about how to execute the work once it's sequenced.

[PLACEHOLDER: Prioritization frameworks you've used - how do you decide what to work on next? When has good prioritization enabled good work? Bad prioritization complicated it?]

The PM saying "this is high priority" means: I need you to work on this now rather than other things. It doesn't mean: I need you to work on this badly rather than well.

## Pace as craft discipline

Pace answers: How should I work on this task?

For almost all knowledge work, the answer is: deliberately. Investigate thoroughly. Understand patterns. Build systematically. Document clearly. Test comprehensively.

This isn't about being slow. Deliberate work is often faster than rushed work because it doesn't create rework. But it's about maintaining craft standards regardless of external pressure.

[PLACEHOLDER: Your own craft discipline - what does deliberate work mean in your domain? Times when maintaining standards felt difficult under pressure? When it paid off?]

The Time Lord Doctrine separates these concerns. Priority remains legitimate - the PM can and should signal sequencing. But pace remains with the craftsperson - the engineer decides how to maintain standards while working on the prioritized task.

## When the doctrine applies

Not all situations warrant the doctrine. Genuine emergencies exist. Production down, security breach, data loss - these require compromised craft in service of immediate resolution. Ship the fix now, clean it up later.

But genuine emergencies are rare. Most "urgent" work is just important work with feeling. The feeling creates pressure. The pressure suggests rushing. The rushing creates problems.

The doctrine applies when:
- External pressure exists (someone is waiting, blocking, expecting)
- The work is important but not emergency
- You feel pulled toward compromised craft
- The pressure is contaminating your approach

That's the signal to stop and check: Is this priority (work on it next) or is this emergency (compromise craft to ship fast)?

[PLACEHOLDER: Distinguishing genuine emergencies from felt urgency - how do you tell the difference? Decision frameworks that have served you? Emergencies that warranted compromise?]

## The conversation that clarifies

When you feel cross-pressured - external urgency pulling toward rush, internal standards pulling toward thoroughness - that's the moment for conversation.

Stop. Check with whoever is signaling urgency. Ask explicitly: Is this an emergency requiring compromised craft? Or is this important work that deserves deliberate approach?

Most of the time, the answer is: important, not emergency. Take the time. Do it right. I can wait for quality.

Sometimes the answer is: yes, emergency. Ship something minimal now, we'll clean it up later. In those cases, compromise is appropriate. But make it explicit. Document what's being compromised. Create follow-up work to address the shortcuts.

[PLACEHOLDER: Conversations that clarified urgency - when has explicit discussion revealed that rush wasn't actually needed? Times when someone said "I can wait for quality"?]

The conversation itself is valuable. It forces the person signaling urgency to think about what they're asking for. Do they want fast or do they want good? Usually they want good. They're just expressing concern about timing.

## What Thursday taught us

The dialog debugging took longer because we stopped to investigate patterns. It revealed component misuse that a quick fix would have masked. The evening's swiss cheese debugging took even longer - three separate issues all hiding behind one symptom.

If we'd rushed, we'd have fixed symptoms without understanding causes. Michelle would have found more issues. Each fix would have created new problems. We'd have spent the week firefighting instead of building.

[PLACEHOLDER: Technical debt from rushed work - when has skipping investigation created more work later? The compounding cost of quick fixes? Times when patience prevented that cycle?]

Instead, we took seventeen hours to investigate thoroughly. Found three layers. Fixed them systematically. Documented the patterns. Created tests that prevent recurrence.

At 10:19 PM Thursday, Michelle created a list. It worked. Not "works on my machine" or "passes tests" but actually worked for a real user doing the thing the feature enables.

That success came from separating priority from pace. The PM's blocking was legitimate priority signal - work on this now. The seventeen-hour thorough investigation was legitimate pace - work on it well.

## The quote that captures it

During Thursday's work, after the reframing conversation, I documented this insight:

> "Priority ≠ rush. Priority = what to work on next. Pace = how to work on it—should remain deliberate."

This isn't novel wisdom. Every senior engineer knows this. But knowing it and practicing it under pressure are different things. The doctrine creates permission to stop and recalibrate when urgency contaminating craft.

[PLACEHOLDER: Wisdom that's easier to know than to practice - principles that sound obvious but require discipline under pressure? How do you maintain craft standards when urgency feels real?]

The doctrine isn't about being slow. It's about refusing to let urgency contaminate craft. Work on the right thing (priority). Work on it right (pace). Don't conflate them.

## When to invoke

Use the Time Lord Doctrine when:
- You feel pressure to rush
- The pressure comes from external signals (blocking, waiting, urgency)
- The work matters but isn't a genuine emergency
- You're about to compromise craft to ship fast
- The urgency feels real but investigation feels right

That's the moment to stop. Check with the person signaling urgency. Clarify whether this is emergency (compromise appropriate) or priority (thoroughness expected).

Most of the time, they'll choose thoroughness. Not because they don't care about timing, but because they care more about quality. They just needed permission to say "I can wait."

The doctrine gives both sides that permission. The craftsperson can maintain standards. The person waiting can expect quality. Priority signals sequencing. Pace remains deliberate.

---

*Next on Building Piper Morgan: The Triad Model - collaboration without hierarchy.*

*How do you separate priority from pace in your work? When has urgency contaminated your approach? What creates permission to maintain craft under pressure?*
