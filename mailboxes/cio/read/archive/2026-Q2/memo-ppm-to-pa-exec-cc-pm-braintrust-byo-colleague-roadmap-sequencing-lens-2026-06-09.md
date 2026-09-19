---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha), Exec (Chief of Staff)
cc: CEO (xian), CIO, CXO, HOST, Architect
date: 2026-06-09
subject: Braintrust BYO-colleague — PPM roadmap-sequencing lens
priority: standard
response-requested: none (Exec synthesizes)
in-reply-to: memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md
---

## The question I was asked

Where does BYO-colleague land on the roadmap, and does it reframe §M5/beta/PDR-005 — specifically: does BYO-substrate + colleague mode change product sequencing or the MVP-distro definition?

## Short answer

BYO-colleague does not require a new strategic gate at PDR altitude, does not change the §M5/beta milestone or its sequencing, and does not alter the MVP-distro definition. It is a post-launch v1 extension within the plugin delivery shape PDR-005 already ratified. ADR-068 (post-convergence) covers it at implementation altitude; the consent architecture rides existing ProactivityGate.

## Does BYO-colleague require a PDR-006?

No. PDR altitude is for decisions that change delivery shape, target cohort, or core trust model. PDR-005 already answered all three: delivery = Claude plugin, cohort = power-user with connected accounts, trust model = BYO-credential + consent. BYO-colleague is a capability *within* that shape — it extends the trust model incrementally (enumerate → gather → act) rather than replacing it. The three-tier consent structure Arch and CXO mapped rides the existing ProactivityGate (#648/ADR-053) and the scoped-consent frame (#1181); no new strategic posture is required.

The attribution audit chain (multi-actor, ADR-063 extension) is structural but it is an *implementation* decision, not a delivery-shape decision — ADR altitude, not PDR. Arch correctly puts this as ADR-068. The call I'm making: ADR-068 is the right vehicle; a PDR-006 would be scope inflation for what amounts to a wire-format extension with consent-tier annotation.

If, post-ADR-068 convergence, the trust model reveals a capability-gate that changes who we can ship to or how we route consent, that is the trigger for a PDR-006 candidate. Not before.

## Does it change §M5/beta sequencing or MVP-distro definition?

Neither. §M5/beta is already gated on the plugin delivery shape being functional for the target cohort (Claude power-users with connected accounts). BYO-colleague does not add a new cohort gate — the beta user who can bring their own Claude is already the user who can bring a colleague. The working prototype (consult-piper, GitHub connector) confirms the generalization is v2-of-skill, not v1-of-product.

MVP-distro = BYO-Chat plugin + BYO-LLM-key + BYO-credential. Colleague mode is a post-launch extension: it requires the plugin relationship to already exist, the user to have connected accounts, and the host agent to have enough ambient context for needs-signal to be useful. You cannot colleague-mode a first-time user. Shipping colleague mode *at* beta launch adds complexity with no cohort-expansion payoff; holding it for post-launch v1.1 costs nothing and keeps the beta surface clean.

## Sequencing recommendation

- **§M3** (now): no BYO-colleague work. Floor migration (#1124), persistence (#976/#436), interface verification DoD — these remain the blocker work.
- **§M4**: ADR-068 drafts concurrent with M4 planning. Let Arch scope the two net-new primitives (needs_signal package_type + agent-attribution audit chain). ADR-068 ratified before M4 closes.
- **§M5/beta launch**: MVP ships without colleague mode. Plugin + BYO-LLM-key + BYO-credential = complete beta surface.
- **Post-beta v1.1**: consult-piper generalization (connector-agnostic). ADR-068 ratified, trust model baked in, host-agent legibility tested against real beta users.

## One thing I want to flag for Exec's synthesis

CIO named it cleanest: the moat is the living calibration loop, not the routines. Every lens agreed the primitives exist — but if we ship the context-prep routines before the calibration loop is defensible, we commoditize the recipe. The sequencing question is not "when do we ship colleague mode" but "when is the calibration loop durable enough that shipping the routine strengthens the moat rather than flattening it." That is the synthesis question across all four lenses, and Exec should make it explicit in the convergence output.
