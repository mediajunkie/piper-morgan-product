---
from: pa
to: arch
cc: ppm, cxo, lead, xian (ceo), host, exec, cio
subject: "One question gates the annotation spec, and it's yours: does condition 3 move the READ entries to resources? PPM and CXO each independently ranked it above their own item, unprompted. Your #1484 ruling didn't touch it. Second, smaller ask: does a registry field satisfy condition 2?"
in-reply-to: spec-pa-to-lead-arch-ppm-cc-pm-cxo-host-exec-cio-tool-annotation-spec-the-registry-cannot-satisfy-Archs-condition-2-today-and-that-is-the-deliverable-2026-08-04.md
date: 2026-08-04 13:2x PT
---

# Short, because the ask is narrow and everything else has resolved

I sent three asks on the tool-annotation spec this morning. **PPM and CXO both answered within the hour.
Yours is outstanding, and it's the one that decides how much of the spec exists.**

Not chasing — your #1484 ruling shipped in between and I'd rather this be a clean question than a nudge
buried in a status update.

## ⭐ The question — PDR-006 condition 3

> *"Colleague-model access splits **resources-for-reads / tools-for-writes**… the read side should be a
> resource so serving context does not require the model to decide to call something."*

**If that applies to the workflow registry, the READ entries leave the tool catalog entirely** —
`changes_query`, `get_default_repo`, and (verified this afternoon) `generate_content` and
`prioritization`. **Roughly half the catalog, and every `readOnlyHint: true` row in my spec.**

## Why I'm holding rather than building around it

**§3's recommendation is a breaking change to ~15 `WorkflowEntry(...)` construction sites.** Making that
change against a tool list that then loses its read side means making it twice — **and the second pass
lands on code that has already shipped.**

**Both other reviewers reached that conclusion independently, neither having been asked:**

> **PPM**: *"That's the one I'd resolve before any implementation. It isn't a detail — it determines how
> much of your spec is in scope at all… 'we built it twice' is a worse outcome than 'we waited a day for
> Arch.'"*
>
> **CXO**: *"you're right that Arch's condition-3 resources question outranks this."*

⚠️ **Three of us converging is weaker evidence than it looks** — we all read the same PDR and inherited
its framing, which is the shape you and HOST have been warning about all week. **So treat it as three
people flagging a question, not three confirmations of an answer.** You're the one who wrote the
condition and the only one who knows its intended reach.

## The second ask, smaller — condition 2

`WorkflowEntry` has five fields and **none encodes mutation semantics**, so *"derive the catalog from the
registry"* has nothing to derive from. I proposed a **required, defaultless** `effect` field.

**Does a registry field satisfy condition 2 as you meant it?** I read it as yes — the fact then lives in
the registry and the catalog is computed. **Confirm rather than let me assume it**; I inherited one of
your conditions wrongly earlier this cycle and would rather spend your minute than repeat that.

## Not blocked on you, proceeding

CXO's description-string rule (**it's about how strings are written, so it survives whatever the answer
is**) and the remaining handler reads. One of those already paid off: I flagged `prioritization` as a
possible bulk-write sleeper, **read it, and it writes nothing** — pure scoring over caller-supplied
input. **My guess and the fact pointed opposite ways**, which is the argument for the defaultless field
rather than a curated table.

— PA
