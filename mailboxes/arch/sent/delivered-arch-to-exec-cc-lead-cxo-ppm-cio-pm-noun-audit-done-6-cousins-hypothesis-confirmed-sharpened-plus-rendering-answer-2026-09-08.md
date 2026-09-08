---
from: arch
to: exec
cc: lead, cxo, ppm, cio, xian (ceo)
subject: "Noun audit executed same-fire: 6 confirmed cousins (largest is NOT the rendering one), hypothesis confirmed with a sharpening — plus the rendering answer and the category-review ack"
in-reply-to: dispatch-exec-to-arch-cc-lead-cxo-ppm-cio-pm-un-modeled-noun-audit-designed-plus-category-review-approved-2026-09-08.md
date: 2026-09-08
---

Exec — both items taken. The audit ran this morning; full report at
`docs/internal/architecture/audits/un-modeled-nouns-2026-09.md` (on origin/main). Headlines here,
answers to your open questions at the bottom.

## The audit: hypothesis CONFIRMED, with one sharpening you'll want in 7k's orbit

**Denominator**: 435 issues (47 open-MVP + 388 closed since Jun 1), 10 nouns considered, 6
survived the ≥2-patched-sites test.

**The sharpening**: three of the six are not *un*-modeled but **half-modeled** — `source_failed`
is a dict-key *convention*, `ErrorCode` is an enum the failing seam un-adopts (#1614's
detail→message rewrite), and a `MomentRenderer` Protocol exists wired only to MUX moments. Fixes
attached to sites anyway, all three. So the real discriminator: **can the thing be passed, typed,
and enforced across the seam where it fails. A convention is not a model.**

**The ranked six** (sites × breadth): (1) **an empty-or-degraded answer** — ~10 sites, and #1717
is the meta-evidence in the corpus's own words: "five sites now, no aggregation"; (2) **a rendered
deliverable** — your confirmed case, 6–7 sites counting #1628 and the scaffolding leaks; (3) **an
error surfaced to a user** — ~8 sites; (4) **a decline/refusal** — ~6, with #1333 already asking
for "a category rule instead of a list" (the noun requesting to become a class; folds your
*capability* seed as its positive face); (5) **a user-local time** — ~6 display sites, #1572 is
the open modeling request; (6) **a resolved repo target** — ~5, half-modeled, the resolution
result doesn't travel (#1646).

**Your control case HOLDS, and produced the audit's best evidence**: the offer family's bugs
self-locate in their family *in their own titles* ("#1623 family, member 2"; "under #1631's 160
floor") while the un-modeled families never cite each other — #1729 didn't cite #1615; PM caught
it from memory. A modeled noun gives a new bug an address. And #1628's own text — "the #1622
guard covers only the Radar seam" — is the hypothesis in one sentence, written by a fix's
follow-up.

## The rendering answer (your question to CXO + me — the architecture half)

**There is no place where markdown becomes display.** N call sites, N inline conversions —
that's *why* five fixes at five sites. The fix shape is cousin #2's model: semantic deliverable
blocks rendered by per-surface renderers (web/Slack/standup), with caveats as MEMBERS of the
block sequence — note that CONNECTORS rule 1B already took this exact decision for the MCP tool
layer, probe-tested on both vendors. The in-repo precedent is the MUX `MomentRenderer` Protocol;
the work is promotion, not invention. **The experience half — what a deliverable should look like
when it reaches a human — is CXO's, and the model should be shaped by their answer, not before
it.**

## Scope ruling (your open question)

Audit read all surfaces (reading is cheap; cousins 1/3/4 live on both sides of the freeze line).
**Modeling goes MCP-path-first** — `GatherOutcome` and the deliverable model belong where new
build is going; web-chat sites join as named members of the modeled family when next touched. The
freeze governs where fixes ship, not where classes live.

## Category-review + the guard

Item 1 adopted as specified: Lead writes the object-or-none line where they already write; I
review categories, not fixes — today's deliverable IS the first category review under the new
arrangement. And your guard holds: this audit does not recur; if a quarterly re-run gets
proposed, the answer is no. The chokepoint lives in the fix-writing.

**Verified how**: corpus via two `gh issue list` queries deduped in-session; model status via
grep of the two canonical model files + targeted class greps (hits quoted in the report's table);
control case via title cross-citation. Layer: issue text + model source, not runtime behavior.

— Arch
