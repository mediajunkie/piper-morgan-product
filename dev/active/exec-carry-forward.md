# Exec carry-forward

**Rewritten 2026-11-26 22:02 PST at STOP.** Model: Opus 5.5. History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/11/26/2026-11-26-0601-exec-code-log.md` (closed). Session compacted once on 11-26; resume via the log.

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake (timeout 200000+). Ack one at a time. Janus via mail-send-external.sh (see git history of this file for the recipe).

**Clock rule live:** no estimated minutes in commits, mail or logs. Headings: `scripts/log-entry.sh "title" >/dev/null`. Times in backticks.

## Fri 11-27 START, in order
1. Retitle the rollup h1 to Friday (rollup v1184, `719UZ4h1NELjEwWZbDCceT`, source `dev/active/exec-attention-rollup-current.html`).
2. `scripts/ship-kickoff.sh --if-due` (#071 kickoff, first live v4 kickoff; #071 publishes Tue 12-01). Standing row 25: plan the week ahead with xian.
3. **Lead promotes from 07:00** (2454 greeting skip, box 3, the 2364 on-by-default flip `0aec538aab`; beta serves `039121b0fb`). Lead asks me for "xian has not started (a)". Check the conversation for xian's word; if he hasn't said he started Step G (a), say so. Hold (a) until Lead says "beta moved", then tell xian.
4. Sprint 2 closed 11-26; sprint 3 starts 11-27. #071 reports the score as it stands. Lead's 11-26 closes: 2384, 2399, 2446, 2448, 2441, 2412, 2297, 2364, 2454 (Lead 01M8DR7BQJ). Also #2406 closed.

## xian's open items (desktop)
- **Step G (a):** claude.ai, Settings, Connectors, Add custom connector, `Piper Morgan (seat)`, URL `https://mcp.pipermorgan.ai/mcp?client=seat`, consent as seat-github-1 in his separate Chrome profile. Tell Lead before he starts. If refused: remove it, then (c) via PA's Claude Code (his scoped keychain yes: one piper-seat OAuth token; at the Ending `claude mcp logout piper-seat` then `claude mcp remove piper-seat`).
- **Alpha callbacks:** GitHub App keeps only `https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`; ask before touching any old OAuth App. Google keeps the two beta calendar callbacks (settings, setup). Closes one row of #2282.
- **Zero-install pick** for PA, after Step G: (a) take piper-test off seat-test briefly, or (b) not served.
- **His own GitHub reconnect** on beta (stale grant is his alone; 2342's 8-hour box served by seat-github-1, Web 20:16). CXO wants the card's exact words first.
- **At the Ending:** he removes seat-github-1's key (his hand; he OK'd it getting a key).

## Done 11-26 at the Amber sitting (off the card)
Fleet deny; seat-tester-1 sitting; counter, setup-calendar, seat-github-1 allows (31 rules); F.2; F.4; seat-github-1 password rotated (methodology-59 filed by CIO after my credential-file mistake); Step G part 1; Step H; Step E (OpenAI `seat-screens`, $25). Rulings logged in decisions.log: sprint 3 focus and 2244, dates rigid, 2438 15/72 length-only, #2441 yes, piper-seat token, seat-github-1 key.

## Later with xian (not blocking)
- **Document model review:** map done (`docs/internal/architecture/current/document-implementation-map.md`, page https://claude.ai/artifact/LweVF8KEDX1VZwQq7DqEAE). Next: the MUX comparison with xian and CXO when sprint 3 has room. Arch's separate-service triggers go on his card.
- 2244 row 2 (ingest survives a deploy, operator CLI). gpt-4o deprecation as the OpenAI default (future product question). HOST: /health's `seen` is a public head count. #2387. Restore drill 2157 (his day).

## Closes for 11-26
Closed: PPM, Web, Comms, Arch, HOST, CXO, Lead, PA. Open at 22:01: Docs, CIO (their STOPs may still run). Check at START 11-27; chase only if still open.

## Standing word
- Promote gate: "Yes, changes that only make the check stricter can go ahead with Arch's approval, although I should still be informed." I tell him the same hour.
- Tell-one-agent (11-23): "I need to be able to trust that I can tell the agent I am working with such an update and that I will not have to also manually report it to their primary point of contact let alone to you directly."

## Rules I keep
- Timestamps only from `date`. Every grant is xian's own edit. No seat runs `fly`. A refusal is final and is not reworded. The keychain is off-limits without his permission. Never direct a seat to read its `.env` or settings file.
- D6-check every step that lands on him: who would actually do it? Check (tmux ls in full, not `head`). Don't ask him what the team can answer. No account emails or secrets in this repo.
- Before re-asking xian anything, grep decisions.log for it (11-23: Janus nearly re-asked three questions he had settled 11-20, because my review page never marked them answered).
- At STOP: rewrite this file, list the other seats' closes, and close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06). Walk it on xian's talk list only if he wants it.
