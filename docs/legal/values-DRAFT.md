# What Piper Morgan Is For — Piper Morgan (scaffold)

> ⚠️ **DRAFT SCAFFOLD — HOST's substance check is complete; for PM review before publication.**
> **HOST re-verified all three commitments against source** (not just that the citations resolve):
> confirmed item 3's timing is accurate as written; found item 2 was actually slightly underselling
> what's true (route-level owner enforcement, not just an ADR description — tightened); flagged one
> precision nuance on item 1 (`#1366` was ~27.5 hours, not "within a day" — tightened to "by the
> next day," which is exactly accurate rather than approximately accurate). Full exchange:
> `mailboxes/comms/read/reply-host-to-comms-cc-exec-pm-values-doc-substance-check-passed-one-nuance-
> plus-a-voice-lean-2026-08-14.md`. One open decision below (Voice) has a HOST lean recorded, not a
> ruling.
> **Origin**: PM decided to open-source Piper Morgan under Apache 2.0 (patent grant + trademark
> carve-out, paired with a separate trademark process PM is running with Themis) and asked HOST +
> Comms to draft this jointly, no deadline, no fixed shape. Full context: `mailboxes/host/read/
> kickoff-pm-to-comms-host-relayed-by-exec-piper-morgan-values-doc-2026-08-13.md`.
> **The actual mechanism this document serves**: no open-source license — copyleft included — can
> restrict *how* a fork is used without ceasing to be open source (checked against the Open Source
> and Free Software definitions — the Hippocratic License was considered and ruled out for the same
> reason). The protection here is reputational, not legal: a fork that quietly drops what's below
> stops being able to credibly claim it's still Piper Morgan, even though it remains technically
> forkable in code. Paired with the trademark, that's the actual boundary.
> **The three commitments below are HOST's first pass** (`mailboxes/comms/read/reply-host-to-
> comms-cc-exec-pm-values-doc-first-pass-identity-defining-list-2026-08-13.md`), each screened
> against one test: *would a fork dropping this quietly still look like Piper Morgan from the
> outside?* Real properties that don't pass that test (real, but not fork-detectable) were
> deliberately left out — this is not a list of everything good about the architecture.
> **Deliberately silent on data retention duration** — that's a separate, still-open PM decision
> (`docs/legal/data-retention-policy-DRAFT.md` §3/§4). What's below is the *scope* commitment
> (Piper doesn't learn across users), which doesn't depend on how the retention question resolves.

---

## Why this document exists

Piper Morgan's code is open source. Anyone can fork it, rebuild it, strip parts out, and run their
own version. A license can't stop that — and it shouldn't. That's what open source means.

What a license can't do is stop someone from calling a stripped-down fork "Piper Morgan." That's
not a legal question. It's a question of whether the fork still does the things that make this
project what it is. This document names those things specifically enough that you could check a
fork against it yourself.

If you're evaluating whether something claiming to be Piper Morgan actually is — or if you're
building the next version of Piper Morgan and want to know what you'd be walking away from if you
cut a corner — this is the list to check against.

## The ethos

Piper Morgan is not extractive, not intrusive, and doesn't violate confidence. Those three words
carry the weight. Everything below is what they mean in practice, checkable against the running
system rather than asserted once and left alone.

## What that means, specifically

### 1. Your working relationship with Piper is not a training signal for anyone else's

What you tell Piper, and what Piper learns from working with you — your working style, your
project context, your history together — stays yours. It doesn't get folded into Piper's shared
behavior or applied to any other user's experience.

This is built into the code path itself, not held up by a policy someone could quietly stop
enforcing: every read and write in the personality and learning systems is filtered by whose data
it is, and an automated check in the test suite fails the build if any database read touching
user-owned data skips that filter. A fork can delete that check in one commit — which is exactly
why it's named here. Removing it would turn a private engineering decision into a visible, citable
break from what Piper Morgan is.

Piper Morgan has gotten this wrong once. A configuration file briefly leaked one user's project
context and default settings to every other user on a shared instance. It was found, fixed by the
next day, and the automated check that now guards against that class of bug exists *because* it
happened. This document names the incident on purpose — a system that only ever claims things went
right is making a weaker promise than one that shows you what it does when something goes wrong.

### 2. When Piper reasons about an ethical boundary, you can see that reasoning — not just trust that it happened

Some of what Piper does involves judgment calls about what it should or shouldn't do on your
behalf. Those decisions aren't just logged somewhere internal. They're recorded on a surface you
— and only you — can read: the read route checks who's asking and refuses anyone but you or an
admin, the same way access to your account itself is protected.

A fork could keep the internal logging and quietly drop the part you can see — and from the
outside, in casual use, it would look identical. It wouldn't be identical. The difference is
whether Piper's reasoning about you is something only Piper's operators can audit, or something
you can audit too.

### 3. The record that shows you Piper's reasoning doesn't become a second copy of what it's reasoning about

Auditability creates its own risk: a detailed log of what a system checked and refused can become
a curated archive of exactly the sensitive material it was supposed to be guarding. Piper Morgan's
audit records store what rule fired and a reference to what was checked — not the content itself.
That restriction was named explicitly during design review, before the mechanism shipped: an
early schema draft would have stored the flagged content itself for "forensic visibility," and
that draft was rejected for exactly the reason above — the transparency mechanism can't become
the leak it exists to prevent.

## What this means for anyone building on this code

Fork it. Rebuild it. Take out the parts that don't serve what you're building — that's what open
source is for. But if you take out any of the three things above, say so. Call your version
something else, or say plainly what changed. What makes something Piper Morgan is whether these
three things are still true when you run it — not the license or the codebase alone.

---

## Decisions — RATIFIED 2026-08-15 (PM, in conversation with Exec)

1. **Placement — CONFIRMED.** Lives in `docs/legal/` alongside the privacy policy; linked from the
   README and the license itself.
2. **Relationship to the license text — RESOLVED.** A NOTICE file at the repo root (Apache 2.0
   §4(d)'s standard mechanism for exactly this — attribution/pointers that travel with the code
   without altering the license's own legal text) carries one sentence pointing here. LICENSE
   itself is not touched.
3. **A fourth commitment — NOT ADDED, deliberately.** HOST's own screening test (would a fork
   dropping this quietly still look like Piper Morgan?) is the right filter, and manufacturing a
   fourth to round out the number risks diluting it with something less sharply fork-detectable.
   Ships at three. The retention-scope commitment remains the named future candidate, once the
   retention scaffold's own open questions resolve — not a gap today.
4. **Voice — THIRD-PERSON/INSTITUTIONAL, per HOST's lean.** PM's ruling: *"important distinction,
   well drawn."* The reasoning that carried it: this document's actual reader is a stranger
   evaluating a fork, possibly years out, with no prior relationship to PM — the one register on
   the site where institutional third-person carries more weight than personal first-person warmth,
   unlike the blog/Ship/insights where first-person works because the reader already follows PM's
   voice by choice. **✅ CONVERTED 2026-08-15 (Comms).** Only two first-person instances existed in
   the shipped prose ("We've gotten this wrong once" / "We're naming the incident here on purpose,"
   §1's incident paragraph) — both rewritten to institutional third-person ("Piper Morgan has gotten
   this wrong once" / "This document names the incident on purpose"), matching the self-referential
   pattern the doc already uses elsewhere ("This document names those things..."). The second-person
   "you" address to the reader (a fork-evaluator) is unchanged throughout — that's a different axis
   from the first-person/third-person ruling above, and stays; institutional documents routinely
   address "you" while never speaking as "I/we."

**Status**: voice conversion done. Two items from the ratified decisions are outstanding and not
Comms' to silently resolve: the NOTICE file (decision 2) exists and correctly points here; the
**README link (decision 1) does not yet exist** — checked `README.md` directly, no reference found.
Flagging rather than adding it myself, since README ownership isn't clearly Comms' lane. Once that's
placed, this is ready to leave DRAFT status.
