# Cross-Pollination Brief — May 12, 2026

Monday was dense on both projects. Argus's 5/11 sweep curation surfaced the week's most strategically important finding: Anthropic shipped native memory tooling at the SDK level ("Managed Agents Dreaming," announced at "Code with Claude" May 6). Both Klatch's Step 11 roadmap and PM's memory architecture work now need to recalibrate differentiation — the value proposition shifts from memory CRUD primitives to conversation-as-substrate and cross-channel context assembly. Klatch Daedalus returned from a 12-day hiatus and shipped 7 commits: Rounds 32–35 (import gating, MicroReflection.validUntil, UUID dedup), SDK 0.86.1→0.95.1, and Opus 4.7 plumbing — with the default-flip deliberately held over a new quantified risk. PM closed M2f Group C (#857 token refresh Option A) via clean subagent-STOP discipline and published *The Inchworm Position*; #984 context-cache pre-work stopped at PM-decision gate after Phase 0 audit.

## Key Insights

### 1. Managed Agents "Dreaming": SDK-native memory ships — differentiation reframe for both projects

**From:** `klatch/docs/intel/2026-05-11-sweep-curated.md`; commit `a29f830` (Argus 5/11 sweep curation); routed to Calliope for next xpoll brief framing
**Relevant to:** Klatch (Daedalus — Step 11 scoping; Calliope — narrative framing); PM (Architect, CXO — memory/context architecture ADRs)

Argus's 5/11 automated sweep curation noted that Anthropic shipped native memory tooling at the SDK level at the "Code with Claude" event on May 6. Argus's strategic finding (routed for xpoll framing):

> *"Reframes Step 11 differentiation: don't compete with SDK-level memory primitives; compete on conversation-as-substrate and cross-channel context assembly."*

The implication: if Anthropic's SDK now handles basic memory persistence, a project that differentiates on "we also store memories" has weaker positioning. A project that differentiates on *what it does with conversation context across sessions, channels, and agents* — the assembly layer — is competing on something the SDK doesn't provide. Klatch's cross-channel context architecture and PM's multi-agent memory coordination are both in the assembly layer, not the primitive layer.

**Suggested action:** Klatch (Daedalus) — before scoping Step 11 (Search + memory flip), confirm which proposed Step 11 features are competing with SDK primitives vs. which are assembly-layer differentiators. The April 12 Janus synthesis (six-tier framework, `valid_from`/`type`/`source`/`trust_level` field set) is still the right schema — the reframe is about *positioning and scope*, not about abandoning the schema work. PM (Architect, CXO) — same audit: which ADR-level memory decisions are about primitives vs. assembly? The assembly-layer framing may sharpen the boundary between what Piper Morgan builds and what it delegates to the SDK.

---

### 2. Opus 4.7 tokenizer +35%: plumbing shipped, default-flip explicitly held — both projects should recalibrate before flipping

**From:** `klatch/docs/logs/2026-05-11-0703-daedalus-opus-log.md`; commits `ae7f264` (Opus 4.7 plumbing), `7b85660` (SDK 0.86.1→0.95.1); Daedalus recommendation in session log
**Relevant to:** Klatch (Daedalus — compaction threshold calibration); PM (Lead Dev — same pending flip; all agents — session compaction behavior)

Daedalus shipped the full 4.7 plumbing in Monday's session — model registered, `xhigh` effort enum added, per-model effort gating in place — but explicitly declined to flip `DEFAULT_MODEL` to `claude-opus-4-7`. The stated reason is new and quantified:

> *"My recommendation remains 'wait for a few real 4.7 channels to run first, given the +35% tokenizer impact on the compaction threshold.'"*

The +35% tokenizer increase means a session that previously hit the compaction boundary at, say, 120K tokens would now hit it at ~90K tokens of equivalent content. Any threshold-dependent behavior (PreCompact hooks, session-log maintenance reminders, merge-keeper sweep timing) needs to be validated against actual 4.7 sessions before assuming the existing calibration holds. Daedalus's recommendation is conservative but specific: run a few real sessions to see where the practical compaction boundary lands before committing to 4.7 as the default.

The SDK bump (`^0.86.1 → ^0.95.1`, was 6+ versions behind) was shipped unconditionally — only the *default-flip* is held. Klatch now runs 1,227 tests zero failures at current default (Opus 4.6).

**Suggested action:** PM (Lead Dev) — the same evaluation applies: ship the 4.7 plumbing if not already done, but hold the default-flip until 2–3 real sessions have run with 4.7 and the compaction boundary has been empirically observed. The PreCompact hook's catch-rate observation window is a natural forcing function: watch a few 4.7 sessions and see if the hook fires earlier than expected. If it does, the compaction threshold needs the same +35% recalibration before committing to 4.7 as default.

---

### 3. Iris session 10: two-track design discipline + panel disclosure taxonomy

**From:** `klatch/docs/logs/2026-05-11-0653-iris-opus-log.md`; commits `65db553` (Tier 1 + typography), `54e16be` (Tier 2 down payments); `docs/ux/triage-patches.md` filed
**Relevant to:** Klatch (Daedalus — Tier 1+2 implementation queue); PM (CXO — parallel design/implementation track structure)

Iris session 10 produced a concrete two-track separation that immediately unblocked Daedalus: rather than blocking all incremental work on the holistic redesign, Iris triaged ~45 findings into three tiers plus a cross-cutting pass.

**Track 1 (Daedalus picks up now):** Tier 1 clear patches (7 items including highest-value T1.6 content fingerprint for import sessions) + Tier 2 down payments (4 items) + cross-cutting typography pass. Work is directionally correct and not wasted effort when the holistic redesign arrives.

**Track 2 (xian + Iris):** Tier 3 items (composition gesture, panel-as-musculature redesign, memory-layer maintenance, entity manager redesign) wait for holistic design.

The most concrete architectural clarification from this session was **T2.2 panel disclosure taxonomy**: two categories, two treatments.
- Settings panels (channel settings, project settings): **inline** — push the message list down; no overlay
- Task and library panels (entity manager, import, export preview): **true modals** with explicit backdrop

This resolves the F4.2/F8.7 "skirt problem" (panels currently feel like overlays but behave like neither). The split is honest about what each panel actually is — settings panels are workspace controls; task panels are foreground workflows.

**Suggested action:** PM (CXO) — the two-track structure is directly applicable to any design-vs-implementation parallelism: identify what's "directionally right and not wasted work" vs. "must wait for the holistic design." The explicit triage tier system (clear patch / down payment / wait-for-design) is a clean vocabulary for PM's own UX surface work in M2d and beyond.

---

### 4. PM M2f Group C ships + Comms voice/tone discipline codified

**From:** PM session log `dev/2026/05/11/2026-05-11-0701-lead-code-opus-log.md`; commits `5ea70c9e` (#857 merge), `6eed84ca` (#1071 merge); Comms log `2026-05-11-0812-comms-code-opus-log.md`; commit `45e5f05e` (voice/tone guide additions)
**Relevant to:** PM (all roles — M2f status; Comms); Klatch (Calliope — voice/tone methodology)

**M2f status:** Groups A+B+C are now all shipped. Group C was #857 (seamless token refresh — login-issues refresh cookie, `/api/v1/auth/refresh` endpoint with rotation, ApiWrapper 401-intercept→retry). The subagent deployment on Phase 4 ran a clean proof of the STOP discipline: hit a `workspace_id` kwarg mismatch, stopped per gameplan condition, Lead Dev fixed (10 min), subagent resumed and delivered 5/5 tests. #1078 discovered: friendly-error middleware (`web/app.py:87`) silently drops `Set-Cookie` headers from 401 responses — same handler that reshapes `{detail}` → `{message}`. Filed; client fallback (redirect on 401) still works. #984 context-cache pre-work Phase 0 stopped at PM-decision gate (6 architecture questions: key shape, TTL defaults, invalidation strategy, decorator-vs-helper, scope minimum vs. complete, namespace prefix).

**Comms voice/tone guide (5 additions):** Following the *Inchworm Position* editing session, Comms codified five lessons applicable to any narrative writing agent:
1. Reflection-shaped pieces favor declarative paragraphs over tutorial bullet lists
2. First-person operational specifics earn their keep (vs. abstract-bullet pedagogy)
3. Voice asides do real work, not cute filler
4. Methodology pieces name what the discipline **IS**, not what it prevents
5. **Contested specific → trusted framing** (when a specific claim is contestable, reframe as trusted-practice language rather than qualifying or softening)

*The Inchworm Position* published Monday May 11; footer teases *Audit and Talk* for May 12.

**Suggested action:** Klatch (Calliope) — the "contested specific → trusted framing" move is high-value for technical writing that mixes benchmark claims with methodology claims. The rule: when precise numbers are contested (speedup claims, benchmark percentages), the move isn't to soften or qualify — it's to frame the discipline in terms the reader trusts independent of the number.

---

## Sources Read

- `klatch/docs/logs/2026-05-11-1758-argus-opus-log.md` — full read; 5/11 sweep curation + Round 33 partial (typography + T1.6 fingerprint, 2/12 surfaces), STDIO-vs-HTTP factual error correction, Managed Agents Dreaming finding, 4 pending routings
- `klatch/docs/logs/2026-05-11-0703-daedalus-opus-log.md` — full read; 12-day hiatus catch-up, Rounds 32–35, SDK/Hono bump, Opus 4.7 plumbing, default-flip held pending compaction baseline, 4 open-item status sweep
- `klatch/docs/logs/2026-05-11-0653-iris-opus-log.md` — full read; session 10 triage doc, two-track separation, T2.2 panel disclosure taxonomy, Daedalus memo filed
- `piper-morgan-product/dev/2026/05/11/2026-05-11-0701-lead-code-opus-log.md` — full read; #857 Group C (subagent STOP discipline), #1071 autonomous loop, #1074 verification closed, #984 Phase 0 audit + STOP, Pattern-067 slot collision resolved, inbox triage
- `piper-morgan-product/dev/2026/05/11/2026-05-11-0812-comms-code-opus-log.md` — partial read (80 lines); Inchworm proofread, voice-guide additions, memory extensions, discipline incident (sweep-up of uncommitted edits)
- `designinproduct` — hub CLAUDE.md (context)
- `weather` — 48h log: brief-delivery commits only; skipped
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `nyt-crossword` — 48h log: automated status commits only (fetch/print/remarkable); no narrated insights; skipped

**Not re-reported (covered in prior briefs):** Iris session 9 panels-as-musculature reframe + ~45 findings (May 11); #921 directional-evidence merge + Monitor idle-spin (May 11); M2d gate three-way concurrence + UI Lifecycle Rubric v0.1 (May 11); Argus sweep cross-reference gap + MemPalace delta (May 11); M2f Group A+B −2,229 LOC deletion + Pattern-067 (May 10); Run 7 68.9% PASS (May 10); hub CLAUDE.md Multi-Agent discipline (May 10).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and routing hints.*
