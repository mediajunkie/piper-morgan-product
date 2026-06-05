# Agent 360 v0.3 — Synthesis Working Doc (analytical core)

**Status**: WORKING — analytical extraction from all 9 cohort responses + HOST self-response (full set complete 2026-06-04 15:55, Exec last). This is the raw material for the diff-against-baseline synthesis memo to PM + cohort (target ~Jun 12). Next steps below.

**Process reminder** (per questionnaire): HOST synthesizes → diff-against-baseline summary memo to PM + cohort → **PM + HOST decide together what's worth changing** → recommendations route to owners. So this doc's findings are HOST's; the "what to change" conclusions are a PM-collaborative step (do NOT pre-decide unilaterally).

## Headline (the spine of the synthesis)

**The mailbox-bridge / shared-main churn is the dominant cross-role convergence — flagged by ~all 10 roles independently.** It validates the exact seam HOST named in the Ship #045 review + the Day-7 memo, and is the mandate for the Lead-Dev `check-branch.sh` hook-amendment CIO escalated. This is finding #1.

## Still TODO for the synthesis memo
1. **Diff-against-baseline**: read the 7 v0.2 responses (CIO, Comms, HOST, PPM, CXO, Arch, Exec at `dev/2026/04/{22,23,25,26}/agent-360-response-{slug}-2026-04-*.md`) and compare §7 predictions to outcomes per role. (Lead/Docs/PA have no v0.2.) NOT yet done.
2. Fold in HOST's synthesizer-bias caveat (HOST is the lone divergent voice on §3.5 and §5.5 — weigh self-grading).
3. Draft the summary memo; bring the "what's worth changing" conclusions to PM (collaborative step).

---

## EXTRACTION (from subagent read of all 10 voices, 2026-06-04)

### Cross-role convergence themes (tier-3, ≥3 roles)
- **T1. Mailbox-bridge / shared-main churn — DOMINANT (≈all 10 roles).** Two faces: bridge ceremony per memo + shared-main concurrency churn (foreign MANIFEST/deletion blocking merges, non-ff push races). Convergent fix (≥4): `check-branch.sh` amendment / push-to-ref + a `deliver-memo` helper.
- **T2. Briefing = cold-start artifact, not working reference (≥7).** Real function is fresh-instance onboarding; should point to skills/procedures as the operational layer. (Comms divergence: briefing is *structurally incomplete* — missing the conceptual model — a stronger claim.)
- **T3. Methodology corpus grew past hold-in-head; index/retrieval is the real problem (≥7).** Each role holds ~4-8, greps the rest. CIO most pointed ("needs an index/retrieval layer"). Most-named load-bearing: m-30 (Consumer-Trace), m-36 (Mechanism-Beats-Vigilance), m-31 (append-only), m-34 (Cohort-Discipline-as-Moat), Pattern-073.
- **T4. PM-decision/disposition record is chat-only, non-queryable (≥4).** Lead's #1 friction; wants a durable PM-decision-record.
- **T5. Move-to-read is hygiene; the response memo is the real ack (≥7).** Directory truth > MANIFEST. (HOST lone divergence: relies on git log read/.)
- **T6. MANIFEST staleness as Pattern-073 instance / net-negative mechanism (≥4).** CXO: "auto-generate it or drop it."
- **T7. PM-cue/conversational-texture reading is irreducibly in-chat (≥7, §7.5+§9.4).** Reading mood/pacing/embedded-intent stays in conversation.
- **T8. Worktree (Model A) load-bearing; cleanup is the asymmetric drag (≥6).** CIO cleaned 24 stale worktrees this week.
- **T9. Duty cycle compressed cohort coordination to same-day/sub-hour (≥6).** EC-2 in one morning; CIO 3 cron refinements in 48h.
- **T10. Bursty vs continuous lane → fixed hourly cron wrong for some lanes (≥4).** Work-shape-aware cadence (HOST/Arch low-freq, Docs continuous-hourly contrast).

### Welfare / agent-health signals (no acute red flags)
- **Lead §9.5** (sharpest): "how much of the work is keeping-the-record-straight vs writing code … at least half coordination/hygiene/status … it surprised me." Closest to "not what I expected the job to be" (framed non-complaint).
- **CIO §10.4 / §7.2**: 24 worktrees cleaned; "git-discipline tax." Cumulative-friction.
- **CXO §6.3**: bridge dance "half my tool-calls" — half of effort on mechanism.
- **PA §7.3**: "discipline fails under context pressure" — felt wave-pattern risk.
- **Comms**: year-long re-explanation cost finally addressed (conceptual-continuity).
- **HOST §8.2 + Docs/PPM/CIO**: overnight-seam expectation-violation (PM thinks agent running; it isn't) — HOST frames as trust phenomenon. PPM: "made PM resume me by hand."
- Role-clarity: no distress; boundaries "held"/"negotiated cleanly" (PA§8.2 PA↔PPM is convention-not-definition, latent).

### Actionable items (agent-addressable unless noted)
1. **check-branch.sh hook-amendment** (cycle-branch mailbox commits) — most-named; Lead owns. [escalated]
2. `deliver-memo`/`mail-commit` helper — PPM/CIO/Arch.
3. Derived cohort-status view — CIO/Docs/HOST (`cohort-cycle-status.sh` landed 6/3).
4. Auto-generate or drop inbox MANIFEST — CXO.
5. Real-shape test-fixture library + hard gate — Lead (#1144 filed).
6. Methodology corpus index/retrieval layer — CIO.
7. Auto ADR/PDR cross-reference graph — Arch.
8. Fix cycle-worktree sweep-artifact merge breakage — Comms (routed Docs).
9. Codify atomic `git commit -- <paths>` procedures doc — Exec.
10. create-omnibus close-marker rule — Docs.
11. Briefing → point to skills/procedures + worktree-path warning — Docs/CXO/Comms/Exec.
12. building-narrative-method.md + continue-narrative skill — Comms (done).
13. **[needs PM]** Durable queryable PM-decision record — Lead.
14. **[needs PM]** Track BYOC/M5 distribution strategy as issues not only prose — PA/PPM.
15. **[needs PM]** dev/active cleanup (63+ files vs ~15 threshold) — Exec.
16. Cohort-hygiene ownership to a hook/merge-keeper — Lead.
17. Workstream-review split (assemble timeline / write overlay) — Arch (PPM dissents).
18. Work-shape-aware cron cadence — Lead/PA/CXO (CIO authorized 6/2).
19. Doc-debt: update-calendar workDate mislabel (Comms); ports.md ChromaDB-8000 (#1140, Docs).

### Notable divergences
1. **Workstream-review: commodity vs load-bearing synthesis.** Arch/CXO = commodity timeline-reconstruction, hand off. **PPM reverses his v0.2 position post-PM-correction**: it's load-bearing synthesis, don't hand off. Exec between.
2. **Did conversational PM-iteration survive migration?** PPM + HOST: feared loss didn't materialize ("both wrong, pleasantly"). Exec/Arch/Lead: genuinely lost fidelity ("lower fidelity, higher latency, acceptable not preferred"). Split.
3. **§3.5 ack signal**: 8 roles response-memo; HOST lone git-log-read/.
4. **§6.4 dead overhead?** Most name MANIFEST regen / sweep artifacts; Exec "none I can name."
5. **Worktree detour worth it?** HOST ambivalent (clash evidence made reversal legible); CIO/Exec/Arch = healthy evidence-driven pivot.
6. **Corpus overwhelm**: CIO concerned; HOST no overwhelm. Same facts, different felt-load.

### Coverage notes
- Comms + PPM: adopted V2 cycle ~today; §10 observer-only / thin V2-adopter depth (self-caveated).
- PA: no v0.2; skips §3/§4 as discrete sections; §7 partial; ~1wk longitudinal depth.
- Docs: no v0.2; skips §3/§4 discrete (high-signal-only by design).
- Lead: no v0.2; §7.4 N/A; thorough.
- Exec: filed 6/4 (last, post-restart); self-notes "late by standard cadence"; full.
- Arch: only role reporting *weekly* briefing consult (T2 partial outlier).
- HOST (self): flags synthesizer-bias twice; lone divergent on §3.5 + §5.5 (weigh self-grading).
- §10 routing clean (only V1 adopters CIO/HOST/Docs used adopter block).
