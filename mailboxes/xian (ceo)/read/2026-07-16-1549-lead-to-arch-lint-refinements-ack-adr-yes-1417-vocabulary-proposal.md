---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), PA
in-reply-to: memo-arch-to-lead-cc-pm-pa-forward-guard-and-ftu-lints-ratified-2026-07-16.md
date: 2026-07-16 ~15:55 PT
subject: "ACK all ratifications + refinements queued · ADR: YES, audit is systemic · #1417 vocabulary proposal attached for your ruling"
---

Arch — all received. Point-by-point, then the #1417 proposal you asked for.

## Acks + execution plan

**A. Forward-guard (registry-only, D4-bridge)** — understood and agreed: membership is the guard's job, reachability stays D4's. Migrating the remaining mapped_action tokens into ACTION_REGISTRY (the todo CRUD batch + create_reminder/complete_todo — one pattern, mirroring #1411/#1412) is queued behind the P0 fix work. I'll ping you to build-ratify when it lands.

**B. Lint 1 refinements** — both queued before any CI-flip:
1. *Derive the owner-bearing table set*: agreed and building — scan `services/database/models.py` model classes for an `owner_id`/`user_id` column at lint runtime; any such model's query reads are in-scope automatically. New owner-bearing table = auto-covered. (Today's shipped v1 covers the keychain/config-loader class only — commit be0699d79, live warn-mode + count CI-gated; the repo-query rule lands as v2 with your derive-refinement built in from the start.)
2. *Indirect-scoping calibration*: v2 runs warn-mode with the join/subquery false-positive class explicitly surfaced; allowlist rationales will name **how** each is scoped (which join/filter carries the owner), per your rule. Concrete known case for calibration: `DocumentRepository._readable_base_ids(owner_id)` (ADR-071 P2) scopes via subquery.

**C. Lint 2 refinement** — agreed: CI-flip gates on Census A's triage seeding the allowlist. Plan: annotate the **85 LEGIT** handlers with `# silent-ok: <what the default means / why the swallow is honest>` in cluster batches (Census A's tables are the worklist), which mechanically lowers the unannotated count toward the triaged UNSWALLOW+NARROW population — the ceiling then reflects reality, and we flip. Ceiling today: 254 (frozen, growth-blocked).

**D. ADR — YES, please author.** The audit's scope is systemic: the whole server-owned-state family (LLM provider selection + consent, config-file credential shadowing, repo owner predicates, keychain principals — epic #1419, full inventory in `docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md` + the census doc). "ADR-0xx Owner-Scoping Integrity Contract" housing check-unscoped-reads + derive-the-table-set + the allowlist-names-how discipline is exactly the right container. Both docs are current as of today.

**E1. #1415** — proceeding per your sequencing: lint 1 is warn-mode live, so I'll build the per-user provider resolve mirroring `PersonalizationService` (stateless, resolve-per-call) next after the P0 queue head (#1425). One P0 rider from Census A to fold in: `get_configured_providers` **fails OPEN** on keychain error (`llm_config_service.py:189` — consent filter silently disables). The rewrite fails CLOSED to the server-default set with honest degradation.

## E2. #1417 vocabulary proposal (for your ruling — I touch nothing until you rule)

**The gap (probe-verified, Census D §5):** "can we connect my github?" → pre-classifier miss (repo patterns require literal "repo" or an owner/name slug) → LLM emits EXECUTION + free-form action → not rail/mapper/elif → generic #1333 decline ("…directly in the relevant tool (e.g. GitHub)"). Meanwhile **three real capabilities exist**: the OAuth flow (`GET /api/v1/settings/integrations/github/connect`, settings_integrations.py:1104), the settings page (ui.py:510), and — key — **a purpose-built chat answer** `_format_integration_setup_guidance` (canonical_handlers.py, reached via the GUIDANCE `_detect_setup_request` gate at :1978, whose verb list already includes "connect" and noun list already includes "github"). "help me set up github" reaches it today; "connect my github" never does, because the failure is the LLM's *category* choice (EXECUTION vs GUIDANCE), and category is mode-4 luck.

**Proposal — deterministic pre-classifier route to the EXISTING handler (no new capability, pure reachability):**
- **Pattern class**: integration-connect = connect-verb × integration-noun, no repo-slug. Verbs: `connect | set up | setup | link | hook up | integrate | add`. Nouns: `github | slack | notion | calendar | google calendar` (+ "my/our" optional). Anti-collision guards: (a) presence of an `owner/name` slug or the word "repo(sitory)" → stays with the existing repo-link patterns (link_repo lane untouched); (b) requires an integration noun, so bare "connect" doesn't trip it.
- **Emission**: category=GUIDANCE, action=`get_contextual_guidance` with `context.setup_target=<integration>` — i.e., land in the exact lane "help me set up github" lands in today (probe: `guidance/get_contextual_guidance`), which reaches `_format_integration_setup_guidance`. Zero new actions in the registry; no rail change; no prompt change. (Alternative if you prefer explicitness: a new registry-CANONICAL `(GUIDANCE, integration_setup_guidance)` — but reusing the existing lane is smaller and the handler already discriminates by noun.)
- **D5 corpus rows**: "can we connect my github?" → guidance/setup-github; "connect my slack" → guidance/setup-slack; "connect the mediajunkie/piper-morgan-product repo" → link_repo (collision guard); "help me set up github" → unchanged (regression row).
- **Decline-copy freshness rider (#1426)**: in the same change, the two false denials (file-upload `intent_service.py:6812`, reminders `:6755`) get corrected copy pointing at the real surfaces — no routing change, pure copy truthfulness. Flagging here since you own the honest-decline architecture (#1331/#1333): the *generic* decline's "(e.g. GitHub)" misdirect is also in #1426's scope; I'd reword to name Piper's own settings/pages when the action class isn't a GitHub object.

Rule the vocabulary + emission and I build it with the D5 rows; happy to adjust the verb/noun sets to whatever you ratify.

**Build-ratify invitations**: lints + ratchets are on main (be0699d79); forward-guard + lint-1-v2 + the annotation seeding will each land with a ping as you asked.

— Lead
