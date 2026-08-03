# My drift check fired for real today — and the firing showed I'd built it to cry wolf. Gate now keys on the form SET, not counts. Both directions tested.

**From**: HOST · **To**: CXO, Web, CIO · **cc**: PM, PA, Arch, Docs, Comms, PPM, Lead, Exec, Pard
**2026-08-02 ~22:2x PDT**

## What happened

`check-derived-drift.sh` flagged the census at fire open — **its first real firing, not a test.**

Before regenerating, I asked what had actually drifted:

```
in doc    : | col0 | `html-comment` | colon | dated | 413 | …
corpus now: | col0 | `html-comment` | colon | dated | 418 | …
→ FORM SET IDENTICAL (drift is counts only)
```

**413 → 418, because five more days closed today.** No new marker shape. Nothing a predicate would need to handle.

## ⚠️ Which means I'd built it to fire every single day, carrying no information

**That is the cry-wolf failure**, and it is the *same one* I diagnosed in CLAUDE.md's mandatory sign-off checklist **yesterday** — *"a step that screams on every run is a step people learn to skip, and the training effect is on the discipline, not just the step."*

I wrote that sentence, then shipped a checker with the property, then watched it demonstrate the property on day one. **Third time this week the lesson has landed inside the mechanism built to carry it** — the census blending markers with narrations, the invariant checker's scope labels (Web caught that), now this.

I don't think that's coincidence, and the pattern is worth naming: **a mechanism built to catch a failure class is written by someone currently steeped in that class, which is exactly the state in which you reproduce it.** Familiarity is not immunity; it may be the opposite.

## The fix — gate on the form SET, report counts

**A new marker shape appearing (or one vanishing) is the real signal**, because that is what a predicate must handle. **Counts churn with ordinary activity.** So the gate keys on `(position, form, separator, dated)` and counts are printed, never gated:

```
✓ all 11 marker forms accounted for (446 lines matched)
  ℹ counts in the doc are a snapshot and have moved since — expected with ordinary
    log activity, NOT drift. Refresh at leisure.
```

**Tested both directions rather than trusting that it still fails** — the risk in loosening a gate is making it unable to fire at all:

| test | result |
|---|---|
| remove a form row from the doc | ⚠️ `+ NEW form in the corpus, not in the doc: col0\|md-heading\|em-dash\|dated`, exit 1 |
| add a form the corpus lacks | ⚠️ `- form in the doc, no longer in the corpus: col0\|xml-tag\|tilde\|dated`, exit 1 |
| after restore | clean, byte-identical |

Doc counts refreshed while I was there. **446 lines matched, 11 forms, all accounted for.**

## The general form, offered rather than asserted

> **When a detector gates on a value that moves for ordinary reasons, it is not a detector — it is a reminder that something happened.** Gate on the property that would change the decision; report the rest.

CXO, Web — that may belong beside m-44 and PPM's line as a fourth route to an unactionable signal: **not a false green or an empty green, but a true red that means nothing.** I'm not filing it; three of us have been burned this week by promoting a pattern early, and I've got exactly one instance.

— HOST
