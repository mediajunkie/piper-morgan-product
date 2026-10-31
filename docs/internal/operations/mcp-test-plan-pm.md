# Hosted MCP: the test plan xian runs

**Owner:** PA (writes and maintains it; checks each result). **Runs it:** xian, from his own accounts.
**Written:** 2026-10-31, against `mcp.pipermorgan.ai` Fly release v15. **Updated** for v16, `git_sha` 742a06d7f5 (#2241 and #2022 served).
**Why:** nothing on the MCP surface gets listed (R7: Smithery, Claude directory, Registry) until xian has
tested it himself. The 10-01 draft was never run. This version replaces it.

Takes about 15 minutes. Run it in one client first (claude.ai or Claude Desktop). Each step says what
you should see. Note anything that differs, in your own words: that note is the test result.

## Before you start

- PA checks `https://mcp.pipermorgan.ai/health` reads `healthy` and names the sha it's testing. Known open items as of v16: the consent page shows a raw ID (#1911); there's no Connected apps page in Piper (#1918).
- Use your **alpha** account (the one you sign in to alpha.pipermorgan.ai with). Signing in with your
  beta account also works today, since there's no allowlist. Whether beta accounts *should* be able to
  connect is xian's decision on #2242 (PPM recommends an allowlist).

## Steps

| # | You do | You should see | If not |
|---|---|---|---|
| 1 | In Claude: Settings → Connectors → remove the existing Piper Morgan connector, if there is one. Then add a custom connector with URL `https://mcp.pipermorgan.ai/mcp`. | Claude opens a browser tab on `alpha.pipermorgan.ai`. | Note the error text Claude shows. |
| 2 | If asked, sign in to alpha. | A consent page asking you to approve the connection. Today it shows a raw ID, not your name (#1911). | Note what the page says. |
| 3 | Click Approve. | You're back in Claude and the connector shows as connected, with one tool: `what_piper_knows_about_me`. | Note where it stopped. |
| 4 | In a new chat, ask: **"What does Piper know about me?"** | Claude calls the tool and describes your profile (organization, projects, priorities), says the colleague model has nothing confirmed yet, and mentions your open GitHub issues. | Note any made-up detail, or a refusal. |
| 5 | Ask: **"How many open GitHub issues do I have, and in which repos?"** | The *total* (255 on 10-31), not the number shown. It should say the count covers issues assigned to you in the repositories your GitHub connection can see, archived ones excluded, and not pin it on one repo. The server's own sentence reads: "255 open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded; showing 42 of them, most recently opened first." | A wrong total or one-repo attribution is #2005/#2022. Note the exact words. |
| 6 | Watch whether the answer to step 4 came back promptly, and whether Claude said anything was cut off. | It renders without a "too large" message. The GitHub list shows up to 50 issues, fewer if the titles are long (42 on 10-31), and the note says how many it's showing. | Note any "too large" or "truncated" message verbatim. |
| 7 | Ask: **"What's my organization?"** | It says Piper doesn't have one on file. It must not guess one. | Any guessed name is an honesty failure. Note it. |
| 8 | In Claude: Settings → Connectors → disconnect / remove Piper Morgan. Note the time. | The connector is gone. | Note the error. |
| 9 | Start a new chat and ask step 4's question again. | Claude no longer has the tool. It says it can't reach Piper. | If it still answers from Piper, revoke didn't take: note the time. |

## After you run it (PA)

- Read your notes and file what failed as MCP-lane issues.
- Step 8: whether Claude's disconnect calls our `/mcp/oauth/revoke` (`web/routers/mcp_oauth.py`) needs the
  alpha app's log around the time you noted. PA's production reads are denied, so CIO or you read it.
  Revoking from Piper's side (Settings → Connected apps) doesn't exist yet (#1918).
- Record the run (date, client, sha, pass/fail per step) in the PA session log and on #1462.

## What this plan doesn't cover

- Failure paths (a failed projects or preferences read): unit pins only (#2218, 7 tests).
- ChatGPT or other MCP clients: one client per run. A second run on the other client is welcome.
- The plugin (MCPB/skills) path: it's not built yet (R7).
