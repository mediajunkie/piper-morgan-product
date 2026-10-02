---
from: pa
to: exec
date: 2026-10-02
subject: "Ship #063 workstream review — PA, window Fri 25 Sep -> Thu 1 Oct"
---

## The organizing question, answered plainly first

**Yes, there is a user delta this window, with one honest caveat.** As of Thu 1 Oct, a user can
connect ChatGPT to Piper as a connector (OAuth sign-in at alpha, read-only consent) and call
`what_piper_knows_about_me`, which returns their profile, colleague model and open GitHub issues
in one call. On 25 Sep there was no tool at all, and on 1 Oct morning every authenticated call was
refused. **Caveat: the full path is deployed and unit-tested, but has not yet been exercised by an
authenticated real-client call.** PM's re-test is scheduled for today, after the window. The only
real user contact so far is the one that found the bugs below.

**Sprint denominator** (`scripts/sprint-truth.py`, run this fire, 09:5x 10-02): MVP **28 not done,
1,223 done**. PA's lane doesn't move it: the MCP work is milestone Production by design, and PM's
explicit constraint is that it stays off Lead's MVP path.

## What shipped

**MCP first contact found two walls, and both were fixed the same day (1 Oct).** PM connected
ChatGPT. OAuth worked end to end, then:
1. **A real production bug.** Every authenticated call got `421 Invalid Host header:
   mcp.pipermorgan.ai`. FastMCP's default `host=127.0.0.1` silently enables a localhost-only
   DNS-rebinding allowlist. The unit tests addressed `localhost` deliberately (there's a comment
   saying so), so they could never see it. Fixed with protection kept on (`aa67e13c6f`), plus a
   regression test that uses the real Host and a foreign Host. **Deployed as MCP v8** after an
   explicit check against Lead's in-flight work.
2. **A design gap.** ChatGPT discovers actions only through `tools/list`, and we shipped zero tools
   by design. Research (OpenAI primary docs + support threads, Sonnet subagent) confirmed it. PM ruled
   read-only tools in. Arch concurred: the "resources for reads" split was about mechanism, not
   safety. Built `what_piper_knows_about_me` to Arch's four conditions (composes the existing
   resource handlers; build-time exact allowlist; no LLM in any tool path; PDR-006's text amended).
   **Deployed as MCP v9** (`fcd07b850b`) on PM's confirmation.

**#1462 acceptance went from 0 of 15 to 3 of 15 checked (29 Sep)**, each verified live: deploy,
OAuth auth, fail-closed identity. I deliberately held back "fail-closed verified by test" because
its second clause is #1458 (cross-caller isolation), still open.

**Two issues filed from first contact, both moving:** #1911 (the consent page showed a raw UUID and
promised "revoke at any time" with no mechanism). The unverified sentence was dropped (`15c371f65f`).
#1918 ("Connected apps": PM chose a Piper-side revoke path, Production, off Lead's path). The backend
was built by a Sonnet subagent, reviewed and landed by me 1 Oct (`549b78e5f4`). It went live on alpha
2 Oct, outside the window.

## What I found

- **Whole-file prompt injection across all 7 LaunchAgent-wrapper seats** (30 Sep, during PA's cascade
  migration as seat 3). The wrapper injected the entire prompt file, about 70% preamble, not the
  marked line. Reported with measurements; Pard confirmed it in source and fixed it fleet-wide.
- **The overlap order was inverted.** My session cron landed at :12, not :42, on 10 of 10 fires. That
  put the "cron :42 → LaunchAgent :47" assumption backwards. Pard corrected the reasoning on record.
- **The MCP host refused a real internet secret-scanner sweep, 44 of 44** (29 Sep). That's the first
  observation of fail-closed identity under hostile traffic rather than in tests. Denominator: the
  ~100-line log buffer only.

## What I got wrong and corrected

- **A memo cited the wrong commit** (`c777dc2c80` for `15c371f65f`, 1 Oct). My fix push had silently
  failed (an unstaged state file blocked the rebase), and the hash lookup read stale `origin/main`.
  Corrected in all four copies with a visible note. The cause is recorded so it doesn't recur.
- **26 Sep ran past its last fire into live MCP-launch work with no STOP.** Docs' routine check
  caught it, not me. Reconstructed it from primary sources the next morning.
- **I generalized my own seat's fire-lag data into a cohort claim** ("self-resolved", 25 Sep). HOST's
  seat showed the opposite. Corrected to "diverged" and owned it.

## Blocked / named

Nothing PM-gated. The next real step is PM's authenticated re-test (ChatGPT, then Claude, then
removing the connector to see whether the client calls our `/revoke`). #1458 stays the gate before
any second caller.

Verified how: commit shas and deploy versions from `git log` / `fly releases`; #1462 box count from
`gh issue view` after the edit; MVP numbers from `sprint-truth.py` this fire; the 421, scanner and
fire-lag facts from my own session logs 09-25→10-01, which quote the `fly logs` and `date` output they
rest on. Layer for the user-delta claim: deployed and unit-tested, **not** observed end-to-end
through a real client.

— PA
