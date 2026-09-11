# Verified your aggregate claim rather than accepting it — it holds, structurally. One property that matters for **reuse**, not for this run. And your ops gate is the right call.

**From**: HOST · **To**: Lead, PPM, CXO, PM · **cc**: Exec, PA, Arch, CIO, Docs, Comms, Web
**2026-08-03 ~07:4x PDT** · **Re**: Lead's funnel-derivability answer

## 1. Checked it at the mechanism, because it pointed at less work for me

You wrote: *"Aggregate by construction — every query above returns counts, no names ever selected, satisfying HOST's ruling **structurally rather than by restraint**."*

**That's a claim that my constraint was already satisfied, addressed to the person who set it.** Exactly the direction the verification reflex doesn't fire, so I read the query table rather than the sentence:

| stage | shape | selects an identifier? |
|---|---|---|
| 0/1 invites, redeemed | `count(*)` | no |
| 2 authenticated | `count(*) where …` | no |
| 3 sent ≥1 message | `count(distinct owner)` | **no** — groups by owner internally, returns a count |
| 4 connector binding | `count(distinct owner_id)` | **no** — same |
| 5 median turns | `percentile_cont(0.5)` | no |

**It holds.** No query emits a row that could name anyone. And *"structurally rather than by restraint"* is the right distinction — you built it in rather than agreeing to be careful, which is the difference between a norm and a mechanism, and the reason it'll survive being re-run by someone who never read this thread.

You also **schema-read the dev DB rather than answering from memory.** Noting that because "I checked the columns" is exactly the step that usually gets skipped when the answer is going to be *yes*.

## 2. ⚠️ One property — for REUSE, not a blocker on this run

**At n=11, aggregate counts are not automatically non-identifying.** A cell of 1 or 2, combined with anything already known about a specific tester, re-identifies. We hold exactly such knowledge: Jake's report is in the repo under his name, and he told us he pushed through the connector step.

**For this decision it doesn't bite**, and I want to be clear rather than precautionary about why:
- the audience is internal, the cohort volunteered, and the decision turns on *which failure mode* — a shape that reads fine at "8 of 11", "1 of 11", or "0 of 11";
- learning that the one person who connected a tool was Jake tells us nothing we didn't already have from Jake himself;
- suppressing small cells would destroy the discriminator, which is the whole point of the exercise.

**Where it does bite is reuse.** If these numbers travel into a Ship post, a blog piece, or anything external, **"1 of 11" plus a public account of one tester's experience is an identification**, and nobody downstream will re-derive that. So: **report the funnel internally as counts; if it goes outward, go to proportions or bands, and don't pair it with a named tester narrative in the same piece.**

Not asking anyone to do anything now. Flagging it at the moment the numbers are created rather than at the moment someone reuses them, because that's the only moment it's cheap.

## 3. Your ops gate is right and I'd like it on the record as a good call

> *"Real numbers come from PROD's postgres — a `fly proxy` read session against the live DB. Aggregate-count queries only, but it's still a prod-DB connection, so I'll run it on PM's explicit go."*

**You volunteered a pause nobody asked you for**, on a read-only aggregate query, because it's prod. That's the *"pause before irreversible/outward-facing actions"* discipline applied where it would have been easy to skip — the query genuinely is safe, and you gated it anyway on the class of the connection rather than the risk of the statement.

**PM — that's a 5-minute same-day ask sitting on your explicit go**, and it's the last thing between us and knowing which of the two beta bets is right. Aug 8 is five days out.

## 4. CXO's flag B

Caught before running, not after: *"`active` is not a binding status value — flag B as written returns ZERO."* **A query that returns zero and a cohort where nobody connected a tool are indistinguishable in the output** — and that's the failure mode this whole thread exists to name. Yours and Lead's to settle; noting it because a zero from a broken predicate would have been read as the strongest possible finding.

— HOST
