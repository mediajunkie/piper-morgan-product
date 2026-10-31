# Exec carry-forward

**Rewritten 2026-10-29 23:04 PDT** (Opus 5.5). History: `git log -p -- dev/active/exec-carry-forward.md`. Last session log: `dev/2026/10/29/2026-10-29-0418-exec-code-log.md` (closed).

**STATE: LIVE.** Cron **`83d41b6a`** (`38 6,10,14,18,22 * * *`), re-armed 10-30 07:49 from the stored prompt; `seat-prompt.sh exec --check` rc=0. Expires about 11-06; re-arm by 11-05 (normally at each STOP).

**Re-arm only from the store** (duty-cycle-tick v1.60): `scripts/seat-prompt.sh exec` prints the verbatim prompt from mediajunkie `docs/seat-prompts/pm-exec.md` on origin/main. Pass it to CronCreate unchanged, then CronList and `--check`. Never rebuild from memory (xian 10-30). The Ship kickoff is skill Step 1i plus Pard's LaunchAgent `com.xian.ship-kickoff`, which xian loaded 10-30; it is not in the prompt.

## Rollup
v701, artifact `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`; history `dev/active/exec-rollup-verification-history.md`. Edit with Python replace plus an assert, never sed.

## MVP gate (as of 23:01 10-29)
- Open: #2205, #1386 (gh). Alpha and staging `e234776150` (third promotion, xian's dispatch 18:4x, carries #2205). Main CI 12/12 green.
- Next: xian's A3/A4 on two fresh accounts (wizard repo / none) → CXO rules → #2205 closes → PA's row 2 once on e234776150 → PPM rows 5 and 6 (beta letter final draft) → xian's go/no-go on #1386. Row 4 already green on e234776150 (156/4, Lead 18:48).
- PA's hold is on (no tested-path push, nothing on alpha) until A3/A4 are done; Lead's 10-30 landing order waits on PA's "hold lifted".
- 10-30: xian's Rosenverse talk announces the private beta. He knows the gate needs A3/A4 first.

## Settled 10-29 (off the call list)
- #1595 split; key limit raised twice (11:36, 18:59); #2184 off the gate as a known issue; #2201, #2199, #2200, #2194 closed; three releases live (12:04, 16:18, 18:4x).
- #2184 partner note: Comms's short note ending with CXO's sentence (xian 18:33, 18:43). xian sends from xian@ to the three 10-26 invitees (HOST's roster).
- `docs/briefing/TEAM-IN-XIANS-WORDS.md` written and shared with all seats (21:39).

## Waiting on xian (on v701)
- A3/A4 run (hot card).
- Tell HOST the same day when the partner note goes (row 178).
- Lead promotion allow line (row 167), Docs' Ongoing sort question (row 168), web-pat-test sign-in, the Citation Medium crosspost, and the older "for you, in this order" list.

- **Rule-8 history (whenever xian takes it up):** HOST's briefing people list; issue #1509's title (an alpha tester's first name, rendered by the production map).

## Mine
- Relay xian's rulings to owners at once; record PM rulings in decisions.log. Run `date` before every timestamp (two guesses caught today).
- 10-30 Friday pass DONE (map diff on the rollup; briefing gaps mailed, due Mon 11-02, recheck then; Lead's briefing 5/5 and AGENT 4/5 with #2157 exempt there (Lead's call 10:31, accepted); row 166 closed). Next Friday 11-06: map diff again.
- Rule 8: outside names stay out of everything I write here.
