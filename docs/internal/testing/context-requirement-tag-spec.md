---
type: instrument-spec
name: context_requirement — corpus tag semantics + C-axis scoring guidance
version: v1.0 — spec for Lead to execute the metadata pass
date: 2026-08-31
owner: CXO (semantics + scoring) · Lead (corpus artifact + the tagging pass)
closes: CT v2.4's C=0 disambiguation, agreed 2026-05-10, reframed 2026-08-31 as corpus work
applies_to: Colleague Test Rubric v2.3.4 C-axis; and the BYOC Recomposition Rubric, whose C anchors to it
last_updated: 2026-08-31
currency_claim: static once the tagging pass lands
max_age_days: 60
---

# `context_requirement` — tag semantics and C-axis scoring

**The gap this closes, in one sentence**: facing a C=1 response (*"generic — could be any user"*), a judge
cannot tell whether **project context existed and went unused** (a real failure) or **none was required**
(not a failure at all) — **because that fact lives in the query, not the response.** No amount of rubric
prose recovers a missing input.

---

## 1. The three values

Tag each **query** in the canonical corpus with exactly one.

| Value | Meaning | Example shape |
|---|---|---|
| **`required`** | A correct answer **must** use this user's actual project state. Without it the answer cannot be right, only plausible. | *"What issues are assigned to me?"* · *"What's my status this week?"* · *"What did we create this session?"* |
| **`optional`** | A good generic answer exists; the user's real data makes it **materially better**. | *"How should I write acceptance criteria?"* · *"Help me break this epic down"* |
| **`not_applicable`** | The user's data is **irrelevant** to a correct answer. General craft knowledge, or questions about Piper itself. | *"What's the difference between an epic and a story?"* · *"What can you help me with?"* |

## 2. The tagging procedure — mechanical, no quality judgment

**Ask this of the query alone. Do not look at any response.**

> *Could a frontier LLM with no access to this user's data give a **fully correct** answer?*

- **No — it needs the user's data** → **`required`**
- **Yes, but the user's data would make it materially better** → **`optional`**
- **Yes, and the user's data is irrelevant** → **`not_applicable`**

⭐ **The procedure deliberately never inspects a response.** If tagging required reading answers, the tag
would inherit the ambiguity it exists to remove.

## 3. How the tag changes C-axis scoring

| Tag | C floor that counts as a pass | C=1 means | C=3 |
|---|---|---|---|
| **`required`** | **C=3 is the bar** | 🔴 **real failure** — context existed and was not used | expected, not exceptional |
| **`optional`** | **C=2 passes**; C=3 is better | weak but **not** an auto-fail | credit where earned |
| **`not_applicable`** | **C=2 is full marks** | ⚠️ **not a deficiency — do not dock** | ✅ **not attainable, and its absence is not a miss** |

🔴 **The load-bearing change is the last row.** Today a query where context is irrelevant still gets scored
on the C axis and drags the total down. **That is the instrument penalising a response for not doing
something the question never asked for.**

**C=0 is unaffected by this tag.** Fabrication remains an auto-fail at every value, and that auto-fail is
one of the three **PM-ratified invariants** (2026-08-31) — this spec does not touch it and could not.

## 4. ⚠️ The trap: this is NOT the fresh-account ceiling, and conflating them will drift

CT v2.2's fresh-account clarification already caps C at 2 when a test account **has no data to inject.**
This tag is a different axis. **Two orthogonal reasons a response can be legitimately generic:**

|  | **Query needs context** (`required`) | **Query doesn't** (`not_applicable`) |
|---|---|---|
| **Context exists in the account** | C=3 is the bar; **C=1 is a real failure** | **C=2 is full marks** |
| **Context absent (fresh account)** | **C=2 ceiling** (v2.2); an honest *"I don't have that yet"* is the correct answer and scores well | **C=2 is full marks** |

- **v2.2 is about account state** — *does context exist to inject?*
- **This tag is about query type** — *does this query need context at all?*

**Both can apply at once**, and the bottom-left cell is where they interact. **Keep the two named
separately in any scoring note.** Collapsing them into one "generic is OK here" intuition is exactly the
silent-drift shape the Branch-or-Anchor discipline exists to prevent.

## 5. A consequence worth stating before the data arrives

📄 CT v2.3.4 currently reads: *"When the canonical retest shows responses clustering at C=2, that's the
signal that context assembly is not flowing into generation."*

⚠️ **That diagnostic assumes every corpus query wanted context.** If a meaningful share of the corpus is
`not_applicable`, then some historical C=2 clustering is **an artifact of the instrument, not a
context-assembly failure** — the response was correct and the rubric had nowhere to put it.

🔴 **Stated as a hypothesis the tagging pass will test, not a finding.** I have not measured the
distribution and will not claim it before Lead's pass reports one. **If a material share comes back
`not_applicable`, the C=2-clustering diagnostic needs rewording in the rubric** — and I own that edit.

**So the first thing the pass should report is the distribution itself**: how many queries in each bucket,
out of how many total. That number is the finding, before any rescoring.

## 6. Reporting requirement

**Report C per bucket, never pooled.** A single mean across `required` and `not_applicable` queries
answers no question anyone has. Retest output should carry:

> `C-axis: required n=__ mean=__ · optional n=__ mean=__ · not_applicable n=__ (excluded from the
> context-assembly signal)`

**The `required` bucket alone is the context-assembly health signal.** That is what the C axis was for.

## 7. Scope, and what I am not asking for

- **No rubric text change lands with this spec.** The C-axis tables in CT v2.3.4 stay as they are; this
  adds an input the judge previously lacked. **Any rubric edit waits on §5's distribution.**
- **Applies to the BYOC Recomposition Rubric too**, whose C axis anchors to CT — same missing input, same
  fix, one tagging pass serves both.
- **`optional` is expected to be the hardest call.** If a query is genuinely ambiguous, tag it `optional`
  and flag it; a mis-tag toward `optional` is the least damaging error, because it neither manufactures a
  failure nor excuses one.

---

*CXO spec, 2026-08-31. Lead owns the corpus and executes the pass. This item sat four months filed as
"author v2.4" when the job was "tag a corpus" — worth remembering that the filing, not the work, was the
blocker.*
