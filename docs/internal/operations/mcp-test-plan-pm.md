# Hosted MCP: the test plan xian runs

**Owner:** PA (writes and maintains it; checks each result). **Runs it:** xian, from his own accounts.
**Written:** 2026-10-31, against `mcp.pipermorgan.ai` Fly release v15, `git_sha` 061de2f98f.
**Why:** nothing on the MCP surface gets listed (R7: Smithery, Claude directory, Registry) until xian has
tested it himself. The 10-01 draft was never run. This version replaces it.

Takes about 15 minutes. Run it in one client first (claude.ai or Claude Desktop). Each step says what
you should see. Note anything that differs, in your own words: that note is the test result.

## Before you start

- PA checks `https://mcp.pipermorgan.ai/health` reads `healthy` and names the sha it's testing.
- Use your **alpha** account (the one you sign in to alpha.pipermorgan.ai with). Signing in with your
  beta account also works today, since there's no allowlist. Whether beta accounts *should* be able to
  connect is an open product question (PA to PPM, 10-31).

## Steps

| # | You do | You should see | If not |
|---|---|---|---|
| 1 | In Claude: Settings → Connectors → remove the existing Piper Morgan connector, if there is one. Then add a custom connector with URL `https://mcp.pipermorgan.ai/mcp`. | Claude opens a browser tab on `alpha.pipermorgan.ai`. | Note the error text Claude shows. |
| 2 | If asked, sign in to alpha. | A consent page asking you to approve the connection. Today it shows a raw ID, not your name (#1911). | Note what the page says. |
| 3 | Click Approve. | You're back in Claude and the connector shows as connected, with one tool: `what_piper_knows_about_me`. | Note where it stopped. |
| 4 | In a new chat, ask: **"What does Piper know about me?"** | Claude calls the tool and describes your profile (organization, projects, priorities), says the colleague model has nothing confirmed yet, and mentions your open GitHub issues. | Note any made-up detail, or a refusal. |
| 5 | Ask: **"How many open GitHub issues do I have, and in which repos?"** | The *total* (about 255 on 10-31), not 50. It shouldn't pin that total on one repo: the search covers issues assigned to you in every non-archived repo your GitHub connection can see. | A wrong total or one-repo attribution is #2005/#2022. Note the exact number it says. Until #2022 serves, the payload doesn't state its scope, so a one-repo answer is expected today. |
| 6 | Look at how long step 4 took and whether Claude said the result was cut off. | It works, but the GitHub section is very large (431k characters, #2241), so Claude may say it truncated or summarized. | Note any "too large" or "truncated" message verbatim: it's #2241's evidence on your client. |
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
