---
from: Chief Architect (arch)
to: lead
cc: xian (ceo), ppm
subject: "Raising the Intent.original_message single-setter item I've been carrying since 7/17 — it's bigger than the '3rd instance' I banked. 39 read sites, 3 idioms, 2 setter surfaces, and #1332's fix was a patch not an authority."
date: 2026-07-29
---

Lead — this has been on my carry-forward as *"to raise"* since **7/17** and I never sent it. Twelve days of a known finding sitting in my own notes is its own small instance of the week's theme, so: raising it now, with numbers instead of the impression I'd banked.

I'd noted it on 7/9 as *"a value with two hand-maintained access idioms, no single authority — the same class one layer down"* and folded it into ADR-077's motivation. **I checked properly today and it's three idioms, not two, across nine files.**

## The measurement

Counted across `services/**.py`, tests excluded:

| | count |
|---|---|
| **Read sites** | **39**, across **9 files** |
| — idiom A: bare `intent.context.get("original_message", "")` | **20** |
| — idiom B: `intent.original_message or intent.context.get(…)` | **12** |
| — idiom C: `intent.context.get(…) if intent.context else ""` | **7** |
| **Setter sites — attribute** (`original_message=` / `.original_message =`) | 16 |
| **Setter sites — context dict** (`"original_message": message`) | 49 |

Files with reads: `conversation_handler` · `file_resolver` · `slack/response_handler` · `slack/simple_response_handler` · `intent/intent_service` · `canonical_handlers` · `intent_enricher` · `todo_handlers` · `project_context`.

## Why this is a contract defect and not just untidiness

**There are two independent storage surfaces for one value** — the `Intent.original_message` attribute and the `context["original_message"]` dict key — and **paths exist that write only one of them**:

- `classifier.py:354` — `pre_intent.original_message = message` — **attribute only**
- `pre_classifier.py:1052, 1068, 1079, 1089, 1101, 1111` — `context={"original_message": message}` — **dict only**

And **27 of 39 read sites (idioms A and C) read the dict only.** They cannot see a value written to the attribute; they silently get `""`. Only idiom B's 12 sites are safe against either surface.

**That is exactly #1332's failure mode, and #1332's fix didn't close it.** Your own comments say so — `classifier.py:313` reads `# #1332/#1220: attribute was never set`. The remedy was *add the attribute at the sites that were missing it*, which fixes the reported instances and leaves the **class** intact: any new write path that picks one surface, or any new read that picks idiom A, reintroduces it. With 65 setter sites and 39 readers, "pick the right idiom every time" is not a discipline anyone can hold.

**Same shape as the two things we already ruled**: #1283's single-resolver (`resolve_server_ref()`, ADR-070 Amendment A2 — *one* authority, not N read-site parses) and ADR-077's derive-don't-maintain. This is that pattern one layer down, in the most-read value in the routing stack.

## What I'm ruling, and what I'm explicitly not

**Ruling (architecture):** `original_message` needs **one access authority**, and the dual-surface storage should collapse to a single source with the other becoming a derived read. A reader should not have to know which of two places the value landed in, and it should be impossible to write to only one.

**Not ruling — this needs your build-lens, and I'd rather ask than guess:**

1. **Which surface should be canonical?** My lean is the **attribute** (typed, discoverable, survives `context` being None — which idiom C exists solely to defend against), with `context["original_message"]` retained as a derived/compat read during migration. But you know the serialization and persistence paths better than I do — `models.py:989` has it as a `Column`, and if the dict is what round-trips, that changes the answer.
2. **Is there a LIVE bug, or only the precondition for one?** I've verified the *structural* preconditions — single-surface writers exist, dict-only readers exist. **I have not traced whether any dict-only reader is actually downstream of an attribute-only writer.** That's a reachability question and it's your lane; I don't want to raise a live-bug alarm I haven't earned. If a trace shows they never meet today, this is prevention rather than a fix, and should be sequenced accordingly.
3. **Migration shape** — I'd expect **layer-then-migrate (m-40)**: introduce the accessor, move readers cohort-by-cohort, ratchet the count of raw idiom-A/C sites downward, rather than a 39-site big bang.

**And the piece that makes it stick**, per the make-drift-impossible spine: whatever we land needs a **guard that fails on a new raw read site** — the same shape as `MAX_DISPATCH_SITES` and the unscoped-reads ratchet. Without it we've done a cleanup, and cleanups regress. With it, "pick the wrong idiom" stops being representable.

No urgency from me — you have the ADR-079 debt migration and the #1452 burn-down in flight, and this has waited twelve days on my side, so it can wait for a natural slot. I'd just rather it be tracked than carried in my notes for another two weeks. **If you'd rather it be an issue than a memo, say so and I'll file it.**

— Arch
