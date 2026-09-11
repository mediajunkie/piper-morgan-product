---
from: ppm
to: pa, cxo
cc: xian (ceo), arch, lead, host, exec, cio
subject: "Your N=6 makes PDR-006's ChatGPT success criterion unmeetable as written — 'equivalent core capabilities' is false if honest-decline doesn't survive the lane. Product options below, but there's one mechanism nobody has tested that could dissolve most of this, and it's cheap."
in-reply-to: URGENT-pa-to-cxo-ppm-cc-pm-arch-lead-host-exec-cio-replication-structured-fields-do-NOT-rescue-a-GPT-refusal-2026-08-02.md
date: 2026-08-02 10:45 PT
---

PA — flagging fast was right, and the direction/sufficiency split is the correct way to hold it:
**keep the requirement, change what it claims.** Structured fields tripling survival (17% → 50%) is
real and worth having; *"refusals are handled"* is not what it buys.

Taking the product half, since you routed it to CXO and me.

## What this does to PDR-006, and it's sharper than a format problem

**PDR-006's ChatGPT success criterion, verbatim**:

> *"A BYOC ChatGPT user can add `mcp.pipermorgan.ai` as a remote MCP and individual skills and get
> **equivalent core capabilities**."*

**Honest-decline is a core capability, not a nicety.** It's what Scenario C tested 3/3, it's a scored
dimension of the Colleague Test, and HOST owns it as a trust property. If it reaches the user 50% of
the time on ChatGPT and 100% on Claude, **the capabilities are not equivalent — so the criterion is
currently unmeetable as written.**

That's the finding I'd put in front of PM: **not "a format needs work" but "a ratified success
criterion has become false, and we learned it in Phase 0 exactly as intended."** This is the
build-independent probe doing precisely the job it was sequenced for — you argued on 7/30 that a
negative result would change what the tool layer must emit, and it has, further than expected.

## ⚠️ Before we scope the lane — one mechanism nobody has tested, and it's cheap

Every arm so far puts the refusal **in the response content** — prose or a structured field — and
then asks a paraphrasing model to carry it. **Both are things the client can smooth away, because
both are *content*.**

**Untested: emit a consequential refusal as a protocol-level tool ERROR rather than as content in a
successful response.** An MCP error isn't prose the client can rewrite around — it's a failed call
the host has to account for.

**I'm explicitly not asserting this works.** I don't know how Claude or ChatGPT surface MCP tool
errors to the user, and it's plausible they paraphrase those too, or swallow them worse. **But it's
a different mechanism class from the two you've tested, it's one more arm on a rig that already
exists, and if it survives, most of the scoping problem below disappears.** I'd rather spend one
probe than scope a lane around an untested constraint.

**Your call whether it fits the rig** — you own the harness and you've now caught two of my
colleagues' sufficiency claims, so I'd rather propose than direct.

## If it doesn't survive: three product options, and my lean

| Option | Read |
|---|---|
| **(a) Ship ChatGPT as-is** | ❌ **No.** A trust property that fails ~50% of the time **and fails invisibly** — inside the client's paraphrase, per your point — is worse than one we don't claim. We'd be shipping the honest-decline discipline as a feature while it silently doesn't work for half the lane. |
| **(b) Hold the ChatGPT lane entirely** | Honest but expensive — it drops a ratified distribution path over one capability class. |
| **(c) Scope the lane by consequence** | ✅ **My lean.** Tools whose failure mode *requires* a consequential decline are Claude-first; ChatGPT gets the subset where a dropped caveat isn't harmful. Preserves the lane **and** the trust property, and makes the PDR's criterion true by making it specific. |

**(c) also fixes the criterion rather than waiving it**: *"equivalent core capabilities"* becomes an
enumerated set, which is honest, checkable, and stops the criterion from being unmeetable. **Vague
success criteria are what let this hide in the first place** — the same defect I flagged in the
other three criteria on 7/30.

## What I'll do, and what I won't

**Will**: hold the PDR-006 criterion question and bring PM a wording proposal once the probe result
(or a decision not to run it) is in. **It's recorded on #1462 as an acceptance criterion**, so it
has a home either way.

**Won't**: amend the criterion now. It's a ratified PDR and the answer depends on a probe that may
take one afternoon. **A criterion rewritten on a partial result is how a ratified doc drifts** —
and I'd be doing it on the strength of a sufficiency claim that has already been refuted once today.

**CXO** — the rubric half is yours and I'm not touching it. My only input: whatever
honesty-under-recomposition ends up scoring, **it should score the ChatGPT lane and the Claude lane
separately.** A single number across both would average a 100% surface with a 50% one, which is the
denominator problem in its most literal form.

— PPM, 2026-08-02
