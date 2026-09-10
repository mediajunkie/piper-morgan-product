---
type: copy-contract
name: GatherOutcome — the user-facing contract (cousin 1's aggregation copy)
version: v0.1
date: 2026-09-09
owner: CXO
assigned_by: Arch 2026-09-09 — "cousin 1's aggregation copy (the N-failures→one-sentence rule) is CXO's
  user-facing contract, with the #1717 composition case as its acceptance test"
applies_to: un-modeled-nouns audit cousin 1 ("an empty-or-degraded answer"); the GatherOutcome epic
acceptance_test: §6
last_updated: 2026-09-09
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
