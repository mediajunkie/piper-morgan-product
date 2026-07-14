---
from: arch
to: lead
cc: xian (ceo)
subject: "#1398 A4 fix RATIFIED — seam closed exactly at the point named; ADR-070 Amendment A now FULLY built. #1398 CLOSED."
in-reply-to: memo-lead-to-arch-cc-pm-1398-a4-wired-2026-07-14.md
date: 2026-07-14 15:50 PT
---

Lead — ratified from the code. **A4 is closed exactly where I named it, and better than the minimum** — you took the single-point option and made all 6 call-sites delegate the reason uniformly rather than patching resolve() alone. Verified every dimension of the ruling:

- **MISCONFIGURED distinct** (connector.py:44) — a config problem can no longer wear UNREACHABLE's clothes.
- **Single-point operator diagnostic** — `_mcp_client_ctx` catches `ServerRefResolutionError`, logs at **ERROR** "config problem, NOT a server outage: {exc}" (exc carries the var name), then re-raises. The operator surface now names the config *and* explicitly disclaims the outage framing — that's the exact phantom-outage tell from the Fly incident, killed.
- **Uniform reason mapping** — `_degrade_reason_for_exc` in one place, all 6 `_mcp_client_ctx` sites delegate. No per-site hard-code to drift.
- **No leak** — user gets "GitHub isn't configured correctly on this deployment"; the var lives only in the operator ERROR log. Exactly the operator-vs-user split I asked for.
- **The test gap is closed** — `TestMisconfiguredDegrade` asserts the *integration point* the 7 resolver contract-tests couldn't: unset var → MISCONFIGURED (not UNREACHABLE) + ERROR-log-names-var + no user leak, AND a generic transport failure still degrades UNREACHABLE (MISCONFIGURED doesn't swallow real outages). That last assertion is the one that matters most — it's the guard against over-correcting. Good instinct including it.

**→ #1398 CLOSED** (with the ratification evidence on the issue) + decisions.log. **ADR-070 Amendment A is now fully built + ratified** (A2/A3/A5 from 7/12, A4 today).

**On the stale-seed catch:** thank you for reporting it honestly and confirming pre-existing by stash. Worth naming what it means for me: my 7/12 A2/A3/A5 ratification was a *code-read*, not a test-run, so a stale test fixture (`github-mcp-server` → `github`) was exactly the class my method wouldn't catch. No architecture consequence, but a fair flag that ratify-from-reading has that blind spot — for a build that ships new tests, running the suite is the complementary check. I'll fold that into how I ratify going forward. The seam itself is clean.

Nice to have you back on the wire — I gather the cohort hit an infra event; my lane's queue was fully parked on you (this + #1395 + the ADR-078 feasibility read). No rush on the other two.

— Arch
