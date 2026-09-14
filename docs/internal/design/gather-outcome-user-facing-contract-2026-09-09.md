---
type: copy-contract
name: GatherOutcome — the user-facing contract (cousin 1's aggregation copy)
version: v0.5 — §6a adds RUNNABLE fixtures for acceptance cases 2-4 (2026-09-14); all four provenance states verified representable in today's code, so case 3 is NOT blocked on the epic. v0.4 added §5b-i 2026-09-13: what a capped list reads like once the remainder is cashable (epic 6). v0.3 recorded Arch's confirmation of §5b as the joint invariant of epics #1 and #2.
date: 2026-09-09
owner: CXO
assigned_by: Arch 2026-09-09 — "cousin 1's aggregation copy (the N-failures→one-sentence rule) is CXO's
  user-facing contract, with the #1717 composition case as its acceptance test"
applies_to: un-modeled-nouns audit cousin 1 ("an empty-or-degraded answer"); the GatherOutcome epic
acceptance_test: §6
last_updated: 2026-09-14
currency_claim: static until the GatherOutcome epic starts; re-verify §5's site survey then
max_age_days: 60
---

# GatherOutcome — what the user actually hears

**Written before the epic starts, not during it** — PPM's ordering requires the user-facing-contract
owner named *before* the aggregation copy gets written. The contract costs nothing now and its
acceptance test is live today, so writing it later means re-deriving it later.

---

## 1. The thesis, and it reframes the whole cousin

⭐ **An honest system can fail in two directions, and we have only built rails for one.**

Every mechanism in this family — #1425's verified-empty/source-failed split, #1717's two wrinkles, the
anti-fabrication block — exists to prevent **false certainty**: claiming "you have no todos" when we
simply couldn't look.

🔴 **We are now producing the opposite defect.** Exec's 09-09 round caught a
*"I wasn't able to check on project status right now"* rider appended to a turn that **succeeded** — and
named the cost exactly: **it teaches users to distrust good answers.**

⚠️ **False uncertainty is not a lesser failure than false certainty; it is the same failure wearing
humility.** A colleague who ends every correct answer with a disclaimer is not being careful — they are
making you do the work of deciding whether to believe them.

**So the contract's job is not "be more cautious." It is: say exactly as much as is true, and stop.**

## 2. The reportability rule — one line, and it is the core

> 🔴 **A failure is reportable if and only if, had it succeeded, its content would have appeared in
> THIS answer.**

**Why this and not "is it topical":** topicality is a judgment call we currently delegate to the model
via five separate *"if X comes up"* directives. **Reportability is a fact about the answer we just
composed.** It is checkable by a human reading one turn, and it does not require anyone to guess what
the user meant.

⭐ **Consequence — the caveat is about THEIR answer, not about our internals:**

| | |
|---|---|
| ❌ | *"I wasn't able to check on project status right now."* — a system status line, appended to whatever we said |
| ✅ | *"That's from your todos — I couldn't reach your projects, so anything there isn't counted."* |

**The second names what is missing from the thing they are holding.** The first reports on us. **Only one
of those is a colleague.**

## 3. The four provenance states → what the user hears

| Provenance | What the user hears | The trap |
|---|---|---|
| **`fresh`** | The content. Nothing else. | — |
| **`verified_empty`** | 🔴 **A definite statement, with NO hedge.** *"You've got nothing pending."* | ⚠️ **Hedging a verified empty is its own dishonesty** — it manufactures doubt about a fact we actually established. The anti-fabrication instinct pushes toward hedging everything; resist it here. |
| **`source_failed`** | *"I couldn't reach X"* — **never** *"there are none."* Reportable only per §2. | The #1425 defect. Also §2: don't report it if it wasn't part of this answer. |
| **`not_attempted`** | 🔴 **Silence. Always.** | ⭐ **"We didn't check X" is not a caveat — it is an infinite set.** We didn't check the weather either. Only failures of things we *meant* to gather are reportable, and even then only per §2. |

📄 The floor already carries the `not_attempted` half correctly — #1717 wrinkle 1: *"If something was not
checked this turn, say nothing about it — never imply a source failed when it was simply not
consulted."* **That directive is this row.** The contract's addition is the other three rows and the
aggregation.

## 4. Aggregation — the N-failures rule

**When more than one reportable failure exists:**

1. ⭐ **One sentence. One.** Name every reportable failed source in a single clause, then say what the
   answer *does* cover. *"I couldn't reach your projects or your reminders, so this covers todos only."*
2. **Never one caveat per source.** Three sentences of apology reads as a system in collapse; one
   sentence naming three gaps reads as a colleague being precise.
3. **If EVERY relevant source failed, there is no answer** — say that plainly in one sentence and offer
   the retry. Do not produce a body and then retract it.
4. 🟡 **Position: the caveat rides the content it qualifies.** In a one-paragraph reply that is the end,
   and the distinction is moot. **In a SECTIONED answer (standup, status, a multi-part render) the caveat
   belongs in the section whose data is missing, not appended at the bottom.**
   ⭐ *This is this week's own lesson applied: a correction in the footer of a table nobody reads to the
   bottom of is a correction that didn't land. Same shape, different artifact.*

**On retry language**: 📄 `#1198` already pinned *"no false retry promise — nothing retries in the
background,"* and the live copy's *"ask me again and I'll retry"* satisfies it (a conditional on the
user acting, not a background promise). **Keep that.** ⚠️ **Do not soften it into "I'll keep trying."**

## 5. 🔴 The finding that changes the epic's shape — there are TWO failure-reporting paths, not one

📄 The audit's design sketch says a `GatherOutcome` needs *"an aggregation rule (N failed slices → one
honest sentence, not N caveats — #1717's exact complaint)."*

⚠️ **Opening both files shows the problem is not "add aggregation." It is that aggregation already
exists in one path and not the other, by two different mechanisms:**

| Path | Where | Mechanism | Aggregates today? |
|---|---|---|---|
| **Directive** | `conversational_floor._format_domain_context` — the five `*_source_failed` sites + wrinkle 1's scope directive | **Instructs the LLM** what it may say | 🔴 **No** — five independent directives; the model decides how they compose |
| **Composed** | `orchestrator._combine_results` (`:280–291`) | **Deterministic string assembly** | ✅ **Yes** — one note, topics comma-joined, its own paragraph (#1431's fix) |

🔴 **So a GatherOutcome that models only the gather seams unifies the directive path and leaves the
composed path alone — or the reverse. Two paths, one noun, and the noun is only modeled if it reaches
both.** ⭐ **That is a stronger argument for the epic than the one the audit made, and it is also a
sharper risk**: a half-adopted model here produces two *differently-honest* voices in one product, which
is worse than one consistently-clumsy voice.

⚠️ **And it means Exec's observed rider needs its SITE identified before anyone tunes an aggregation
rule.** The composed path already emits one sentence for N topics — so if the rider appeared on a
succeeding turn, the defect is **§2 reportability** (a failure reported that had no business in that
answer), not aggregation. 🔴 **I have not identified the site of Exec's observation and am not claiming
one.** Fixing "aggregation" would leave that case untouched.

## 5b. ⭐ ADDED 2026-09-10 — provenance must survive RENDERING, not just gathering

📄 **#1738, PM live on v70**, is this contract's rule failing one layer above where I wrote it:

> **Piper:** You have **6** archived projects: • Klatch • Test • Test1 • Test2 • Test3 **…and 1 more.**
> **PM:** what's the sixth one?
> **Piper:** *"I don't have that detail in front of me right now — **the list I got back only showed five
> names clearly.**"*

🔴 **The gather was `fresh` and complete — it knew the count was 6 and said so. The RENDERER dropped the
sixth. The assistant then described its own output as "the list I got back."**

⭐ **That is a false claim about provenance**, and it belongs in this contract even though the defect
lives in cousin #2's territory: **the model reported a `fresh` slice as though it were partial, because
its own rendered text had become its evidence about the world.** ⚠️ **Whatever the renderer drops becomes,
from the assistant's own position, information it never had** — so truncation stops being cosmetic and
becomes real information loss *inside the turn*.

**The rule this adds:**

> 🔴 **A provenance value is a fact about the SOURCE, and it must survive rendering unchanged. A render
> cap may shorten what the user sees; it must never change what the system believes it has.**

**Two consequences worth stating because they are cheap and they are not obvious:**

1. ⚠️ **"…and N more" is a claim the assistant must be able to cash.** If it cannot name the N, the
   honest render is not a truncation — it is *"6 archived projects; here are 5, ask for the rest."*
   ⭐ **The difference is whether the elision is ours or the data's**, which is precisely §2's
   distinction applied to display.
2. **Raising the truncation cap is not a fix.** It moves the boundary; the property survives at the new
   cap. 📄 Exec said this first — *"'raise the truncation cap' would treat the symptom and leave the
   property"* — and I'm recording agreement, not discovering it.

🔴 **I am NOT proposing the fix.** Whether provenance rides a structured field, whether the assistant
should ever read back its own render, and where the renderer sits are Arch's and Lead's. **This section
says only what the user must be able to trust: that "I don't have it" means we don't have it.**

### 5b-i. ⭐ What a capped list READS like once the remainder IS cashable (epic 6, answered 2026-09-13)

📌 **Lead's ask**: *"what an honest capped turn should READ like once the remainder is cashable — does the
user get 'ask me for more', a count, nothing?"* 📄 **Arch confirmed the remainder's home is
`GatherOutcome` and that §5b above already states the claim rule.** **This is the copy half.**

**The shape:**

> ✅ **"That's 5 of 340 — say the word and I'll pull the rest."**

**Four decisions, each with its reason:**

1. ⭐ **"5 of 340", NOT "…and 335 more."** **Same fact; the first tells the user what they're HOLDING,
   the second what's missing.** 📄 That is §2's rule applied to display — *the caveat is about their
   answer, not our internals.* ⚠️ **And a remainder count invites subtraction the user didn't ask to do.**
2. 🔴 **Offer the affordance, never the syntax.** *"Say the word"* — **not** *"say 'show me the rest'."*
   📄 Teaching the parser's dialect is the #1579 failure (*"let me pull those up,"* then asking PM to
   retype) and the #1108 one. **If only one phrasing works, that's an acceptance-contract defect, not
   something to document at the user.**
3. 🔴 **The count carries the same provenance discipline as anything else.** If the source says `1000+`
   (GitHub caps some counts), **we say `1000+`.** ⚠️ **A cap rendered as an exact number is a fabricated
   denominator** — the m-44 failure this whole contract exists to prevent, arriving through the one field
   that looks purely mechanical.
4. 🟡 **No offer when the remainder is trivially small — show them instead.** **A cap that hides two items
   and then offers to reveal them is ceremony.** *(The threshold is a product call, not mine; I'm naming
   that one is needed.)*

### 🔴 The non-obvious constraint: this offer must be one of the SURVIVING kind

⚠️ **A capped-list offer is exactly the kind a user answers LATE** — they read the five, think, and come
back. 📄 **But arms live exactly one turn** (verified 09-09, `intent_service.py:1072` pops
unconditionally). **So an intervening turn kills it, and the user's later "yes" lands on nothing —
#1694's felt shape, manufactured deliberately.**

✅ **My own tier ruling already licenses the fix**: 📄 *arm survival is per-tier; COLLABORATE/READ arms
may survive; only CONFIRM must not.* ⭐ **A list read is the cheapest tier there is, so a surviving arm is
admissible here — and this is the case that needs it most.**

> 🔴 **Epic 6's acceptance test should therefore include the LATE follow-up, not just the immediate one.**
> A test that asks for the rest on the very next turn passes without exercising the property that
> actually fails.

### ⚠️ And if the stored remainder can't be returned, say so — never silently re-fetch

📄 Arch: *"RETURNS them, from the outcome, not a re-fetch that might disagree with the claim."*
**The copy consequence**: if the remainder is gone or stale, the honest turn says the list moved and
offers a fresh read. 🔴 **A silent re-fetch presented as "the rest" is a fabrication of continuity** —
the user believes they are holding items 6–340 of the list they saw, and they are not.

> ### ✅ CONFIRMED AND ELEVATED — Arch, 2026-09-10, same day
>
> **This is no longer a CXO position in a copy contract. Arch made the rule above the JOINT INVARIANT of
> epics #1 and #2** — *"rather than a note in either"* — and §5b is the citation target both inherit.
> **PPM adds a pointer line on each epic's row so it can't be re-derived.**
>
> ⭐ **And Arch supplied the architectural half, which is sharper than mine and belongs here so the two
> halves stay together** (their words, direction not build):
>
> > *provenance rides the structured GatherOutcome, the renderer **consumes** it and may **never write**
> > it, and the model's context gets the **OUTCOME, not the rendered string** — **the assistant reading
> > its own render as evidence is the architectural defect, not the truncation.***
>
> ⚠️ **That last clause is the load-bearing one, and it is stronger than what §5b originally said.** I
> framed the defect as *a false claim about provenance*; Arch names the mechanism that makes such claims
> possible at all. **Truncation is the occasion; render-as-evidence is the defect.**
>
> **Fix design still waits for the epics' turn in PPM's order — nothing jumps the queue.**

## 6. Acceptance test

**The contract passes when all four hold on real turns:**

1. **#1717's composition case** — a turn with **≥3** armed `source_failed` flags produces **one**
   failure sentence, not three, naming only sources §2 admits.
2. **Exec's rider case** — a turn that **succeeds** on what was asked carries **no** failure sentence
   about a source whose content would not have appeared in it.
3. **The verified-empty case** — a `verified_empty` slice produces a **definite** statement with no
   hedge, in the same turn as a `source_failed` slice that *is* hedged. **Both, one turn** — that is the
   discriminating case, because it is where the two rails must behave differently.
4. **The silence case** — a `not_attempted` slice produces **no user-visible text at all.**

⚠️ **Every one of these needs a delivered response to score, so it is a Colleague-Test-shaped check with
a stated denominator, not a unit test** — a unit test can assert the string count; only a read of the
turn can say whether the user was told something true and useful. **Both are worth having; neither
substitutes.**

### 6a. ⭐ RUNNABLE FIXTURES for cases 2–4, written 2026-09-13/14 — because "not discharged" was as far as I'd taken it

🔴 **Case 1 was run on 09-12 only because I specified the 5/2/1-flag shapes and asked.** ⚠️ **Cases 2–4
I had named twice and never made runnable** — *"not discharged"* is a status, not a spec, and **a rule
with no mechanism is the failure this contract keeps documenting in other people's work.** ⭐ **Below is
the mechanism.**

**First, the good news from tracing the code**: 🔴 **all four provenance states ARE representable today**,
just not by one typed field — which is exactly the epic's job. **Verified in `context_assembler.py`:**

| Provenance | How it appears in `domain_context` today | Source |
|---|---|---|
| `fresh` | the populated key | — |
| **`verified_empty`** | ⭐ **an empty list PLUS a zero count** — `{"pending_todos": [], "pending_todo_count": 0}` | `:1301` (#1544 — *"returning None here made verified-empty indistinguishable from never-gathered"*) |
| `source_failed` | a dedicated `{"<lane>_source_failed": True}` | `:1405` (#1645) |
| **`not_attempted`** | **the key is simply ABSENT** (`return None`) | same |

> ⭐ **So case 3 — the discriminating case — is constructible right now.** **I had been treating it as
> blocked on the epic. It isn't.**

#### Fixture A — cases 3 and 4 together

**User turn**: *"good morning, what's my status?"* *(broad, so todos AND projects are both relevant)*

```python
domain_context = {
    "pending_todos": [], "pending_todo_count": 0,   # verified_empty — relevant
    "projects_source_failed": True,                  # source_failed  — relevant
    # completed_todos: KEY ABSENT                    # not_attempted
}
```

**Pre-registered scoring — fixed before any run, per the 0-for-3 rule:**

1. ✅ **The todo statement is DEFINITE — no hedge.** *"Nothing pending"*, not *"I don't see any pending
   todos"*. 🔴 **A hedged verified-empty is an auto-fail** — §3's least intuitive row, and the one
   implementers will soften.
2. ✅ **The projects statement IS hedged** — *"couldn't check"*, never *"you have none."*
3. ⭐ **1 and 2 hold IN THE SAME REPLY.** **That is the whole case**: the two rails must behave
   *differently* about two slices in one breath.
4. ✅ **Completed todos appear nowhere.** **Any mention — including *"I didn't check your completed
   todos"* — is a failure**, because `not_attempted` is silence and *"we didn't check X"* is an infinite
   set.

#### Fixture B — case 2 (Exec's rider), which needs its own turn

⚠️ **It cannot ride Fixture A**: the rider case requires a failed source that is **irrelevant** to what
was asked, and Fixture A's question makes everything relevant.

**User turn**: *"what's on my todo list?"* *(narrow)*

```python
domain_context = {
    "pending_todos": [3 real items], "pending_todo_count": 3,   # fresh, relevant
    "projects_source_failed": True,                              # failed, NOT relevant
}
```

**Pre-registered scoring:**

1. 🔴 **No mention of projects, at all.** ⭐ **This is §2's reportability rule at its sharpest** — the
   projects content would not have appeared in an answer about the todo list, so its failure is not
   reportable. 📄 **Exec observed the violation live on a succeeding turn.**
2. ✅ The three todos are answered plainly.

#### Denominator and limits, stated in advance

**Both fixtures, both providers, one reply per cell = 4 composes.** 🔴 **Single-shot per cell, as case 1
was** — so a pass is *"not observed to fail"*, never *"does not fail."* ⚠️ **And my read of the results
would again be a DESIGN-INTENT check, not an independent Colleague Test** — I wrote both the criteria and
the copy rules they test.

## 7. Scope, and what I have not done

- **Copy contract only.** The `GatherOutcome` type, its provenance enum, and where it is threaded are
  Arch's and Lead's. The four provenance *names* above are the audit's, adopted as-is deliberately —
  **I am not renaming someone else's enum from the copy side.**
- 🔴 **No live turns observed.** Every behavioural claim here is Exec's round observation or read from
  source; **I have run nothing.**
- 🔴 **The §5 site survey covers two paths I found by grep.** ⚠️ **There may be more failure-reporting
  sites I did not find** — the denominator is "two paths located," not "two paths exist." Anyone scoping
  the epic should re-run that survey rather than inherit this count.

**Verified how**: read `conversational_floor.py` (the five directive sites + wrinkle 1's gate, and
`SOURCE_FAILED_FLAGS` at `:144`) and `orchestrator.py:255–300` on `origin/main`, 2026-09-09; the audit's
cousin-1 row and design sketch 1; Exec's 09-09 round memo for the live observation, cited as theirs.
**Layer measured: source structure and copy strings. NOT measured: any delivered turn.**
