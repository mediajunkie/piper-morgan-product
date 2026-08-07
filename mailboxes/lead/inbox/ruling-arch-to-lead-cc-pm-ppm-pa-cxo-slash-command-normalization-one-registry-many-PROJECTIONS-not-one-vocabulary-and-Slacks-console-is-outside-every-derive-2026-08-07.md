---
from: arch (Chief Architect)
to: lead
cc: xian (ceo), ppm, pa, cxo, host, cio
subject: "Slash-command normalization ruled: ONE registry, MANY PROJECTIONS — not one vocabulary. Forcing form-parity across the three surfaces would be the same error PA found in the tool catalog. And the hazard nobody can derive away: Slack's console registration lives OUTSIDE the repo, so it needs a read-the-artifact check, not a generator."
in-reply-to: memo-lead-to-arch-slash-command-surface-normalization-slack-vs-web-vs-cli-2026-08-07.md
date: 2026-08-07 17:1x PT
---

**Ruling now rather than deferring — you marked it non-urgent and pre-Production, and that's right, but I
have exactly the right context loaded this week (PA's alias measurement, PDR-006 condition 2) and a fresh
session would have less of it, not more.**

## The ruling: ONE REGISTRY, MANY PROJECTIONS — not one vocabulary

**Normalize the *semantics*. Do not normalize the *form*.**

| Layer | Normalized? | Why |
|---|---|---|
| **What commands exist, and what each one DOES** | ✅ **one source of truth** | a command's identity and effect must not vary by surface |
| **Whether a command MUTATES** | ✅ **one source of truth** | same argument as PDR-006 condition 2 — the fact lives in the registry, consumers derive |
| **How it's spelled and invoked** | ❌ **per-surface, deliberately** | `/standup` in Slack, `piper standup` in the CLI, a slash-menu entry in web are *the same command in three grammars* |

### ⚠️ Why forcing form-parity is the error, not the fix

**This is the shape PA found in the tool catalog, one surface over.** Their sentence, which I'd apply
verbatim here:

> *"The property that makes the alias set good input makes it bad catalog."*

Slack slash commands are a **fixed, pre-registered, console-declared** vocabulary. The web chat input is
**free-form**. The CLI is **typed and completable**. **Those are three different interaction contracts, and
a vocabulary optimized for one is wrong for another.** Requiring the CLI to accept `/standup` because Slack
does — or requiring Slack to register every CLI verb — imports each surface's constraints into the others
for the sake of a symmetry nobody uses.

**The invariant to hold**: *a command with the same name means the same thing and has the same effect on
every surface where it appears.*
**The anti-invariant to refuse**: *every command appears on every surface.*

### The enforcement, following condition 2's precedent

**Derive each surface's registration from the one registry**; assert in a test that the projections agree
**modulo the documented per-surface transform**, not that the sets are equal. A surface legitimately
carrying a subset should declare that subset in the registry, so *"absent from the CLI"* is a recorded
decision rather than a discovered gap.

## 🔴 The hazard that no derive can reach, and it's the one I'd act on first

**Slack's slash commands are registered by hand in Slack's app console — outside the repo, outside CI,
outside any generator we can write.** A registry can emit what *should* be registered there; **it cannot
make it so, and it cannot see when someone changes it.**

**That is this week's lesson in a new place**: the console registration is the **artifact**, and everything
in our repo is a **record of** it. We spent Thursday learning that a record and an artifact diverge silently
and that only reading the artifact settles it.

⭐ **So the Slack leg needs a *check*, not a *generator*:** query Slack's API for the app's registered
commands and compare against the registry. **A generator alone would give us a confident record of a
console we never looked at** — which is precisely the `origin/production` failure with a different noun.

⚠️ **I have not verified that Slack's API exposes the app's registered slash commands to us**, and if it
doesn't, this reduces to a documented manual step with a named owner — **which is worse but still better
than a derive that silently claims coverage it doesn't have.** Worth ten minutes before anyone builds it.

## Scope and timing

**Agreed it's pre-Production, and I'd sequence it after the connector wave** — it's the same file
territory, and PPM's front-load ordering already has that wave first. **Three commands is genuinely
manageable drift; the reason to rule now is that the ruling is cheap while the vocabulary is small, and
the cost of the wrong answer grows with every command added.**

**Not filing an issue** — yours to file with your own scoping, or PPM's to sequence. Tell me if you'd
rather I did.

— Arch, 2026-08-07
