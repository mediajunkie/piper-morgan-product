# PM Ideas Inbox

**Purpose**: a low-friction drop point for links, articles, and stray ideas PM wants reviewed "in case anything is useful for us." Append one entry whenever you save something — a URL and a few words is enough, no formatting required. CIO (or whoever orients from this file) checks it as part of routine session-start, the same way the carry-forward gets read.

**How this works**: new entries go under "New" as you add them. Whoever reviews an entry moves it to "Reviewed" with a one-line disposition (relevant / not relevant / filed as X / discussed on Y date) — the point isn't to delete anything, just to make it visible what's been looked at vs. not. Nothing here is urgent by default; PM sets the pace of when to discuss.

**Digestion cadence (PM, 2026-07-16)**: pick at least one item from "New" every time PM and CIO converse, and work through its relevance together — not a unilateral verdict, an actual discussion. Backlog is large (16 items as of the first batch); this is the mechanism for working it down without a dedicated big session.

---

## New (not yet reviewed / discussed)

*Batch import, 2026-07-16 — PM's saved-links backlog, first use of this file. Titles/notes below are PM's own where given; CIO added a one-line relevance tag only where the connection to current Piper Morgan work is immediate and confident — left blank where it needs PM's own read first.*

1. **Ethan Mollick on organizational theory for agentic AI** (spans of control, boundary objects, coupling) — https://www.linkedin.com/posts/emollick_i-think-agentic-ai-would-work-much-better-share-7426069086507499521-nbZ1/ — *PM: "not sure if I shared that already"*

2. **Anthropic's official `code-simplifier` plugin agent** — https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md — *PM: "also not sure if ever discussed"*

3. **"The Death of the AI Wrapper"** (Medium) — Amodei/Patil "world of atoms" moat argument, build-for-day-100 framing — https://medium.com/activated-thinker/the-death-of-the-ai-wrapper-anthropics-founders-reveal-the-ultimate-tech-moat-5a8e9aa374a3 — *PM: "back to Feb, may be starting too far back"*

4. **"Why LLMs Fail at Knowledge Graph Extraction"** (Towards AI) — entity disambiguation, asserted vs. augmented graphs — https://pub.towardsai.net/why-llms-fail-at-knowledge-graph-extraction-and-what-works-instead-dcb029f35f5b

5. **MELT memory-lifecycle benchmark** (ShisaD vs. Memobase, 217-case fixture) — https://www.linkedin.com/posts/randomfoo_while-building-the-memory-system-for-shisad-share-7482451245018918913--lei/ — includes the per-axis results table PM screenshotted (temporal/as-of recall is the weak axis for both systems)

6. **`closedtab` (npm)** — Agent Action Record tooling: structured intent/action/judgment/deviation/consequence/change records per agent run, reconcile-against-trace, private-fence redaction — https://www.npmjs.com/package/closedtab — *CIO tag: adjacent to our own session-log + sign-off discipline; worth a look for whether the reconcile-against-trace idea has anything we're missing.*

7. **Orchestrator-executor cost economics** (Laurie Voss / Arize) — cheap-executor-model architecture, cost-per-completed-task as the right metric — https://www.linkedin.com/posts/seldo_can-you-run-your-agents-at-half-the-cost-activity-7481494851620954112-8w_7/ — *CIO tag: directly relevant to the per-role model map (Opus/Sonnet split) — worth a read before the next model-assignment review.*

8. **"Frontier Labs, Enterprises, and the AI Value Chain"** (randomfoo/Shisa.AI, ~15K word brief) — who captures value as AI labs deploy into businesses — https://www.linkedin.com/posts/randomfoo_the-past-few-weeks-have-been-unusually-eventful-activity-7480641718409670656-ZyYf/ — includes the "Partners and rivals" table PM screenshotted

9. **"Why Your Mac LLM Just Died"** — KV cache as the unoptimized bottleneck on Apple Silicon, VeloxQuant-MLX compression library — https://medium.com/@rajveer.rathod1301/why-your-mac-llm-just-died-and-the-missing-piece-nobody-talks-about-240039733d6a — *PM: "may need to also discuss with Pard of Design in Product and Mediajunkie, who is working on my Mac Studio and local LLM infrastructure"*

10. **PM's own idea, not a link**: each of PM's agents should have a "home page" — a profile stating what they work on, which team, what types of work, accomplishments. *CIO tag: this may already be partially covered by the `ROLE-PORTFOLIO-{ROLE}.md` docs and `BRIEFING-ESSENTIAL-{ROLE}.md` files — worth checking whether PM means something more public-facing/visual than what exists, or whether the existing docs already do this and just need surfacing.*

11. **Open Knowledge Format (OKF)** — Google's June 2026 spec for portable agent knowledge bundles (markdown + frontmatter, `index.md`/`log.md` convention, progressive disclosure) — https://medium.com/@AkhilAIWorld/google-just-quietly-released-the-missing-piece-for-ai-agents-its-called-okf-7e96a33898ce — *PM: "relevant for Klatch, too."* *CIO tag: strikingly relevant to the CLAUDE.md refactor work in progress right now — the "what belongs in CLAUDE.md vs. skills vs. linked docs" question we're mid-scoping is close to exactly what OKF is trying to standardize. Worth a real read before Docs's Pass 2 lands.*

12. **"How to Fix the Security Flaw Built Into Every..."** — Shisa D framework, Ledger hardware-backed approval for high-stakes agent actions, "lethal trifecta" (data access + action + internet) — https://www.linkedin.com/posts/randomfoo_how-to-fix-the-security-flaw-built-into-every-activity-7480107129690025984-ywSx/

13. **Postman Passport** — credential-reference + secure proxy model so agents never touch real API keys — https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/

14. **"Claude Dreams, But It Doesn't Weather"** — memory-as-surface argument (architecture/weathering metaphor), Patina Protocol prototype — https://medium.com/@amber_m_bouabdallah/claude-dreams-but-it-doesnt-weather-f3eec692881c — *PM's own header: "weathering (lifecycle experience / mux)"*

15. **"What is AX Design?"** — Agentic Experience as a discipline distinct from UX; detective/enabler/builder role split — https://medium.com/design-bootcamp/what-is-ax-design-why-do-we-need-this-new-role-e21dff4dd541

16. **"Agent Harnesses"** — proposed standard bundling multiple Skills + shared references under one `HARNESS.md`, for agents that need many skills in tandem — https://medium.com/intuitively-and-exhaustively-explained/agent-harnesses-intuitively-and-exhaustively-explained-52aa6b4e7ebd

*PM's own note on this batch: "gonna stop there in case i'm overlapping with stuff we've processed in the past... we can take the time needed to discuss any of these items to the extent warranted... I can also go through the rest of the items for which I am unsure."*

---

## Reviewed

*(none yet)*
