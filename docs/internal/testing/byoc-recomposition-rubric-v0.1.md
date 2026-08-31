---
type: scoring-instrument
name: BYOC Recomposition Rubric
version: v0.2 — DRAFT, unratified. T=3 REVISED on probe evidence 2026-08-30 (the "must render" claim
  was falsified); axis still PENDING-PROBE for issuing a PASS — one vendor, n=1/cell, known design confound.
date: 2026-08-30
owner: CXO
branched_from: Colleague Test Rubric v2.3.2 (`colleague-test-rubric.md`), per its own §"How to Extend
  This Rubric — Branch-or-Anchor Discipline" (v2.3)
tier_status: instrument UNRATIFIED (PPM/PM own tier) — but the REQUIREMENT it serves is ratified law
  as of 2026-08-30 (ESSENCE v1.0 commitment 7). See the status banner; the two are not the same thing.
closes: one of PDR-006's two named pre-user gates ("the recomposition rubric branch", PDR-006:35)
last_updated: 2026-08-30
currency_claim: revise-on-probe-result
---

# BYOC Recomposition Rubric — v0.2

**The instrument for scoring Piper's quality on a surface where Piper does not compose what the user
reads.**

> ### 🔴 STATUS CHANGE 2026-08-30 — ratified law now depends on this, and it is not finished
>
> **ESSENCE v1.0 was ratified this afternoon. Commitment 7 says: *"Operationalized by the already-ratified
> Colleague Test…; on the BYOC path, its recomposition variant carries the same gate."*** Verified in the
> file, not taken from a summary.
>
> **Read the two halves separately, because they have different status:**
>
> - ✅ **RATIFIED — the requirement.** That the colleague property is gated on BYOC by a
>   recomposition-aware variant is now current law.
> - 🔴 **NOT RATIFIED — this instrument.** v0.2 is a draft. Its **T axis has now been probed once and
>   partly falsified** (§3 revision banner): T=3 was rewritten on the evidence, and the axis still scores
>   `PENDING-PROBE` rather than PASS — one vendor, n=1 per cell, and a design confound I introduced.
>
> ⚠️ **So the gate named in ratified law cannot currently issue a pass on its load-bearing axis.** That is
> not a defect in the ruling — the requirement is right. It means **#1463 stopped being PDR-006
> housekeeping and became load-bearing for a ratified commitment**, and the probe
> (`byoc-recomposition-probe-packet-2026-08-30.md`) is what closes the gap. Recorded here so the two
> can't drift apart, and so nobody discovers it by trying to apply the instrument.

> ⚠️ **This is a BRANCH, not an extension.** Per CT v2.3's Branch-or-Anchor discipline and its canonical
> worked example (UI Lifecycle Verification Rubric v0.1, PPM 2026-05-10), a new instrument for a different
> measurement surface must be **named, versioned, given provenance, and cross-referenced back** — never
> silently adapted. The Apr 26 C-axis incident is what happens otherwise: two responsibly-authored rubrics
> sharing a letter with different meanings, converging on PASS while their methodology silently diverged.

---

## 1. Why a branch is required, not optional

📄 **PDR-006:246, ratified**: *"Colleague Test rubric (R/C/T) — built for response text Piper composes.
Here the client LLM composes what the user reads. **We are no longer scoring what the user sees**; tone in
particular becomes the client's."*

The Colleague Test's unit of analysis is **the reply**. On the BYOC/MCP path there is no reply of ours —
there is **tool output**, which a model we do not control paraphrases into a reply. Applying R/C/T here
does not produce a wrong score; it produces a score **of a different artifact than the one the user read**,
reported in the vocabulary of a ratified gate. That is m-44 in its most expensive form: not an error, a
false clear.

**This matters right now, not eventually.** 📄 PDR-006:35 names exactly two open pre-user gates: #1458
(cross-caller state isolation) and *"the recomposition rubric branch"* — this document. And ESSENCE v0.1
(2026-08-29) makes the MCP path the surface **all new build goes to**, with the web-chat surface in
maintenance mode. The gate now stands in front of the only lane that's moving.

## 2. What this instrument scores

**The measurement surface is the tool layer's output** — what we hand the host: tool results, tool
descriptions, error and decline strings. Not the user-visible reply, which we cannot score because we
cannot author it.

**Shape preserved for cohort coherence** (per the branch discipline): three dimensions, **0–3 each**,
**≥7/9 PASS**, **any single 0 is auto-fail**. Meanings branch as follows.

## 3. The dimensions

### R — Sufficiency *(branched from CT's Relevance)*

*Does our output carry enough for the host to compose a correct, specific answer without inventing the
parts we left out?*

| Score | Criteria |
|---|---|
| 0 | Bare identifiers, status codes, or an empty envelope — nothing the host can say anything true about. **The host must invent or say nothing, and it will not choose "say nothing."** Auto-fail. |
| 1 | Technically complete but machine-shaped (IDs, enum codes, unlabeled fields). The host can only paraphrase it into vagueness. |
| 2 | Enough to answer, but flat — the host must decide what matters, and its guess is not our judgment. |
| 3 | Carries the answer **and its salience**. The host can compose a good reply without making a product decision we should have made. |

⭐ **Why salience is a scored dimension and not a nicety**: on the chat surface, Piper's judgment about
what matters shows up in how Piper writes the sentence. Here that sentence is written by someone else.
**If salience isn't in the payload, it isn't anywhere.**

### C — Context *(meaning ANCHORED to CT v2.3.2; evidence standard BRANCHED)*

*Does the output use Piper's real assembled project state, and is it honest about gaps?*

**Anchored deliberately** — this is a property of what we emit, so CT's meaning transfers intact, and
anchoring is a decision recorded here rather than an omission. Score 0–3 per CT v2.3.2's Context table,
including its fabrication auto-fail and its fresh-account C=2 ceiling.

⚠️ **One narrow divergence, and it must be stated**: CT's C=3 requires project-context injection to be
*"visible"* — visible **in the response**. Here visibility is the host's decision, not ours. So the
evidence standard shifts from **visible to the reader** to **present and unavoidable in what we emit**.
Same meaning, different place to look for it.

### T — Honesty-under-recomposition *(fully branched; REPLACES Tone)*

*Does the output's honesty survive paraphrase by a model we do not control?*

**CT's Tone axis is unscoreable on this surface and must not be carried over.** Voice, cadence, brevity,
the absence of bot tells — every one is composed by the host. Scoring Tone here would be scoring the host
vendor, not Piper.

What replaces it is the risk PDR-006 called *"the sharp one"*: 📄 *"Our honest-decline discipline… is a
property of **text we control.** Hand a hedged tool response to someone else's LLM and the hedge may not
survive into what the user reads."*

**The governing principle, and the reason this axis is actionable rather than merely worrying:**

> ⭐ **Honesty carried in prose is droppable. Honesty carried in a *directive* field is harder to drop.**
> 🔴 **REVISED 2026-08-30 on probe evidence — the original read "…in structure is not [droppable]," and
> that is FALSIFIED.** A host silently dropped `coverage: "partial"` (item 3). **Structure alone buys
> nothing; a field that constrains what may be claimed is what survived.** Full evidence, the two
> competing explanations, and the confound in my own packet are in the revision banner below the table
> — but the claim is corrected *here*, at the point of assertion, because a correction that lives only
> further down is one a reader can quote past.
> A sentence saying "I don't have data for last quarter" is an input to paraphrase. A field saying
> `may_claim_complete: false` constrains the claim rather than describing the data. This is the same move
> ESSENCE commitment 1 makes for portability (*"architectural, not policy"*) and commitment 4 makes for
> honesty (*"enforced structurally where possible… rather than by vigilance"*) — applied to the one
> surface where our own vigilance provably cannot reach.

| Score | Criteria |
|---|---|
| 0 | The output **permits a confident overclaim** — e.g. an empty result set returned as an empty list with no explicit absence marker, letting the host fill the silence. Auto-fail. |
| 1 | Uncertainty is present but purely prose, buried mid-payload, and easy to drop under summarization pressure. |
| 2 | Uncertainty is prose but prominent and hard to miss — survives a careful paraphrase, probably not a terse one. |
| 3 | ~~Absence, partiality, staleness and decline are carried in **structure the host must render or visibly omit**, not in sentences it may quietly drop.~~ **FALSIFIED 2026-08-30 — see below.** Revised: the qualification is carried in a field that **constrains what may be claimed** (a directive), not merely one that **describes the data** (a descriptor). |

> ### 🔴 T-AXIS REVISED ON EVIDENCE, 2026-08-30 — my governing hypothesis is PARTLY FALSIFIED
>
> PA ran the probe (Claude arm; full results `dev/active/probes/RESULTS-probe-b-recomposition-2026-08-30.md`).
> **The core case confirmed the hypothesis and a second case reversed it**, so the scale changes.
>
> - ✅ **Item 1 (failed read vs. empty)** — prose **fabricated**: *"your todo list is currently empty"*
>   stated from a **failed** read, the exact claim `conversational_floor.py:214–226` exists to forbid,
>   reproduced live with no floor to block it. Structured stayed clean.
> - 🔴 **Item 3 (partial coverage)** — **structured DROPPED the hedge that prose kept.** No mention of
>   partial coverage anywhere in the reply.
>
> ⚠️ **So "structure the host MUST render or visibly omit" is false as written.** A host can silently
> drop a structured field exactly as it drops a sentence. That clause promised a guarantee the format
> does not provide, and it was the load-bearing word in the whole scale.
>
> #### ⚠️ And the reason the run cannot settle *why* is a design flaw in my own packet
>
> **I varied two things at once inside the "structured" arm and called it one variable.** Checking my
> own payloads after the fact:
>
> | Item | Structured field | Relation to the question asked | Outcome |
> |---|---|---|---|
> | **1** | `may_claim_empty: false` — **a DIRECTIVE** (+ `read_status`) | the failure *is* the whole answer | ✅ survived |
> | **3** | `coverage: "partial"` — **descriptor** | peripheral; 3 real issues to enumerate instead | 🔴 **dropped** |
> | **4** | `freshness: "stale"` — descriptor | central ("what's the current state?") | ✅ survived |
> | **6** | `action_performed: false` — descriptor | *is* the answer | ✅ survived |
>
> **Item 1 is the only structured payload carrying a directive field.** So the run cannot separate
> *"structure helps"* from *"directives help"* — and a third variable (whether the qualification is
> central or peripheral to the question) tracks the outcomes just as well: item 3 is both the only pure
> descriptor that was peripheral, and the only one dropped.
>
> **Two candidate explanations, deliberately not chosen** (n=1 per cell, one vendor):
> **(a) directive > descriptive** — a field that constrains a claim is honored; one that merely
> describes data is treated as decoration. **(b) central > peripheral** — a qualification survives when
> omitting it would leave the question unanswered, and is dropped when there is ample positive content
> to fill the reply without it.
>
> **The next run must hold one constant while varying the other** — e.g. item 3 re-run with
> `may_claim_total: false` alongside `coverage: partial`. That is a two-call experiment.
>
> #### What changes now, and what does not
>
> - ✅ **The scale changes now** — T=3 requires a *directive* field, on the evidence above.
> - 🔴 **The axis stays `PENDING-PROBE` for issuing a PASS.** One vendor (the GPT arm collected **zero**
>   data — an OpenAI quota exhaustion, not a finding), n=1 per cell, and a known confound in the design.
>   **Revising criteria on evidence and licensing a pass are different acts**; only the first is earned.

#### Worked example, traced in running code — and it changes the question

**Take the #1425 honesty class**: a source read *fails*, and the rule is that Piper must say it couldn't
check, **never** present the failure as emptiness. This is a shipped, tested implementation of ESSENCE
commitment 4. Trace where it actually lives, naming the layer (m-43):

- ✅ **Structured half already exists and travels.** A failed read returns `{"source_failed": True}`
  (`first_contact.py:197,214`; `canonical_handlers.py:1650,1656`), the assembler merges it
  (`context_assembler.py:278,424`), and it survives as a **field**, not a sentence.
- 🔴 **The honesty half is a PROMPT DIRECTIVE.** The rule is enforced by appending instructions to the
  floor's system prompt — `conversational_floor.py:762`, `:817`, `:1078`: *"say you couldn't check
  GitHub just now — never claim the repo is empty and never invent items."* That is `lines.append(...)`
  into a prompt for **our own** LLM.

⚠️ **On the BYOC surface there is no floor prompt, because there is no model of ours in the loop.** So
for this class the honest framing is not *"will our hedge survive paraphrase?"* — **there is currently no
hedge in the payload to survive.** The honesty exists as an instruction to a model that does not exist on
that surface. *Correctly scoped: nothing has been lost, because the hosted server isn't built yet
(`services/mcp/` today is the MCP **client** family — PDR-006's conflation guard applies). Nothing has
been designed either, and this is exactly the design input PA said was cheaper to have before the tools
are written than after.*

⭐ **And the fix is nearly free, which is why this example is worth tracing rather than theorizing.**
The flag already exists end-to-end; only the *rendering instruction* is chat-specific. **Emitting
`source_failed` as a structured field in the tool payload is a T=3 shape at roughly the cost of not
dropping it** — the expensive-looking option is already most of the way built.

> 🔴 **The T-axis criteria above are HYPOTHESES, not validated scoring.** I have not tested whether hedges
> survive recomposition; nobody has. **Until §6's probe runs, this rubric must not be used to issue a PASS
> on T** — a score from an untested criterion is exactly the false clear this document exists to prevent,
> and shipping one inside the instrument built to catch it would be the third iteration of that shape this
> month. Score R and C; record T as `PENDING-PROBE`.

## 4. Capability truthfulness — a precondition, not a fourth dimension

PDR-006:249 proposed three branch dimensions; the third, **capability truthfulness**, is a property of the
**tool catalog** — evaluated once per tool, not once per response. Making it a fourth axis would break the
0–9/≥7 shape the branch discipline says to preserve, for a thing that isn't per-response anyway.

**So it is a gate precondition**: before any tool ships, its name and description must claim only what it
does. On this surface the description is read by the host as much as by the human, and 📄 PPM's recorded
counter-risk applies — situation-shaped names may route *worse* than object-shaped ones, and **nobody
knows which way that goes.** Both questions share a rig with §6's probe.

## 5. What this instrument does NOT tell you

- **Nothing about what the user actually read.** By construction. A 9/9 here means we handed the host
  everything it needed and made the honesty hard to drop — not that the reply was good.
- **Nothing about tone, voice, or whether it sounded like a colleague.** Those are the host's.
- **Nothing about routing** — whether the host picked the right tool is a separate measurement.

**The Colleague Test itself remains the right instrument for the chat surface**, which is in maintenance
mode but still carries every real tester today. This branch does not supersede it. Two surfaces, two
instruments, one question.

## 6. The probe this rubric is blocked on

📄 **PA, 2026-07-30, and it is still true**: *"Testable NOW — this gate does not depend on the build. It
needs a hedged/qualified text blob and a client LLM, not `mcp.pipermorgan.ai`. So it can close during
Phase 0 rather than waiting on Phase 2, and it should — a negative result would change what the tool layer
has to emit, which is cheaper to learn before the tools are written."*

**As of today that window is still open**: #1688 is the only MVP-milestone item on the MCP path and has
no build commits yet. It closes the moment tool output starts being written.

**Design:**

1. **Corpus** — the hedge shapes we actually emit, not invented ones: honest decline, partial data,
   empty result, stale data, degraded-provider fallback. Draw the wording from the shipped strings
   (`consent_gate.py`, `first_contact.py`, the decline paths) so the probe tests our real prose.
2. **Treatment** — present each inside a realistic tool-result frame to the hosts we target
   (Claude, ChatGPT), with a user question that creates summarization pressure.
3. **Measure** — does the qualification survive into the composed reply, weakened, or vanish?
4. ⚠️ **Negative control, non-optional** — include *unhedged, confident* outputs. If the probe reports
   "survives" for both hedged and unhedged, it is not measuring hedge survival and its positive result is
   meaningless. **A probe that cannot fail has not passed.**
5. **Paired structural variant** — run the same fact as prose-hedge and as structured-field, to test §3's
   governing principle directly rather than assuming it. It is the whole basis of the T scale and it is
   currently my hypothesis, nothing more.
6. **Denominator, stated** — which hosts, which model versions, how many trials, on what date.

> ⚠️ **This result carries an expiry date, and the rubric must say so where the result lands.** The model
> composing our text ships new versions without telling us; a hedge that survives today's host may not
> survive its successor. **This is a standing property of the BYOC surface, not a caveat on one probe** —
> every claim we make about recomposition behavior is a claim about a third party's current build.

## 7. Provenance and cross-reference

- **Branched from**: Colleague Test Rubric **v2.3.2**, per its §"How to Extend This Rubric —
  Branch-or-Anchor Discipline" (v2.3, CXO 2026-04-27, from CIO's Apr 26 rubric-drift framing).
- **Pattern followed**: UI Lifecycle Verification Rubric v0.1 (PPM, 2026-05-10) — the canonical worked
  example of legitimate branching. Shape preserved, meanings explicitly branched, provenance stated,
  cross-referenced back.
- **Divergence summary** — R branched (Relevance → Sufficiency) · C anchored in meaning, branched in
  evidence standard · **T fully branched** (Tone → Honesty-under-recomposition; CT's Tone is unscoreable
  here) · capability truthfulness held as a precondition rather than a fourth axis.
- **Grounded in**: PDR-006 §"Pre-user gates" (:35) and §246–265; ESSENCE v0.1 commitments 4 and 6.
- **Add a back-reference in `colleague-test-rubric.md` §"How to Extend This Rubric"** when this branch is
  ratified — not before, so the CT rubric never points at an unratified instrument.

---

*CXO v0.1, 2026-08-30. Written because PDR-006 named this gate open on 2026-07-19 and ESSENCE made the
surface it gates the only one being built on. **The instrument is not done until §6's probe runs** — what
exists today is a scoreable R and C, an honest T-shaped hypothesis, and a test that can falsify it.*
