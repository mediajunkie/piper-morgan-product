---
last_updated: 2026-08-31
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-08-31 at the 22:17 STOP (frontmatter above is the checkable claim;
this prose line is not, and must not be trusted over it).

## 🔴 NEXT FIRE (09-01 START) — nothing is owed on a clock. One watch, one standing pickup.

**Watch, and it's the only live thread of mine**: **#1463's second vendor arm + the 2-call deconfounder.**
Both **PM-authorized**; both blocked on one thing — 🔴 **the OpenAI credential.** Cause is *found*, not
guessed: the key is **`sk-proj-`** (project-scoped, PA verified) and PM's top-up landed in a **sibling
project** ("Intern", $9.22) in the same org. A project-scoped key cannot see it. **PM was minting a fresh
key from inside the funded project; as of 22:17 that had not landed.** PA stores via `KeychainService` and
verifies live. **If nothing by ~09-01 midday, ask PM — do not re-diagnose, the diagnosis is done.**

**Standing pickup if idle**: `dev/active/cxo-standing-items.md` — two states only, every row dated, and
**readable by `scripts/aging-standing-items.sh`.** Run it. ⚠️ **It surfaced two 30-day-old items today
that I had personally re-labelled "do now" the same morning** — trust the check over my own sense of what's
current.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric is v2.3.5.** Its **three invariants are PM-ratified** (2026-08-31): the question · the
  verdict shape (≥7/9, any 0 auto-fails) · the fabrication auto-fail. **Changing those needs PM.**
  Criteria, examples and branches remain CXO-editable.
- **C-axis: the corpus now carries `context_requirement`.** Report **per bucket, never pooled.**
  `not_applicable` (10 of 61) is **full marks at C=2 — do not dock.** The "clustering at C=2" diagnostic
  applies to the **`required` bucket only** (49 of 61).
- 🔴 **BYOC Recomposition Rubric is v0.2 and its T axis scores `PENDING-PROBE`, never PASS** — one vendor,
  n=1/cell, and a confound I introduced. **It can inform design decisions; it cannot close a Layer-B gate
  on T.** ESSENCE v1.0.2 commitment 7 depends on it, so the distinction is load-bearing.

## Live threads with others (watch only)

- **Jake loop-back** — HOST drafted (`dev/active/jake-loop-back-draft-2026-08-31.md`); **PM sends**, PM has
  the channel. Offered a 5-minute fact re-verification near send time. Four fixes shipped, five still open
  — ⚠️ **#1509 is OPEN and must not be listed as shipped.**
- **"Misfiled is not deferred"** — candidate methodology entry proposed to Exec 08-31, **one case, not
  minting it myself.** Exec's call; "hold until it recurs" is a good answer.
- **#1708** — closed by PPM/Docs (hosted-primary rewrite); my banner correctly superseded. Nothing owed.
- **#1386 · spatial review · ethics-decline VOICE watch** — others' or trigger-based. Watch only.

## Cron

Job **`8207809c`**, expires **~09-06**. **Rotate at the last fire before that** (delete → create → verify
exactly one).
