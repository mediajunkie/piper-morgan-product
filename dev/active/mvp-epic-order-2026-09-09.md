# MVP Sprint Backlog — Ordered Epics (source of truth)

**Owner**: PPM. **Status**: live working order — update in place as epics close/reorder, don't
fork a new file per revision. **Purpose**: per PM's 2026-09-09 directive (relayed by Exec), Lead
works ONE epic at a time, fully, before moving to the next. This file is what Lead consults
without needing to ask anyone. Board Status/Sprint fields are the per-issue record; this file is
the *order*, which no GitHub field currently encodes.

**The rule, verbatim from PM's directive**: work the current epic until it's fully closed.
Discovered work goes into (a) the same epic, (b) another epic, or (c) a later milestone — only
work added to the SAME epic delays that epic's closure. Epic-relative progress is legible;
pile-relative progress (the flat "N not done" count) is not.

**Provenance**: cause-factoring by Arch (`factoring-arch-to-ppm...-2026-09-09.md`), 37 Sprint
Backlog items live-pulled 2026-09-09, cross-checked against a fresh pull before ordering (both
agree: 37 items, same membership). Ordering and any reclassification below is PPM's.

---

## Order

### 1. CI/infra red (3 items) — cheap, and it's a quiet tax on every epic after it
`#1687` four CI workflows standing red · `#1711` Keychain ACL hang blocks server startup silently
· `#1637` 6 standing test failures poisoning 6 more when run combined.

**Why first**: every day CI stays red, every other epic's evidence weakens (a green suite means
less when four workflows are already known-broken). Cheap relative to its value. If it turns out
not-cheap, the fallback is explicitly accepting these as known-red rather than let them silently
discount every later epic's signal.

### 2. Security/tenancy (4 items) — before beta wave 1, regardless of everything else
`#1734` [SECURITY] personality API PUT-rewrites the global config (any user's save clobbers the
instance overlay) · `#1690` demo plugin live-mounted by default in every prod deploy · `#1732`
[SECURITY] chat-render XSS, no sanitizer · `#1733` stale unauthenticated duplicate page.

**Why here, non-negotiable**: `#1734` is a global-write hazard live on the hosted beta right now.
This epic's position doesn't move for scheduling convenience.

### 3. Acceptance contract (8 items) — freshest pain, design is DONE, unblocks a whole cluster
`#1739` (umbrella) · `#1663` · `#1652` · `#1653` · `#1654` · `#1694` · `#1696` · `#1596`.

**Why third**: PM's live round converged three failures onto this one contract today. Both design
passes are already in (Arch's sequencing ruling + CXO's two-axis correction, conceded by Arch) —
Lead builds against a finished spec, not an open question. Closing this epic unblocks the
reminder/standup UX cluster wholesale, per Arch's read.

### 4. Corpus/classifier deposits (6 items) — no dependency, pick up opportunistically
`#1505` `#1527` `#1559` `#1579` `#1606` `#1693`.

**Why here, not strictly ordered**: Arch's own note — these parallelize freely, cheap,
ratchet-governed gate-side deposits with no dependency on anything else in this list. Placed
fourth as a resting point, but if a fire has spare capacity before epic 3 closes and none of
these touch epic 3's files, pulling one is not a violation of "one epic at a time" — they're
independent by construction. If in doubt, finish the current epic first anyway.

### 5. Honest-empty / GatherOutcome (4 items) — lands after the acceptance-contract idiom proves out
`#1717` (the audit's own meta-evidence for this cousin) · `#1730` · `#1736` · `#1738` (shared with
Deliverable below).

**Why after epic 3, not before**: Arch's note — this is design-then-fix, and it benefits from the
acceptance contract proving the single-source-predicate idiom on a live seam first, rather than
inventing a second one in parallel.

⚠️ **CXO's flag, carried forward — one line, not a gate**: this cousin is copy-shaped (the model
settles what's *true*; the user-facing sentence is a separate artifact — see `#1717`'s own
standing proof, a correctly-composed turn that still read as a broken-system litany). **Whoever
scopes this epic's build should name, in the epic issue itself, whose the user-facing contract
is** (CXO's, by the existing pattern) before writing the aggregation copy, not after.

### 6. Rendered deliverable (2 items + 2 shared with GatherOutcome/Security) — same reasoning as 5
`#1729` · shares `#1732` (security) and `#1738` (GatherOutcome).

**Why here**: same "prove the idiom first" logic as epic 5; MCP-path-first per the ratified scope
ruling, per Arch. **Same CXO flag applies** — name the copy-owner before scoping the fix.

### 7. False-trails / claimed-not-wired (3 items) — pre-existing epic, no stated urgency
`#1522` (the epic itself, PM-directed) · `#1735` · `#1678`.

### 8. Spatial-disposal (2 items) — pre-existing epic, no stated urgency
`#1698` (the epic itself, PM-ruled 08-15/16) · `#1700`.

### Singletons (6 items) — forcing these into groups would be taxonomy theater (Arch's framing)
`#1423` (silent-death pattern — genuinely its own epic-of-one) · `#1695` · `#1697` · `#1708` ·
`#1718` · `#1737`.

**Handling**: no group dependency to respect. Pick up opportunistically between epics, or fold
into whichever numbered epic above touches the same file if one turns out to overlap on
inspection — these were classified from titles, not full reads; PPM's own read of an individual
issue may reclassify it without changing the shape of the other 36.

---

## The falsifiability note, carried from Arch's memo (why this ordering is checkable, not asserted)

10 of 37 map directly to the un-modeled-noun audit's cousins; the acceptance-contract control case
arguably makes it 18. The rest group under four pre-existing cause-epics. **If a future factoring
pass finds the singletons refusing to shrink, or an epic's membership turning out wrong on a full
read, that's real information — update this file, don't defend the original grouping.**

## Change log
- 2026-09-09 (PPM): first version, built from Arch's factoring + dependency notes + CXO's
  copy-contract flag. 37 items, 8 epics + 6 singletons.
