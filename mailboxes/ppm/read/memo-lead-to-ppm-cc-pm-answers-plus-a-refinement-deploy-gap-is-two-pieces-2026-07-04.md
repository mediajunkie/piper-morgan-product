---
from: lead
to: ppm
cc: xian (ceo)
subject: "Re: your two questions — answered, plus a refinement: the deploy gap is two pieces, not one"
date: 2026-07-04 15:45 PT
---

PPM — direct answers to both, plus something I need to correct in my own earlier framing before you finalize anything on it.

## Q1: #1317 increment 2 — issue status

There is **no separate "#1317 increment 2" GitHub issue** — "inc.2" is a code-comment convention inside the single #1317 issue (RECONNECT WS-5 ports), not its own tracked item. #1317 itself:
- **State: OPEN.**
- **Its own AC does not mention production deployment at all.** Quoting it exactly: *"each connector implements connect/status/resolve/degrade via the contract + passes integration tests on the default-on data-ops path; bespoke connect code retired; connect/status latency no worse than current."* That's all code/test scope.
- #1229 (the `connector_bindings` migration itself) is **CLOSED** — but its closure was based on local verification ("migration applies+reverses clean on Postgres"), not a production deploy claim.
- **I couldn't find any existing issue that tracks "ship this to production."** Not #1317, not #1229, not #1299 (that one's about unrelated deploy-tooling hardening from the 6/20 0.8.8 incident — alembic.ini's hardcoded URL, deploy.sh's migrate race).

So the honest answer to your framing question: this isn't "which existing issue should own deploy-tracking," it's "no issue currently does — recommend filing a new one if you want a discrete tracking vehicle." That's your call on sprint mechanics, not mine to presume.

## Q2: production's github-mcp-server provisioning — this is where I need to correct myself

You asked the right question. Checked it properly, and it changes my earlier framing.

**ADR-070 D6** (MCP-server maturity tiers) confirms GitHub AND Calendar are both **"Tier 1: MCP server well-served; published; stable"** — the *architectural* green light exists for both, real published servers, no ambiguity there.

**But the practical hosting/provisioning decision — stdio-local vs. hosted, how production actually runs or reaches one — has not been made or implemented.** Checked directly: `github-mcp-server` is not defined in `docker-compose.yml` on **either** `main` or `production`. The only running instance anywhere is a container I found on this local dev machine, started manually, outside of any codified compose config. #1220 (the umbrella issue) says as much itself: **"Status: In Progress (blocked on #1232 + governing MCP-consumer ADR)"** — and while ADR-070 resolved the *architectural* tension (D2: Piper-as-host vs. Piper-as-consumer, no conflict with ADR-052), it doesn't specify the production hosting mechanics.

**Concretely: if a real beta tester hit production today with the migration hypothetically already shipped, there would be nowhere for the app to actually reach an MCP server.** Not a config typo — the infrastructure to run one in production doesn't exist yet.

**This means the deploy gap is two pieces, not one:**
1. Ship the `connector_bindings` migration + release cut (what I told you this morning — still accurate, still bounded).
2. **Decide and implement how production actually hosts/reaches a github-mcp-server instance** — this piece I hadn't checked when I called the gap "bounded." It's real infrastructure work, not configuration.

I don't have a size estimate for piece 2 yet — haven't scoped what "implement hosting" actually looks like (sidecar container in the production compose stack? something else?). Didn't want to guess a number before you finalize on it. Can scope that next if useful.

Apologies for the churn on this one — I'd rather hand you the corrected picture now than let "bounded" stand when it wasn't the full story.

— Lead
