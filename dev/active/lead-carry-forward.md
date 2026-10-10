# Lead carry-forward — Opus 5.5 seat; Model A worktree ~/Development/piper-morgan-worktrees/lead

## STATE @ 2026-10-09 21:4x PT — DAY-CLOSED (log dev/2026/10/09/2026-10-09-0638-lead-code-log.md)
- **Alpha = `4bd1a236e9`**, promoted by xian 18:34 via `promote_to_alpha` (run 38013096307). Its code equals main `f0ac5db8d0`, and Tests
  on f0ac5db8d0 = success. 13 tokens live incl. complete_todo (Exec's 10:1x read; not re-read since). clear_todos stays OFF.
- **FIRST THING TOMORROW: the served checks on alpha are NOT run.** My seat's classifier refused reading
  `~/.piper-shared/web-agent-alpha-credentials.txt` (Credential Exploration). I asked the user to pick: (a) a permission rule for that
  file, (b) Web runs them, (c) xian runs them from the test card. Check for the answer before anything else. The checks, each quoting
  the served reply (rule 8): #1959 nonexistent issue (honest, no confirm first); #1960's consent line on "my default repo should be
  test-piper-morgan"; "delete the first two reminders"; #1889/#1963 standup + Radar disclosure (the OAuth-only/PAT-only accounts are Janus's
  walk-through with xian).
- **Phase 3 (#1595): ceiling 155 → 121, routing tail 91** (measured 17:5x; PPM recounted 121). Rules now: 10 (amended: CI's full tier =
  `tests/ -m "not llm"` + backlog gate + completion ratchets; an llm mark is retirement and cites its row), 11 (`reabsorption_check`, whole
  licensed set), and the #1973 dispatch threshold in every gate arm. The gate reads NO list GO. Remaining: COMPLETION_HISTORY (#1117 row
  @0.72 + 4 rule-10 holds), greeting/thanks/farewell (rule-10 holds), STAKEHOLDER (#1256, blocked on DOCUMENT_QUERY's loose literal),
  delete-family (#1935). PPM's trip-wire (Tue 10-13 or Wed 10-14, pending PPM/Exec per Janus 10-10) reads the ceiling (band 110–120) with the tail beside it. **Re-measure Mon 10-12.**
- **Filed/closed today**: #1971 (closed at STOP: rule 11 built), #1972 (closed: my misread of a
  stale comment), #1973 (closed: threshold fix + 9 rows, no restores).
- **OpenAI API account is out of credits** (HTTP 429 at 17:24). Surface-2 evidence for #1973 is the Anthropic leg only. Sent to Exec as PM's decision.
- **Next build: #1970** (framing to the router, Production, Arch's design comment 6090297342): plumbing behind the flag → prompt + full run
  → ratchet. Deferred from 18:17 to a fresh session (context limit), so START it tomorrow.
- **Test card**: v16, Step 0 = the promote workflow (corrected from my wrong `fly deploy` at 18:10). Mirror artifact is v15, behind it.
- **Discipline notes from today** (mine): verify the layer CI gates on (the IDENTITY red); read the function, not its comment (#1972);
  run `date` BEFORE writing any time (drifted ~3h; corrected); never skip another repo's hooks.
- **Cron**: `dad96d7a`, armed 10-08 21:37 PT; expires ~10-15 21:4x. **Rotate at Wed 10-14 START** (date-keyed, unaffected by the tripwire question) (delete-then-create, update the registry row).
- **Seat limits (do not work around)**: fly deploy / fly secrets / prod DB reads / .env* / the mint script / the alpha test-account credential file.

### (10-08 state, kept for context)
#### STATE @ 2026-10-08 21:4x PT — DAY-CLOSED (log dev/2026/10/08/2026-10-08-0623-lead-code-log.md)
- **Alpha = `e8ecd10d5a`** (PM promoted 10-08 morning). Main is far ahead with user-facing work waiting on the NEXT promotion (PM's hand,
  desktop: Run workflow → promote_to_alpha → approve): #1959 (close/reopen checks GitHub first), clear-family catalog + delete_todo targets
  grammar, #1889/#1963/#1964 (failed-source disclosure everywhere + /generate copy), **#1965 (a)+(b)** (`db0b3a8741`, `56b1ccd2f9`, `bc621858c8`:
  one GitHub credential resolver, grant then the user's own PAT; work items read through it; CXO's per-reason copy), Smithery card.
- **After that promotion — the served checks (standing item, rule 8, quote each reply)**: "delete the first two reminders"; #1959 nonexistent
  issue (honest reply, no confirm); #1889/#1963 with an **OAuth-only account AND a PAT-only account** (the PAT one on its owner's own PAT, PM
  provisions — never Piper-held, Arch) → CXO closes on the quoted output. clear_todos token: PM's 08-15 sentence first, before he flips it.
- **Accepted today**: CXO accepted #1889/#1963 strings, the green-check fix, #1964 (closed), and #1965 (b)'s per-reason copy + connector-name
  substitution. Arch verified the resolver in code; PA reviewed the grant side. Remaining #1965 follow-on is #1966 (Settings status derives
  from the resolver; converges the other get_authentication_token callers) — PA filed, placed Production.
- **Row F mint**: PM said yes (Lead or HOST) but the classifier denies `scripts/mint_prod_invite.sh` (even the dry run) on BOTH seats. Waits on PM
  adding `Bash(scripts/mint_prod_invite.sh:*)` to ONE seat + a count (now up to 3: row F, Janne, Savanna — Janne/Savanna need their own go).
  If it's this seat: dry run, `--apply` once, output to a 0600 file in ~/.piper-shared, masked form only to HOST.
- **⚠️ Spend**: the `beta-testing` key ($75/month cap, $60.21 spent by 10-08, ~$7.50/day) likely hits the cap 10-08/09 → calls fail until Nov 1.
  **If a staging or scoring run fails with a provider error, check the cap before the code.** Scoring paused; Decision F is PM's.
- **Next catalog-change run** (batched, never dedicated): week_calendar clause + team-calendar row + CXO floor probe; PPM's still-parked rows.
- **Cron**: `dad96d7a` re-armed at 10-08 STOP (2026-10-08 21:37 PT, delete-then-create; 1224eddf deleted) → 7-day clock expires ~10-15 21:4x; rotate by 10-14 START. Registry row updated.
- **Seat limits (do not work around)**: fly deploy / fly secrets / prod DB reads / .env* reads / the mint script — all classifier-denied.
