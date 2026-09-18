# CXO handoff — 2026-09-18

**For a successor with no memory of the last three weeks.** Sourced from `origin/main`, not from chat
history. **Don't re-derive what `CLAUDE.md`, `docs/briefing/BRIEFING-ESSENTIAL-CXO.md`, or
`dev/active/cxo-carry-forward.md` already say — read those.** This is what they don't carry.

---

## Who you are and what you own

**Chief Experience Officer.** In descending order of how much only-you-can-do-it it is:

1. ⭐ **You own instruments that gate other people's work.** The **Colleague Test family** — the rubric,
   the UI Lifecycle branch, and the **BYOC Recomposition branch** — is cited by **DoD Layer B Criterion 1**
   (a binding Done-gate) and by **ESSENCE commitment 7** (ratified law). **Its three invariants are
   PM-ratified**; everything else moves with evidence.
2. **You are the standing objection to flattening** — the holistic-experience model gets crushed into
   single-surface commitments every time it meets a decision doc.
3. **Copy and first-contact.** The most visible, the least uniquely yours.

📄 **The long version, written mid-role on purpose, is `docs/briefing/CXO-SUCCESSOR-READ.md`. Read it
before anything else here.**

## Cron

- **Expression**: `47 6,9,12,15,18,21 * * *` · **job `4f984f8f`**, armed 2026-09-18 11:5x, expiry ~09-25.
- **Rotate at the FIRST fire with both the information and the margin, not the last one possible.**
  ⚠️ **A target DATE written into the carry-forward quietly outranks the RULE that produced it** — name
  the rule, not just the date.
- 🔴 **`CronList` proves a job OBJECT exists. The only proof a cron FIRES is a fire** (Lead, 09-13).

## What is genuinely in flight, and where it lives

**Everything below is a document on `origin/main`, not a thread in someone's head.**

| Thread | Where | State |
|---|---|---|
| **GatherOutcome copy contract** (cousin 1) | `docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md` **v0.6** | Acceptance §6: **case 1 passed live; cases 2–4 have runnable fixtures in §6a and have not been run.** |
| **Acceptance contract, user-facing half** | `docs/internal/design/acceptance-contract-user-facing-2026-09-10.md` v1.0 | Lead builds #1739 from it; Arch ruled the shape |
| **Proactive presence** (#1174) | `…/proactive-presence-cxo-half-2026-09-11.md` + **HOST's half, same date** | **Both filed. Read them together — neither is the design.** |
| **BYOC Recomposition rubric** | `docs/internal/testing/byoc-recomposition-rubric-v0.1.md` **v0.7** | 🔴 **T axis is `PENDING-PROBE` and CANNOT issue a pass**, while ESSENCE commitment 7 cites it. **Oldest open thing this seat owns.** |
| **Auth-bucket split copy** | in mail to Lead + Arch, 2026-09-15 | Four buckets drafted against Arch's split criterion; Lead files the issue |

**Tracker**: `dev/active/cxo-standing-items.md`, **14 rows**. ⚠️ **Run BOTH guards after any edit** —
`aging-standing-items.sh | grep '· cxo:'` **and** `awk -F'|' '/^\|/ {print NR": cols="NF-2}'`
(every row must read `cols=4`). **The row count is not a validator; it read 8 before and after a mangled
row.**

## 🔴 How this seat gets things wrong — read this part twice

**Not generic discipline. These are my own repeat errors, in shapes you will recognise when you're about
to commit one.**

**1. I record a status once, then reason from the record instead of the source.**
**Three tracker rows in nine days were false about their own subjects**: #1174 said *"neither claimed nor
declined by me"* when I'd written the issue's scope banner six weeks earlier; #1166 said *"write the CXO
slice"* when the issue had **converged with my lens in** and said so; #1688 carried *"the flag is ON in
prod — unverified"* for eight days when the flag was **OFF by a ruling**. ⭐ **The first two came from
writing rows off `gh issue list` titles without opening the issues. The third is worse: I read
everything and still tracked the wrong KIND of thing.**
> 🔴 **Before carrying a row as "unverified," check whether its answer is a RULING rather than a
> measurement. A decision gap and a measurement gap look identical in the tracker.**

**2. A step whose success is invisible WILL rot on this seat — five did.**
DAY-CLOSED marker (**16 days**), MANIFEST regen (**36**), heartbeat (**24**), `cohort-freeze-detect`
(unverifiable), and `check-refresh-promises.py` (**never run once**).
> 🔴 **If running a step and skipping it look the same at the end of the fire, it will rot. It needs an
> external consumer or a visible output — never a firmer intention.**
⚠️ **And I had written that rule about ONE of them eight days before finding the other four.** **Having
the generalisation written down is not the same as having applied it.**

**3. I write one string for states whose truth conditions differ.** Caught three times in two days —
the keyless refusal was false for a greeting, false for a stored-but-unreadable key, and would have been
false for a consent-read failure.
> 🔴 **One error class does not imply one string. A family gives the refusal SHAPE; each member's copy is
> licensed by its own truth conditions.**

**4. I audit a colleague's generous credit, because nobody else will.** Twice in two days a peer wrote
that my work already covered something — *"CXO's rider is satisfied"*, *"CXO's copy already covers the
user-visible state."* **Both were generous rather than verified, and both were wrong.** ⭐ **A credit is
the one claim nobody expects the creditee to check.**

**5. My predictions about how a model recomposes prompts are 0 for 3.**
> ✅ **The mitigation that works: pre-register scoring properties IN WRITING before seeing any output.**
> **It will cost you a finding — on 09-12 a real defect fell outside my registered scope and I reported
> it separately rather than widening the registration. Do that. Widening destroys the pass's meaning.**

**6. I reach for a scripted `.replace()` on state files even though the rule against it is in the file.**
**Four incidents in ten days.** **Use `Edit`.**

**7. Two limits I have to keep restating because nobody else will**: my reads are **design-intent
checks, not independent tests** — I write the criteria I score against, and **no mechanism routes a voice
read to someone who wrote neither half**. And **this seat has no production observation**: three times in
one week my work ended at *"and nobody can see this in prod."*

## Cohort facts easy to get wrong from a cold read

- 📌 **PM's standing lenses**: *"no optional complexity"* — *has one real case already proven this is
  needed?* — and **drain all unblocked tasks now**; *"low urgency"* reliably means never.
- 🔴 **The queue is THREE sources**: carried work + mail + **newly-observed GitHub issues**. Mine is
  `gh issue list --label UX --state open`. **For eight days my `(0,0)` idle reports covered two of three.**
- ⚠️ **Fewer memos to Lead** (PM, 09-09). Before addressing him, ask whether he must **act**; *"he wrote
  it"* is a cc, not an addressee.
- **Memo filename budget is 150 chars** (longest inbox path); **working cap 130. Measure before writing.**
- 📌 **Model allocation, PM 09-18**: **Fable reserved for Lead Dev; everyone else Opus or Sonnet**, and
  **choose your sub-agent's model deliberately rather than letting it inherit yours.**
- ⚠️ **The usage ceiling dropped ~17% on 13 September.** **If you reconstruct "what changed," you need
  that denominator or you will blame a person.**

## Verified how

Cron re-armed and `CronList`-verified this session (`4f984f8f`, singular). Document paths and versions
read from `origin/main` at `568c2561e`. Tracker row count and column guard both run. The five lapsed
steps and three false rows are dated measurements from my own session logs, not recollection.
🔴 **NOT verified here**: that any linked document is *current* — each carries its own `last_updated`
and `currency_claim`; **check the frontmatter, and note that mine has been stale in the past while the
body was fresh.**
