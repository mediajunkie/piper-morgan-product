# Promotion Is a Re-Verification Event — The Durable Copy Needs a Named Source

**Status**: **EMERGING.** Limb 2 now has a **shipped, independently-run mechanism**; **limb 1 remains vigilance and this file says so rather than implying coverage.** HOST's hold (*"I don't want to file it as prose-only"*) is **discharged**. Numbering and corpus placement remain CIO's.
**Filed**: 2026-07-30 by CXO (draft) · mechanism landed 2026-07-31 (HOST, `d697a7736`) · status advanced 2026-07-31
**Origin**: Proposed by **CXO** after doing it twice in two days to the same document. **HOST** ruled it *sibling, not instance* of m-44 and contributed the second limb from an independent instance the same morning. **Arch** applied it to its own artifact unprompted and added the third.
**Related**: methodology-44 (Clear Is Not a Measurement), methodology-45 (Agreement Is Not Replication), methodology-43 (Name the Layer), methodology-36 (mechanisms over vigilance)

## The claim

**Moving a claim onto a more durable, higher-authority surface is itself an event that requires
re-verification — at the moment of the move, against live state.**

And the general form, which covers both limbs below:

> **A durable artifact is a COPY. Every copy needs a named source and a re-check at the moment of
> copying. If you cannot say which copy is the source, you have already lost.**

### Why it is counterintuitive — this is the part that makes it stick

The whole *reason* to promote a claim is that memos are ephemeral and the corpus is durable. That
framing makes promotion feel like a **safety improvement**, so the verification bar feels *lower* —
*"this was already reviewed, I'm just relocating it."*

**It is the opposite.** Durability amplifies whatever you put into it, **including error**. A stale
claim in a memo scrolls away. **A stale claim in the corpus is what future agents trust**, and it is
read long after the correcting memo is gone.

## Two limbs

**Limb 1 — promotion is a re-verification event** *(CXO's instance)*. A claim verified at T1 and
promoted at T2 is **unverified at T2**. The verification was valid when performed; correctness does
not travel with the text.

**Limb 2 — don't keep a measurable fact in prose when a tool can emit it** *(HOST's instance)*. When
a fact is both hand-written and generated, the hand-written copy will be maintained and the generator
will silently revert it — or vice versa. **When you must keep both, name which is the source.**

The limbs are one methodology because they are the same question at two moments: *which copy is
authoritative, and is it current?* Limb 1's source is **live state**; limb 2's source is **the
generator**.

## Boundary — why this is not m-43, m-44, or m-45

| | fails | why it doesn't cover this |
|---|---|---|
| **m-43** Name the Layer | the agent checks the right property on the **wrong object** | here the object was right |
| **m-44** Clear Is Not a Measurement | the **instrument** emits a pass indistinguishable from never running | here the instrument worked and genuinely measured what it measured |
| **m-45** Agreement Is Not Replication | the **social layer** — N agents' convergence is one confound run N times | here a single agent, no convergence involved |
| **m-46** Promotion Is a Re-Verification Event | the **temporal / custodial layer** — a correct verification made stale by relocation, or a fact maintained on the copy instead of the source | — |

**The discriminator, stated as HOST put it**: m-44 is *the right property checked on the wrong
object*; **m-46 is the right property, checked correctly, at the wrong time.** Same family, different
axis. Folding it into m-44 would blur the discriminator that makes m-44 usable.

## The evidence

**Instance 1 — CXO, 2026-07-29.** PM asked that the CXO spatial argument be moved out of memo-only
storage into the ADR corpus, precisely because memos are ephemeral. The doc was written against
Arch's 07-19 code characterization. **Arch corrected that characterization at 15:50 the same day**,
and ruled explicitly that nothing in the review could ratify on the old version. CXO was mid-push.
**Caught only by a rebase conflict in `decisions.log`** that put Arch's correction on screen — file
contention, not process. Ten minutes earlier it would have landed.

**Instance 2 — CXO, 2026-07-30, same document.** Arch's import-graph map superseded it again: the doc
said three layers and five cold modules; the measured truth was four and ten. **Two corrections in
two days, on the surface created *because* it was durable.**

**Instance 3 — HOST, 2026-07-30, opposite direction.** Comms hand-edited `MEMORY.md`'s header to
reclaim six lines — a correct call and a real win. But `rebuild-memory-index.py` still emitted the old
long header, so **the next regen would have silently reverted it.** Discovered only by running the
script. *Comms fixed the artifact; the generator held the real value.* Nothing was destroyed — this
limb fails harmlessly and silently, which is why it goes unnoticed.

**Corroboration — Arch, 2026-07-30.** On being sent limb 2, Arch applied it to its **own** artifact
rather than assuming its case differed: the layer map is prose containing a live/cold table built from
the import graph. *"The graph was the right source; freezing it into prose reintroduces the staleness
one layer down."* The map now carries the regenerating command, the line **"if this table and the tool
disagree, the tool is right,"** and no exemption for itself.

## The cure — structural, not attentional

**Not "verify harder."** Three roles were already being careful; carefulness is what produced the
prose copies in the first place.

1. **Don't duplicate measurable facts into prose at all.** Prose cannot be re-run; a tool can. The
   fix that worked: the CXO thesis doc now **defers to Arch's map for all live/cold facts and says so
   explicitly**, keeping only what *cannot* be derived from the import graph — the experience
   argument, the who-initiates discriminator, the falsifiability conditions.
2. **When a durable doc must carry generated facts, ship three things with them**: the command that
   regenerates them, an explicit *"if this and the tool disagree, the tool is right,"* and no
   self-exemption.
3. **The shape to aim for**: *assert the decision, point at the tool for the facts.* (Arch's phrasing;
   intended for the ADR-038 amendment.)
4. **Treat the act of promoting as a trigger**, the way a release is a trigger: re-check the claim
   against live state at the moment it moves, not at the moment it was written.

## The mechanism (limb 2) — and the obstacle is itself the finding

**`scripts/check-derived-drift.sh` + `--check` on `rebuild-memory-index.py`** (HOST, 2026-07-31,
`d697a7736`). Renders each registered derived artifact, compares to the committed copy, prints the
first differing line, exits non-zero, **writes nothing.**

### ★ Why this was hard, and it generalizes past memory indexes

> **A plain rebuild REPAIRS the drift it would have detected.** Run the generator to find out whether
> the artifact still matches it, and you have destroyed the evidence — the answer is always *"it
> matches now."*

**A detector that repairs what it measures cannot report.** That is the general obstacle to
mechanizing limb 2, and it is why this went unmechanized for so long: the obvious implementation
(*just re-run the generator and look*) is not a detector at all. **The precondition for registering
any generated artifact is that its generator can render without writing.**

This is a **sibling of m-44 at the instrument layer**: m-44 is an instrument that reports clear
without measuring; this is an instrument that *silently fixes* the thing it was asked to measure, so
it reports clear **truthfully** and still tells you nothing. Both emit a green you cannot act on.

**The corroborating incident**: Comms's hand-compacted `MEMORY.md` header (07-30) was caught only
because HOST ran the rebuild for an unrelated reason **and read the output — one turn before the fix
would have erased the symptom.** A minute later, unread, and the reclaim would have vanished with no
record it had existed.

### Coverage is a first-class output, deliberately

The runner prints, every run, **what it does not check** — and closes with *"No drift among REGISTERED
artifacts. This is not a statement about the unregistered ones."* Currently **1 registered, 2
explicitly excluded** (the census needs delimited generated-block markers; the briefing is
hand-maintained and covered by a different mechanism).

That property is not decoration. **A drift-check covering one artifact while reading as a clean bill
of health would be the same failure as a green probe exercising only the mitigated path** — the exact
thing this family exists to catch, rebuilt inside the fix.

### Verified by someone other than its author

Per the standing caveat — *a script is not a mechanism until someone other than its author has seen it
do the thing* — **Comms ran it independently (4 of 4, including the drift case), and CXO ran it
(clean case, coverage output as documented).** Not wired to cron, hook, or CI **by deliberate choice**:
HOST declined to automate before knowing the false-positive rate, on the grounds that four
counter-hypotheses died this week on data that fit them perfectly.

## What is NOT established

- ⚠️ **Limb 1 has no mechanism and this is not it.** The drift check addresses limb 2 (*don't keep a
  measurable fact in prose when a tool can emit it*) **directly**, and limb 1 (*promotion is a
  re-verification event*) **only indirectly** — nothing mechanically catches a claim that was true at
  T1 and stale at T2 when it is promoted into prose. **Instance 1 was caught by a rebase conflict;
  instance 3 by someone checking a citation on a whim. Limb 1 is still vigilance.** Stated plainly at
  HOST's insistence, because a file that showcased a shipped mechanism while staying silent here would
  imply coverage it does not have — which is this family's own failure mode.
- **Registered coverage is one artifact.** Honest by design, but small.
- **Four instances, three roles, four days.** Enough to name and now to mechanize half of; not enough
  to call Proven.
- **The generalization to judgment-shaped claims is untested.** All instances involve facts a tool
  could emit. Design positions and product calls arguably *should* live in prose — which is why the
  CXO cure was deferring the *measurable half*, not deleting the doc.
- **Three instances, two roles, four days.** Enough to name, not enough to call Proven. Deliberately
  filed as **Emerging/Proposed**.
- **The generalization to non-code facts is untested.** All three instances involve facts a tool could
  emit. Whether the same discipline helps for judgment-shaped claims (a design position, a product
  call) is unknown — arguably those are exactly the claims that *should* live in prose, which is why
  the CXO cure was *deferral of the measurable half*, not deletion of the doc.

---

*Routed to CIO and HOST for the filing call. HOST offered to draft or review; CXO wrote it per HOST's
"your finding, your call." Corrections welcome — and per the methodology's own content, if this file
and the memos it derives from disagree, **the memos are the source**: `memo-cxo-to-cio-…-step0-detector-false-pass-plus-m44-candidate-…-2026-07-30`,
`note-host-to-cxo-cio-…-m44-ruling-sibling-not-instance-2026-07-30`,
`memo-arch-to-cxo-…-all-four-folded-…-2026-07-30`.*
