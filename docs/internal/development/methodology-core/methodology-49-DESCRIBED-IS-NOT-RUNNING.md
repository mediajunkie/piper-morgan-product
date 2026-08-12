# methodology-49 — Described Is Not Running

**Status**: Emerging (one canonical instance plus three corroborating; watching for independent
cross-project recurrence before Proven)
**Filed**: 2026-08-12 (CIO) · **Found by**: Janus (canonical instance) · **Routed by**: Docs
(candidate correctly left to CIO to govern rather than self-filed — per methodology-28's own
slot-availability discipline, which this file's neighbors, methodology-19/37, just paid the cost
of skipping the same day)
**Companions**: [[methodology-44]] (instrument-side twin — see Boundary below) ·
[[methodology-36]] (mechanisms over vigilance) · [[methodology-30]] (consumer-trace verification)

---

## The rule

**"The fix is described" and "the fix is running" are different claims, and only a behavioral
observation distinguishes them.** A mechanism's documentation, its config, its comment, even its
own passing description in a status doc — none of these are the mechanism. Only watching it fire
is.

**Corollary, and the sharper half**: an artifact that describes a bug faithfully enough can become
the bug's next instance, one level up. Description isn't a neutral, inert copy of its referent —
it's itself an artifact, subject to the same class of defect it's describing.

## The canonical instance (Janus, 2026-08-12)

`BRIEFING-CURRENT-STATE.md` documented an old Jekyll/Liquid template-parsing bug — and quoted the
literal `{%...%}` tag while doing it. Jekyll's Liquid parser parses `{%...%}` **inside markdown
code spans**, so the documentation of the template-parsing bug reproduced the same bug one level
up, silently killing the docs Pages build for **2.5 months**. Nobody was wrong about the bug —
the record of the fix was itself the new instance.

This is the sharpest instance on record because there is no gap between the failure and its own
description: the artifact whose *job* was to name the defect *was* the defect, in the same
breath.

## Three corroborating instances, same week

- **The PreCompact sign-off hook** — registered to an empty array for ten weeks while CLAUDE.md
  described it as live (already documented at CLAUDE.md's Sign-Off Discipline section; the
  unblocking fix landed the next day, but the *restore* — verifying it fires — was never anyone's
  job until it was).
- **#1593's link-checker** — detection described and even running, but its output wired to
  nothing. Detection existing is not detection *reaching* anyone.
- **The Amber project-hooks investigation** (CLAUDE.md, "the pre-commit hooks were dead
  everywhere") — config presence, correct registration, and the script running fine by hand all
  proved nothing; the hook still didn't fire in the actual gated path. **"Hooks are ADVISORY, not
  a control... an absent hook and a silent hook look identical"** is this exact rule, already
  operative in this repo's prose, pre-dating this filing.

## Boundary — this is not methodology-44 restated

m-44's claim is about an **instrument's output**: a check emits "clear" identically whether it
measured correctly, measured the wrong thing, measured partially, or never ran — the failure lives
in what a *measurement* asserts. This entry's claim is about a **description's referent**: a doc,
config, or comment asserting a mechanism exists or works, when existence-of-the-assertion and
existence-of-the-mechanism are not the same fact. The PreCompact hook instance sits on the seam
(a *documentation* claim that also functioned as an unaudited all-clear) — genuinely both — but the
canonical instance (Janus's Jekyll case) is pure m-49: there was no check, no exit code, no
"clear" anywhere in the failure. There was only a sentence that was true about what it described
and false about what it was.

**Practical distinction**: if the artifact in question is a check/gate/instrument that produces a
verdict, start with m-44. If it's prose, config, or a comment asserting a mechanism's *state*
(live, fixed, wired, armed), this is m-49.

## The rule, operationally

- **Verify behaviorally, never by presence.** A hook's config, a doc's claim, a comment's
  assertion — none substitute for watching the thing fire. (Already CLAUDE.md prose; this entry is
  where that prose's origin instances live, cited rather than re-derived.)
- **When you write documentation ABOUT a defect, treat the documentation itself as a candidate
  instance of the same defect class** — especially when the defect is about parsing, escaping, or
  literal reproduction of the very syntax you're describing. Quoting the bug is not automatically
  safe.
- **"Built" and "wired" are different claims from "reaching someone."** #1593's link-checker
  needed all three named separately, not collapsed into one "shipped" status.

## How to apply

- Before writing "X is live / fixed / running" in any durable doc, ask: have I watched X do the
  thing, or am I inferring it from X's own description of itself?
- When documenting a parsing/escaping bug, check whether your own documentation reproduces the
  literal syntax that triggers it — in the same rendering pipeline the bug lives in, not just in
  your source markdown.
- A detector's existence is not its reach. Ask what consumes its output before calling it done.
