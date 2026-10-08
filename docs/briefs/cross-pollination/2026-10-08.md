
# Cross-Pollination Brief — October 8, 2026

Piper Morgan's Architect issued a ruling about how "armed turns" (stateful pending-offers waiting for user input) should handle the router's output classes. A required live probe then overturned the ruling: the class labeled CLARIFY fires not only when a user is genuinely unclear, but also when the router encounters a command it has no matching operation for — two opposite situations that look identical at the output boundary. One key insight from this window.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A live probe of the served model caught an architectural ruling error that reasoning from ADR principles alone missed — Piper Morgan, Arch + Lead Dev, commits `19276a70b` · correction `0ece35153`

**From:** Piper Morgan, Architect and Lead Developer  
**Relevant to:** Klatch, and any team building routing logic that branches off an LLM classifier's output classes

PM has a stateful "armed turn" mechanism: when a user interaction puts the system in a pending state waiting for a specific answer (a project name, a confirmation), the next turn is routed differently — the system looks for an answer to the pending question. The question is how to handle each of the router's output classes on that armed turn:

- The router returns an operation name (e.g. `manage_portfolio` with confidence ≥ 0.8) → release: the user gave a new command, not an answer
- The router returns `NONE` (no recognizable command) → bind: the user answered the pending question
- The router returns `CLARIFY` (uncertain classification) → ???

Arch's ruling: CLARIFY = "user is unclear about their answer" → bind as the answer, create the project.

Lead Dev ran a 10-call live probe of the served model (PM's own router, 10 sample phrasings, ~$0.03). Result 9/10 correct — but "delete my project Klatch" drew CLARIFY, not a high-confidence `manage_portfolio`. The reason: the router has no `delete-project` operation in its catalog; when it can't classify a command, it returns CLARIFY as a routing failure output, not as an expression of user uncertainty. Under Arch's ruling, "delete my project Klatch" would have created a project named "delete my project Klatch."

Correction: only NONE binds as an answer. CLARIFY and below-threshold outputs confirm (ask the user to clarify) instead of binding. Arch's own post-mortem: "I grouped CLARIFY ('unsure') with NONE ('not a command'), misapplying my own ADR-080 D4 in the ruling meant to enforce it... I ruled from a mental model of the router's outputs, not its measured behaviour."

The mechanism that caught it: **Rule 8**, a recently added process requirement that a live probe of the served model is required before landing any change that routes off classifier output classes. This was its first required use. It caught the error.

The transferable principle: LLM classifier output class labels describe their training-time semantics — "CLARIFY" means "the model is uncertain how to classify this." In deployment, the same class can fire for structurally different reasons: genuine user ambiguity *and* commands that fall outside the classifier's trained scope. Routing decisions that treat all instances of a class identically (CLARIFY = bind) can be correct for one trigger and catastrophically wrong for the other. The only way to verify which inputs actually produce each class in the served model is to probe it directly.

**Suggested action for Klatch:** If any entity routing or context-layer dispatch uses an LLM classifier's output classes to decide "is this an answer to a pending question or a new command?", probe what out-of-scope inputs produce in the classifier before launching. CLARIFY in particular has been shown to fire for routing failures, not just genuine uncertainty — and the two cases require opposite handling.

## Sources Read

- **Klatch** `origin/main` — head `5e361ddd` (2026-10-07T21:33Z). Rounds 345–350 active (AAXT scaffolded probing, CUREs built and tested). Intensive probe-round activity, all Klatch-internal testing methodology; no brief-worthy transferable insights.
- **Piper Morgan** `origin/main` — head `100dde585` (2026-10-08T03:23Z). Arch session log `dev/2026/10/07/2026-10-07-0627-arch-code-log.md`; Lead Dev log `dev/2026/10/07/2026-10-07-0623-lead-code-log.md`. Key insight sourced from the CLARIFY ruling correction. Also read: `flyctl status --json` ImageRef fix in `fly-deploy.yml` (Fly.io-specific, not broadly transferable); E2E CI key reshaped to keyless for local runs (#1956, operational).
- **Globe** — commits present; DNS migration gap (`globe.dinp.xyz` NXDOMAIN after Hover→Cloudflare move, missing CNAME). `fire_check.sh` updated to distinguish NXDOMAIN from HTTP failure. Application of recent briefs' "name the layer" principle; operational incident, not a new insight.
- **One Job** — build 40 submitted to external beta review; Pilot tester history corrected. Operational.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
