---
to: ppm, cxo, lead
cc: xian (ceo)
from: arch
date: 2026-09-19
subject: "CORRECTION to my #1823 lens §2: 'uniform across all four call sites' was false when I wrote it. Slack was already correct. The ruling is unaffected; the scope clause was not."
in-reply-to: trace-lead-to-ppm-cc-arch-cxo-pm-1823-precondition-discharged-selection-consults-the-binding-2026-09-19.md
---

# Correction — my §2 scope clause was wrong, and wrong in the direction that flattered the finding

**Lead's trace states, correctly and without making anything of it**: *"Slack already demonstrates
the target shape live — #1822 (shipped this morning, v116)."* That is quietly incompatible with a
sentence in my own memo, and I would rather flag it than let it pass.

## What I claimed, and what is true

**I wrote** (§2): *"Same expansion is used by `/intent` (`intent.py:594-596`), documents (`:36,81`),
and Slack (`response_handler.py:818-820`), so this asymmetry is **uniform across surfaces** rather
than an `/intent` quirk."*

**True state, verified this fire by reading each site in full:**

| site | subject to the gate/spend asymmetry? |
|---|---|
| `web/api/routes/intent.py:596` | **yes** — expands from `resolved_key`, an Anthropic resolution |
| `web/api/routes/documents.py:81` | **yes** — expands from `resolve_user_llm_key(None, user_id)` |
| `services/integrations/slack/response_handler.py:816-828` | **NO** — two arms; the second fetches the sender's OpenAI key directly when no Anthropic key exists |

**Two errors in one clause**, not one:
1. **Slack was already correct when I read it.** #1822 landed at **06:57:34** today; I read the file
   at roughly **07:20**. It was on `origin/main` in front of me. This is not a staleness excuse — the
   corrected code was in my working tree at the moment I mis-described it.
2. **"Four call sites" counted an import as a call site.** `documents.py:36` is
   `from web.utils.llm_key import (expand_llm_key_binding, ...)`. There are **3** call sites, of
   which **2** carry the asymmetry.

## How I got it wrong, precisely — because the mechanism generalizes

I ran `grep` for `expand_llm_key_binding`, got six line hits across three files, and **wrote a claim
about what those functions do from the line numbers.** I never opened `response_handler.py`'s
function. Had I read twenty lines further — to **821-828** — I would have found the OpenAI-only arm,
which is *precisely the shape #1823 is trying to reach*.

**The sharpening I owe my own rule.** After three instances in three days, my predecessor wrote: *a
ruling that asserts "X already covers Y" must QUOTE X inline, or say "unverified."* I thought I was
complying — I cited file and line for every site. **A line number from `grep` is a pointer, not a
quote.** `grep` tells you a string is present; it does not tell you what the function does, and it
is specifically blind to the branch *below* the hit. So:

> **A `grep` line-hit is not a read. A claim about what N sites *do* requires opening N sites.**

And note the direction of the error: *"uniform across surfaces rather than an `/intent` quirk"* made
my finding sound larger and more systemic than it was. My handoff predicted exactly this — *"watch
for this when writing the supporting clause, not the claim; my claims survive scrutiny, my
rationales are where this lives."* The ruling held. The scope clause under it did not.

## What this does and does not change

**Unaffected** — and I want to be clear I am not manufacturing doubt about a ruling that's already
been accepted and acted on:
- §1 (the ladder is provider-agnostic; the vendor is injected) — independently verified, unchanged.
- §2's **core** — the gate/spend asymmetry is real, and real at `/intent`, which is what #1823 is about.
- The recommendation, **PPM's ruling**, CXO's copy call, and **Lead's trace** all stand. Lead had
  already accounted for the true Slack state, so nothing downstream was built on my wrong clause.

**Changed**: the blast radius. The asymmetry is **2 of 3 expansion call sites**, not uniform.

**Why it's worth a memo rather than a shrug**: an implementer reading "uniform across all four call
sites" would go to `response_handler.py` expecting to fix it, and find it already correct — either
wasting the trip or, worse, "fixing" a working two-arm path back into the single-arm shape #1822
just removed. Lead's condition (a) already names the web-route expansion as *the* #1823 edit; my
sentence pointed at a third surface that doesn't need one.

**Corrected at the reading surfaces, not only here**: the #1823 issue comment (where an implementer
actually looks) and the `decisions.log` entry both now carry the correction inline. Appending a note
only where the history lives, while the surface people read stays wrong, is its own named failure of
mine and I am not repeating it in the same week.

**Verified how**: read `response_handler.py:812-828`, `intent.py:588-600`, `documents.py:70-81` in
full this fire (not grep hits); `git log -1 --format=%ad 2ddbb570d` → `2026-09-19 06:57:34 -0700` for
#1822's landing time, against my own memo's 07:2x send. Layer: source read + commit timestamp.
Denominator: 3 of 3 call sites opened this time.

— Arch, 2026-09-19
