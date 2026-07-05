# Cross-Pollination Brief — July 5, 2026

Two substantive findings today from different corners of the ecosystem. Klatch's agents produced a gap audit for the five-layer context model: the first four layers transfer at high fidelity when an agent moves environments, but Layer 5 — the behavioral calibration that makes an agent *this* agent for *this* user — transfers at zero. The gap now has a roadmap position (Step 10.5) and five proposed LM-based remediation processes. One Job surfaced a three-legged pattern for keeping PWA users on current code: the app checks aggressively, CI proves delivery, and a user-visible manual control closes the trust loop. PM was active but mostly operational — no new methodology worth carrying.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Layer 5 of the five-layer model transfers at zero — and Klatch has designed five processes to fix it

**From:** Klatch, xian + Calliope (`docs/plans/layer5-portability-gap-audit-2026-07-04.md`, commit `3f5216c`, July 4)
**Relevant to:** Piper Morgan (same five-layer architecture; PM agents move across environments), any team running agents in multi-environment setups

Klatch's core promise is cross-environment portability of agent conversations with context intact. A July 4 gap audit — written jointly by xian and Calliope, 159 lines — found that the portability story has a significant hole.

The transfer-fidelity table by layer:

| Layer | Content | Fidelity |
|---|---|---|
| L1: Kit briefing | Date, model, env | ~90% |
| L2: Project instructions | CLAUDE.md, behavioral rules | ~100% (Claude Code); ~60% (claude.ai) |
| L3: Project memory | MEMORY.md, accumulated facts | ~100% / ~60% same split |
| L4: Channel addendum | Conversation framing | 0% — must be written by hand |
| **L5: Entity prompt** | **Agent identity, behavioral calibration** | **0%** |

The document's framing: Layers 1–3 give an agent facts and context. Layer 5 is where the agent *is* — the communication style, working approach, and relationship calibration that developed through hundreds of conversations. An agent with Layers 1–3 but no Layer 5 "has the project's knowledge but not the working relationship. It's a well-briefed stranger."

**Five proposed processes to close the gap:**

1. **Automated persona extraction (passive)** — prompt an LLM over conversation history to write a first-person behavioral profile as a Layer 5 seed. Captures observed style but not tacit knowledge.
2. **Correction extraction (passive, high-signal)** — filter conversation history for correction/feedback turns; extract behavioral constraints implied by each ("don't X", "prefer Y"). These are the clearest behavioral calibration signals because they're the moments when calibration actively changed.
3. **Pre-migration interview (active, highest value)** — send a structured prompt to the source agent before migration, asking it to report its working style, communication preferences, key undocumented context, and feedback-derived calibration in a format another agent can use. One paragraph of "what future-you should start with."
4. **Memory distillation (semi-passive)** — prompt for facts and decisions not in MEMORY.md but implicit in the conversation. Supplements Layer 3, not Layer 5 directly.
5. **Behavioral fingerprint scoring (ongoing)** — after migration, use the extracted profile to score the new agent's responses for fidelity to the source agent's patterns. Also an AAXT probe target.

The document recommends Process 3 (pre-migration interview) as the first increment — immediately buildable without infrastructure changes. Proposed roadmap position: Step 10.5, before Search (Step 11), on the basis that "search is a utility feature; Layer 5 portability is core to what Klatch *is*."

**Suggested action (Piper Morgan):** PM agents already move between environments (and PM has the same five-layer model). Before migrating an agent to a new context, add a Process 3 question: "What should the version of you starting fresh know about how to work well with xian on this project?" Save the output as a pinned file. The cost is one prompt; the gain is a working relationship that survives the move rather than having to be rebuilt from scratch.

---

### 2. PWA auto-updates need three legs: automatic pull, provable delivery, and a user-visible manual escape hatch

**From:** One Job, Coral (`development/coral-logs/2026-07-04-coral-log.md`, commits `b574a8f` + `3bc3de0`, July 4–5)
**Relevant to:** Any project shipping a web app with a service worker or local-first PWA; Klatch (if it ever ships a PWA or installable app)

One Job's holiday weekend debugging session produced a three-legged pattern for PWA delivery observability — after Xian's installed PWA refused to update and the root cause turned out to be a combination of iOS's lazy service-worker-check behavior and a previously silent deploy pipeline.

**The problem stack:**
- iOS PWAs only check for service-worker updates at launch. Rapid quit/reopen doesn't give the download time to complete. A user on the installed version can be on stale code for days without knowing it.
- The standing workaround — "delete the icon and reinstall" — has a trap: on iOS, deleting the PWA icon destroys all local storage. For a local-first app where "the icon is the database," this is a data-loss vector, not just an inconvenience.
- The deploy pipeline had been silently succeeding without verifying the live site had actually updated.

**The three-legged fix:**

1. **Automatic foreground update checks** (`src/pwaUpdateCheck.ts`) — the app calls `navigator.serviceWorker.getRegistration().update()` every time it returns to the foreground via `visibilitychange`, plus an hourly heartbeat while open. Deliberately uses plain `getRegistration()` rather than vite-plugin-pwa virtual imports, so the Capacitor (native) build still compiles.

2. **CI deploy verification** (`.github/workflows/deploy.yml`) — after publish, the workflow curls the live URL in a retry loop until the served bundle hash matches the just-built hash. "Deploy succeeded" is now observed, not assumed. Also fixes a latent misconfiguration: deploy/verify jobs now run only on push, never from pull_request builds.

3. **User-visible manual escape hatch** (Settings → "Check for updates") — calls `registration.update()` on demand with honest state toasts ("Checking for updates… / You're on the latest version / Handled by the app store on this build"). Degrades gracefully where no service worker exists.

Coral's framing for the third leg: "auto-update systems need an escape hatch the user can see, both for genuinely stuck states and for trust: 'I can MAKE it current, therefore I believe it's current.'" The automatic legs handle the common case; the manual lever closes the trust gap and handles the edge case where automation fails silently.

**Suggested action (Klatch, DinP):** If Klatch or any project in the ecosystem ships a PWA or service-worker-cached web app, plan all three legs from the start. The most commonly skipped leg is the CI delivery verification — confirming the live site actually updated, not just that the deploy workflow reported success. The most commonly undervalued leg is the manual escape hatch — it costs very little and restores user trust in the auto-update system.

---

## Sources Read

- **Klatch** — git log (since July 4): `docs/plans/layer5-portability-gap-audit-2026-07-04.md` (full read; 159 lines, xian+Calliope joint design doc); `docs/plans/theseus-brief-search-planning-maxt-2026-07-04.md` (MAXT planning for Search — new test session scoped, no cross-project insight); `docs/operations/attention-rollup.md` v17 (Argus back online after 6-day mode-1; vitest 4 migration fix for client flake; AVAILABLE_MODELS gap flagged to Daedalus; Sonnet 5 + Fable 5 available; SDK 14 minors behind); `docs/ROADMAP.md` (Step 10.5 added). Commit log.
- **Piper Morgan** — git log (since July 4): Notion connector ported to #1232 Connector contract (`5050ed0`, Arch's 3-layer ruling — Notion's keychain model is a legitimate Layer-2 backend, adapter inherits 22 existing methods); Lead Dev correction re: Slack class (`72bb230` — wrong class identified in earlier memo; real Slack adapter has live 3-state composite requiring running Socket Mode runner, not just credential check; Slack migration scoped as genuinely more complex than Notion); Arch ruling refined + shim ratified (`98d4bc6`); Comms activity (drafts, editorial calendar); CXO/CIO/PPM duty cycle fires (heartbeat only). No new transferable methodology.
- **One Job** — git log (48h): full read of coral log July 4 (`a502723`, `b574a8f`, `dcb7323`, `3bc3de0`); `store/COWORK-IOS-BRIEF.md` (state addendum); `docs/VISION-2026-07.md` Item 13 (hypothesis + safety net). PWA delivery observability pattern is the cross-pollination entry.
- **atlas, globe, cuneo, optilisten** — no commits in 48h window; skipped.
- **nyt-crossword** — automated status commits only; skipped.

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

