---
type: methodology
title: Open It — A Summary Is Not Its Contents
valid_from: "2026-09-07"
last_updated: "2026-11-12"
---

# Open It — A Summary Is Not Its Contents

**Status**: Proven. Set 2026-11-12 by CIO (standing item 9p).
**Summary**: Do not judge a document, ticket or report by its title or summary; open it and read the contents before relying on it.

**Status note**: **PROVEN (2026-10-19)**: the promotion trigger below was met by a third instance from a
third seat (Lead, #2081, evidence item 3), six weeks after filing, on an unrelated topic, with a
measured cost (xian: "it has wasted at least half a day"). As filed: **Two instances, two seats, one week** — CXO's own m-45 miscitation and Exec's
#1386 criterion-3 miss — arrived at independently in real time (two separate real mistakes, on two
unrelated topics), with only the *discriminator connecting them* found afterward, not the incidents
themselves copied from one another. That's real cross-seat corroboration, not a shared confound —
already a stronger evidentiary footing than methodology-51 had at its own filing (one seat).
**Promotion trigger**: a third independent instance, from a third seat. *(Met 2026-10-19.)*
**Filed**: 2026-09-07 by CIO · **Discriminator ("watch it fire" vs. "open it")**: CXO, 2026-09-07,
found by actually opening methodology-49 rather than reasoning from its title — noted by CXO as the
minimum given what was under discussion. **Origin material**: CXO's re-sort of their own m-51
evidence (2026-09-07), which surfaced this shape as a byproduct while correcting a different entry.
**Related**: [[methodology-49]] (the close neighbor this entry had to be checked against before
filing — see Boundary), [[methodology-45]] (the hygiene discipline this entry's own evidence had to
survive twice), [[methodology-51]] (the entry this material was originally, and wrongly, sorted
into)

## The claim

**When an artifact's actual content is available by simply reading it — static, present, no
runtime state in question — reasoning from a summary, title, or memory of that artifact instead of
opening it is a distinct failure from not having verified a mechanism's live behavior.**

Two real instances this week: CXO cited methodology-45 for a claim it doesn't make, working from
memory of what the document was about rather than its actual text. Exec ruled a gate criterion
"definitional, no re-run needed" because "three multi-turn scenarios" sounded like a fixed
definition — without opening the checklist, which said the scenarios must be *executed against the
deployed Fly artifact* on a specific date, an artifact-execution claim exactly like the other
perishable criteria in the same gate. In both cases the correct answer was sitting in a file,
unopened, the whole time.

## Boundary — checked directly against methodology-49 before filing, not assumed distinct

This entry started as a hypothesis that a batch of instances might be m-49 read at a different
altitude. CXO tested that by opening m-49's actual text rather than reasoning from its title — the
same discipline this entry is about, applied to filing it. The result narrowed the candidate family
from five to three to two, and the boundary that survived is precise:

> **m-49's remedy is "watch it fire." This entry's remedy is "open it."**

m-49 ("Described Is Not Running") is about **runtime state that cannot be established by reading
anything** — a hook's liveness, a fix's actual effect — because the only way to know is to observe
it fire. Two of the five original candidate instances (CXO's FTUX-copy promise, the #1688 narrowing)
are squarely m-49: each asserted something about a mechanism's *running behavior* that only a
behavioral observation could confirm, and neither was confirmed. Those were folded into m-49's own
corroborating-instance list rather than duplicated here.

**The two instances that survived into this entry needed no observation of anything running.** The
m-45 document was sitting there, correctly text, doing exactly what it was supposed to do — CXO's
error was never about m-45's behavior, only about what CXO believed it said. The gate checklist was
a static record with a plainly-readable execution requirement — nothing needed to fire for the
"multi-turn scenarios" description to resolve into its actual, checkable content. Where m-49 says
*you cannot know without watching*, this entry says *you could have known by reading, and didn't.*

| | m-49 | This entry |
|---|---|---|
| What's in question | a mechanism's **runtime state** (live? firing? actually fixed?) | a **static artifact's content** (what does it actually say?) |
| Why the error happens | the artifact's own description is mistaken for its behavior | a summary, title, or memory of the artifact is mistaken for its content |
| The cure | observe it fire — nothing else resolves it | open it — the answer was already sitting there |

## The evidence

1. **CXO's methodology-45 miscitation.** Cited "m-45" for a self-attestation-adjacent claim from
   memory of the document's general subject, when m-45's actual and only claim is about independent
   agents sharing a procedural confound (agreement, not replication) — a different failure mode
   entirely, later filed correctly as methodology-50. The document was never opened before being
   cited.
2. **Exec's #1386 criterion-3 miss.** Classified a gate criterion as "definitional, needs no
   re-run" from its one-line description ("three multi-turn scenarios") without opening the
   checklist, which specified execution against a dated deployed artifact — making it perishable
   evidence exactly like the other three criteria that DID get re-run, and in fact the *oldest*
   evidence in the whole gate (2026-07-12, older than any of the others).
3. **Lead's "one-admin rule" (#2081, 2026-10-18 → 10-19; the promoting instance).** HOST's ruling 1
   on #2081 (10-18 07:32 PT, an issue comment) reads: "Admin = xian's account only, through the
   existing fail-closed `require_admin` gate; no agent test account gets `is_admin`." Its point was
   *no agent accounts*. Lead's 10-18 log weighed granting admin to xian's mvp-tester account and
   recorded "HOST's one-admin rule argues against", dropped that lane, and chose a password reset
   for the seeded `dinp` account instead. On 10-19 the reset found no `dinp` user in the Fly
   database at all, and Lead's memo to HOST cited the ruling *inside quotation marks* as "admin
   stays on dinp only; mvp-tester not granted". Those words appear in no HOST text: a `grep` of the
   10-18 and 10-19 logs, sent mail and decisions.log finds them only in Lead's memo and in HOST's
   rebuttal. HOST opened the comment, found the gap and answered in one memo (10-19 10:03 PT): there is no
   one-admin rule, and two admin accounts of xian's are inside ruling 1. **Cost**: the grant waited a
   day on a rule nobody wrote; xian, 10-19 10:01: "We are standing on ceremony not granting admin to
   my mvp-tester account and it has wasted at least half a day."

   *Corroborating, same thread, CIO's own seat (not counted toward promotion):* my 10-18 log filed
   my own near miss on #2081 (describing migration a1599 from its filename before reading it) as
   "m-44's shape (a summary is not its content)". That is this entry's shape, cited under the wrong
   number from memory: m-44 is "Clear Is Not a Measurement". An m-52 instance in the act of naming one.

### What the third instance adds

- **A state and a ruling fused into a rule nobody wrote.** "dinp is the only admin" was a *state*,
  left by #1599's seeding migration on 08-12. "xian's account only" was a *ruling* with one
  ambiguous word (account, singular). Read together from memory, they became "the one-admin rule",
  and the summary then carried more authority than either source. Opening the ruling separates them:
  the text says who may not be admin, and says nothing about how many.
- **Quotation marks claim that you opened it.** A paraphrase in quotes, attributed to a seat, is
  read by everyone downstream as that seat's words, and an override then gets built against text
  that doesn't exist. Quote only what you have just read; otherwise paraphrase and say so.
- **The cheapest catch is the cited seat.** HOST corrected it in one read because HOST was cc'd on
  the memo that quoted it. A ruling cited back to its author gets checked; one cited only to others
  doesn't.

The first two instances share the identical shape: a plausible-sounding classification made from a fragment
(a title, a remembered gist, a one-line description) that a single read would have corrected, with
no ambiguity or judgment call once the actual text was in view.

## Why this earns its own entry rather than riding inside m-44 or m-45

m-44 is about an *instrument's* output misrepresenting its own coverage. m-45 is about *agreement
between agents* being mistaken for independent replication. Neither is about a single agent's
private act of citing or classifying an artifact from its own summary. This is closest kin to
CLAUDE.md's own standing rule — **"investigate before extending... read the whole source artifact
before acting on a fragment"** — and this entry is best read as the methodology-corpus record of
that prose rule's own failure mode, with dated real instances, rather than a new invention.

## The rule

> **Before classifying, citing, or ruling on an artifact based on its title, description, or your
> memory of it, open it. If the actual answer is available by reading — not by observing behavior,
> not by waiting for something to fire — a summary is never a substitute for having read it.**

Operational corollaries:

- **A one-line description in a checklist, an issue, or a title is a label, not the content.** If a
  ruling depends on what that item actually specifies, read the item.
- **A quotation is a claim that you just read it.** Put a seat's words in quotes only after opening
  the text; a ruling cited from memory gets paraphrased and labelled as such (evidence item 3).
- **An observed state is not a ruling.** "X is the only admin" may be what a migration left behind;
  before treating it as policy, find the text that made it one.
- **Citing a document by name, from memory of its general subject, is not citing its content.**
  Open it before attributing a specific claim to it — CLAUDE.md already says this for facts and
  figures; this entry extends it explicitly to citations.
- **The discriminator for whether this rule or m-49 applies**: ask whether the answer could, in
  principle, be settled by reading alone. If yes, this entry. If the answer requires watching
  something actually happen, m-49.

## How to apply

- Before ruling on anything whose classification depends on an artifact's specifics (a checklist
  item, a cited document, a criterion's exact wording), open the artifact and read the relevant
  passage — don't classify from its label.
- When citing a prior finding, a methodology entry, or a document by name, quote or closely
  paraphrase its actual claim rather than characterize it from memory — the two miscitations that
  motivate this entry (this one and methodology-45's own propagation incident) both happened this
  way.
- If you're unsure whether a shape belongs here or in methodology-49, ask whether observing runtime
  behavior would have changed the outcome. If reading alone would have sufficed, it's this entry.
