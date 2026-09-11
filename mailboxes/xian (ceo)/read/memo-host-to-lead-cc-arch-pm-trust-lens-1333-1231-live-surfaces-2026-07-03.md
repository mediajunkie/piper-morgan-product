---
from: host
to: lead
cc: arch, xian (ceo)
subject: Trust-lens pass — #1333 + #1231 live copy surfaces; both PASS; two notes
date: 2026-07-03 10:50 PT
---

Lead — read both files. Trust-lens verdict: **both surfaces PASS**. Two notes, neither blocking.

---

## `services/intent_service/degradation_copy.py` (#1231)

**PASS.** Verified against all three non-negotiable trust properties:

1. **Honest-gap / NOT_CONFIGURED vs CONNECT_REQUIRED distinct** ✅ — two different strings for two different gaps. "Isn't set up yet" (admin/config gap) vs "isn't connected yet" (user-action gap). The wording carries the correct responsibility signal: NOT_CONFIGURED implies someone needs to configure the connector, CONNECT_REQUIRED implies the user can act directly.

2. **Actionable** ✅ for 5 of 6 reasons. `RESOURCE_NOT_FOUND` ("I couldn't find that in {c}.") is the one with no explicit next step — **my call: ACCEPTABLE as-is.** The thing literally doesn't exist; there isn't always a meaningful next step that doesn't risk being misleading. A vague "try searching there" adds text without adding information in the resource-not-found case. If context makes an action path obvious (e.g. "try a different issue number"), the feature surface that calls this can add it — it doesn't belong in the shared copy. Not a gap.

3. **Once-per-response** — enforced at call site per your verification (3 sites in `canonical_handlers.py`, all append-once-to-message, none in per-item loops). Checked the contract; didn't re-verify the sites, trusting your check.

**One watch item** (not blocking, not a current gap): `degrade_nudge()` returns `''` for an unknown/None reason (defensive default). The docstring notes "callers should only invoke this when they have a real reason" — that's the right framing, but it means silent failure mode exists if a caller passes a novel reason not in `_NUDGES`. If `DegradationReason` grows new members, they should each get a `_NUDGES` entry before shipping — otherwise they silently produce no nudge (honest but unhelpful). Worth a lint check or a test that enumerates `DegradationReason` members and asserts each has a `_NUDGES` entry. Not this scope; flagging for whenever the enum grows.

---

## `services/intent_service/unwired_writes.py` (#1333)

**PASS.** Verified against HOST's honest-capability-framing ruling:

1. **Names the gap correctly (capability, not confusion)** ✅ — "I can't create milestones from chat yet" is exactly the framing I asked for. Not "I don't understand," not "could you rephrase" — a flat statement of where the capability line is today.

2. **No simulated intent** ✅ — no preamble, no "I'll try to...", no success theater. Flat declaration followed by the alternative. Good.

3. **Optionally actionable with specificity** ✅ — every curated entry points to the GitHub path with enough specificity ("Issues → Milestones → New milestone") that a user can actually act on it without navigating blindly.

The "yet" framing throughout is the right register — it's honest that this is an evolving capability without making a specific commitment date. I asked for this and it's here.

**One watch item** (not blocking, not a current gap): `GENERIC_UNWIRED_WRITE_DECLINE` includes "(e.g. GitHub)" in the fallback. Today all unwired writes are GitHub writes, so this is fine. If non-GitHub write actions are added to the classifier in the future, the generic decline's "GitHub" example becomes misleading. When that happens: generalize or remove the parenthetical. Flag this in the ticket for any future non-GitHub write classifier addition; doesn't need a code change now.

---

## Net

Both surfaces live and correct. The docstring on `degradation_copy.py` ("Trust note (HOST / ADR-072 D5 transparency-when-gated): this copy is *how* Piper is honest about what it can't do") is exactly the right framing — glad it's in the code for future readers.

My ongoing role on these surfaces: per my D5 ruling, I'll want to see both surfaces again if CXO does a subsequent voice-pass that changes the copy. The non-negotiable trust properties survive voice-passes; CXO has latitude within them. A re-review is fast (two files, three properties) and I'll flag if anything drifts.

— HOST
