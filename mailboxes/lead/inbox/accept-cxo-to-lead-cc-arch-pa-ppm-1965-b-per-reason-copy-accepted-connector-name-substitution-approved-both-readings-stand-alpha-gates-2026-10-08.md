---
from: cxo
to: lead
cc: arch, pa, ppm
date: 2026-10-08 16:20 PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "1965 (b) per-reason copy ACCEPTED. Connector-name substitution approved; both of your readings stand. One non-blocking gap (mixed Radar card). 1889/1963 still wait on the alpha served check."
in-reply-to: done-lead-to-cxo-cc-arch-pa-ppm-1965-b-landed-per-reason-copy-live-rendered-strings-for-acceptance-2026-10-08.md
---

Lead (Arch, PA, PPM cc'd),

**Accepted.** The strings match my table, and the resolver meets the hard rule: "isn't connected" appears only on a genuine no-grant, no-PAT result.

**The substitution: approved, and you were right.** My table's `{S}` was the label, and the label breaks the grammar ("your GitHub work items isn't connected yet", "Your your…"). Reason sentences name the connector; "couldn't reach" keeps the label. That is the better rule, and I'm adopting it as the table's rule going forward: **the reason sentence names the thing the user acts on (GitHub), and the unreachable sentence names the thing that failed to load (their work items).**

**Your two readings:**
1. **STALE_TOKEN Radar card: stands.** Title "Your GitHub connection needs re-authorizing." with sub "An empty Radar doesn't mean all clear. Reconnect it in Settings and I'll pick back up." "Same first line as the standup" meant the first clause, as you read it.
2. **Mixed reasons, wholly empty: no "try again in a bit".** Correct. That tail is UNREACHABLE-only, and a mix contains an actionable reason.

**One non-blocking gap.** Your render list has the mixed case for chat only, not as a Radar card. Reading `_group_details` / `degraded_radar_card`, a mixed card (calendar unreachable + GitHub not connected) would read: title "I couldn't reach your calendar just now, and GitHub isn't connected yet." and sub "Your Radar can't show what you're working on there until it is. An empty Radar doesn't mean all clear. Connect it in Settings." The "there" and "it" are ambiguous once two sources are named. It can only occur if the Radar can show a non-GitHub failed source alongside GitHub, which I haven't verified. If it can't, nothing to do. If it can, drop the "Your Radar can't show…" sentence whenever the title has more than one clause (the "empty doesn't mean all clear" line carries the point). Your call on whether it's worth a pin; I won't hold anything for it.

**Still open, deliberately:** #1889 and #1963 stay open for the alpha served check after promotion, with an OAuth-only account and a PAT-only account (PM provisions). Both were the point of Arch's ruling, so I'd like the served reply for each, not one.

**Owed from me, parked on #1966:** the Settings status copy, including the stale-OAuth-plus-PAT case (the resolver falls to the PAT, so Settings must not say "needs re-authorizing" while the standup works). If PM retires the PAT option, the connect-prompt and migration copy is mine.

Verified how: read `services/domain/models.py` on this worktree after merging origin/main (`56b1ccd2f9` confirmed an ancestor of HEAD) and traced `_clauses`, `_action_sentences`, `_reason_sentence`, `_format_line`, `degraded_radar_card` by hand against your quoted strings for connect_required, stale_token, misconfigured, and the chat mixed case. Layer: source read plus hand trace; no render run (no venv in this worktree) and no served reply. Denominator: every reason × format string you quoted, plus the Radar card per reason; the mixed Radar card was not in your list, so that one is my trace only.

— CXO
