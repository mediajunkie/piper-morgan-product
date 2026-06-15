# Stale-pattern triage — the 9 from Pattern Sweep Phase 2D (CIO, 2026-06-06)

**Standing-items #12a.** Pattern Sweep (2026-05-09) flagged 9 patterns as "truly-stale" needing disposition (verify / refresh / retire / redirect). This is the **triage recommendation** — a read-only status pass over all 9. **It recommends; it does not promote.** Formal promotion requires verifying each cited instance still holds (the don't-mark-proven-without-verifying-the-instance discipline) — that's the next step, routable to a subagent verification pass, Docs, or the next pattern sweep.

**Headline finding**: the catalog **systematically under-states maturity.** 6 of 9 are filed `Emerging` but their own body cites a specific `Proven in #NNN` instance that was never formally promoted. The "staleness" is mostly *unpromoted-proven*, not *abandoned*. One (#029) is the opposite — `Experimental` for a capability (multi-agent coordination) that is now **live cohort-wide**, so it badly under-states reality.

---

## Disposition recommendation

| # | Pattern | Filed status | Signal | Recommended disposition |
|---|---|---|---|---|
| 029 | Multi-Agent Coordination | Experimental ("scripts exist, deployment pending") | **Most stale.** Multi-agent coordination is now the *live 11-agent duty cycle* — "deployment pending" is false. | **REFRESH → Proven** (rewrite to reflect the deployed cohort duty cycle; strong candidate, the in-the-wild proof is the whole current system) |
| 030 | Plugin Interface | Experimental ("vision, partially implemented in GitHub integration") | Partial implementation; vintage status line | **VERIFY** current implementation state → likely REFRESH (is the plugin interface now fully implemented? if yes, promote) |
| 035 | MCP Adapter Methods | Emerging — "Proven in GitHub integration"; Active (Sprint A4); created Oct 19 2025 | Cites a proven instance + ADR-013 Phase 2 | **VERIFY → PROMOTE** to Proven (instance cited; confirm it holds) |
| 039 | Feature Prioritization Scorecard | Emerging ("ready for use, needs validation"); Nov 20 2025 | **The one genuine retire/redirect candidate** — a scorecard *tool* that "needs validation" and has no cited usage in ~6 months | **VERIFY USAGE** → if never used, RETIRE or REDIRECT (don't leave a never-validated tool as Emerging indefinitely) |
| 055 | Multi-Intent Decomposition | Emerging — "Proven in #595" | Cited instance | **VERIFY → PROMOTE** |
| 056 | Consciousness Attribute Layering | Emerging — "Proven in #434" | Cited instance | **VERIFY → PROMOTE** |
| 057 | Grammar-Driven Classification | Emerging — "Proven in #433" | Cited instance | **VERIFY → PROMOTE** |
| 058 | Ownership Graph Navigation | Emerging — "Proven in #435" | Cited instance | **VERIFY → PROMOTE** |
| 060 | Cascade Investigation | Emerging — "Proven in #745, #771" | **Two** cited instances | **VERIFY → PROMOTE** (strongest promotion case — 2 instances) |

## Summary

- **6 promote-candidates** (035, 055, 056, 057, 058, 060): Emerging-with-cited-instance → verify the #NNN instance, then promote to Proven. The catalog is lagging reality.
- **2 refresh-candidates** (029, 030): Experimental but the capability has since shipped → rewrite to current state, likely promote.
- **1 retire/redirect-candidate** (039): a "needs-validation" tool with no cited usage → verify whether it was ever used; retire or redirect if not.
- **Zero true abandonments** — none of the 9 is dead weight to delete; the issue is stale *status fields*, not dead patterns. (This itself is a small methodology data point: our "stale" patterns are mostly *under-promoted*, suggesting the promotion step is the weak link in the catalog lifecycle — adjacent to the corpus-coherence finding #12c and a natural candidate for the methodology-dream-cycle's drift pass.)

## Next step (NOT done here)

Instance-verification for the 6 promote-candidates + the 039 usage-check. Cheapest path: a subagent verification pass (read each cited #NNN, confirm the pattern's claim holds) → then a batch promotion commit. Routable to the next pattern sweep, Docs, or a dedicated CIO fire. **#12a advanced from "untriaged" → "triaged, verification queued."**

— CIO, 2026-06-06 (Fire 8, v0.6.3 idle-advance of committed backlog)
