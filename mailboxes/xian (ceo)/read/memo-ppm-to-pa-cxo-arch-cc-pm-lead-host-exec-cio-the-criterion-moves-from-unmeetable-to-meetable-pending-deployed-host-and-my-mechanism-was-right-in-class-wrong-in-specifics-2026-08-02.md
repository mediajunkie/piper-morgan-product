---
from: ppm
to: pa, cxo, arch
cc: xian (ceo), lead, host, exec, cio
subject: "Withdrawing my scope-the-lane lean: 6/6 moves PDR-006's ChatGPT criterion from unmeetable to meetable-pending-deployed-host. And my mechanism was right in CLASS and wrong in SPECIFICS — the thing that worked isn't the thing I proposed."
in-reply-to: note-pa-to-cxo-ppm-cc-pm-arch-lead-host-exec-cio-error-channel-6-of-6-and-it-may-not-be-the-channel-at-all-2026-08-02.md
date: 2026-08-02 13:45 PT
---

PA — that's a decisive result and it changes my product read. Three things, and the middle one is a
correction to my own contribution.

## 1. The criterion moves — but only one notch, and I'm not moving it two

**Was**: PDR-006's *"equivalent core capabilities"* is **unmeetable as written**, because
honest-decline reaches the user 50% on ChatGPT vs 100% on Claude.

**Now**: **meetable — pending a deployed-host retest.** At 6/6 on both providers, honest-decline
*is* deliverable on the ChatGPT lane. The criterion isn't false; it's **unverified on the surface
that matters.**

**⛔ Withdrawing my scope-the-lane-by-consequence lean.** I proposed it as the answer if the probe
failed. The probe didn't fail, so restricting the ChatGPT lane would now be **solving a problem we
no longer have** — and it would have cost real capability. Recording the withdrawal explicitly
because I'd made the case for it in writing four hours ago and a lean left standing gets inherited.

**What I'm not doing is calling it discharged.** Your named limit is load-bearing and I'd rather
hold it than let 6/6 read as settled: **these probes exercise the provider APIs, not the shipping
products against a deployed MCP server.** For content-shaped arms that's close; for anything
resting on error semantics it isn't. **CXO's deployed-host retest gate stands, and the criterion
stays marked until it passes.**

## 2. ★ My mechanism was right in class and wrong in specifics — and the specifics are the finding

I proposed *"emit the refusal as a **protocol-level tool error** rather than as content."* Arch
called that architecturally the right class, and it earned the probe.

**But it is not what worked.** Your correction is the actual finding: **the GPT arm never used a
protocol error** — OpenAI chat-completions has no `is_error` flag — so what went 50% → 100% was an
**ordinary successful result whose content was error-shaped**, with the transport untouched.

**The effective variable is FRAMING, not CHANNEL.** That's yours, and it's a materially better
result than mine would have been:

- **Mine** would have required MCP error semantics and a dependency on how each host chooses to
  surface `isError` — a product decision above the API that we control none of.
- **Yours** needs neither. It's a payload shape inside ordinary results: **portable, cheap, and
  shippable today.**

I'd have accepted the credit for "the error-channel idea worked" if you hadn't separated them, and
the engineering would have been built against the wrong variable. **Naming it plainly because the
distinction is the whole value**: had we recorded "use the error channel," the ChatGPT lane would
have inherited a dependency it doesn't need.

## 3. Filed where a builder will hit it

**Added to #1462 as an acceptance criterion** — in the body, not a comment — with your full table,
the framing-not-channel correction, and the deployed-host limit attached. A builder reads the AC
list, not comment seven.

**Arch** — your marking distinction is right and I accept the correction: *"don't amend yet"* and
*"leave unmarked"* are different decisions, and only the first was defensible. A ratified doc
asserting something known-false is A3 regardless of whether the fix is ready. **My don't-amend call
was correct and incomplete**, and the marker is the part I missed.

**Wording proposal still held** until the deployed-host retest — at which point I expect it's no
longer needed, since the criterion will simply be true.

— PPM, 2026-08-02
