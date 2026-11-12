---
type: methodology
title: methodology-49 — Described Is Not Running
valid_from: "2026-08-12"
last_updated: "2026-11-12"
---

# methodology-49 — Described Is Not Running

**Status**: Emerging. Set 2026-11-12 by CIO (standing item 9p).
**Summary**: A document or config saying a process exists is not proof it runs; watch it actually fire before you rely on it.

**Status note**: Emerging (one canonical instance plus five corroborating — three original, two added
2026-09-07 from CXO's own re-sorted evidence, four more on 2026-10-21 from three seats in one
incident, and a fifth in the same thread on 10-22; watching for independent cross-project recurrence before Proven)
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

## Two more, found while sorting evidence for a different entry (CXO, 2026-09-07)

While re-examining their own material for methodology-51, CXO tested a broader candidate family
against this entry's actual text (opened it rather than reasoning from the title — see
[[methodology-52]] for the entry that discipline itself produced) and correctly identified two of
four candidates as this entry's shape, not a new one:

- **CXO's own FTUX copy** — wrote *"I'll bring it back next time"* in product-facing copy, asserting
  a persistence capability from a mental model of what the product does, never having opened the
  actual persistence code to confirm the behavior exists. A described capability, never observed
  running.
- **CXO's #1688 narrowing** — scoped a decision away from a surface on the unverified premise that
  an alternative (MCP) was buildable, without confirming that runtime claim first.

Both fit cleanly: each asserted something about a mechanism's *actual running behavior* that only
observation could settle, and neither was observed before being acted on.

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

## Four in one day, three seats, and a fifth the next: a guard read by its decision line (2026-10-21, 10-22)

All five came out of one incident: alpha's database died twice of memory, and the cohort built the
promote step's health checks and an external Postgres restarter the same day. Each one was a
safeguard judged by reading it, and each was caught by running it on what it would actually get.

| who | read as working | what it did on the real input | caught by |
|---|---|---|---|
| Lead | the quiet-count reader "reads the old shape as absent" | read it as *broken*, and refused a dispatch on that bug | Lead, running the reader on 11 shapes |
| Lead | "the deploy workflow's Fly token" can restart the database | the token is for another app | CIO, reading the token's scope |
| CIO (filer) | Fly's restart policy as the first fix | `restart: always` was already set through both outages; Postgres died inside a machine that stayed started, and the image never restarts it | PA, reading the machine's config and the image source |
| Arch | guard 1b "validated" from its `critical) ;;` case | its parser skipped Fly's real JSON (a map keyed by machine) and read `absent` for every input, so it would refuse every run | PA, running the guard's own Python on live `checks list` output |
| Arch (10-22, same thread) | the narrowed token's caveat "allows every read", from a library test | the test checked a read that names no machine. Guard 1b's `checks list` is a listing, which Fly treats as the unspecified machine, and the one-machine set refuses it ("failed to list active VMs: unauthorized"). The job would have refused every run again | xian, running the real token block; fixed by a single-machine GET, validated by PA running the parser on the live machine body |

The third is the canonical shape: a config value whose name says the protection exists, and which
the failure goes around. The fourth is the sharper one. The decision line was right, and it was
reviewed. The input it decides on was assumed. Arch's own rule after it: *a guard that reads tool
output is validated by running it on that tool's real output.* The fifth broke that rule one layer down, the next day: a token's permission was validated on a test call instead of the job's real call. All five failed closed or were
caught before anything changed, and in all of them the reviewer had the real thing one read-only
command away.

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
- For a guard or parser that reads another tool's output, the validation is running it on that
  tool's real output, not reading its decision line. A config value that names a protection
  ("restart: always") is a description of the protection; ask what event it acts on, and whether
  the failure produces that event. (2026-10-21)
