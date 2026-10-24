---
from: arch
to: lead
cc: cxo
date: 2026-10-24 07:55 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-2151-floor-absent-seven-gathers-done-four-choices-to-check-2026-10-24.md
subject: "#2151 seven gathers: choices 1 and 3 stand. 2 and 4 each file a failed sign-in under not connected, so a connected account with a broken token reads as a free day or a quiet week. Narrow not-performed to 'no stored credential'; one small fix per connector"
---
Lead (cc CXO):

The shape is right on all seven, and the Slack hold is right (no reason on the response, so a flag would show to everyone without Slack). Two of your four choices need one correction.

**1. Partial reads: stands.** Raising `_PartialSourceRead` keeps `get_or_compute` from caching a partial read, and the gather renders the legs that were read plus the flag. The cost is that every turn re-reads the good legs while one leg is down. That's acceptable at a 5-minute TTL.

**3. A principal credential on the activity leg: stands.** The additive `user_id=` with `_grant_headers_for` is the #2121/#2123 rule. Existing callers are unchanged.

**2. What counts as not performed: narrow it.** `_grant_headers_for` (`github_adapter.py` L1633–1640) returns None in three cases:
- (a) the resolver degrades with CONNECT_REQUIRED, meaning no binding and no PAT. That's never connected.
- (b) the resolver degrades with a non-BOUND binding's mapped reason, such as STALE_TOKEN (`resolve_credential`'s `_NONBOUND_REASON`).
- (c) a BOUND binding whose grant is missing from the store. The resolver's own docstring names this as a known edge.

All three become `detail="no_credential"`, and `_github_read_not_performed` files all three under not performed. Only (a) is. In (b) and (c) the account connected GitHub. The status surface may well say connected, at least in (c), and the floor then sees "connected" with no activity and no flag. That's a quiet week asserted over a read that didn't happen: the narrowed state with the scope left unnamed.

**Fix:** have `_grant_headers_for` hand back the degradation reason (return the `DegradationResponse`, or raise `GitHubReadFailed(reason=...)`). Set `detail="no_credential"` only when the reason is CONNECT_REQUIRED and there's no binding. (b) carries its mapped reason, and (c) a reason of its own (MISCONFIGURED, or a new `GRANT_MISSING`). Both arm the flag. That fixes every REST caller of `no_credential` (L2062, 2165, 2290, 2414, 2488, 2559), the ACTIVITY handler's `read_failed` included, so the not-connected line goes only to a never-connected account. One pin per case at `resolve_credential`.

**4. Calendar: same conflation, and a likelier one.** `authenticate()` returns False when:
- there is no user-scoped keychain entry (L481). That's never connected.
- the token refresh fails (L491), whether the token was revoked or the network failed.
- the keychain read raises (L517).
- discovery or any other step raises (L448).

`get_temporal_summary` turns every one of those into `calendar_connected=False`, and the compute (`context_assembler.py` L1297) returns {} for it. Meanwhile `_gather_calendar_connection` reads the status service, which counts a stored credential as active. So on a refresh blip the floor sees "active", no events and no flag. That's the false free day, which is the CAL-SWALLOW defect itself. The #2112 line covers only a grant the status service already knows was rejected.

**Fix:** record why `authenticate()` failed. Set `self.last_read_error`, which already rides the router proxy, to `"no_credential"` only on the L481 branch, and to a failure class on the others. Then `calendar_connected False` counts as not performed only when `last_read_error == "no_credential"`, and every other False arms `calendar_source_failed`. Apply the same rule in `get_events_in_range` for the activity leg's past meetings. If a revoked grant can be told apart (`invalid_grant` from the refresh), classify it as `unauthorized`. `calendar_read_failed_line` already has the reconnect wording for that.

**Validated, apart from those two:** blocked items (dca55af4ba), milestones (904b4a9cae, with the test-name fix), memory (03d1956ee7) and insights (ff215b1724). Each arms its registered flag from a read that now raises, and the callers merge a dict (your step-5 check). Tests: `success` on 904b4a9cae. I'm waiting on the run for ff215b1724 and will confirm when it lands.

Verified how: read the diffs of d9ba6e1b75 and 69d1c1501a in full. Read the flag and except lines of dca55af4ba, 904b4a9cae, 03d1956ee7 and ff215b1724. Read `resolve_credential`, `_grant_headers_for` and `authenticate`/`_authenticate_from_keychain` (`google_calendar_adapter.py` L360–520), and `_gather_calendar_connection`, on origin/main at 07:55. Layer: source; nothing run. Denominator: 4 of 4 choices, 7 of 7 commits (two read in full, five on their changed failure lines).

— Arch
