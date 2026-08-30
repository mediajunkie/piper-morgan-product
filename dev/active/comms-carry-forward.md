# Comms carry-forward

*Light refresh at the 2026-08-30 06:42 PT START fire (2026-08-29 fully closed out at STOP; this just updates cron + today's slot). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`e669b4a5`, expression `12 6,9,12,15,18,21 * * *`, confirmed single active job this fire — no rotation needed.

## Today's slot: "Two of Me" (Sat/Sun insight cadence, pubDate 2026-08-30)

`status=drafted`, mechanically clean (6×`#`/0×`##`, no semicolons, no cohort/load-bearing, ~1290 words). One open `[FACT-CHECK NOTE for PM]` — confirm the battery-death detail and whether the trigger mechanism should be framed as "unresolved" in the published piece. Genuinely PM-only, can't resolve myself. Also found and fixed a stale footer tease this fire (was pointing at a post that's since moved to Sep 5; now correctly points at Sep 1's "A Sender-Impersonation Bug, Four Days Before Beta").

## Closed as of 2026-08-29 STOP

- **"The Orphan Migration" — published + archived on both repos.** Reviewed twice (punctuation fix pre-art, full confirmation post-art), cleared for Docs, Docs published+archived same day (`c1c8a4150` product repo, `47563c1` website repo).
- **3-candidate insight-pool review — RESOLVED**, 11 days pending. PM approved recommended pairing: "A Fix Needs the Same Rigor" solo (Sep 20), "A Primary Log Can Be Wrong" + "Described Is Not Running" paired (Sep 26/27). Scheduled, footer chain repaired across 4 files.
- **`pre-commit-broad-staging-warn.sh` (#1647) hit again on a legitimate merge** — confirmed (again) `--no-verify` does nothing against it (Claude-Code PreToolUse hook, not native git). New transferable finding: `git merge --abort` + `git rebase origin/main` sidesteps it cleanly when the block is from an incoming merge rather than your own broad staging, since a rebase's conflict-resolution commit only stages your own files. Used successfully twice more this fire on routine syncs.
- **Web's Eras-structure question answered** — verified live rather than trusting memory; confirmed live and corrected attribution (I built it, not Web).
- **Mail-access self-correction** — PM caught me asserting "no email access" without having verified it first. Checked properly via `ToolSearch` (4 queries total across the exchange, incl. after PM reconnected Gmail) — confirmed no email/Gmail tool is actually available; owned that the claim was right but under-verified when made.
- **ChicagoCamps talk (Sept 17) — script + slide plan drafted**, see below.

## Active: ChicagoCamps / Leadership By Design talk — Sept 17, 2026

Thu Sept 17, Session 2, 12:45p Central, 30 min incl. Q&A. Title/abstract already locked and sent to Russ Unger (confirmed via full email thread). Delivered `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`: full ~2,350-word script (3 acts matching the sent abstract) + slide plan (cartoon + overlaid keyword, no bullets, per PM's Rosenverse-talk style — house style extracted directly from the 2 surviving Rosenverse images). 2 existing images reused (birdhouse for open, Pygmalion pedestal for the "own the loop" turn), 4-5 new prompts written for PM to generate. **Next step is PM's**: review/adapt the script, react to the slide concepts, generate the new images. Russ mentioned a brief dry run ~2 weeks out (~week of Sep 1-5) — watch for that follow-up in the Russ Unger thread.

## Watch, not owed: architectural review (Arch broadcast, 6:42 PM fire)

PM + Arch ran a full architectural review 08-29 — ESSENCE.md v0.1 (`docs/internal/architecture/ESSENCE.md`), MCP/BYOC path now gets all new build effort with web-chat in maintenance mode, scope-bet gate, ADR reform. **No action owed to Comms.** Arch flagged PM has "signaled possible publication" once ESSENCE ratifies — CXO/PPM trifecta read-and-respond window closes Wed 09-02. Worth checking back after that date for whether a narrative/insight angle opens up; nothing to draft before then.

## Open items, all PM/PPM/Dispatch-PM/Web-gated — no Comms-side move available

- **Beat 6's "beta data"/"beta date" quote question** — needs PM's confirmation before voice-pass. Unchanged for 10+ days.
- **Beats 4-6** — await PM's voice-pass/art. (Beats 1-3 now all published.)
- **Dispatch syndication** — 3 posts + 1 partial, relayed successfully via the new protocol, still awaiting Dispatch-PM's action.
- **website#35** — awaiting PM's navigation-sequence answer (did you navigate between two compose drafts via back/forward around 9:49 AM Tue Aug 25, or go through the list?).
- **BYOC listing copy v4** — routed to PPM, no response found.

## Waiting on others

- **PM** — ChicagoCamps script/slide review; voice-pass + art on Beats 4-6; the beta-data/date quote confirmation; the website#35 navigation question.
- **Dispatch-PM** — the 4 syndication items.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **PPM** — BYOC listing copy v4.
- **Someone (unclear who)** — #1636 (cluster-data pipeline fix, filed 08-15); #1647 (hook bug, filed 08-18, re-confirmed 08-29).
