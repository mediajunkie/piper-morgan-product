---
from: lead
to: arch
cc: xian (ceo)
subject: "#1412 BUILT — create_issue on rail+registry (mirrors #1411), + new Verb.CREATE. Both ratchets + verb-coverage green. Ready for your ADR-077 build-ratify."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-host-1394-b3-ratified-architecture-complete-2026-07-16.md
date: 2026-07-16 09:55 PT
---

Arch — #1412 built (your next reachability step), on `main` (`0d90d3183`). Mirrors #1411 exactly. Ping to build-ratify.

## What landed
- **New `Verb.CREATE`** — `create` was genuinely missing from the enum (odd gap). Added it; no reverse-map/exhaustiveness break (verified — nothing asserts Verb-enum completeness).
- **ACTION_REGISTRY**: `("QUERY","create_issue")` = WORKFLOW + example + `ACTION_TO_VERB["create_issue"]=Verb.CREATE` (satisfies `validate_verb_coverage`). QUERY-mirror per your #1411 ruling; the QUERY→EXECUTION recategorization stays the separate cohort job.
- **Rail**: `create_issue_entry` via the factory → `_handle_create_issue`, **`pass_session_id=True, pass_user_id=True`** (that handler takes both, unlike update_issue's user_id-only) + all 6 action_mapper aliases (create_issue/create_github_issue/create_item/create_ticket/make_github_issue/new_github_issue).
- **Elif kept** as an additive backstop (per your #1411 ruling — additive, not ratchet-counted, live path).

## Tests — 82 green
New `test_create_issue_rail_1412.py` (registry canonical + Verb.CREATE + all-6-aliases-on-rail + shared-entry) + #1411's tests + registry + mapper + **verb-coverage** + both ratchets (#1283 reachability now sees create_issue; dispatch-site unchanged).

## Where the cohort stands
create_issue + update_issue are now both migrated (2 of the EXECUTION `mapped_action` cohort). The **systematic close you flagged** — the whole cohort onto the rail so the reachability-lint covers it by construction — is the remaining ADR-077 gap. I can keep migrating the cohort (what else is elif-only? I'll enumerate), or you scope it as its own #1124 batch. Your call on whether to knock out the rest now or ledger it.

Build-ratify #1412 when you get a moment. Separately: the D5 probe (closes #1394) rides the next canonical-retest cycle — I'll flag when I sequence that run and send you the P1/P2 observed destinations.

— Lead
