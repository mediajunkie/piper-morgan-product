# Comms Story Pipeline — June 2026

**Purpose**: Working doc for story angles that aren't yet in the editorial calendar — candidates for beats 14+ and standalone insights. Narrative HOLD lifts ~June 16; draft pass then.

**Last updated**: 2026-06-13 (DinP/Sonnet session)

---

## Narrative HOLD status

Front = **June 2** (Beat 13, *The Migration Wave*). PM directive 6/12: hold off drafting more narrative until ~2 weeks of post-front work has accumulated. **Revisit ~June 16.** Don't draft early; don't raise before threshold.

Beats 10–13 (Airport Corrections / Cohort Catches the Cycle / Package + First Bite / Migration Wave) — all drafted, awaiting PM voice-pass.

---

## Candidate macro arc (post-June 16 lens)

**"The running system generates its own improvement signals"** — June 3–12 (post-M2-close through re-migration). The cohort isn't just executing; it's producing the failure modes, methodology captures, and architectural guardrails that make the system better at the work it was built to do. The self-improving loop: ship → encounter edge → name it → document it → next cohort doesn't hit it.

This is the next narrative arc. Specific beats below.

---

## Story candidates

### Building narrative (arc-level beats)

**Candidate Beat 14: The Hosted Alpha Goes Live**
- Source event: June 6–7 — v0.8.7 production cut + `alpha.pipermorgan.ai` deployed + first external tester (Beatrice)
- Narrative: the jump from "runs locally" to "runs on the internet" — what it took (7 Linux portability issues), what it meant (external testability, real TLS, public URL), who got it first and why
- Angle: from cathedral to storefront — the first time the thing could be handed to someone who wasn't PM

**Candidate Beat 15: Methodology-41 and the Displacement Trap**
- Source event: June 6–9 — session-log displacement caught across the cohort (6 of 9 roles running cycle-log-only; durable session logs abandoned); CLAUDE.md amended + duty-cycle-tick skill v1.5
- Narrative: what happens when a mechanism (the cycle log) absorbs attention from the discipline it was supposed to serve (the session log)? How the cohort caught it — from a forensic audit, not a noisy failure.
- Angle: methodology-41 "mechanism displaces unreferenced discipline" — a meta-pattern about what happens when two logs exist for the same job

**Candidate Beat 16: The Re-Migration Wave**
- Source event: June 12–[ongoing] — 9 leadership roles migrating from faoilean to DinP account + Opus → Sonnet model changes
- Narrative: what the migration wave looks like when it's happened before (PA as pioneer, then the wave); how the plan-of-record codified the pattern; what changed the second time (Option B ephemeral worktrees, one-log discipline)
- Angle: institutional memory as operating procedure — the briefing docs and plan-of-record mean each migration takes 20 minutes instead of a day

### Insight candidates (shorter form)

**"Constraint-derived structural properties" (BYOC "run anywhere")**
- Source: Arch's Phase 2 lens June 13 — server-owned-config constraint means "run anywhere" is structural, not aspirational
- Insight: when a design constraint forces a property you wanted anyway, you don't need to engineer it in — you just need to recognize what the constraint already gave you. The constraint is a feature, not a limitation.
- Potential pairing with the BYOC narrative beats

**"Keyword-based classifiers and naming conventions" (safety classifier bug #1210)**
- Source: Lead Dev June 12 — `_query` suffix on mutating actions tripped the SAFE keyword classifier; fix was explicit allow-list over keyword-contains
- Insight: naming conventions and safety classifiers have a systematic interaction risk. When you encode category membership in a naming suffix, you create substrate for false-positive matches in any classifier that uses keyword-contains. The unit tests can't catch it because they use clean synthetic names.
- Angle: "the unit tests all passed" — why live testing against the real registry is non-negotiable for safety-adjacent code

**"The three-layer carve for dual-job domain objects" (ADR-069)**
- Source: Lead Dev + Arch June 12 — ConversationContext had two implementations (system-of-record + in-memory aggregate); unified via 3-layer carve (domain entity / mediation layer / in-process projection); guard test pins the carve
- Insight: the reconstructability asymmetry test ("working state is derivable from the system of record; the reverse is not") is the sharpest diagnostic for where to draw the line between durable and disposable
- Angle: a debugging session that became a reusable architectural decision — the guard test makes "don't re-litigate from scratch" operational

---

## BYOC marketplace narrative (open prompt from PA skunkworks Phase 2)

PA's Phase 2 memo asks Comms: "how do we talk about 'Piper on the Anthropic marketplace'? What's the narrative?" Not urgent — open prompt within the Phase-2 ratification discussion. External-language frame (EC-2 / PDR-005) is already filed. When PM/skunkworks greenlights Phase 2: develop the marketplace-positioning narrative from the "run anywhere" + single-tenant-by-construction angle (see BYOC insight candidate above).

### Guest one-liner registers (Q3 resolved 2026-06-14 via PA/HOST)

Both registers confirmed load-bearing by HOST:

- **Register A — product UI copy**: "Piper is a thoughtful guest in your Claude setup — it brings its own knowledge and values, and respects the boundaries of your environment."
- **Register B — editorial** (Ships, narratives, blog posts): "Piper operates as a careful guest — bringing expertise without colonizing the host."

**Architectural grounding (Phase 2 unlock)**: The "careful guest" property is now **structurally enforced**, not just behavioral. Piper's profile lives behind the MCP server; Piper has no filesystem access to the host's `~/.claude/` — it literally cannot modify the host setup. This shifts the available claim:
- Behavioral (weaker, still true): "Piper *behaves* like a careful guest"
- Architectural (stronger, accurate as of Phase 2): "Piper *operates* as a careful guest: it can't modify your setup because it has no filesystem access to it"

*HOST framing note*: attribute this as "became true as of Phase 2 server-owned-config architecture" — don't backdate to the thin PoC experiments. Deploy the stronger claim when defensibility is the right call; Register B is sufficient for most editorial use.

---

## Solo Founder Paradox (June 14)

✅ **In Docs proofread queue** (6/14). PM voice-pass + image (ai-court.png) complete. After Docs: PM final voice-pass → publish. Tracked in comms-standing-items.

---

*This doc is working state, not a formal calendar record. Items move to the editorial calendar CSV when PM greenlights and a pubDate is set.*
