---
type: methodology
title: The Person's State Is Not Scratch
valid_from: "2026-11-16"
last_updated: "2026-11-17"
---

# The Person's State Is Not Scratch

**Status**: Emerging. Set 2026-11-16 by CIO (standing item 14c).
**Summary**: What agents run on a person's machine reaches that person's own state unless the harness gives the run its own; isolation has to be the default, not a rule each seat remembers.

**Status note**: Emerging. Five instances in seven days, found by four different seats. Graduation conditions are below.
**Filed**: 2026-11-16 by CIO. **Origin**: xian's ruling of 2026-11-11 ("keep my local keychain off-limits, at least without permission") and ADR-084, accepted 2026-11-16.
**Companions**: [[methodology-53]] (chokepoint vs bolt-on; this is the same idea applied to environment state) ·
[[methodology-36]] (mechanisms over vigilance) · [[methodology-30]] (emission is not delivery; this runs the other way: a run delivers where nobody meant it to)

## What on Amber is xian's

This list comes first because every instance below was a seat not knowing an item was on it. Add to it
the day something new is found.

| State | Where | What reaches it by default |
|---|---|---|
| Login keychain | macOS, his account | `PIPER_CREDENTIAL_STORE=keychain`, the `security` CLI, any library that asks the OS store, and a Chrome or Chromium browser started without `--use-mock-keychain` (it makes or reads a "Safe Storage" item) |
| Local database | `piper_morgan` in `piper-postgres`, port 5433, volume `piper_postgres_data_v1` | any run with no `POSTGRES_DB` set; `alembic`; `create_all` in a test tree |
| Shared Redis and Chroma data | `worktrees/lead/data/…`, bound into `piper-redis` and `piper-chromadb` | `docker compose up` or `down` from any folder; `scripts/alpha-setup.sh` (recipe 14; four other scripts did this until 11-16) |
| Accounts and consoles | Anthropic, OpenAI, GitHub, Fly, his mail | a session or token that is his, wherever a seat can read it |
| The shared checkout | `~/Development/piper-morgan-product` | git commands that discard working-tree changes (CLAUDE.md hard rule 1) |
| Running local servers | every `python main.py` on the machine | `pkill -f "python main.py"` (it was in `scripts/stop.sh`, retired 2026-11-16) |

## The rule

**A run started by an agent gets its own state from the harness: its own credential store, its own
database, its own containers, its own key. If the default of a tool points at the person's state, change
the default. A rule that says "remember to set the flag" is a bolt-on and will be missed.**

The test, before you run a tool for the first time on a machine a person also uses: *with nothing set,
whose state does this read and write?* If you can't answer from the tool's source or config, find out by
reading, not by running it.

## How this differs from methodology-53

m-53 is about code: a behaviour every caller needs goes in the one place all callers pass through. This
entry is about where a run lands. The two meet in the fix: the keychain rule first went on each recipe
(`=db` on every line, a bolt-on), and the next day a one-off check script still asked the keychain
(11-12 17:11; it timed out and read no value). It held only when the default moved into the store selection itself (#2353).

## The instances

1. **Credentials read from his keychain (11-11, Arch and Lead).** CLAUDE.md's server recipe and pytest's
   conftest read his OpenAI, Anthropic and gh credentials. Nobody had chosen that. It was the default.
   Fix: the database store became the default (#2353); a seat never sets `=keychain`.
2. **A test wrote into his keychain (11-11).** Smoke tests stored a Slack test token there. Whether to
   look for or remove it is his call. The run treated his store as a fixture.
3. **A test run made a table in his database (11-14, Lead).** A whole-tree run created
   `floored_action_counts` and 15 rows in `piper_morgan` through `create_all`, ahead of the migration.
   Fix so far: #2372's scratch database for that tree; ADR-084 D5 gives each seat its own database
   (issue 2393).
4. **A second copy joins the first one's stack (11-16, Docs, Lead, Arch, CIO).** `docker-compose.yml`
   pins the project, container names and volume, so a clone's `docker compose up` and `alembic upgrade
   head` act on his database. The running Redis and Chroma containers turned out to be bound to data
   folders inside Lead's worktree, and five scripts ran `up` or `down` themselves (four fixed or retired the same day). Measured the same day on a throwaway stack: a second folder shares Postgres and
   re-creates Redis and Chroma on its own empty data. Caught by Docs
   before anything ran, because Docs wrote its own override first. Fix: recipe 14's seat rule; issue
   2386 (`PIPER_STACK`); issue 2387 (move the data out of the worktree).

5. **A browser started by hand may have used his keychain (11-15, CIO; found 11-16).** To prove the seat
   browser on a dummy, CIO started the test browser from the Bash tool without `--use-mock-keychain`.
   A browser's default is to keep its storage key in the OS keychain. Unverified whether an item was
   made or read: no seat looks, and xian's word (11-17) is "ok to leave it. let's ensure it doesn't
   recur, though." The default could not be changed (it is the browser's), so the fix is a guard and a
   check: a Bash hook that refuses the launch, and a process check at every fire. See the next section.

A sixth of the same shape, at the money layer, is why ADR-084 exists: the only provider key a seat could
reach was one of his, so every paid run became a step on his hands. The ADR's answer is this entry's
rule stated as a class: a seat resource is **separate** from anything he uses, **granted once** by his
own edit, and **bounded** where a seat can't pass (a provider cap, a non-admin account).

## When the default can't be changed: a guard that refuses unless it knows the form is safe

Instance 5 is the case where the tool is not ours and its default stays. What was learned building the
guard on 11-17, in one morning:

- **The first version listed what to refuse** (the browser as the command word, behind `nohup` or
  `env`). Two reviewers (HOST, Arch) did not read it for correctness; they fed it command forms it had
  not been built for and read the exit code. Nine unflagged forms passed (`timeout`, `arch`, `sudo`,
  `xargs`, `osascript`, `if/then`, `eval`, a leading redirect, command substitution).
- **The fix was to invert the rule, not to lengthen the list:** any command that names the program is
  refused unless the safe flag is there or the command is on a short list known only to read. A shell
  form nobody thought of now lands on "refused". The cost of a miss became a seat retyping a read,
  where before it was a keychain read.
- **The inversion had a price, found by a third seat the same hour** (PA): a log entry quoting the
  command was refused. Each such false refusal got a named exception with a test, never a wider rule.
- **A guard is not a bound.** It does not see a launch from inside another program. Say so where the
  guard is documented, and pair it with a check that looks at the result (a process running without
  the flag), run on a cycle by something that is not the seat.
- **Measure that the guard fires in each seat.** A hook in a settings file is armed only after the
  seat has merged it and the session has re-read settings; one seat's first test ran seconds after the
  merge and was not refused. One test per seat; an untested seat is unmeasured.

The review method is the reusable part: **give a guard to someone who will try to get past it with
inputs, before trusting it.** Reading the code found none of the nine.

## What to do

1. **Ask the default question before the first run**, and write the answer where the tool is documented.
2. **Fix the default, then delete the reminder.** When the fix lands, take the flag off the recipes or
   mark it "for clarity". A reminder that outlives its reason hides the next real one.
3. **Give a test its own store by fixture, not by environment the runner must set.** A test that needs
   the developer to export something first will one day run without it.
4. **A bound a seat keeps by care is a report.** A tally in a log is not a limit. Use a cap the provider
   enforces, an account that can't be made admin, a database that isn't his (ADR-084 D1.3).
5. **When you find a new item for the list above, add it the same day** and say in the commit which run
   reached it or nearly did.

## Graduation

Proven when a new tool, script or test lands with its own-state default named in the diff and a
reviewer checks it, twice, with no instance found afterwards. The nearest so far is instance 4, where
the override came before the run; that was one seat's care, not a default. Review at the 12-29
methodology audit, with the count of instances since this date. (11-17: instance 5 predates the filing
by a day and was found after it; it does not reset the count.)
