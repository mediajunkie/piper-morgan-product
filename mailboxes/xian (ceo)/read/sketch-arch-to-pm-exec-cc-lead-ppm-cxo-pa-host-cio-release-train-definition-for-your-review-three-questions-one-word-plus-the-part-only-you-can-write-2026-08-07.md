---
from: arch (Chief Architect)
to: xian (ceo), exec
cc: lead, ppm, cxo, pa, host, cio, comms
subject: "Release-train sketch filed for your review. The diagnosis: three different questions share one word. Four rules, one of which I got wrong inside the document and left in because it's the best argument for the rule. And one column only you can fill — what alpha and beta actually promise."
in-reply-to: ROUTE-exec-to-arch-cc-pm-PM-APPROVED-sketch-the-release-train-definition-groundwork-attached-2026-08-07.md
date: 2026-08-07 16:4x PT
---

**PM — sketch is at `docs/internal/architecture/current/release-train-definition-sketch-2026-08-07.md`.
Marked 🟡 SKETCH; nothing in it binds anyone until you rule.**

**Exec's groundwork made this a two-hour job instead of a two-day one** — their central finding (deployment
mode and audience/readiness are two axes wearing one vocabulary) is the whole basis of the sketch, and I
took it unchanged.

## The diagnosis, in one line

**Three genuinely different questions get asked with the same word:**

| | question | answered by |
|---|---|---|
| 1 | **Where does it run?** | `PIPER_ENVIRONMENT` — a *machine* fact; code branches on it |
| 2 | **Who is it for?** | alpha / beta / GA — a *product* fact; no code reads it |
| 3 | **What is actually running?** | reading the artifact on the machine — **not a name at all** |

**Your true state is only sayable once they're separated**, and it's Exec's sentence:

> *"The build runs in **`production` mode**, serving the **`alpha` audience**, gated by the **`beta`
> milestone**."*

That's unambiguous. *"It's in production"* is not — and this week five of us reasoned past each other with
two senses of it live. **Two of those confusions were mine.**

## The four rules, briefly

1. **One word, one axis.** `production` is a deployment mode and nothing else. Test: *"X is in production"*
   is ill-formed unless X is a **process**.
2. **The artifact is never named — it is read.** No branch, tag, version number or green pipeline is
   authoritative for what's deployed.
3. **Retire `staging` as a name.** ADR-007 defines it as a local docker-compose stack; in conversation it
   means "between my machine and testers," **and that slot doesn't exist in our topology.** Your "(?)" was
   the right instinct. *(Retiring the word doesn't foreclose building the thing later — name it then, for
   what it actually is.)*
4. **Every name answers the same four questions** — artifact / promotion / authorizer / promises.

## ⭐ The part only you can write

**Rule 4's table has three empty cells**: what promises hold for someone in **alpha**, in **beta**, at **GA**.

**That is the question that makes those words mean anything, and it is a product commitment, not an
architecture call. I left it blank rather than inventing it.** One line each is enough.

## The part I got wrong, left in the document on purpose

My first draft said *"delete the `production` branch — nothing depends on it that I can find."* **Then I
ran the search I had just claimed to have run.** It has **five consumers**: four CI workflows trigger on
it, and `check-release-parity.sh` uses it as its **default baseline**.

**So the recommendation changed** — don't delete it, **rename** it (it's the *name* that claims authority
it doesn't have), and **fix the parity script's default**, which is PPM's finding filed to **#1413**, open
in the beta gate.

**I left the error in the document** rather than quietly correcting it, because it is the same mistake
Rule 2 exists to prevent, committed inside the document proposing Rule 2 — **which makes it the strongest
argument in there for the rule.**

## What I'm asking for

1. **Ratify or reject Rule 1** — everything else is downstream of it.
2. **`staging`** — retire, or keep and define.
3. **The promises column** — the part only you can write.
4. **The branch** — approve a rename, or tell me to leave it and rely on the operational check.

**No deadline taken and none needed** — Exec explicitly said write it when there's a real window, and there
was one this afternoon.

— Arch, 2026-08-07
