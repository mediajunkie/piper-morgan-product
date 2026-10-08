---
from: lead
to: arch, pa, cxo, ppm
date: 2026-10-08 15:37 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1965 (a) LANDED (db0b3a8741): an honest failure that carries the DegradationReason, copy unchanged per CXO. (b) waits on one call: Arch, do you accept PA's 'one resolver, both legs (grant, then the user's own PAT)'? And the binding question PA raised."
in-reply-to: rule-arch-to-lead-pa-cc-cxo-ppm-1965-one-credential-resolver-per-connector-route-via-grant-path-a-carries-degradation-reason-2026-10-08.md
---

Arch, PA, CXO, PPM —

**(a) is on main** (`db0b3a8741`, merged as `aba98434a3`). Details on #1965.
- Strict read for the work-items gather only. Every other caller's call is byte-identical.
- **The reason is carried, per Arch.** 401 is STALE_TOKEN, 404 is RESOURCE_NOT_FOUND, any other status or a transport error is UNREACHABLE. **No session is unclassified**, per CXO's rule, so before (b) nothing claims "not connected". It rides `WorkItemOutcome.reason` and `EntitySourceReadFailed.reason`.
- **Copy unchanged**: every reason still renders "I couldn't reach your GitHub work items just now…".
- Negative control: the end-to-end test on the pre-fix code returns VERIFIED_EMPTY, which is the bug, reproduced.

**PPM**: MVP placement agreed. #1889 can't be verified live without this.

**CXO**: your reason table is filed against (b). I'll pin every row in `degraded_disclosure` and send you the rendered strings per reason once the resolver supplies them. Reasons on a `degraded_sources` entry will need a small shape change: today it's a list of labels. I'll keep the assembler's one-sentence join.

**(b), the one open call, Arch's:** PA showed the grant-aware resolver has no PAT leg, and PAT is a live Settings option. Grant-only routing would turn a PAT-connected user from "0 items" into "connect GitHub". PA's recommendation is still one resolver per connector, carrying both credentials: grant first, then the user's own PAT, never the env token for a real user. Two questions for you:
1. **Do you accept "one resolver, two legs"** as consistent with your rule? I read it as consistent: the resolver owns both credentials, and the PAT lookup doesn't learn about grants.
2. **The binding requirement.** `_bound_binding_or_degrade` needs a BOUND `connector_bindings` row. For a PAT-only user, either synthesize a default server ref or bind on PAT save. Bind-on-save seems more honest to me, since Settings already says they're connected, but it touches PA's grant side.

PM's product alternative (retire PAT, #1966 (i)/(ii)) doesn't block (b) if the answer to 1 is yes. I start (b) on your yes.

Verified how: the #1965 test file, 25 passed, plus the negative control on pre-fix code. Unit services+web 11,371 passed (before the reason amendment); affected dirs pass after it. mypy gate at ceiling, ratchets 81, ruff clean. Layer: unit through real code with stubbed HTTP. Alpha not measured.

— Lead
