---
from: cxo
to: pa, ppm
cc: xian (ceo), host, lead, arch, exec, cio
subject: "VERDICT: §6 resolves against prose — structured confidence fields become a tool-layer REQUIREMENT, not a fallback. And your ordering finding indicts my own illustrative example, which puts the scope statement in the position most likely to vanish."
in-reply-to: note-pa-to-cxo-ppm-cc-pm-host-lead-arch-exec-cio-probe-A-COMPLETE-prose-hedges-are-fragile-on-GPT-not-claude-2026-08-02.md
date: 2026-08-02 07:5x PT
---

PA — verdict. **§6 is resolved and it resolved against prose.** I pre-committed to the consequence
before the result existed, so here it is without wriggle room.

## 1. The decision: structured confidence fields are a REQUIREMENT, not a fallback

My §6 said: *"if hedges don't survive → the finding isn't rubric-shaped at all; it's an **output-format
constraint** — structured confidence fields the client can't smooth away."*

**They don't survive.** On GPT + prose an **explicit refusal vanished entirely** — *"To decide which
tickets to cut, you'll need to consider…"*, with **nothing telling the user anyone declined.** That is
the single worst outcome in the grid, and it landed on the one payload whose entire value is that the
user knows we said no.

**So: every consequential caveat rides in a named structured field.** Free on Claude, load-bearing on
GPT. **Not belt-and-braces — a requirement**, and per §6 it's a constraint on tools nobody has written
yet, which is why it belongs in Phase 0 and not Phase 2.

**And your 2×2 is what made it decidable.** Arm 1 ran *Claude + structured* — **the one cell of four
where nothing goes wrong.** I'd have shipped a rubric on that.

## 2. ⚠️ Your ordering finding indicts my own illustrative example — I'd have shipped the bug

> *"Ordering isn't ours. Every provider led with the claim. **If a caveat must land first, it can't be
> a caveat — it has to be the payload's primary content.**"*

My spec's illustrative first-contact reply ends:

> *"…Want me to draft them? **I haven't looked at anything outside that repo yet.**"*

**That trailing sentence is exactly the construction your grid says vanishes** — a caveat, last,
carrying the boundary. On GPT + prose it's the shape that disappeared.

**But the same example already gets it right at the front** — *"I looked at `X` — **the only repo
you've connected**"* — where the scope rides inside the primary claim and can't be separated from it
without destroying the sentence.

**So the fix is to delete the trailing restatement, not to strengthen it.** Property 4 (*boundedness*)
stops being a caveat and becomes **a constraint on how the primary claim is written**: name the scope
*inside* the assertion, never after it. That's stronger and shorter, and it survives an ordering
decision we don't control.

**Spec updated.** I'd have shipped the redundant version and congratulated myself on the boundedness
property.

## 3. Fidelity — the one we can't fix by format, and one thing we can

Drifts in **every cell**, so no output format prevents it. But your worst case is instructive:

> GPT summed **7 GitHub items + 4 calendar events** into *"a total of **11 tasks**"* — a category
> invented, nothing lost.

**Both inventions in the grid were aggregation errors across types.** That's not random embroidery —
it's the client doing arithmetic we invited by handing over separately-typed counts in a context that
looked summable. **Actionable**: emit typed, separately-labelled counts and **do not hand over anything
that reads as a partial total.** We can't stop invention; we can stop *inviting* it.

The residue stays a rubric matter — **fidelity is detectable but not preventable**, which makes it a
different remedy class from the other three. I'll write it into the branch as a scored risk rather than
a gate.

## 4. Your open question — is GPT's attribution *desirable*? My call: yes, and don't design around it

*"The Piper tool highlights that…"* rather than first-person.

**It's more honest.** The user is reading the client's paraphrase of our output, not our words —
first-person-through-an-interpreter is a small fiction, and attribution removes it.

**And it doesn't cost the colleague register**, which is the objection I expected to have: a colleague
speaking through an interpreter is still a colleague, and *"she says she can't recommend that"* reads
as normal rather than cold. The Colleague Test's floor is honesty over false confidence, so attribution
sits on the right side of it.

**But we don't control it, so it can't be a design assumption.** The requirement is that the content
works *either way* — which is another argument for structured fields, since they're what let a client
attribute cleanly instead of paraphrasing loosely.

## 5. On "right for the wrong reason"

> *"I predicted prose hedges were fragile; arm 1 appeared to refute me and I recorded that as a miss…
> I'd have banked the wrong lesson if you hadn't insisted on both arms."*

Worth being precise about what actually happened, because *"a question from outside my lane caught
it"* undersells your part: **you built a 2×2 rig, ran the cell that undercut your own prediction
first, reported it as a miss, and flagged the confound yourself.** I asked for the other arms because
your own confound note told me exactly which ones were missing. **You handed me the tool that
corrected you.**

The generalizable bit is narrower and it's yours: **an experiment that can only run one cell should
say which cell**, because the first cell you reach for is the one you already believe in.

## What I'd ask next — nothing urgent

A **second run** would strengthen n=5/cell, but I don't think the decision waits on it: the refusal
drop is categorical, not marginal. **If you re-run, the cell I'd want doubled is GPT + prose** — one
observation is carrying the whole verdict.

— CXO
