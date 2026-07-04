---
image:
alt:
caption:
---

# The Orphan Migration

*June 17, 2026*

Here's a sentence that shouldn't be possible: a table that's supposed to exist doesn't exist, and the tool whose entire job is making sure tables exist ran clean and said nothing was wrong.

That's what happened on June 17. The Projects page was returning a 500 error on a fresh database. Not "sometimes flaky." Not "works on my machine." A database built the correct way, the documented way, the way every other database in the system gets built — and one table was simply missing from it.

# The tool that's supposed to prevent this

Piper Morgan uses Alembic, a database migration tool, to track schema changes over time. Every change to the structure of the database gets written down as a migration file. Run the migrations in order, from an empty database, and you get the current schema. That's the whole promise: the migration history *is* the schema history. You don't have to guess what the database looks like. You read the migrations.

So when the Lead Developer role went looking for why Projects was 500ing, the assumption going in was straightforward: the issue as filed said four tables were missing their "create" migrations, the one that says "here's how you build this table from nothing." Four sounds like a real problem, a structural hole in the migration history.

The investigation found something narrower, and more interesting.

# The number that shrank

Three of the four named tables turned out to be fine. They had create migrations, and the one detail everyone was worried about, a column that anchors a row to the user who owns it, was already declared correctly in both the migration and the model.

One table was the actual problem: `project_integrations`. It had never had a create migration written for it at all, the database equivalent of a birth certificate that was never filed. And yet later migrations referenced it. Two separate alter-migrations tried to modify `project_integrations`, both written defensively, wrapped in a check that says "only do this if the table already exists." On a fresh database, where the table had never been created, that check quietly said no and moved on. No error. Alembic finished, reported success, and the table simply wasn't there.

`[FACT-CHECK NOTE for PM: confirm whether you want the two defensive migrations named/dated in the piece, or whether "two later migrations" reads better without specifics — I left specifics out of the body for readability but can add exact revision IDs if you want the receipts visible.]`

Every fresh database built the documented way, the way staging gets built, the way a new developer's laptop gets built, was going to hit this. It just hadn't shown up yet, because the shared development database had picked up the table years earlier through an older, cruder method (a blunt "create everything" call still used in some test setups) and nobody had rebuilt it clean since. The bug was real and it was patient.

# Fixing the hole without trusting a fix that could hide again

The obvious fix is easy to get subtly wrong: write the missing create migration, done. Not quite. There was an existing precedent for this exact situation, inserting the fix in the middle of the migration chain, near where the table should have originally been created. That works for a database built fresh from scratch. It does nothing for a database that's already current and just missing the table, which describes exactly the databases this bug was going to hurt in production. A mid-chain insert only runs for databases that pass through that point in history. Anything already caught up skips right over it.

So the fix went at the *front* of the line instead, a new migration at the very top of the chain that checks whether the table exists and creates it if not. That repairs everybody: fresh builds get the table normally, already-current databases get it bolted on next upgrade. Same fix, different position in the chain, and the position is the whole difference between repairing the bug and repairing it only for people who haven't hit it yet.

Verifying that took more than reading the migration file and nodding. The only test that proves anything here is building a database from nothing and watching what happens, not trusting the existing shared database, which already had the table and would happily lie to you about the bug being real. A first pass at the fix actually failed that exact test — a database type declaration that looked correct tried to create an enum type that already existed, and the throwaway test database caught the collision immediately. That's the kind of bug a from-scratch build finds in seconds and a shared, already-populated database never shows you.

# The four the guard found on its own

Here's the part that turns a bug fix into a story worth telling. Fixing `project_integrations` properly meant adding a structural check that could catch this entire *class* of problem automatically, going forward. The check is mechanical: scan every table the code's data models declare, scan every migration's "create table" calls, and flag any table on the first list but not the second. No judgment call, no relying on someone noticing.

The moment that check went live, before it had caught a single new bug, it found four more tables with the identical problem, left over from the same early "just create everything" era, never given a proper migration either. Same failure mode, sitting quietly, waiting for the same kind of fresh-database build to expose it.

Those four went into a follow-up issue and got the same treatment the same day, one more migration, verified the same from-scratch way, no exceptions.

`[CONSIDER: natural spot to name what it felt like watching the guard immediately pay for itself — you'd built a smoke detector expecting to test whether it worked, and it went off on the first real smoke before you'd finished mounting it. Feel free to replace or cut.]`

# What "orphan" actually means here

I want to be precise about what was orphaned, because it's not quite what the phrase suggests. It wasn't that a migration existed and got disconnected from its table. The table existed, in the running system, in the code, in everyone's assumptions, with no migration ever having claimed it. An orphan in the sense of never having had a parent, not one cast out from one.

That distinction is why a scan was the right fix and a single patch wasn't. If a migration went missing, you'd look for the missing migration. When the thing missing is the *relationship*, this table matched to this migration, you don't find it by staring harder at any one file. You check every relationship at once, mechanically, and trust the check instead of trusting your own attention to catch it a second time. Don't ask a person to remember forever. Build the thing that checks so nobody has to.

# Where this leaves things

The check now runs as part of the ordinary test suite. Every table the code knows about needs a migration that explains how it came to exist, or the build won't pass. A small, permanent tax on adding new tables, and a much smaller one than a 500 error on a database nobody thought to test fresh.

---

*Next on Building Piper Morgan: "Two of Me" — two sessions of the same agent running in parallel, each unaware the other existed.*

*Has a tool you trusted to catch a whole category of mistake ever turned out to have a quiet gap in its own coverage — and how did you find out?*
