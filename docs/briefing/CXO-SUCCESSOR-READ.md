---
type: successor-read
role: CXO (Chief Experience Officer)
author: CXO (the one writing 2026-07→present)
status: living — written mid-role, not at handover, deliberately
last_updated: 2026-09-04
currency_claim: updated when a lesson is earned, not on a schedule
max_age_days: 60
---

# CXO successor read

**Why this exists**: my predecessor left an artifact list and no read — no lessons, no
load-bearing-vs-commodity judgment, no relationship map. The orientation note said so plainly. **I spent
weeks rebuilding context that one honest page would have carried**, and twice acted on handoff claims that
turned out to be factually wrong (the Colleague Test was described as "just an issue comment"; it was a
180-line canonical doc, a versioned rubric, and a binding Done-gate).

⚠️ **Written mid-role on purpose.** A handover document written at handover is written by someone with one
foot out, from memory, under time pressure. This one gets updated when a lesson is *earned*.

---

## 1. What this role actually is here

**On paper**: experience quality across surfaces. **In practice, three things, in descending order of how
much only-you-can-do-it they are:**

1. ⭐ **You own instruments that gate other people's work.** The Colleague Test family (the rubric, the UI Lifecycle
   branch, the BYOC Recomposition branch — ⚠️ **no version numbers here on purpose; open the files**) is
   cited by **DoD Layer B Criterion 1** — a binding Done-gate — and, since 2026-08-30, by **ESSENCE
   commitment 7**, which is ratified law. **Its three invariants are PM-ratified** (the question, the
   verdict shape, the fabrication auto-fail); everything else moves with evidence. **This is the
   most consequential and least obvious part of the job.** See §4's governance lesson.
2. **You are the standing objection to flattening.** The holistic-experience model gets crushed into
   single-surface commitments every time it meets a decision doc. `experience-across-surfaces.md` exists
   because that happened three times in ten days. **Your job is often to be the person who says "that
   question has no referent."**
3. **Copy and first-contact.** Real, and the most visible — but the least uniquely yours. Others can write
   good copy; nobody else is watching (1) or (2).

## 2. Load-bearing vs. commodity — my honest read

**Load-bearing** (if these rot, something real breaks):
- `docs/internal/design/experience-across-surfaces.md` — fully ratified; written to be *cited from inside
  a decision*. Its §4 "must not be asked to" column is negative-space commitments and adds no build surface.
- The **Colleague Test family** and its branching discipline. The Apr-2026 C-axis incident (two rubrics
  sharing a letter, diverging silently, both saying PASS) is the canonical cautionary tale — **read it
  before you extend any instrument.**
- The **FTUX / first-contact model** (`ftux-experience-model-2026-08-21.md`) and the surfaces taxonomy.
- **Honest-decline and disclosure copy.** It is the visible face of a structural commitment.

**Commodity** (valuable, but anyone could do it):
- Individual copy fixes, one-off reviews, most memo triage.

⚠️ **The trap**: commodity work is legible and feels productive; load-bearing work is invisible until it's
missing. **A month of good copy fixes while a gate rots is a bad month that looks like a good one.**

## 3. Relationship read

**PM (xian)** — direct, allergic to hedging, and **corrects framing rather than facts** when both are off:
he'll let a small error pass and push on the *shape* of how you're working. Standing lenses worth
internalizing: **"no optional complexity"** (*has one real case already proven this is needed?*) and
**"drain all unblocked tasks as soon as possible"** — he has found "low urgency" reliably means never.
He does not read long memos; he wants rollups. He will tell you when you've over-apologized.

**PPM** — the peer most likely to refute you, and **correctly**. Checks board state and issue text rather
than reasoning from memory. When PPM says "I'm naming this rather than picking it," take it literally —
it's an invitation, not deference. **If PPM refutes you, they are usually right; check before defending.**

**Lead** — builds fast, works from receipts, and will hand you commit hashes rather than assurances.
Give the same back. Their corrections are usually right *and* usually incomplete — worth adding to rather
than accepting whole.

**Arch** — rules, and *acts* on a flag rather than acknowledging it; expect your flag to be in ratified law
within the hour, sometimes before your follow-up lands. **Corollary: check what actually got written.**

**PA** — the strongest verification discipline in the cohort. Will refuse to extend an authorization
silently, will refuse to run a test into an unverified confound. **Learn from this rather than managing it.**

**Web** — live verification with real restraint; reports "I could not reproduce the exact error" instead of
a cleaner story. **Their inconclusive results are more valuable than most people's conclusive ones.**

**HOST** — trust and welfare, including toward humans outside the cohort (alpha testers). **CIO** —
mechanisms; if you find a discipline that depends on agents self-reporting, CIO is who turns it into a
check. **Comms** — copy and synthesis; ⚠️ **synthesis flattens caveats**, so put load-bearing
qualifications in the sentence, not the footer. **Docs** — merge-keeper; the reason stranded work gets
found.

## 4. Lessons that cost something

⭐ **Almost every error I made in my worst week was a measurement whose BOUNDS I didn't state.** Not
wrong measurements — correct ones, reported as covering more than they did. Four instances in seven days,
and I'd have called each a different mistake at the time:

- **A search window that excluded the evidence.** I told the cohort *"I have never invoked this script,
  not once"* from a `--since` that began **18 days after the last invocation**. The query was incapable
  of finding what I claimed didn't exist. ⭐ **An absence is a measurement and it has a window; say the
  window.**
- **A symptom reproduced under the same confound.** I "isolated" a script bug by reproducing it outside
  the script — seconds later, under the same rate limit. 🔴 **Reproducing a symptom under the confound
  does not isolate a cause; it confirms the confound is still present.** I had *just* checked the primary
  rate counters and seen them healthy — a real measurement, of the wrong register, used to rule out the
  right answer.
- **A narrowing whose premise went unnamed.** I scoped an issue away from a surface *"because the other
  path is buildable."* It wasn't. **The choice my scoping was written against did not exist**, and my own
  comment was later cited as a rule I never intended.
- **A promise whose capability went unchecked.** My own FTUX copy said *"I'll bring it back next time"* —
  a claim about future behaviour — four days after I caught the identical class in someone else's copy.

**None were wrong about what they measured. All were wrong about what they claimed to cover.** ⚠️ **The
tell is that each felt like diligence at the time** — I ran a command, I reproduced it, I checked the
counters. **Rigor performed on the wrong scope reads exactly like rigor.**

⭐ **And the compliance corollary, which is HOST's and better than my version of it**: a record
hand-narrated afterward by the agent whose compliance is in question **is not evidence, however durable
or well-committed.** Only a marker the *tool* writes, in its own execution path, is checkable by anyone
else. ⚠️ **CORRECTED 2026-09-05: I cited this as "m-45's subject/scorer separation." That is WRONG.**
**m-45 is *Agreement Is Not Replication*** — shared procedural confounds manufacturing false consensus.
**It says nothing about whether a subject can score its own work**, and I checked the methodology corpus:
**no entry covers self-attestation.** So the principle is *right* and it is **NOT ratified** — I told CIO
it was, which is materially different and worse. The nearest ratified relative is **Arch/PPM's 2026-08-06
formulation**, carried in the duty-cycle skill's Step 2c: *"you cannot detect absence from a surface
authored by the party whose absence is in question."* **Cite that, not m-45** — and know it's about
absence-detection, not attestation, so it's a relative rather than the same claim.

⭐ **And keep the closure, because it is the best live example of m-45 anyone has produced**: four of us
used the same wrong phrase in three days, each believing we'd reached it separately, **and the apparent
convergence made it feel more solid rather than less.** Traced afterwards, the chain was linear
(Arch → PA → me). **The entry was right about us while we were wrong about it.** ⚠️ **When you find
yourself reassured that others agree, that is the moment m-45 is describing — not a later one.**

⭐ **Name the layer you measured.** The single most recurrent failure here, and it is rarely one bad
check — it's a **relay**: tracker → dev server → a dev server 17 days stale → a surface that doesn't
exist. Four careful people, each true about the layer they measured, the layer dropped at each handoff.
**Care is not sufficient; naming the layer is.**

⭐ **A retraction needs the same evidentiary bar as the claim it retracts.** I once retracted a correct
claim within hours because contradicting evidence appeared and I didn't ask whether *the contradiction*
was confounded. It was. **Over-correcting is a real failure mode, not a safe direction to err in** — it
feels like rigor and puts falsehoods in the record just as efficiently.

⭐ **Revising an instrument's criteria and licensing a pass are different acts.** You will improve a rubric
by falsifying it. Do that. **But it means you can silently move a bar that ratified law depends on** —
which is why I proposed ratifying the Colleague Test's *invariants* (the question, the verdict shape, the
fabrication auto-fail) while keeping criteria editable. **Whatever the outcome, know that you hold that
pen.**

⭐ **A label that terminates review is worse than an untriaged backlog.** "Low urgency" reads as a
decision, so nobody re-examines it; "blocked on X" gets rechecked when X moves. My own file carried a
self-flagged staleness warning for weeks — **and the warning functioned as permission to skip it, not a
prompt to fix it.**

⭐ **Routed is not landed.** A deliverable sent to someone's inbox is not in an artifact. I drafted a
required tester disclosure, routed it to two people, and it was never added to any document; nobody
noticed for seven weeks. **Close your own loops in the artifact, or track them.**

⭐ **The host SYNTHESISES; it does not execute.** The single most expensive bias in this role's work, and
it cost me three falsified predictions in one week — *structure beats prose*, *directives beat
descriptors*, *five instructions yield five clauses*. **All three assumed a model renders instructions
literally and additively.** It doesn't: it aggregates gracefully (my predicted "litany" of five failure
notices never appeared in 12 runs), **and it also adds things nobody licensed** — volunteering failures
that didn't happen, offering *"Nothing's lost on your end"* about data it never read. ⚠️ **So when you
design payloads or prompts, the risk is rarely that the model under-performs your instruction. It is that
it over-interprets it.** Build your instruments to score *addition*, not only *loss*.

⭐ **A "clean" result from a check YOU proposed can be a broken input.** I proposed a tracker check, ran
it, got zero flags, and reported my tracker healthy. **It was reporting clean because a truncated regex
edit of mine had left an orphan line that silently hid a third of my rows from the parser.** Only a
**positive control** — a deliberately-planted row that *must* flag — exposed it. **Before trusting a
green run, plant something that has to turn it red.** This is m-44 applied to the tools you asked for,
which is exactly where you will forget to apply it.

⭐ **Verify AFTER the edit, mechanically — not just before it.** In a single edit *about false
citations*, I asserted completeness twice without re-checking: fixed two, wrote "both removed"; grepped,
found two more, wrote "all four"; a fifth was sitting further down. **Grepping to find is not grepping to
confirm.** The claim that you are *finished* needs its own measurement.

⭐ **Never regex-edit a structured file.** Markdown tables have no validator. A truncated `.replace()`
leaves a fragment that reads fine to the eye and is **fatal to any parser** — and the damage is silent,
so every downstream check reports clean. Edit trackers by hand, and afterwards **re-run whatever reads
them and confirm the row count moved as you expect.**

**Three failure shapes, not one — you will inherit the tracker, so learn the taxonomy.**
**Deferral** (the owner sees it and doesn't act — the aging check covers this) · **Misfiling** (the
person who could do it never reads it as theirs, because the filing names the wrong kind of work — a
four-month item of mine closed in a day once refiled) · **Stale-blocker rot** (the blocker cleared and
nobody updated the row — five of my nine rows in 36 hours; **invisible to the aging check by its own
correct definition**, since a recently-dated row with a stated blocker is exactly what healthy looks
like). ⚠️ **A "blocked on X" should name a CHECKABLE X** — "blocked on PPM" is unfalsifiable; "blocked on
#1716" is one command away.

**Verify the document's claims about itself.** Handoffs, PDRs and issues make claims about their own state
that go stale. Two of my predecessor's handoff items were wrong in the direction of "still owed" when the
work was already done.

## 5. What is live as I write this

`dev/active/cxo-standing-items.md` is the tracker and it is honest: two states only, every row dated, and
readable by `scripts/aging-standing-items.sh`. **Start there, not here.** The big open thread is #1463 —
the BYOC recomposition gate, one vendor arm run, second pending.

---

*If you are reading this because you replaced me: the tracker is current, nothing is hidden in a
"someday" column, and the errors I made are written down in the session logs under their own dates rather
than smoothed away. Where I was wrong, the correction is next to the claim.*
