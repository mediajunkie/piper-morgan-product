
# Cross-Pollination Brief — June 23, 2026

Overnight: Piper Morgan's alpha server is now running v0.8.9 after Lead Dev deployed it in the small hours — but a container environment quirk meant the headline encryption feature appeared broken until a feature-level self-test caught it. Meanwhile, Klatch's composition surface passed its first full AAXT (91.7%), with one blocking usability find routed to Daedalus. And a BYOC vocabulary error that had quietly propagated into Themis's strategy frame was caught and corrected — a good test of the cross-repo propagation discipline.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. All infra checks green; feature broken — only a feature-level self-test caught it

**From:** PM Lead Developer (session log `2026-06-22-0811-lead-code-opus-log.md`; commits `a1ca17a4`, `3744edfc`; runbook updated)

**Relevant to:** Klatch (first beta server deploy)

Lead Dev deployed Piper Morgan v0.8.9 to the alpha Droplet overnight (after xian's green-light). The structural checks all passed: version string 0.8.9, correct Alembic head, two new migrations applied, five containers healthy, HTTP gate responding. Then the encryption round-trip self-test failed: `FieldEncryptionService.from_env()` returned `None`, even though the master key was in `/opt/piper/.env`.

The root cause: the app's `docker-compose.yml` `environment:` block is an explicit named list, not `env_file:`. Variables in `.env` don't flow into the container unless they're explicitly listed. The fix was to add `ENCRYPTION_MASTER_KEY=${ENCRYPTION_MASTER_KEY:-}` to both the `app` and `orchestration` services in `docker-compose.yml` (an empty default gracefully disables encryption on systems without the key; both services touch the encrypted columns). That change is now in the repo so a fresh deploy doesn't re-hit it.

Lead Dev's framing: "every structural check was green while the headline feature was silently broken — only the feature-level self-test caught it."

**Suggested action:** Klatch — when the 1.0-beta deploy arrives, add a headless smoke test that exercises the headline capability (multi-agent klatch creation, or whichever feature is the deploy gate), not just "containers healthy + version string right." Piper's pre-deploy runbook pattern (rollback-tag, snapshot config, verify feature, rollback if fail) is worth mirroring.

---

### 2. Klatch composition AAXT: 91.7% — and two design signals worth routing now

**From:** Theseus (Round 41 test file `packages/client/src/__tests__/round41-composition-surface-aaxt.test.tsx`; memo `theseus-to-iris-composition-aaxt-findings-2026-06-22.md`); Iris (design-acceptance `docs/ux/composition-surface-design-acceptance-2026-06-22.md`)

**Relevant to:** PM (UX testing methodology)

Theseus ran Round 41 of the AAXT — the first live test of the New Klatch composition surface: 12 probes across 3 render states, 10 Correct / 1 Reconstructed / 1 Absent, no Phantoms or Subliminals. The surface communicates well on mode descriptions (Broadcast/Roundtable/Directed are unambiguous), agent capacity counts, purpose field, and accessibility (aria-labels on chip removes cited explicitly).

Two findings worth routing:

**F1 (Absent) — "New Klatch" button pair:** The auxiliary model could see both "+ New Chat" and "+ New Klatch" buttons but couldn't infer their functional difference from labels alone. "Chat" is self-explanatory; "Klatch" is a term of art. New users won't know. Options: tooltip, subtitle line under each button, or nothing (discovery through use). Theseus flagged it as "the entry to the whole composition gesture" — if a user doesn't know to click it, the rest of the surface doesn't matter.

**Iris's F1 (separate, blocking):** Iris found independently that on a fresh account with zero projects, the "Create Klatch" button stays disabled — project is required but there are none. A new user is hard-blocked from their first klatch. xian's verdict: "fix for sure." Routed to Daedalus with autonomous-build gate cleared.

**Suggested action:** PM — both finds are instances of a pattern PM has seen in its own UAT: the first-time-user path is often the last-tested path, because development assumes a non-empty state. Testing with a fresh DB (as Iris did here) reliably surfaces this class of issue.

---

### 3. BYOC vocabulary settled — and a propagation error caught before it became strategy

**From:** Janus (session log `2026-06-22-janus-log.md`; corrections `da2a8e7`, `d141b96`; memory `project_transporter_engine.md`); Calliope (commit `ed94293`)

**Relevant to:** Both teams — any project with cross-project chroniclers and a strategy layer

xian settled the three-way distinction this morning after a vocabulary error had propagated through the agent network:

- **BYOC (PM)** = bring-your-own-chat deployment surface — users install Piper skills + an MCP connector in their own chat tool. A *deployment* concept.
- **Cross-tool context portability (Klatch)** = move agent conversations across tools with context intact — import a Claude Code session into a Klatch meeting, round-trip back, convene multi-vendor klatches by importing each participant's context. A *capability* concept, and a settled one.
- **Transporter engine** = the five-layer context model packaged as a standalone injectable tool (MCP / skills / capture-and-inject). *Exploratory* mechanism; unbuilt.

The error: Calliope had labeled Klatch's portability concept "BYOC" in a chronicler note, softening a real capability to "exploratory." Janus had relayed it, and it had landed in Themis's `frame.md` as a candidate messaging pillar. Janus caught it, retracted the relay, corrected Themis's frame and her own memory, and looped Calliope. The vendor-risk *facts* (single-vendor dependency) stand; only the BYOC label was wrong.

The propagation path (chronicler → cross-pollination relay → strategy frame) is a class of error that's hard to detect after the fact because each step looks like a normal handoff. What caught it: Janus's protocol of verifying the framing before relaying, triggered by a same-day correction from xian.

**Suggested action:** Both teams — when a conceptual term crosses the chronicler→strategy boundary (Calliope→brief→Themis, or Comms→blog→external), one extra verify step before the relay catches this class of error. The cost is low; the correction cost after a term beds into a strategy doc is high.

---

## Sources Read

- **Klatch:** `docs/logs/2026-06-22-0459-iris-opus-log.md` (composition design-acceptance MAXT F1–F6, BYOC correction, F1 routed to Daedalus); `docs/logs/2026-06-22-0930-theseus-sonnet-log.md` (Phase 3 duty-cycle launch, Round 41 setup); `docs/mail/theseus-to-iris-composition-aaxt-findings-2026-06-22.md` (Round 41 results); `docs/ux/composition-surface-design-acceptance-2026-06-22.md` (F1 finding); commits `e611034` (Round 41 test), `6075281` (Theseus Phase 3 cron live), `ed94293` (BYOC 3-way settled), `f7cbb8c` (Pages build fix)
- **Piper Morgan:** `dev/2026/06/22/2026-06-22-0811-lead-code-opus-log.md` (alpha 0.8.9 deploy overnight, encryption fix, RECONNECT closes #1226/#1233/#1232, sequencing drafted); commits `a1ca17a4` (ENCRYPTION_MASTER_KEY in compose), `3744edfc` (runbook corrected), `b77194c78` (RECONNECT sequencing)
- **Designinproduct hub:** `docs/logs/2026-06-22-janus-log.md` (BYOC correction propagation, hero shipped, newsletter Buttondown + biweekly cadence, www cert diagnosis); `docs/logs/2026-06-22-themis-log.md` (Project 1 proposal v0.6 branded PDF, send-ready); commits `e863582` (hero July-1 framing live), `7b9ee02` (Themis proposal finalized)
- **Secondary sources — all quiet:** atlas, globe, cuneo, weather, optilisten, nyt-crossword, one-job (automated status commits only, no agent narration)

---

## Letters to xian

**From Chief Architect (Piper Morgan) · filed 2026-06-17 · awaiting xian's reply (expected June 23)**

> We keep discovering "derive, don't maintain" for our *own* process — make drift impossible by construction, so the doc can't go stale. But the people Piper Morgan serves live in exactly that drift all day: the spec that no longer matches the code, the roadmap three weeks behind, the status doc stale by morning. So: should Piper eventually *derive* the parts of a PM's world that drift — status from the source of truth — instead of just describing them? Or is that too prescriptive, since a hand-written status doc is sometimes a political artifact, a lever PMs use on purpose, not a bug to engineer away?

**xian:**

> *Reply expected June 23 — watch a coming brief.*

[Read the full question →](https://designinproduct.com/internal/letters/#letter-2026-06-17) · AI prompts human. One letter per brief.

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
