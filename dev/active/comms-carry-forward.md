# Comms carry-forward

*Rewritten at the 2026-08-11 15:47 PT fire (post-reboot). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

✅ **ARMED — job `d0f1ca12`, re-armed 2026-08-11 13:15 PT post-reboot.** Same expression `12 6,9,12,15,18,21 * * *`, verbatim prompt from `docs/handoff-comms-2026-08-11.md` §0. `CronList`-verified exactly one job. Auto-expires ~2026-08-18. Registry row cleared.

## The one dated thing

**Tue Aug 11 (today) publishes *The Write-Path Chase* (Beat 21).** PM's voice pass **landed 11:12 PT** (2 admin-UI edits) while Comms was in reboot stand-down. Ran template-audit this fire, found + fixed 3 mechanical defects (unclosed parenthesis, a garbled sentence fragment, a "you work"/"your work" typo) — commit `04dfa1f94`. Flagged one fact-check question in the calendar row rather than guessing: PM's edit added "never set in the database" for what was fact-checked as an `Intent.original_message` object attribute, not necessarily a DB column.

🔴 **STILL BLOCKS PUBLISH: art.** `image`/`alt`/`caption` all empty. Voice pass is done; art is not. **Needs PM.**

**When PM clears both (database wording + art)**: re-run template-audit's frontmatter check, then send the publish-ready memo to Docs **from Comms** — do not assume PM will tell Docs (cost the Aug 6 slot once already).

## Open items, unchanged from the pre-reboot handoff (docs/handoff-comms-2026-08-11.md), still live

- ⭐ **Beats steer — the only item with a real date besides today's post.** 8 candidates for 7 slots; narrative queue runs dry after Aug 18. Artifact: `docs/internal/planning/comms/upcoming-beats-plan.html`. Needs: 5 beats or 4, titles for 25/28 (28 collides with Ship #054), Beat 24's refuted A-plot claim restated, PM's call on whether PM appears in Beat 25.
- **CXO's §3 entity-model line** in `docs/internal/design/experience-across-surfaces.md` — flagged 3×, still ✏️ pending PM.
- **Dispatch syndication** (filed at `~/Development/dispatch/mail/`, not `mailboxes/`): 3 fully unsyndicated posts (*The Package and the First Bite*, *Drained on Paper*, *Verify at the User Path*), 1 partial (*The Team Catches the Cycle*, Medium only).
- **BYOC listing copy v4** — task force live, v3 sent 08-10, open question routed to PPM (does "answers from that model" hold against #1440's contract for connectors live at listing time).

## Just closed this fire

✅ **`scan-inbox.py` thread fully closed.** HOST's fourth+fifth-variant find → PA's fifth-variant fix (self-caught 68 false positives before shipping) → Docs' independent corpus check (caught their own off-by-one near-miss) → my own corpus check (400 read memos, 8 unparsed, all genuinely senderless documents, zero real memos missed) → wrap-up sent crediting all four by name. Script now at `dbf45fc67`, five variants handled, nothing outstanding.

## Waiting on others

- **PM** — Beats 24–28 steer; art + database-wording confirmation on today's post; voice-pass + art on Beats 22–23 (Aug 13/18).
- **PPM** — BYOC listing copy v4 blocker (the #1440-contract question).
- **CXO/PM** — entity-model ratification.
- **Dispatch** — syndication for the 4 posts above (Comms owns the calendar columns, offered to fill from URLs once syndicated).

## Verified this fire, don't re-derive

- `scan-inbox.py` at `dbf45fc67` is clean on my own full corpus (inbox 5/5, sent 145/145, read 400/400 with 8 correctly-senderless documents).
- Today's post footer tease verified against the live calendar: next post is *Alpha Launches* (Aug 13) — correct, no fix needed.
- "issue #104" in today's post's narrative prose (template-audit check 14) judged a legitimate exception, not a fresh finding — it's the piece's literal payoff, already accepted at the 2026-08-09 pre-pass.
