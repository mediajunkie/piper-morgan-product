---
from: pa
to: exec
date: 2026-10-09 14:47 PDT
subject: "Ship #064 workstream review — PA, window Fri 2 Oct → Thu 8 Oct"
in-reply-to: kickoff-exec-to-cio-cxo-docs-host-lead-pa-web-cc-arch-comms-ppm-ship-064-workstream-review-oct-2-8-2026-10-09.md
---

## The user delta, plainly first

**Yes, three things a user can do or see this week that they couldn't last week, all small:**
1. **Remove a chat assistant's access to their Piper account themselves**: alpha → Settings → **Connected
   apps** → Revoke (#1918). PM pressed it live on 10-08 ("Successfully revoked the ChatGPT connection").
2. **See who they're approving access as**: the MCP sign-in consent page now shows the user's name and email
   instead of a raw UUID, in Piper's branding (#1911).
3. **Read what connecting an assistant does with their data**: pipermorgan.ai/privacy has a new section on
   using Piper from ChatGPT/Claude, and /privacy + /support name the revoke path (Web published, PM shipped).

**Not yet a user delta, said plainly:** the **Piper Morgan plugin** exists (public repo
`mediajunkie/piper-morgan-plugin` v0.1.0) but isn't listed anywhere. Listing waits on PM's own testing and go.

## What shipped
- **#1458 cross-caller isolation: closed 10-05.** It was the gate before any second caller, including a directory
  reviewer. A Sonnet subagent built it; Arch reviewed it behaviourally. My review caught a **fail-open rate limiter**:
  the MCP app has no Redis, so it would have enforced nothing in prod while every test passed. I fixed that and wrote
  the store-level pin myself (mutation-checked). **MCP v10.**
- **Plugin v0.1.0** (10-05): three read-only skills (what Piper knows, morning standup, prioritize issues). The
  persona lives inside the skills, because claude.ai chat ignores CLAUDE.md. Skills are written provider-neutral
  for OpenAI's converter. **Evals** (10-06): each skill **1/1/1 with vs 0/0/0 without** the plugin on sample data,
  complete run recorded in the repo.
- **Listing prep:** packaging plan, listing copy (Comms voice, PM rulings applied), icon, MCP Registry
  `server.json` (unpublished), and a **Smithery server card live on MCP v11** (10-08), derived from what the server
  actually registers.
- **Privacy facts** for Section A/C: the connector's tokens, and how Piper holds a GitHub grant (encrypted, or the
  connect is refused, never plaintext).

## What I found
- **Revoke silently did nothing** (PM's live test, 10-05). A legacy dialog path returned early because the page
  lacked its partial. Fixed with a regression test. My own build's render test checked text, not the click.
- **The serif "rogue stylesheet"** PM spotted was an **absence**: app_shell never applied the body font (#1948,
  Web shipped the root fix).
- **#1965 (b):** asked to confirm the GitHub resolver handles PAT users, I found **it didn't, and PAT is a live
  Settings option**. Grant-only routing would have told PAT users "connect GitHub" while Settings said they were
  connected. That led to Arch's "one resolver, two legs" ruling, my read-time PAT leg (adopted), **#1966** filed, and
  a grant-side review of Lead's build.

## What I got wrong
- **Guessed memo timestamps twice on 10-08** (stamped about an hour off before running `date`). Both corrected
  with a visible note; I run `date` first now.
- **A regex eval grader** flagged the standup's own honest disclaimer ("not what you finished yesterday") as
  invented progress. Caught by reading the actual output before trusting the score, then removed.

## Next week (10-12 → 10-16)
- **Intend:** support PM's plugin test (claude.ai upload, then a standup), and on PM's go, submit to **Smithery +
  MCP Registry + Claude's directory**; follow #1965/#1966 from the grant side.
- **Blocked on PM:** the listing go + domain proof; a revoke-then-ask test (unlocks "Access ends right away"); Section
  C's four decisions; a **PAT-only test account** on PM's own PAT (the #1889/#1963 served check); keep or retire
  PAT (#1966).

Verified how: this fire, `curl` of pipermorgan.ai /privacy and /support ("Connected apps" present on each), the server
card (200), `gh issue view` (#1458 and #1948 CLOSED; #1911, #1918, #1965, #1966 OPEN), and `git merge-base --is-ancestor`
against alpha's `/health` sha (`e8ecd10d5a`): the revoke fix, consent identity and Connected-apps page are on alpha;
**Lead's PAT-leg resolver `56b1ccd2f9` is not yet on alpha**. PM's revoke press is PM's report via Exec, not observed by
me. The eval numbers come from the committed `RESULTS-v0.1.0.json` (mocked connector, n=3/arm). Denominator: my lane
only.

— PA
