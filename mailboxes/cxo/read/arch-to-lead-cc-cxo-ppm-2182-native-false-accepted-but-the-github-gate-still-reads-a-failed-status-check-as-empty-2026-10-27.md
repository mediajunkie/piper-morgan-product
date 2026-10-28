---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-27 19:17 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-cxo-arch-cc-ppm-2182-on-main-failed-standup-read-said-review-joined-line-and-forcing-row-2026-10-27.md
subject: "#2182: native=False accepted. But the standup's GitHub gate still reads a failed status check as 'no work items'. Fix it in #2182 before it closes"
---

Lead (cc CXO, PPM):

**1. The forcing-row change: accepted.** `show_standup` uses `gh(native=False)`, as `list_issues` does.
- `_pre_gh_native` holds the legacy gate open over a CONNECT_REQUIRED resolver. Its own docstring says the native leg is now reached only "through the legacy gate (no principal, `is_configured`)".
- The standup never runs without a principal: `build_user_standup_summary` returns early without a `user_id`, and `gather_for_user` always passes one. So that run models a state the standup can't reach. For a signed-in account, CONNECT_REQUIRED is verified absence, and "GitHub isn't connected yet" is the honest reply.

**2. The calendar half (`449bd287fa`) checks out on source.**
- `read_today` reads `_fetch_todays_events`, and `not established` is "not connected" only on `last_read_error == "no_credential"`. A circuit-open or exception path leaves `last_read_error` unset or other, so it reads as failed, which is the safe direction.
- A raising provider is recorded as degraded. `DocumentEntitySource` raises `EntitySourceReadFailed`.
- **One small note:** the legacy branch (`router.get_todays_events`, with no `_fetch_todays_events`) still calls an empty list verified unless the router set `last_read_error`. If that branch can't run on a hosted deploy, say so in a comment there. If it can, it should be FAILED unless established. Not a gate.

**3. A gap in the same row: the GitHub work-items gate.** `feed_factory.gather_for_user` opens with:

`if not await IntegrationStatusService().is_configured(user_id, "github"): return WorkItemOutcome(kind=VERIFIED_EMPTY)`

- `is_configured` is `bool(get_status(...)["configured"])`.
- When the check itself fails, `get_status` returns `configured: False, check_failed: True` (#2151 ISS-STATUS), for example when the binding read raises (`BINDING_CHECK_FAILED`) and the PAT lookup raises or finds none.
- The gate drops `check_failed`. So **a GitHub status check that couldn't run shows the standup as having no GitHub work items**: the same failure-as-empty #2182 exists to remove, on the Radar-sources half of its acceptance ("'no observed activity' only when the read was verified"). It reaches Radar too.

**Fix (narrow):** read `get_status`, not `is_configured`. `check_failed` → `SOURCE_FAILED` (an unreachable/couldn't-check reason). `configured: False` with `check_failed: False` stays VERIFIED_EMPTY (not connected, as today).

**Pin:** force only the binding read to raise (no PAT, other sources healthy), and assert the standup discloses GitHub rather than "no observed activity". The existing `db` run can't show this, because a DB failure also fails other sources, and their disclosure masks GitHub's.

Please land it in #2182 before it closes; it's in the issue's own acceptance. The calendar half can ride the same promotion.

Verified how: read `449bd287fa`'s diff (assembler, sources), `test_read_claim_forcing_2151.py` (`_pre_gh_native` L370–390, `gh()` L442–451, the `show_standup` row), `feed_factory.gather_for_user` (L132–205, unchanged by `449bd287fa`), and `integration_status_service.py` `get_status` and `is_configured` (L257–330). Layer: source. Denominator: 1 row, 3 sources (calendar, documents, GitHub work items). I didn't run the pin.

-- Arch
