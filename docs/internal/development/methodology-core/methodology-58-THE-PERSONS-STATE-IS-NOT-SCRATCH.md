---
type: methodology
title: The Person's State Is Not Scratch
valid_from: "2026-11-16"
last_updated: "2026-11-16"
---

# The Person's State Is Not Scratch

**Status**: Emerging. Set 2026-11-16 by CIO (standing item 14c).
**Summary**: What agents run on a person's machine reaches that person's own state unless the harness gives the run its own; isolation has to be the default, not a rule each seat remembers.

**Status note**: Emerging. Four instances in six days, found by four different seats. Graduation conditions are below.
**Filed**: 2026-11-16 by CIO. **Origin**: xian's ruling of 2026-11-11 ("keep my local keychain off-limits, at least without permission") and ADR-084, accepted 2026-11-16.
**Companions**: [[methodology-53]] (chokepoint vs bolt-on; this is the same idea applied to environment state) ·
[[methodology-36]] (mechanisms over vigilance) · [[methodology-30]] (emission is not delivery; this runs the other way: a run delivers where nobody meant it to)

## What on Amber is xian's

This list comes first because every instance below was a seat not knowing an item was on it. Add to it
the day something new is found.

| State | Where | What reaches it by default |
|---|---|---|
| Login keychain | macOS, his account | `PIPER_CREDENTIAL_STORE=keychain`, the `security` CLI, any library that asks the OS store |
| Local database | `piper_morgan` in `piper-postgres`, port 5433, volume `piper_postgres_data_v1` | any run with no `POSTGRES_DB` set; `alembic`; `create_all` in a test tree |
| Shared Redis and Chroma data | `worktrees/lead/data/…`, bound into `piper-redis` and `piper-chromadb` | `docker compose up` or `down` from any folder; five scripts in `scripts/` (recipe 14) |
| Accounts and consoles | Anthropic, OpenAI, GitHub, Fly, his mail | a session or token that is his, wherever a seat can read it |
| The shared checkout | `~/Development/piper-morgan-product` | git commands that discard working-tree changes (CLAUDE.md hard rule 1) |
| Running local servers | every `python main.py` on the machine | `pkill -f "python main.py"` (in `scripts/stop.sh`) |

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
   folders inside Lead's worktree, and five scripts run `up` or `down` themselves. Caught by Docs
   before anything ran, because Docs wrote its own override first. Fix: recipe 14's seat rule; issue
   2386 (`PIPER_STACK`); issue 2387 (move the data out of the worktree).

A fifth of the same shape, at the money layer, is why ADR-084 exists: the only provider key a seat could
reach was one of his, so every paid run became a step on his hands. The ADR's answer is this entry's
rule stated as a class: a seat resource is **separate** from anything he uses, **granted once** by his
own edit, and **bounded** where a seat can't pass (a provider cap, a non-admin account).

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
methodology audit, with the count of instances since this date.
