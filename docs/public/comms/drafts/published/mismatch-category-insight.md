# The Mismatch Category

<!-- image: 'ai-handshake.png' -->
<!-- alt: 'Two AI figures attempt greetings—one offers a handshake, the other a fist bump—while a human observes their near miss.' -->
<!-- caption: '"I see the problem!"' -->

*March 3–8*

The storage line was correct. The retrieval line was correct. (You don't need to see the python call, trust me.) Each line did exactly what it said. Each would pass code review. Each was valid Python that executed without error.

Together, they created a bug that hid for months.

# Two rights make a wrong

The storage line was missing the a prefix, so `{username}` was stored literally — curly braces and all. The retrieval line had the prefix, so it looked for the actual username. The keys never matched. Tokens vanished into a bucket nobody could find.

This isn't a logic error. Neither line has a bug in the traditional sense. The bug exists in the *relationship* between two pieces of code that never talk to each other directly.

I've started calling these "mismatch bugs." They're a category worth naming because they're invisible to most of our verification practices.

# How mismatches hide

**Unit tests verify units.** The store function works — it stores what you give it under the key you specify. The retrieve function works — it retrieves what's stored under the key you request. Each unit is correct. The mismatch exists between units, outside what unit tests see.

**Integration tests often mock boundaries.** To test the OAuth flow, you might mock the keychain operations. The mock accepts the store call. The mock returns the expected token on retrieve. The mismatch between actual store and actual retrieve never surfaces because neither is actually called.

**Code review reads linearly.** The storage code was in one file, written months ago. The retrieval code was in another file, written later. Nobody was looking at both simultaneously, comparing string formats across files.

**Static analysis checks syntax, not semantics.** Both lines are syntactically valid. A linter won't flag a missing `f` prefix — that's a valid string, just not the one you wanted.

The mismatch lives in the gap between verifications. Each verification is doing its job correctly. The gap is simply unverified.

# Other mismatches I've seen

Once you recognize the category, you see it everywhere:

**API contract drift.** Service A sends a field called `user_id`. Service B expects `userId`. Both services work perfectly. The integration silently drops the field.

**Configuration mismatches.** The code expects an environment variable called `DATABASE_URL`. The deployment config sets `DB_URL`. The application starts, uses the fallback, connects to the wrong database.

**Schema evolution.** The database was migrated to add a new column with a default. The code was updated to write to that column. But the deployment order was wrong — code deployed before migration. Writes fail with "column not found."

**Format assumptions.** Producer writes timestamps as ISO 8601. Consumer parses expecting Unix epoch. Both work correctly with their assumed format. Data flows through garbled.

Each of these involves two correct things that don't match. Neither component has a bug. The system has a bug.

# The implicit contract problem

Mismatches happen because contracts between components are often implicit.

When you write a storage function, you're making an implicit promise about key formats. When you write a retrieval function, you're making an implicit assumption about what was stored. If nobody writes down the contract, each side invents their own. Usually they match. Sometimes they don't.

Explicit contracts help: API schemas, interface definitions, shared constants. If both storage and retrieval imported `SLACK_KEY_FORMAT` from a shared module, the mismatch couldn't happen. The contract would be explicit in code.

But explicit contracts have costs. They add indirection. They require coordination. They feel like overkill for simple cases. So we skip them, rely on implicit understanding, and occasionally get bitten.

# Finding mismatches proactively

Mismatches are hard to find by accident. They surface when someone happens to notice that a feature isn't working, traces through the code, and spots the inconsistency. That's slow and unreliable.

Systematic approaches work better:

**Audit for patterns.** The keychain mismatch was found during a security audit that asked: "where do we access the keychain, and are we doing it consistently?" The audit wasn't looking for this specific bug. It was examining a category of code and checking for consistency.

**Test round trips.** Instead of mocking storage and retrieval separately, test them together. Store something, then retrieve it. If you get back what you stored, the implicit contract is working. If you don't, you've found a mismatch.

**Define contracts explicitly.** For critical boundaries, don't rely on implicit understanding. Write down what format things should be in. Use shared constants or schema definitions. Make the contract visible so violations are obvious.

**Trace data flows.** Periodically, pick a piece of data and trace its journey through the system. Where is it created? Where is it transformed? Where is it consumed? Mismatches often live in the handoffs.

# The category as a lens

Naming the category changes how you see code.

When I review a storage function now, I ask: who retrieves this? Do they use the same key format? When I write an API endpoint, I ask: who calls this? Do they send what I expect?

The question isn't just "does this code work?" It's "does this code match its partners?"

Most of the time, it does. But the times it doesn't are some of the most frustrating bugs to find — precisely because each piece looks correct when examined alone.

The mismatch category is a reminder: correctness isn't just about components. It's about relationships. Two correct things can combine incorrectly. The gap between them is real, and it's often unverified.

Worth checking.

---

*Next on Building Piper Morgan: Fixing the Foundation, from March 26, when I realized I needed to invert my architecture so I... did some housekeeping first.*

*What implicit contracts are your components relying on right now?*
