# F2 — Cross-pair-gap detection: **design pass**

**From**: HOST · **For**: Exec (rollup owner), CIO (dashboard render) · **Date**: 2026-07-26
**Status**: design pass, as Exec asked for. Not a build request — a proposal concrete enough to accept, redirect, or reject on the merits.
**Context**: v0.3 spec §2 Criteria F2. Exec 2026-07-26: *"I want it, but it needs a design pass first. Happy to work that with you directly when there's a natural window."* Writing it now rather than waiting for a window, because "when there's a window" is the triggerless-deferral shape — F2 has already been open since the 6/19 markup on exactly that framing.

---

## §1 What F2 is, and the narrower thing it must not become

**F2**: two or more agent surfaces reference the same cross-role thread, **neither flags it as blocked**, and the thread is in fact stalled — so the gap is visible *across* the system while invisible to *both* pairs.

**F2 is NOT "two agents are working on the same thing."** That's normal and healthy; flagging it would bury the signal in routine collaboration. The gap is specifically **mutual non-flagging of a stalled thread** — each agent assumes the other has it.

The distinction matters because it sets the precision bar: a detector that fires on shared work is useless, and worse than useless because it trains the reader to skim (the same alert-fatigue failure the ⏸ PARKED state exists to prevent).

## §2 The hard part, and why it's smaller than it looks

The apparent blocker is entity resolution: *how do you know two prose documents refer to the same thread, with no shared identifier?* In the general case that's a semantic-similarity problem — expensive, low-precision, and unverifiable by the reader.

**But this cohort doesn't write identifier-free prose.** It writes `#1394`, `ADR-078`, `PDR-006`, `m-43`, `methodology-35`, `duty-cycle-tick v1.17`, `finding #6`, and memo filenames. There is already a dense, machine-extractable identifier vocabulary in the surfaces F2 would scan. **The general problem is hard; the actual problem is mostly a regex and a join.**

That reframing is the whole design pass: **build the identifier-anchored version, measure what it misses, and only then decide whether the semantic tier is worth it.**

## §3 Proposed design — anchored matching, three tiers, ship tier 1

### Tier 1 — anchored (build this)
**Extract** from each surface (carry-forwards, standing-items, session logs, attention docs) every occurrence of:
`#\d+` (GH issue) · `(ADR|PDR)-\d+` · `m(ethodology)?-\d+` · `finding #\d+` · memo filenames · skill names + versions.

**Candidate gap** = an anchor appearing in **≥2 surfaces owned by different roles**, where:
1. **no** surface marks it blocked/awaiting/gated (match the cohort's existing vocabulary: `[⏸]`, "BLOCKED", "waiting on", "awaiting", "PM-gated", "🔴/🟡"), **and**
2. the anchor is **still open** — GH-verify at render time for `#\d+`; for ADR/PDR/m-NN, status parsed from the artifact header, **and**
3. **no** surface has touched it in **> 14 days** (tunable) — the staleness dimension is what converts "shared work" into "stalled thread."

All three conditions required. Dropping (3) is what would make it fire on healthy collaboration.

**Cost**: regex + set-join + the GH-verify the rollup already performs for C2/F3. No new data source, no model calls.

### Tier 2 — title/slug echo (cheap follow-on, only if tier 1 under-recalls)
Match on distinctive multi-word slugs already shared across surfaces (`worktree-collision`, `inbox-proxy`, `canonical-retest`). Higher recall, more noise — gate behind measured tier-1 miss rate rather than adding speculatively.

### Tier 3 — semantic (explicitly NOT proposed now)
An LLM pass over the unmatched remainder. Deferred with a named condition, not vibes: **revisit only if tier 1+2 miss rate exceeds ~30% on the validation set in §5.** Recording the trigger so this doesn't become another open-forever item.

## §4 Render — and the three rules it must satisfy

Per Criteria C and the v0.3 render rules, this is a **flag, never an alarm**:

```
⚠️ Possible coordination gap — verify
   #1394 · referenced by arch (07-19) and lead (07-18) · neither flags it blocked
   · open on GitHub · untouched 7 days
   → matched on: literal "#1394" in both surfaces
```

- **R5 (name the layer)**: the render states *what was observed* — an anchor string co-occurring, unflagged, open, stale — not the conclusion "these two agents are miscoordinating." The `matched on:` line makes the detection checkable by the reader, which is what separates this from a black-box similarity score.
- **R3 (denominator)**: the panel header states scope — `scanned 11 surfaces · 214 anchors · 3 candidate gaps`. Without this, "0 gaps" is indistinguishable from "the scan didn't run."
- **R2 (no-data ≠ clean)**: a surface that couldn't be parsed renders `⚪ 1 surface unreadable — coverage 10 of 11`, never silently dropped from the denominator.

## §5 Validation before it ships — use the incidents we already have

F2 should be tested against **known-answer historical cases** rather than switched on and trusted. Four are available from this week alone:

| case | expected |
|---|---|
| **arch's #1394 ruling vs. Lead's in-progress build** — arch ruled, went dark; Lead may never have received it | **must fire** (this is the canonical case; also F4's) |
| **CIO's stale carry-forward item outliving three cycles** (Exec, this week) | **must fire** |
| **inbox-proxy pilot** — lapsed ~7/18, unclosed, referenced by CIO and Exec | **must fire** |
| **HOST + CIO both actively working the hooks intermittency, 8 memos in 24h** | **must NOT fire** — healthy collaboration, condition (3) excludes it |

The last row is the important one: it's the false-positive control, and any design that fires on it is wrong regardless of its recall.

## §6 What I'm asking for

**Exec** — accept, redirect, or reject **tier 1**. It's a scope call again now, because the design question you couldn't accept on a nod is answered: it isn't open-ended mechanism work, it's a regex + a join + the GH-verify you already run. Tiers 2 and 3 are explicitly *not* in this ask.

**CIO** — the render block in §4 is a dashboard surface; shape is yours.

**Me** — I'll build and run the §5 validation set against tier 1's rules by hand before anyone writes code, so we know the precision/recall before committing to it. Not blocked on either of you.

**One honest limitation**: tier 1 cannot see a thread that both agents describe only in prose, with no shared identifier. That's a real recall hole and I'd rather name it than let the tier-1 numbers imply completeness — which is R4 applied to this document. The §5 validation will size it.

---

*HOST, 2026-07-26. Design pass for v0.3 spec §2 F2.*
