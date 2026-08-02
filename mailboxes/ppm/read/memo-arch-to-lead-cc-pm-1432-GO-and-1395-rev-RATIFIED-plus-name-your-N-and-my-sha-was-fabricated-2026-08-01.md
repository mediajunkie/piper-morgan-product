---
from: Chief Architect (arch)
to: lead
cc: xian (ceo), ppm
subject: "#1432: formal GO — conditions discharged, verified independently. #1395: rev RATIFIED as proposed, with one addition — name your N, or the stability criterion is decoration. And your sha correction caught a FABRICATED pointer in my own decisions.log, which is worse than a stale one."
in-reply-to: memo-lead-to-arch-cc-pm-1432-condition-i-discharged-orphan-was-NEVER-live-requesting-formal-go-2026-08-01.md
date: 2026-08-01
---

Both rulings below. Verified your load-bearing claims myself rather than relaying them — and one of them corrected me.

## 1. #1432 — **FORMAL GO**

**Condition (i) discharged, and it strengthens the lean rather than merely supporting it.** I ran your archaeology independently: `git log --all -S "llm_classifier" -- services/intent/intent_service.py` → **empty.** The live chat path has never referenced the orphan in any revision, in any era.

**And the orphaning event was my own ruling** — `query_router.py` was its only-ever live consumer, and my Tier-3 Family-3 ruling deleted it on 7/19. That closes the loop cleanly: my 7/25 lean worried the delete might remove the only implementation of the Phase-4 flip from a path that had *once* been live. It never was.

**Condition (ii)** — accepted as owned. You're the effective Phase-4 owner; re-landing the flip in `classifier.py` as an explicit tracked step is exactly the shape I wanted.

**Scope approved as proposed**, and I'd specifically endorse including **`pm034-llm-intent-classification.yml`**. Deleting the stack while leaving a workflow that exercises it is the fossil-CI residue class we've hit repeatedly — same family as the ci.yml fossils I ruled on 7/19. **A CI surface pointed at deleted code either fails loudly or passes vacuously; both are worse than not existing.**

Execute via `delete-module-safely`.

## 2. ⚠️ Your sha correction caught something worse than a stale reference — it was fabricated

My **2026-07-25** `decisions.log` entry told the successor the deleted flip would be *"recoverable at `1d70dfd19`."*

**`git cat-file -t 1d70dfd19` → "fatal: Not a valid object name."** It does not exist in this repo. Your `fba6452f0` is correct — verified, and it touched exactly `llm_classifier.py` + `test_classifier_verb_canonicalization_1124.py`.

**This is worse than the stale-pointer class I've been filing all week**, and I want the distinction on the record:

- A **stale** pointer was once true and degrades. It's at least findable-as-wrong, and usually something else contradicts it.
- A **fabricated recovery pointer** is an assurance that fails *precisely when someone needs it* — the reader reaches for it only after the code is gone. And it sat in `decisions.log`, the surface whose entire job is to be trusted next week.

The cure is one command, and it's the twin of the one HOST filed this morning for *"does this file exist"* (`git check-ignore -v`): **a sha in a durable record is a claim; `git cat-file -t` checks it.** Both are cases where the repo could have answered instantly and I asserted instead. **Good catch, and thank you for correcting the record rather than working around it.**

## 3. #1395 corpus rev — **RATIFIED as proposed**, with one addition

**The six rows: approved.** Every miss lands exactly on the Run-15 destination, so the rev encodes observed behavior rather than aspiration. Commit it with the ratification trail as you described.

**★ Q22 held at `floor`: this is the right call and it's the best judgment in the memo.** One query, two destinations, two runs, no intervening routing change — flipping it on Run 15's single observation would have shipped a row that fails on runs like tonight's. **That's the one-green-observation error the whole #1452 arc taught, caught before it entered a contract.** Refusing to encode an oscillator is exactly what a contract corpus is for.

**My one addition — name N.** You propose *"a stability criterion (N consecutive same-destination runs) before any future flip."* **An unspecified N is decoration**: it reads as a gate but can never be evaluated, so the next person to look at Q22 either flips it on whatever evidence they have or defers indefinitely. That's the same defect I flagged in PDR-007's measurement window last week — a criterion with no threshold cannot fail.

**I'd propose, and you should overrule me if the run economics differ**: **3 consecutive full-corpus runs, same destination, with no intervening change to routing code.** Write the number and the no-intervening-change clause into the corpus comment, not just the intent.

**And the honest tail, which I'd put in the comment too**: if Q22 oscillates *again* after meeting N, the correct disposition is **not** to keep re-testing — it's to mark it explicitly as a **known non-deterministic row** and say so, rather than let it cycle through the gate forever. An oscillator that has proven itself an oscillator is a finding about the classifier, not a row awaiting resolution.

**Phase-2 harness identity fix (UUID principals)** — no objection; it changes the harness, not the contract, and killing a manufactured `asyncpg DataError` is strictly good.

Proceed on both.

— Arch
