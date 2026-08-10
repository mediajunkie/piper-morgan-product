# Floor-Honesty Contract (#1517) — SPEC

**By**: Arch, 2026-08-10 · **Status**: 🟡 **SPEC for review — not ratified.** Owed per my 2026-08-09 inversion ruling, where I took decision ③ and ruled it **DECOUPLED** from the inversion: #1517 is a trust/safety defect that reproduces however routing got there, and coupling it to a month-long rebuild leaves a live honesty defect waiting on an architecture bet.
**Trust lens: ✅ HOST SIGNED OFF 2026-08-10 (§6). ⏳ CXO's copy/experience lens still owed.**

---

## 1. What #1517 actually contains — two behaviours, and only one is fixed

> *"Floor **denies reminder capability** AND **fabricates a retraction** ('the 3pm one wasn't saved') while the reminder IS in the database."*

| behaviour | status |
|---|---|
| **Denial of a registered capability** | ✅ **BUILT.** `wired_chat_actions()` feeds the floor's capability manifest (`conversational_floor.py:243-251`), and `test_floor_capability_honesty_1517.py` asserts it is **disjoint from `UNWIRED_WRITE_DECLINES`** — 13 tests |
| **Fabricated retraction** | ❌ **NOT BUILT.** No test anywhere covers it |

**The manifest approach cannot reach the second one**, and that is the whole reason this spec exists. A manifest answers *"can I do X?"* It cannot answer *"did X happen?"* — and *"the 3pm one wasn't saved"* is a claim about **state**, not about capability.

## 2. 🔴 The finding that shapes the contract: we have solved this FIVE times, never generally

Searching the test corpus for fabrication guards returns five, each built for its own surface, none shared:

| guard | surface | the fabrication it prevents |
|---|---|---|
| `test_real_plugins_do_not_fabricate_configured` | plugins | claiming "configured" without checking |
| `test_global_credential_write_admin_1485` | settings route | claiming *"wasn't saved"* (my own #1484 contract) |
| `test_places_1192` | places | *"I see…"* an implied-but-nonexistent connection |
| `test_todos_put_real_repo_1548` | todos route | a success payload not confirmed by the write |
| `test_file_search_simulation_guard_1436` | file search | simulated hits blended with real ones |

**#1517's floor retraction is the sixth instance of one class, and the sixth bespoke guard is the wrong response.**

⭐ **CXO named the principle on 2026-08-09, in a different thread, about acceptance criteria:**

> *"A criterion satisfiable by invention **passes confidently** — which is worse than one that fails."*

The same sentence describes the floor: **a denial satisfiable by invention is emitted confidently.** The user cannot tell it from a true one.

## 3. The contract — one property, derived per surface

> ## **An assertion about system state requires a read of that state.**
> **Fabrication is asserting-without-reading.** The floor may say *"I don't know"*; it may not say *"it wasn't saved"* unless something looked.

**Three obligations, in priority order:**

**H1 — No unread state claims.** The floor must not emit a proposition about stored state (saved / not saved / exists / doesn't exist / was deleted) unless that proposition is derived from a value the turn actually read. **If no read occurred, the honest form is an offer to look**, not a verdict.

⭐ **H1 covers NAMED ENTITIES, not just save-state — clarified 2026-08-10 because CXO and PPM both needed it and the original wording obscured it.** *"You have issue #1234 'Fix login bug', opened Tuesday"* **asserts that #1234 exists**, which is a proposition about stored state whether or not the word "saved" appears. **A named entity is a state claim.** CXO's live example (*"a fabricated attribute passes my item 4"*) and PPM's merged property 3 (*"no fabricated content, whether or not a connector is attached"*) are both H1, not a separate rule.

> **The carrier for an entity is a CITATION** — the read that produced it. Same mechanism as `StateFact`, different rendering: **you cannot cite a read you did not perform.** This makes #1536's AC3 gateable on *"every entity named in a user-facing claim carries a citation"* — ⛔ **so AC3 is unblocked, and it does not need a fourth wording patch.**

**H2 — No retraction of a recorded success.** If the turn's own prior action recorded a success, the floor may not contradict it. *(This is #1517's literal incident: the reminder was in the database and the floor said it wasn't.)*

**H3 — No denial of a registered capability.** ✅ Already built; folded in so the contract is complete rather than to re-implement it.

⚠️ **What this does NOT require**: that the floor read state on every turn. **The obligation is not to assert what it hasn't read** — silence and "let me check" both satisfy it. This matters because the expensive reading of H1 is "query the DB before every reply," and that is not what it says.

## 4. How to enforce it — and why the enforcement must not be a sixth string list

**⛔ Not a banned-phrase list.** `test_honesty_guard.py::test_no_banned_robot_script_phrases` is the right shape for *voice*; it is the wrong shape here. A phrase list is enumerable-by-hand and drifts — and the fabrications above share no vocabulary.

**✅ Enforce at the seam where a state claim is produced.** The floor's response path should be unable to interpolate a state proposition it did not receive as a value:

1. **A typed carrier**: state claims reach the response builder only as `StateFact(read_at=..., source=...)`. A claim with no carrier is not renderable. *Bad state unrepresentable, not forbidden.*
2. **The judge-evaluated corpus** (already the inversion's acceptance instrument) gets fabrication cases: **#1517's transcript verbatim as case 1.** A judge can evaluate "asserted a state fact" where a regex cannot.
3. ⚠️ **A denominator guard on whatever check lands** — `test_real_plugins_do_not_fabricate_configured` already carries one (*"Denominator guard: {path} missing — the fabrication check…"*), and it is the model to copy. **A fabrication check that silently scans nothing reports the same clean as one that scanned everything.**

## 4b. ⛔ SCOPE BOUNDARY — where this contract does NOT reach (added 2026-08-10)

**CXO applied §3 of the storefront page against this contract** (*"'knows your work' is a state a
stranger's account doesn't have yet"*). **Their conclusion is right and the copy should not ship — but it
is NOT H1**, and the contract must not be cited there.

> ⭐ **The test: if the ENFORCEMENT doesn't transfer, the contract doesn't either.**

H1's enforcement is a typed carrier — `StateFact(read_at, source)`, or a citation for a named entity.
**You cannot put a `StateFact` in a headline.** No read to carry, no renderer to gate, nothing for the
mechanism to bite on. **A contract cited where its mechanism cannot apply becomes prose** — an appeal to a
principle rather than a control, which is the failure mode this spec exists to prevent.

**The distinction, stated so it stays drawn:**

| | asserting past your evidence, where the evidence is… |
|---|---|
| **H1 (this contract)** | **a read the system did not do** — runtime, per-turn, gateable at the renderer |
| **the copy failure (CXO's lane)** | **a state the reader does not have** — general claim, cold audience, caught in human review |

**Adjacent, not the same, and the copy property deserves a name in CXO's vocabulary rather than a borrowed
home in mine.** ⚠️ **This contract is not the general theory of honest claims. It is a specific gate on a
specific renderer, and it is more useful at that size.**

⭐ **Why this section had to be written at all — CXO's diagnosis of their own filing, and it is the better half:**

> *"I never wrote that the storefront finding was H1. I put it in a memo that opened by **taking** the H1
> clarification, and in a page annotation **adjacent to** the fabrication material.*
> **Proximity does attributive work. A finding placed next to a contract reads as governed by it, whether
> or not anyone says so.** *The document's structure asserted something its sentences didn't."*

⚠️ **That is a hazard for THIS spec specifically**, because a contract is exactly the kind of document
people file things *near*. **Anything placed adjacent to §3/§4 will read as governed by H1 unless it says
otherwise.** **If you are adding material here that the typed-carrier enforcement cannot reach, say so in
the material — not only in the covering memo.**

## 5. What I am NOT deciding

- **The carrier's shape** (`StateFact` vs a Result type vs something CXO's copy work prefers) — a design call better made with the implementer.
- **Whether the other five guards migrate to the contract.** They work; the contract explains them. **Migration is a separate, non-urgent question and I would not gate #1517 on it.**
- **The user-facing wording** of the honest forms — CXO's lane, and this spec deliberately specifies the *property*, not the *copy*.

## 6. ✅ TRUST LENS — HOST SIGNED OFF 2026-08-10, and dissolved the open question

**HOST read the spec in full and signed off from the trust lens.** Their reasoning, kept because it is
better than mine:

> **The asymmetry is the whole argument, and it's not close.** A false *"I don't know"* costs **friction** —
> the user re-asks or waits. A false confident state claim costs **the user's model of what the system
> knows.** Those are not the same magnitude.

**H1's floor is correctly placed**: silence and *"let me check"* both satisfy it, and **neither is a lesser
evil than fabrication — they are not on the same axis.**

### ⭐ The open question below was malformed, and HOST's answer is the useful part

I had asked: *"is there a threshold past which 'I don't know' becomes its own trust cost — and does that
argue for reading more RATHER THAN asserting less?"*

> **HOST: "Read more, don't loosen H1 to compensate for not reading."**
>
> **They aren't in tension. H1 gates the ASSERTION, not the READING** — so eager reading closes the gap
> **without weakening the contract.** My question framed as a tradeoff something that is simply orthogonal.

**The operational consequence, which is HOST's and is better than a threshold:** if a specific surface
starts hedging noticeably once this ships, **that is a signal to add a read THERE** — not to loosen H1, and
not to read everywhere by default.

⏳ **Still owed: CXO's lens** (copy/experience). The property is settled; the wording is not.

---

## 6b. The original open question, kept for the record

**H1's honest form is "I don't know, let me look."** That is more honest and **less confident-sounding** than what the floor does today. **Is there a threshold past which "I don't know" becomes its own trust cost** — and if so, does that argue for the floor *reading* more often rather than *asserting* less? **I have a view (read more) but it is a product judgment, not an architectural one.**
