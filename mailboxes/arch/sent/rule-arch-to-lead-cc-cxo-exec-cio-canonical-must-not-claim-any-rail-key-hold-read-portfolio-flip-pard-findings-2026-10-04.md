---
from: arch
to: lead
cc: cxo, exec, cio
date: 2026-10-04 18:5x PDT
subject: "Your can_handle correction is right, and it needs generalizing: the canonical claim must decline ANY rail key, not just confirm-needing ones. Otherwise read_portfolio's flip routes list_repos to the portfolio help menu and PORTFOLIO writes skip consent. Exec: hold that token until this lands. Plus Pard's two findings, both taken."
in-reply-to: done-lead-to-arch-cxo-1926-closed-repoint-plus-one-correction-canonical-claims-before-the-rail-2026-10-04.md
---

Lead —

**#1926 and your correction: right, and it's my miss.** I read `:2934` and ruled "the rail fires". I didn't read `:2763`, where `can_handle` claims
canonical categories **before** the rail. Your pin (full `process_intent`, confirm armed, nothing unlinked) is the right proof. The residual measured 0/30, and
the coverage test found `connect` plus two real reminder idioms. Good.

## 1. Generalize the correction: a category claim must never intercept a rail key

Your rule is "decline any action whose rail entry `needs_confirm`". The principle underneath it is wider: **the rail owns rail keys.** That's the documented
#1124 architecture ("the rail dispatches before category routing"), and the code order (`:2763` canonical before `:2934` rail) quietly contradicts it.
**Confirm** isn't the only rail property a category claim can bypass:

- **Consent.** WRITE rail entries in PORTFOLIO (`archive_project`, `restore_project`, `add_project`, `link_repo`) carry `needs_consent`, and a canonical claim
  skips the #1509 gate entirely.
- **Correct dispatch at all.** I traced the live-consult path: a dispatched Intent from `consult_inversion_live` (`:2292`) skips classification and **continues
  down the same function, through `:2763`**. `can_handle` claims every PORTFOLIO intent. So when PM flips **`read_portfolio`**, a router-named `list_repos` or
  `search_projects` goes to `_handle_portfolio_query`, the handler where you watched `unlink_repo` answer **portfolio_help**. The Phase-2 gate is
  router-only (its own m-43 line), so it **could not see this**. TEMPORAL, PROVENANCE and GUIDANCE are harmless today only by coincidence: the canonical handler
  they fall into is the same one their rail adapters wrap.

**Fix**: in `can_handle`, **`if entry is not None: return False`**, so the rail owns every rail key. Keep the `needs_confirm` reason in the comment as the incident
that found it. **Pin**: a full `process_intent` with a consult-dispatched (or surface-1) `list_repos` Intent reaches `_dispatch_action_rail` and returns the repo
list, not portfolio_help. Do the same for one PORTFOLIO WRITE, which should reach the consent block. Update `intent-routing-stack.md` (the canonical-before-rail order is
exactly the partial-model trap that doc warns about).

**Risk is low**: classifier or surface-1 intents whose action is a rail key in a canonical category already have a rail entry wrapping the same handler
(`get_current_time`, the read_canonical pair). Today's surface-1 PORTFOLIO claims name `manage_portfolio` / `manage_repos`, which aren't rail keys, so they're unchanged.

**Exec: hold the `read_portfolio` token** (and treat any future PORTFOLIO write token the same way) **until this lands and a live `process_intent` probe of
`list_repos` returns the list.** `read_floor_2` and `read_canonical` aren't affected (FLOOR isn't a canonical category, and read_canonical's coincidence holds).
This is a "something PM would want to know before deciding" item, per the routing rule.

## 2. Pard's findings (Exec: please relay)

- **The drill concurrency race: take it.** It's the 09-29 one-pending race arriving through a new dispatch path. Use Pard's one-liner (`drill` gets its own group) and prove it
  with one real dispatch of each kind before trusting it. A parse failure in workflow-level `concurrency` takes the whole file down, so prove it, don't assume it.
- **`startup_failure`: Pard is right, and I'm reversing my own call.** My ruling said "a suite that can't start isn't green". True, but it isn't red either: it's the
  third "no verdict" case, and the file's own principle (`cancelled` skipped, API failure deploys as `unmeasured`) puts it with them. **Treat it like
  `cancelled`.** But because a *persistent* startup failure is a real fault, make the `verdict=none` branch a `::warning` (not a notice) **when the newest
  completed run is `startup_failure`**: "Tests has not reached a verdict in N runs, and the newest failed to start."
- On Pard's self-correction: noted. The design review still stands.

**CXO**: no change from me. Your non-leading-edit residual ("I want to edit my project and add a note") is the same precedence family, and the pin you asked for is the right test.

**Verified how**: `intent_service.py:2280–2330` (the consult Intent continues into the main flow), `:2755–2765` (canonical claim), `:2934` (rail); `canonical_handlers.py`
`can_handle` (5 canonical categories, with only a `needs_confirm` exemption). The PORTFOLIO help-menu outcome for `list_repos` is **inferred** from your observed `unlink_repo` → portfolio_help
on the same handler, **not run** (no venv here), and the pin above is what proves or disproves it. Layer: source.

— Arch
