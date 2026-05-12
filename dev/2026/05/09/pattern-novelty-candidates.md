# Pattern Novelty Candidates — Phase 2C

**Built**: 2026-05-09
**Sweep**: Pattern Sweep #1025 (March 17 → April 28, 2026 window)
**Phase**: Phase 2C of Pattern Sweep 2.0 — Novelty Detection
**Author**: Novelty Detector sub-agent under CIO orchestration
**Reference**: `dev/active/pattern-library-index.md` (Phase 1, 65 indexed patterns)

This file enumerates candidate phenomena that may have genuinely emerged during the window and applies the FALSE POSITIVE TEST to each: *for any candidate flagged TRUE EMERGENCE, the closest existing patterns must have been examined and rejected as not-the-same.*

Per framework hypothesis, expected TRUE EMERGENCE per 6-week window is 0–2 candidates.

---

## 1. TRUE EMERGENCE candidates

### TE-1: Stacked Silent Failures (diagnostic pattern)

**Provisional name**: Stacked Silent Failures
**Origin instance**: CIO Apr 10 weekly memo, `dev/2026/04/11/memo-cio-to-exec-weekly-2026-04-10.md` §1 ("The Three-Layer Root Cause — A New Diagnostic Pattern"); explicitly named by CIO with deliberate intent to add to catalog. Subsequently referenced in `dev/2026/04/17/methodology-audit-2026-04-17.md` §"New diagnostic pattern identified", in CIO Chat→Code handoff `dev/2026/04/23/handoff-cio-chat-to-code-2026-04-23.md` (cited as a canonical-vocabulary watch term alongside "indoor plumbing"), and in Apr 14 omnibus session learnings ("Same diagnostic pattern as the 'Stacked Silent Failures' the CIO named last week"). M1 audit pattern catalog disposition memo lists it as an outstanding S-tier item.

**Diagnostic question**: After fixing the apparent root cause, does the symptom *actually change*? If a multi-round investigation keeps failing with the same composite symptom, are you peeling stacked layers where each layer's failure was masking the next?

**Signature**:
- Multi-round investigation where each fix reveals the next layer
- Each individual failure is itself silent (looks intentional, returns plausible default, etc.)
- Composite behavior appears as a single problem
- Diagnostic principle: *"if the fix doesn't change the symptom, the diagnosis was wrong"* (CIO formulation)
- Reference instance: M1 gate Apr 3–9 — deprecated model ID (silent 404) → undifferentiated fallback template (masks failure mode) → missing `response` field in `ConversationTurn` (one-sided context assembly)

**Verification trail (FALSE POSITIVE TEST)**:

| Nearest neighbor | Distinct because |
|---|---|
| Pattern-045 (Green Tests, Red User) | CIO explicitly distinguishes: P-045 *tells you tests are inadequate*; Stacked Silent Failures *tells you why diagnosis takes multiple rounds*. P-045 is about test/reality gap; this is about layered failure-masking during root-cause analysis. |
| Pattern-041 (Systematic Fix Planning) | P-041 is about planning fixes for *related* issues at the planning layer (plan-then-fix). Stacked Silent Failures is about *unrelated co-occurring* failures discovered during diagnosis where each masks the other's symptoms. |
| Pattern-042 (Investigation-Only Protocol) | P-042 is methodology discipline (don't fix during investigation). Stacked Silent Failures is the diagnostic *shape* that motivates needing the discipline; orthogonal. |
| Pattern-043 (Defense-in-Depth Prevention) | P-043 is *prevention* across multiple layers (canonical source, briefing, enforcement, audit). Stacked Silent Failures is *diagnosis* across multiple layers post-incident. Different time direction. |
| Pattern-060 (Cascade Investigation) | P-060: after fixing a bug, look for *adjacent related* bugs that share root cause. Stacked Silent Failures: a *single* user-visible symptom that requires layer-by-layer peeling, not breadth-first scan for relatives. P-060 is post-fix; Stacked is pre-fix. |
| Pattern-062 (Assembly Assumption) | P-062: components individually correct, integration fails. Stacked Silent Failures: components individually *wrong* (each broken), but each broken-ness is silent so they accumulate. P-062 about integration gap; Stacked about *masking* of independent layer failures. |

None of the near-neighbors describe the specific shape: multi-layer *independent* failures where each layer's silent mode masks the next. Pattern-045 is conceptually closest but CIO's authoring explicitly carved out the distinction. The principle "if the fix doesn't change the symptom, the diagnosis was wrong" is novel to this candidate and appears nowhere else in the catalog.

**5-tier classification**: **TRUE EMERGENCE**.

**Rationale**: New name coined by CIO with explicit "worth naming" intent; new diagnostic principle; reference instance is the M1 gate failure (a load-bearing operational moment); subsequently invoked as canonical vocabulary by successor CIO; never matched any existing pattern's signature. Three independent later citations (Apr 14 omnibus session learning, Apr 17 M1 audit, Apr 23 handoff watch-list) demonstrate the term is operating in working vocabulary, not just one-time naming.

**Recommendation**: **File as Emerging in next pattern catalog cycle**. CIO has authoring authority. Suggested filename: `pattern-066-stacked-silent-failures.md`. Suggested category: Investigation & Root Cause. Sibling-relate to Pattern-045 (the explicit distinction is structural to the pattern's identity) and Pattern-060 (both about layered investigation, distinct directions).

---

## 2. NEAR-MISSES (anti-amnesia signal — discipline working)

These initially looked novel but the FALSE POSITIVE TEST identified them as evolutions or applications of existing patterns. They are noted explicitly so future sweeps don't re-rediscover them.

### NM-1: Pattern-063 (Parallel-Authoring Drift) — filed Apr 27

**Why it might look novel**: Filed during the window with new vocabulary ("branch-or-anchor", "rubric drift", "C-axis reconciliation"). Methodology-24 (Branch-or-Anchor Discipline) lands the same week. Could appear to be a TRUE EMERGENCE candidate from this sweep.

**Why it's not TRUE EMERGENCE for this sweep**: Already in canonical library at row 63 of the Phase 1 index. Filed Emerging Apr 27 by CIO; promoted to Proven May 8 with full evidence trail. Per task instructions: *"Pattern-063… filed during the window… are now Proven. They are PATTERN EVOLUTION of Pattern-062."* Mention here as PATTERN EVOLUTION (vocabulary-layer manifestation of Pattern-062's component-layer assembly assumption). **Already canonical; no further action.**

### NM-2: Pattern-064 (Extension Without Integration) — filed Apr 28

**Why it might look novel**: Apr 28 ADR-061 + Pattern-064 land together; "alive scaffolding" architectural-debt class named; sibling sub-pattern of Pattern-062 explicitly. Note: Mar 19 omnibus referenced "Extension Without Integration" as Pattern-063 *under that pre-renumbering*; the canonical Pattern-064 (Apr 25 sketch → Apr 28 formalization) is the eventual catalog entry.

**Why it's not TRUE EMERGENCE for this sweep**: Already in canonical library at row 64. PATTERN EVOLUTION (extension-layer manifestation of Pattern-062). **Already canonical; no further action.**

### NM-3: Pattern-065 (Continuity Memo Before the Seam) — filed Apr 27

**Why it might look novel**: Three-project convergence (Piper Docs Apr 13 "externalize before the seam, not at it"; OpenLaws coffee-spill handoff; Klatch Phase 3.5 prompt). Six-section structure validated through 7 cohort migrations Apr 22–26. PP-002 emerged via this pattern's Section 6 candor mechanism.

**Why it's not TRUE EMERGENCE for this sweep**: Already in canonical library at row 65. Filed Emerging Apr 27, promoted Proven May 8. PATTERN EVOLUTION-adjacent (relates to Pattern-021 Development Session Management and Pattern-029 Multi-Agent Coordination, but distinct enough to stand alone as own pattern). **Already canonical; no further action.**

### NM-4: "Alive scaffolding" architectural-debt class

**Why it might look novel**: Named Apr 27 by Architect after observing across 4 lens-review batches. Referenced as candidate Pattern-catalog entry in Architect session log + codebase-review-batch-4-findings. Methodologically distinctive ("designed + coded + tested + exported, but never instantiated or never the load-bearing path").

**Why it's NOT TRUE EMERGENCE this sweep**: Pattern-064 (Extension Without Integration), filed Apr 28, was authored *explicitly* to canonicalize the alive-scaffolding observation. Architect Apr 28 session log: *"Adjacent manifestations enumerated (phantom imports, alive scaffolding cluster)"* in Pattern-064's documentation. Alive scaffolding is therefore PATTERN USAGE / sibling-instance of Pattern-064, not a separate candidate. The architectural-debt class name persists as operational vocabulary inside Pattern-064. **Subsumed; already canonical via 064.**

### NM-5: PP-002 Load-Bearing vs. Commodity Work in a Role

**Why it might look novel**: HOST 360 v0.2 cohort synthesis Apr 27 named PP-002 as a tier-3 finding. Cross-role manifestation table covers 9 roles. Named "third-degree value" of the Agent 360 instrument by PM Apr 27. Filed in `PROTO-PATTERNS.md` as active proto-pattern with explicit elevation criteria.

**FALSE POSITIVE TEST against existing patterns**:
- Pattern-045 (Green Tests, Red User): PP-002 author cites explicit relation — "commodity work *passing* doesn't mean role is *succeeding*" — at the role-allocation layer.
- Pattern-062 (Assembly Assumption): PP-002 author cites — "load-bearing/commodity is a Pattern-062 manifestation at the role-allocation layer."

**Why it's NOT TRUE EMERGENCE this sweep**: PP-002 is *explicitly logged as a proto-pattern* awaiting elevation evidence (one full sprint of post-migration operation; Lead Dev + Docs distinctions to validate). Per the proto-pattern process documented in `PROTO-PATTERNS.md`, this is the canonical PP-N waiting room for novelty candidates. Treating it as TRUE EMERGENCE here would short-circuit the elevation process the project has explicitly defined. Classification: **PATTERN EVOLUTION (role-allocation-layer manifestation of Pattern-062)** + **active proto-pattern under standard elevation review**. Should be re-evaluated at the next pattern sweep with one-sprint-post-migration evidence as the framework prescribes.

### NM-6: "Externalize before the seam, not at it" (Apr 13)

**Why it might look novel**: Phrasing first appeared in Docs Apr 13 session learning ("Docs named context pressure on day 15 and wrote the carry-forward proactively, not reactively"). PA cross-pollination brief Apr 14 independently named the same pattern from OpenLaws' continuity memo experience.

**Why it's not TRUE EMERGENCE**: This is Pattern-065 (Continuity Memo Before the Seam) before formalization. Apr 13 is precisely one of the three-project convergence instances cited in Pattern-065's documentation. **Subsumed by Pattern-065.**

### NM-7: "Three-layer bugs need three-layer investigation" (Apr 14 omnibus)

**Why it might look novel**: Distinct framing by Docs Apr 14 omnibus author about blog-duplication bug.

**Why it's not TRUE EMERGENCE**: Same omnibus learning cites explicitly — *"Same diagnostic pattern as the 'Stacked Silent Failures' the CIO named last week."* Subsumed by TE-1 above (this is the second instance that supports TE-1's promotion case). Treat this as PATTERN USAGE supporting evidence for TE-1, not a separate candidate.

### NM-8: "Singleton → pair → many" framing (Apr 23)

**Why it might look novel**: PM coined Apr 23 during three-migrations-in-48-hours observation. Methodology-level epistemology framing.

**Why it's not TRUE EMERGENCE**: Foundational research-methodology framing (one data point, two = hypothesis, three = testable pattern) — not a project-specific operational pattern. It's a *research norm* the project applies, not a recurring failure mode being detected. Belongs in operational vocabulary, not pattern catalog. (Also closely related to Pattern-038 Temporal Clustering at the meta-pattern layer.) **Operational vocabulary; no pattern entry warranted.**

---

## 3. OPERATIONAL VOCABULARY worth watching

Terms that surfaced during the window that have not yet risen to pattern candidacy but should be tracked for future sweeps. These are pre-canonical operational vocabulary; recurring use in working memos signals possible pattern emergence.

| Term | First-instance origin | Notes |
|---|---|---|
| **"Alpha catch-22"** | PM Apr/May (Phase F context — referenced in Apr 28 PPM Phase F memo recommendation v5 catch-22 reframe) | Reframing of the alpha-vs-build-quality testing tension. Recurs in #1004 Phase F decision discussion. Watch list. |
| **"From Diagnosis to Discipline in 24 Hours"** | (Likely a Ship #040 / methodology-codification framing — cited in working materials) | Description of the methodology-compounding rate observed Apr 27 (PP-002 → Pattern-063 → Methodology-24/25 → CT v2.3 in 24 hours). Watch list. |
| **"Decreasing review-volume signal"** | Exec Apr 26 §6 + omnibus Session Learning #1 ("Decreasing review volume across migrations is the right outcome, not concerning") | Methodology indicator that pattern stabilization, not laxity, is occurring. Repeated framing across HOST → Exec migration cohort. Could codify as a methodology indicator. Watch list. |
| **"Spark vs holder"** | (Comms vocabulary; surfaces in narrative work re: who originates an insight vs who carries it forward) | Observed in Comms voice work; relates to attribution discipline. Pre-canonical. Watch list. |
| **"Load-bearing vs commodity"** | HOST 360 v0.2 cohort synthesis Apr 27; promoted to PROTO-PATTERNS as PP-002 | Now formalized as proto-pattern; vocabulary in active circulation across briefings. Move tracking from this list to PP-002. |
| **"Methodology-to-runtime latency"** / **"Methodology-to-automation latency"** | Apr 28 omnibus Core Theme #1 ("Methodology-to-automation latency is now hours, not days") | New unit of measurement for the project — the time between a methodology landing (norm/discipline) and operational automation closing the loop. Could codify as a velocity metric or observability concept. Watch list. |
| **"Discipline-failure recovery"** | Apr 26 mail-discipline emergency norm landing | Pattern of fast hook-enforced norm landing within hours of discipline failure (e.g., `check-branch.sh` after the mail-on-feature-branch cascade). Sibling concept to "methodology-to-automation latency"; specifically about *recovery* not steady-state compounding. Watch list. |
| **"Captain last off the ship"** | Exec Apr 26 final Chat session sign-off | Migration-cohort role discipline (last role to migrate gets meta-observation privilege). Specific to migration wave; unlikely to recur unless new cohort migrations happen. Catalog as historical methodology vocabulary. |
| **"Audit the composition"** | CIO Apr 16 Flywheel reformulation (5th practice formalization of Pattern-062) | Now canonical methodology-00 vocabulary. Move from watch list to canonical methodology vocabulary. |
| **"Branch-or-anchor"** | CIO Apr 27 Methodology-24 | Now canonical (methodology-24-BRANCH-OR-ANCHOR.md). Move from watch list to canonical. |
| **"Commit-before-handoff"** | HOST migration Finding A (Apr 22) | Migration-cohort discipline. Encoded into sign-off discipline norm Apr 28 + check-branch.sh hook. Now canonical CLAUDE.md vocabulary. |
| **"Reception-first reading"** | Pattern-065 doc + cohort migration practice | Now canonical via Pattern-065. |
| **"Third-degree value"** | PM Apr 27 Agent 360 v0.2 framing in PP-002 | Methodology meta-insight (an instrument designed for purpose A gains purpose B and now purpose C). Watch list — single-use so far. |

---

## 4. Promotion-worthy items (Emerging → Proven candidates)

Pattern-063, Pattern-064, Pattern-065 — all already promoted on May 8, 2026 (per task brief instructions). **Excluded from this section.**

Reviewing the remaining Emerging-status patterns from the Phase 1 index for trial-application evidence accumulated during the window (Mar 17 – Apr 28):

| Pattern | Status (per index) | Window evidence | Promotion recommendation |
|---|---|---|---|
| **035 — MCP Adapter Methods** | Emerging | No new in-window evidence surfaced via omnibus session learnings or session logs sampled. ADR-038/ADR-052 work largely pre-window. | **No change**. Remains Emerging; needs broader-adoption trial-application instances to promote. |
| **039 — Feature Prioritization Scorecard** | Emerging (template artifact issue noted in Phase 1) | No in-window scorecard application evidence surfaced. | **No change**. Template-cleanup ticket already noted in Phase 1 index footnotes. |
| **055 — Multi-Intent Decomposition** | Emerging (proven in #NNN) | Grammar-application cluster work largely pre-window (Jan 21). | **No change in this sweep**. |
| **056 — Consciousness Attribute Layering** | Emerging | Some Apr 16 ethics-voice guidance work referenced consciousness-as-architecture framing (omnibus Apr 16 §"ethics denial voice guidance"). Single in-window instance only. | **No change in this sweep**. Continue monitoring. |
| **057 — Grammar-Driven Classification** | Emerging | Floor-inversion arc completed Mar–Apr (Apr 13 omnibus: "floor inversion trilogy"). MUX/grammar-classification work in production. | **Candidate for promotion review** — but trial-application evidence is largely from inversion remediation, which is a sub-feature application rather than independent confirmation. Suggest CIO assess whether the inversion arc constitutes proven trial application. **HANDOFF TO PHASE 2D Evolution Tracker.** |
| **058 — Ownership Graph Navigation** | Emerging | No in-window evidence surfaced. | **No change in this sweep**. |
| **059 — Leadership Caucus** | Emerging | No in-window caucus instances surfaced. The Apr 22–26 migration cohort *could* be re-framed as a kind of caucus, but it's structurally different (sequential migrations, not synchronous alignment). | **No change in this sweep**. |
| **060 — Cascade Investigation** | Emerging (per index) — though file may say Proven | M1 audit dispositions referenced cascade investigation discipline. | **HANDOFF TO PHASE 2D Evolution Tracker** for cross-checking actual file status vs index. |

**Bottom line on Section 4**: One soft promotion candidate (Pattern-057, on the strength of floor-inversion-trilogy completion); one index-vs-file consistency check (Pattern-060). Both flagged for Phase 2D Evolution Tracker rather than asserted here.

---

## 5. Items to bring to CIO directly before finalizing

None of the candidates in Sections 1–4 are suspicious enough to require CIO sanity-check before this report finalizes. **TE-1 (Stacked Silent Failures)** is the only TRUE EMERGENCE finding, and the FALSE POSITIVE TEST trail is documented above. Standard Phase 2D handoff to Evolution Tracker should suffice. The recommendation to file TE-1 as Pattern-066 Emerging is within CIO's standard self-approval authority per `methodology-audit-policy-updates-2026-03-16.md`.

If anything in this report would benefit from CIO direct-attention before finalizing, it would be the **Pattern-057 promotion question** — whether the floor-inversion-trilogy work constitutes "trial application" in the proper sense, or whether it's the same author's own work and therefore doesn't validate broader-adoption. That's a judgment call CIO is best-placed to make.

---

## Sources

- `dev/active/pattern-library-index.md` (Phase 1 reference catalog)
- `docs/omnibus-logs/2026-03-{17..31}-omnibus-log.md` and `2026-04-{01..28}-omnibus-log.md` — Session Learnings sections
- `dev/2026/04/11/memo-cio-to-exec-weekly-2026-04-10.md` — origin instance for TE-1 (Stacked Silent Failures)
- `dev/2026/04/17/methodology-audit-2026-04-17.md` — second-instance citation for TE-1
- `dev/2026/04/23/handoff-cio-chat-to-code-2026-04-23.md` — third-instance citation for TE-1
- `docs/internal/architecture/current/patterns/PROTO-PATTERNS.md` — PP-002 Load-Bearing vs. Commodity entry
- `docs/internal/architecture/current/patterns/pattern-{063,064,065}-*.md` — already-canonical PATTERN EVOLUTION entries (NM-1, NM-2, NM-3)
- `dev/2026/04/27/codebase-review-batch-4-findings-2026-04-27.md` — alive-scaffolding origin (NM-4)
- `dev/2026/04/27/2026-04-27-0815-arch-opus-log.md` — Architect alive-scaffolding observations
- `docs/internal/development/methodology-core/methodology-23-M1-INNOVATIONS.md` — M1-era methodology innovations (cross-checked)

---

*End of Phase 2C Novelty Detection report.*
