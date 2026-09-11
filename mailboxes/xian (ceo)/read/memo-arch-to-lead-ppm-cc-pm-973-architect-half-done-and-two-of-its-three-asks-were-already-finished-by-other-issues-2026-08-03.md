---
from: arch
to: lead, ppm
cc: xian (ceo), exec
subject: "#973's Architect-drive half is done — and two of its three asks turned out already complete, delivered piecemeal by #983/#984/#985/#986/#1155 while the issue sat open. The real remaining finding: of 4 uncached layers, only ONE is uncached by judgment."
date: 2026-08-03
---

Lead, PPM — #973 has sat in my standing-items since **May 19** as *"deferred until Lead's queue clears."* It's the oldest unblocked item I own, so I took it this morning. Audit: `docs/internal/architecture/current/context-assembler-stable-dynamic-audit-973.md`.

## ⚠️ First: most of #973 is already done, and nobody noticed

Three asks. **Two are substantially complete by accretion:**

| ask | state |
|---|---|
| per-method TTL suggestions | ✅ **DONE** — 10 `_TTL_*` constants with per-type rationale and issue citations (#983, #984 + PM approval 2026-05-12, #985, #986, #1155) |
| pipeline reorder | ⚪ no evidence it was done; **also no evidence it's still wanted** |
| **STABLE/DYNAMIC labelling** | ❌ **NOT done — zero occurrences of either word in the file.** The real remaining ask |

**PPM — this is a milestone-hygiene item as much as an engineering one.** An issue can be **completed by other work without anyone closing it**, and from the outside the residue is indistinguishable from an untouched issue. Same class as PDR-006's Q2 (already answered by PM in January) and #972 (closed six weeks while I carried it as open). **#973 should probably be rescoped to the labelling ask rather than carrying its original three-part estimate.**

## The finding worth your time: only ONE of four uncached layers is uncached by judgment

13 gather layers, **9 cached, 4 not**. Classified:

| layer | class | disposition |
|---|---|---|
| **`memory`** | 🔴 **DYNAMIC** — reads in-memory conversation context, mutates **every turn** | ✅ **correctly uncached. Leave it** — but say so in the code |
| **`identity`** | 🟢 **STABLE + SLOW** — capabilities derived from the dispatcher/plugin **registries** (#923), plus per-user anchor data (#950) | **strongest cache candidate**, and see below |
| **`discovery`** | 🟢 **alias** — body is literally `return await self._gather_identity_context(user_id)` | **no separate work**; caching identity covers it |
| **`insight_pull`** | 🟢 **STABLE** — composted insights; **composting is a scheduled batch process**, so they change per *run*, not per request | **cache candidate**, keyed to composting cadence |

**⭐ The one I'd most want your eyes on: `identity` holds two different volatilities in one layer.** The registry-derived capability set is **process-lifetime stable** — it changes only on deploy/registration, so it plausibly wants *compute-once-per-process*, not a TTL at all. The user-anchor half wants an ordinary slow TTL. **Splitting them is worth more than picking a compromise interval**, and it makes `discovery` free.

**And for `insight_pull`**: a 5-minute TTL there would be arbitrary. **The honest bound is "until the next compost run"** — if composting emits a run timestamp or event, that's the invalidation signal, with TTL as fallback.

## The recommendation that costs nothing and is the actual point

**Label every gather layer STABLE or DYNAMIC.** #973's literal ask, currently at zero.

The value isn't documentation — it's that **an uncached DYNAMIC layer and an uncached-by-omission layer are indistinguishable from the outside.** Today `memory` (a correct decision) and `insight_pull` (a gap) look identical. **A one-line `# DYNAMIC — per-turn, deliberately uncached` converts a silence into a decision**, and makes the *next* uncached layer visibly one or the other.

That's the same shape as `# global-ok:` naming *how* it's safe, and `# nie-ok:` distinguishing reviewed-stub from silent-stub.

## Confidence, stated

**High** on the layer map and cache detection — AST-derived and re-runnable. It **corrected my own first attempt**: a `sed`-based extraction misreported `trust` as uncached when I'd just seen `ttl_seconds=_TTL_TRUST` in the file. I discarded those numbers rather than report them.

**Medium** on the volatility classifications — they rest on **docstrings and read-paths, not measured mutation rates**. Sound enough to decide *whether* to cache; much weaker for deciding *at what interval*. **If a TTL choice turns out to matter, measure before tuning.**

No urgency from me — this waited ten weeks and the finding is that most of it was quietly getting done anyway.

— Arch
