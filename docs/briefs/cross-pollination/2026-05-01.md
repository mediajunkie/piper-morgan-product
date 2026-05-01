
# Cross-Pollination Brief — May 1, 2026

PM's ethics enforcement went live on April 30 (CEO directive): `ENABLE_ETHICS_ENFORCEMENT=true` merged to production, closing #992 after the full Phase A → F arc. The final unlock was naming an alpha catch-22 — the "wait for real-traffic calibration" posture was unreachable from a pre-release product, so PM directed a simulation-first reframe instead of an indefinite hold. On the Klatch side, Iris returned after a two-week gap, settled three UX questions on transport-fidelity loss, then received xian's testing observations: the biggest gap is a missing capability, not a polish issue — there is no UI path for the central act of composing a klatch from existing entities.

## Key Insights

### 1. Phase F activated: ENABLE_ETHICS_ENFORCEMENT=true live — alpha catch-22 named and resolved

**From:** PM `dev/2026/04/30/2026-04-30-0632-lead-code-opus-log.md`; commits `deecc816` (Phase F merge), `62bb9c64` (flip-now memo); Architect ADR-061 v1.0 commit
**Relevant to:** Klatch (any future safety/trust layer; calibration-before-shipping design question)

`ENABLE_ETHICS_ENFORCEMENT=true` is now live in PM's docker-compose `app` service. #992 ETHICS-ACTIVATE is closed, completing the full Phase A → B → C → D → E → #1002/#1003 → #1004 → Phase F arc.

The final unlock: PM named the **alpha catch-22**. The April 28 AUTHORIZE-WHEN-OBSERVED posture ("wait ~7–14 days for calibration data") required real production traffic. PM is pre-release. The wait was for data that doesn't exist yet. PM directed: flip now, reframe calibration as simulation-first in three phases — **Phase A**: synthetic input population via Gemma generator (ships with flip, grounded in run-2 probe set: 18/20 PASS, 112/112 ethics suite); **Phase B**: beta-traffic refinement post-onboarding; **Phase C**: stable. Architect's calibration-enhancement design simplifies as a result — both layers run with flag on from the start; no on/off log-only mode needed.

ADR-061 v1.0 is architecturally complete: Architect folded all 6 review findings (three-way detector discriminator `literal-trigger | semantic | none`; `fast_path_hit` + `cache_hit` in audit data; latency claim replaced with measured numbers p_min 2.1s / p_avg 3.2s / p_max 4.9s). Awaiting PM formal ratification.

Lead Dev's self-flag, added as permanent memory: "When 'where does this data come from?' = 'real users' AND we are in alpha, surface that immediately rather than treating the wait as a normal sequencing step."

**Suggested action:** Klatch — the alpha catch-22 is a project-stage constraint, not a failure mode. If Daedalus designs a safety feature that requires real-traffic calibration before shipping, ask at design time: "Is there a path to the real traffic this gate needs?" If not, simulation-first (build a synthetic input population using existing probe methodology) is the viable alternative. Name the dependency early.

---

### 2. Klatch Iris session 6: composition gap named as capability gap; transport-fidelity UX settled

**From:** Klatch `docs/logs/2026-04-28-0639-iris-opus-log.md`; commit `a0d760a`
**Relevant to:** PM (multi-entity/agent assembly UX design; first-class import/export flow patterns)

Iris returned April 28 after a two-week gap (52 commits in). Three UX questions on transport-fidelity loss settled with xian:

1. **Fidelity-loss panel at transport-selection**: YES — visibility-gap principle applied to the export moment; system knows what's about to be lost before the user decides
2. **Transport-aware Phase 3.5 defaults**: YES — smart defaults: claude.ai default-on (bridge exists, silent loss without it); canonical zip default-off (no loss to bridge)
3. **Structural L4 loss in claude.ai round-trip**: honest declaration at export time; reject folding L4 into L2/L3 with provenance markers ("sounds clever but obscures actual loss")

xian's three testing findings:

1. **Import is buried** in the footer grab-bag alongside theme toggle — it's a first-class verb of the product, not a settings-adjacent action
2. **Import-as-modal is wrong** — should be full-screen; import/export work IS the work, not an interruption to chat
3. **No UI for composing a klatch from existing entities** — biggest gap; capability gap not polish gap. The central job-to-be-done has no path through the UI.

The third finding confirms the entity reframe from the user side (filed by Calliope April 18): when entities are existing conversations promoted into roles, composition IS the central act — and the current UI doesn't surface it. A combined 8-topic list (Iris's 5 + xian's 3, deduped) is assembled; walkthrough session with xian is pending.

**Suggested action:** PM — Klatch's entity-as-promoted-conversation finding applies to any multi-agent or multi-model assembly UX. The design question is: is the central act **creation** (design a creation flow) or **promotion and composition** (design a selection + assignment surface)? Klatch found that the entire composition gesture was missing because it wasn't treated as the primary surface. If PM ever designs a "bring agents or context into a room" interaction, the Klatch experience is a direct precedent for what falls through the gap when this isn't explicitly designed.

---

### 3. "The Floor Comes Alive" published; Ship #041 IAC arc framing proposed

**From:** PM `docs/public/comms/drafts/published/the-floor-comes-alive.md`; PM editorial calendar commits `fd35e06`, `17d94db`; `mailboxes/comms/inbox/memo-exec-to-comms-cc-cohort-ceo-iac-retrospective-fold-ship-041-2026-04-30.md`
**Relevant to:** Klatch Calliope (building narrative series methodology; talk-to-implementation arc as a story shape)

Third Building Piper Morgan narrative installment published on Medium April 30. It covers April 8-10: the first Colleague Test pass (5/9 → 7/9 in two days). The sharpest line: three characters in a model identifier string changed the experience from "a wall of canned text" to "an actual working conversation." The post names what a gate is for — not to prove the system works, but to prove specifically, measurably, repeatably how it doesn't.

Also April 30: Exec proposes Comms weave the April 17 IAC conference talk ("Ethics as Information Architecture," Philadelphia) into the Ship #041 narrative. The case: the April 24-30 week's work (#1004 shipping, ADR-061 v0.1, Phase F decision arc, CT v2.3 Branch-or-Anchor) made the talk's claims operational in code. Ship #040 didn't surface the talk-to-implementation relationship; #041 has the better vantage because the arc is now closed.

**Suggested action:** Klatch Calliope — two patterns worth tracking. First: the "three chars" narrative is a version of Klatch's own configuration-gap stories — those are the most shareable moments because they make an invisible failure visible. Second: the talk-to-implementation arc pattern is a specific narrative shape: articulate a design principle publicly → implement it → write the piece once the implementation arc is complete (not before). The arc only works from the closed-end vantage. Klatch has natural candidates (the five-layer architecture as a pub-talk pitch vs. as a live system; the entity reframe; the round-trip story). The ship is the precondition for writing the piece.

---

## Sources Read

- `piper-morgan-product/dev/2026/04/30/2026-04-30-0632-lead-code-opus-log.md` — full read; Phase F activation, alpha catch-22 named, ADR-061 v1.0 architectural completion, #1018 Phase 1 ratified, IoC scan clean
- PM commits `deecc816` (Phase F merge), `62bb9c64` (flip-now memo), `fcdfb8e0` (IoC scan), `aa0748e` (ADR-061 v1.0 Arch commit) — stat/message read
- `piper-morgan-product/docs/public/comms/drafts/published/the-floor-comes-alive.md` — full read
- `piper-morgan-product/mailboxes/comms/inbox/memo-exec-to-comms-cc-cohort-ceo-iac-retrospective-fold-ship-041-2026-04-30.md` — partial read; IAC retrospective + Ship #041 framing
- `klatch/docs/logs/2026-04-28-0639-iris-opus-log.md` — full read; Session 6 catch-up, UX questions settled, xian's three testing findings, composition gap, combined topic list
- Klatch commit `a0d760a` (Iris session 6) — stat/message read
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `weather`, `nyt-crossword` — 48h logs non-empty (brief delivery + automated status prints only); no narrated insights

**Not re-reported (covered in prior briefs):** verify-before-assuming methodology (Apr 30); Pattern-064 Extension Without Integration (Apr 30); branch-discipline synthesis v1.0 (Apr 30); /import/klatch bidirectional 1203 tests (Apr 29); deliver-mail b1 + merge-keeper-sweep (Apr 29); ADR-061 completeness gaps filed (Apr 29); #1004 112/112 PASS (Apr 28); first live MCP stdio 27/27 (Apr 28).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
