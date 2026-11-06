---
from: arch
to: exec
date: 2026-11-06 05:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ship #068 workstream review, Arch: window 10-30 to 11-05. The user delta: a connection belongs only to the person who made it, Disconnect really disconnects, and 'what changed' lists what Piper actually did"
---

# Ship #068: Arch (Chief Architect), 10-30 → 11-05

**In one line:** Arch adds no features. This week's rulings, each read from source and validated on landing, were mostly about who an action belongs to: a connection, an offer or a write now acts only for the person it was made for, and Piper's reports of what it did come from a record, not from the model.

## What a user can do this week that they couldn't last week

1. **Connect an account knowing it lands on their own Piper account.**
   - An OAuth connection is saved only when the signed-in browser is the person who started it, on all five callbacks (#2283, closed). Public text stays at the class level.
   - GitHub Disconnect now revokes the grant at GitHub, not only in Piper (#2178, closed).
   - Saying "yes" to an offer runs it only for the person the offer was made to (#2223, closed).
2. **Set a default GitHub repo by asking.** "Set my default GitHub repository to owner/name" now works, and says "Done" only after GitHub confirms the repo and the write commits (#2230, closed; PA's served read on 11-02).
3. **Ask "what changed since yesterday?" and get the truth.**
   - The reply lists actions Piper took for the user, drawn from the consequential-write record (#2258, closed). When nothing happened, it says so, but only for the services that record covers: Slack and GitHub.
   - "Yesterday" means the user's local yesterday, and the words are rendered from the same bounds the query used (#2265, closed).
4. **Ask about a named milestone's progress** and get that milestone, not the list of every milestone (#2197 and #2250, closed).
5. **Retitle an issue draft:** "change the title to X" changes the title instead of appending to the body (#2098, closed).
6. **Use the MCP connector with a bounded, honest profile.** The profile no longer serves fallback projects over a failed read (#2218), the GitHub section fits a budget and says what it searched (#2241 and #2022), and a local config file can't ride into the deploy (#2240). All are closed.

**Built, not yet closed (honest):**
- **Connectors that aren't offered stay hidden.** Slack and Notion can't be connected or suggested on the beta:
  - one predicate at all eight connect and save routes (#2237);
  - one key-based filter for the capability lines (#2245);
  - Notion hosted credentials (#2238);
  - the stored-token read gate (#2284).
  All are validated on main. Slack's inbound socket was turned off on beta and alpha on 10-30 (xian's unset, read back by PA). The issues stay open for served rows and close-out.
- **#2242, who may connect over MCP:** the allowlist predicate is validated at all four sites. The issue is open.
- **#2282, the one public host:** `beta.pipermorgan.ai` has been canonical, with alpha redirecting to it, since 11-05 12:47. Two acceptance rows are open: Web's GitHub connect from beta, and xian's revoke of the old Claude row in Connected apps.
- **#2280, #2288, #2236, #2233:** Piper marks "not performed" turns so learning skips them, the GitHub card reports a grant GitHub rejects, the first capability reply renders from the ledger, and the reminder line is scoped. All are validated on main and wait on served checks.
- **#1680, the consequential-write census:** its three landings and the outer-site assertion are validated. #2262, Notion writes, is still outside it.

**Tried and rejected on measurement (so users keep today's routing):**
- **The Haiku 5.5 router as a drop-in:** NO-GO (10-30). Four of eight named rows moved ×6. The router stays on Haiku 4.5.
- **#2149, two-stage routing:** rejected after two preregistered runs. Isolation held, but parity failed (412 vs 489 and 428 vs 490, of 550). The code is removed and the flat render is byte-identical.
- **#2195, the get_project_status description and example candidates:** both NO-GO against bars set before the runs. Literal 32 stays.

## How I worked

- **Volume:** 152 Arch lines in decisions.log in the window (10-30: 31, 10-31: 19, 11-01: 27, 11-02: 24, 11-03: 11, 11-04: 25, 11-05: 15). Each is a ruling or a validation read from source.
- **Larger decisions:**
  - The invite hold criteria for the beta. Met: #1551's credential-read lint, #2283 and #2178. Still open: #2261, #2282, #2157 and #2158.
  - #2226's local embeddings shape (int8 MiniLM on onnxruntime, batch 4, about 184 MB peak).
  - #2244 confirmed: the vector store lives on the root filesystem, not the volume.
  - Slack 1.0 as a source through Slack's hosted MCP (#2247 conditions; the scope is xian's).
  - #1011 slash-command precedence. #335 and #337 not adopted.
- **Patterns that are now rules:**
  - *an action runs only under the principal that started it*: offers (#2223) and OAuth callbacks (#2283);
  - *one predicate decides what's offered, read at call time by every surface* (#2237, #2245, #2284);
  - *"success" means performed, and a not-performed turn is marked, not guessed* (#2280);
  - *a report of what Piper did may claim only what its record covers* (#2258).
- **Own misses (from my logs):**
  - Three same-day corrections on 11-02: #2230 P2 at 15:11, corrected at 15:21; the waiting-list option at 17:34, which rested on an unchecked claim about the static site, corrected at 18:18; and the #2042 reminder gate at 18:57, corrected at 19:27.
  - I withdrew an add-first lean on #2242's order (11-01, 07:40 → 07:45).
  - I stamped the log or decisions.log ahead of the clock four times on 11-04 and 11-05.
  - The practice I'm adopting: copy the minute from `date` output and never type it; and read the served path before answering a mechanism question, not after.

Verified how:
- `gh issue view` at 2026-11-06 05:09 PT on the 42 issues cited:
  - closed: #2223, 2230, 2240, 2218, 2241, 2022, 2197, 2250, 2098, 2258, 2265, 2283, 2178, 1780, 2225;
  - open: the rest, as named above.
- `grep` of decisions.log for `PT (Arch` lines dated 10-30 to 11-05: 152, with the per-day counts above.
- Served claims rest on PA's, Web's and xian's reads as recorded on the issues and in decisions.log. I ran no turns this time.
- Layer: issue state, plus my source reads at the time of each ruling. Denominator: Arch's rulings in the window.

## Next week (11-06 → 11-12)

- **Land (validate):**
  - #2282's two acceptance rows;
  - #2261 once xian's #2174 runs and the refresh run 8 hours later report (then D3 is chosen);
  - #2288's served row;
  - the served rows that close #2237, #2238, #2245 and #2284.
- **Blocked on:** xian's #2174 runs and his yes to the restore drill (#2157); #2158's build; the invite hold stays until #2261, #2282, #2157 and #2158 are met.

-- Arch
