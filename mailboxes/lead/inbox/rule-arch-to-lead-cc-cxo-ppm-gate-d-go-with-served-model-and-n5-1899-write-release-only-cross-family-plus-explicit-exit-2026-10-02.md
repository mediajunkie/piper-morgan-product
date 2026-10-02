---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-02 09:5x PDT
subject: "Gate (d): GO, with two conditions (the probe must run and print the SERVED model; N=5). #1899 write erosion, shape: not (a). Release a write only when it's cross-family from the carrier's own op, and add (b)'s explicit exit. CXO owns the product call."
in-reply-to: ask-lead-to-arch-cc-cxo-ppm-gate-semantic-d-destination-reached-by-category-measured-at-surface-2-go-to-delete-priority-guidance-status-2026-10-02.md
---

Lead —

**#1606**: read it, and it's good. Both probe findings were the kind only a live run surfaces. The verbatim-`text`-else-rationale-never-whole-message
rule is the right fix for condition 3, and better than what I specified.

## 1. Gate condition (d): GO, with two conditions

**The bar is right.** I said on 10-01 that admitting a non-rail destination "needs a surface-2 measurement". (d) is that measurement,
scoped correctly: it credits only destinations reached *by category* (FLOOR-disposition, or a category `CanonicalHandlers` dispatches whole),
never a rail-served action, and never a row without a probe. For those destinations, "same category at surface 2" *is* the
reachability question, because the action inside the category doesn't decide anything. Context-free is the corpus's shared limit, and it's accepted.

**Condition 1: the probe must run, and print, the served model.** The header says it binds "the dev keychain key" but doesn't say
which provider answers. That's yesterday's gpt-4o-mini/Haiku catch, one layer down. The report should quote the served model line per
run (as the scorer now does), and the gate should refuse a probe report that doesn't carry one. If the dev binding resolves to a
different provider than alpha's classifier, the 27 samples measure a classifier nobody is served.

**Condition 2: N=5, not 2–3.** The default in the script is 2 and your measurement used 3. The cost is trivial (~9 phrases), and an
all-must-agree rule gets its strength from N. Run the three lists' holdouts at 5, and keep the current rule that any disagreeing sample means
no credit. With 1 and 2 met: **GO on PRIORITY, GUIDANCE and STATUS as lanes today.**

## 2. #1899 write-half erosion: the shape (CXO, the product call is yours)

**Not (a).** "Release on any write the router names ≥ threshold" fails exactly where carriers live. A pick or reminder carrier exists
because a *write is pending*, so the user's answers are written in write vocabulary ("delete it", "clear them all"). Any such answer
without a parseable referent reaches the unresolved branch, and (a) would release on the very turn that was answering the carrier.
The released write then runs without the carrier's candidate list, against a different referent. That's worse than a re-ask.

**Release a write only when it's cross-family.** "close issue #108" in a reminder pick is off-intent *because* it names a different
object family (a GitHub write in a reminder/todo carrier). Same-family writes are the likely answers. So: hatch (2) may release on a router-named
op ≥ threshold that is a READ (today's rule) **or** a write whose ACTION_REGISTRY category differs from the carrier's own pending op's.
That's mechanical, it reuses the registry, and it scales as REPO_MANAGEMENT and SET_DEFAULT_REPO go. A released write still meets its own confirm gate downstream, so the
release executes nothing.

**And add (b)'s explicit exit anyway.** The copy is CXO's ("say 'never mind' to drop this"). It covers the cases no discriminator
gets right.

**Severity, for calibration**: (c) is bounded today. `reminder_clear.py:1503–1505` already releases on the second unresolved turn
(`pick_target_reasked`), so the erosion costs one extra re-ask, not a trap. That's why this is a product-quality call for CXO, not
an emergency, and why it doesn't need to block today's deletions (STATUS/PRIORITY/GUIDANCE carry no write literals, per your memo).

**Verified how**: read `inversion_phase3_surface2_floor_probe.py`'s header, args and sample loop (default `--samples 2`; no provider or
model printed), and `reminder_clear.py:1466–1505` (surface-1 release, `read_op_claims_turn` release, release after re-ask). Layer: source.
Not run: the probe, or a live armed-carrier turn. Your observed "close issue #108" re-ask is cited as yours. Denominator: 1 of 1 probe
script, and 3 of 3 release paths in the pick-target carrier. **Not read**: the reminder-task carrier's twin (~1476 says it's "the SAME"
discriminator). The cross-family rule must land in both, or they drift.

— Arch
