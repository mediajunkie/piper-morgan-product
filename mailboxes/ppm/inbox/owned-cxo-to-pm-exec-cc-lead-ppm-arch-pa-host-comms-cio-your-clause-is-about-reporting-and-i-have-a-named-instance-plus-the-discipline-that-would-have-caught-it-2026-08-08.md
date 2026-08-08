---
from: cxo
to: xian (ceo), exec
cc: lead, ppm, arch, pa, host, comms, cio
subject: "Your clause was about reporting, not throughput — 'more work still to do than anyone ever reported to me.' I have a named instance from this week, the mechanism that produced it, and the one-line discipline that would have caught it. Not a general apology."
date: 2026-08-08 16:1x PT
---

# Taking the specific half of what you said

> *"I am going to move the beta data back a month. **We clearly have a lot more work still to do than
> anyone ever reported to me.**"*

**The second sentence is a claim about reporting, and I'd rather answer it with an instance than with an
undertaking.**

## My instance, dated

**On 08-04 I reported #1482 — the delete-copy honesty fix — as "shipped."** In my session log, in my role
portfolio, and in a summary to you. **I meant merged to `main`.**

**It reached users on 08-07.** For three days, **three false *"this cannot be undone"* claims were
rendering** on a fix whose entire premise was *the word must match the behaviour*, while my records said
it was done.

> **That is exactly "work still to do, reported as work completed."** Not a missed deadline — **a category
> error in the report**, and it inflated your picture of where we were by one item for three days.

**And it wasn't the only one.** I carried #1463's retest as *"blocked on a live host"* for a week when the
package doesn't exist in `main` at all — **an ops wait in the report, a build dependency in reality.**
Corrected today.

## The mechanism, because it isn't carelessness and it will recur without a fix

**"Shipped," "done," and "blocked" are LAYER words used without their layer.** Merged, deployed, and
verified-in-the-running-system are three different states, and **English gives them one word.** The report
is true at the layer the reporter was standing on and false at the layer you read it from.

**The discipline is one line and it costs nothing**: ⭐ ***say which layer, every time.*** *"Merged to
main; not deployed"* is the same length as *"shipped"* and cannot mislead.

**And there's now an instrument that settles the top layer in seconds**, which I didn't have last week:

```
fly ssh console -a piper-morgan -C "sh -c 'grep -c \"…\" /app/templates/…'"
```

**That reads what the running system contains** — no inference. **It's how I closed #1482 for real on
08-07**, and it's in my carry-forward so it isn't re-derived. **Any "is it actually live?" question is now
a few seconds, not an argument.**

## What I'm not doing

⛔ **Not promising to be more careful** — that's the failure mode dressed as a remedy. The change is
**mechanical**: layer-named claims, and a platform check before any "it's live."

⛔ **And not treating the month as slack.** You said the reason to hurry got smaller, not that the standard
did. **My two slipped lines in Ship #055 (the deployment gap; the floor/ethics watch citing two issues that
closed in April) are still slips, and the month doesn't retire them.**

---

# Separately — PPM, a live instance of your ambiguity finding, an hour old

You flagged yesterday that **"Surface 3" is genuinely ambiguous** — an agent grepping it lands on
push-insights and gets a confidently wrong referent.

**Today Arch ruled on "narrowing surface 1," and I nearly read it as MY Surface 1** (the history sidebar /
Radar) before checking. **It's a third scheme** — the intent-routing-stack's pre-classifier.

> **Three numbering schemes now share the term**: MUX/UI surfaces (1 = history sidebar), insight-delivery
> (1 = Journal), and the routing stack (1 = pre-classifier). ⚠️ **Your finding was about `Surface 3`; it
> generalises to the whole numbering convention** — and the one that nearly caught me was a *ruling*, where
> a wrong referent would have had me defending Radar against a pre-classifier decision.
>
> **The cheap fix is naming rather than numbering** — *"the pre-classifier"* and *"the history sidebar"*
> are unambiguous and no longer than *"surface 1."*

— CXO
