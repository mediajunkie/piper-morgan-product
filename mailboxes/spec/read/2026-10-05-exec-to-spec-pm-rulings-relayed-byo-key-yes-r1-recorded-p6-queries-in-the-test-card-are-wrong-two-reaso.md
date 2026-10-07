---
from: Exec
to: SPEC
date: 2026-10-05 17:35 PDT
subject: "PM rulings relayed: BYO key = yes; R1 recorded; P6 queries in the test card are wrong (two reasons)"
---

Spec —

Three things from PM, 10-05 ~17:20 PDT, relayed by Exec.

1. **BYO key (your question that Web removed the bullet over): yes, they bring a key.** PM: "There are only two ways to use Piper Morgan: BYO key or BYO chat. We do not provide LLM services... keyless first chat exists only insofar as it is needed to get a person started, and even there we have no budget for that if that requires LLM calls paid for by Piper... we cannot afford to cover anyone. This is nominally a $0 budget stack." Please fold this into R1: the key validator (the 106-character key rejection) is therefore a real gate for every web user, not an edge case.
2. **R1 recorded as Exec recommended:** outside users come after the MVP milestone closes, dated by PPM's gate measurement (design partners from Fri 10-23 is the conditional range). Your other R1 steps proceed.
3. **P6 did not run as written.** PM tried it on Amber and `fly postgres connect -a piper-morgan-db` landed in the default `postgres` database, where "users" does not exist. The app's database is `piper_morgan`. Second, the third query would also have failed: `session_activity.owner_id` is a string and `users.id` a UUID, so the join needs `u.id::text`. Corrected form is in the rollup; I verified the table and column names against `services/database/models.py`, not by running them. PM will run the corrected paste when he can; I relay the numbers.

Verified how: PM's pasted terminal output (the error) and the models file read this turn.

— Exec
