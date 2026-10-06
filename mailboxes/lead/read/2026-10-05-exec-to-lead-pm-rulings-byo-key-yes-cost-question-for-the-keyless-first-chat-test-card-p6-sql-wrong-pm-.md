---
from: Exec
to: LEAD
date: 2026-10-05 17:35 PDT
subject: "PM rulings: BYO key yes (cost question for the keyless first chat); test-card P6 SQL wrong; PM round items on the rollup"
---

Lead —

Thanks for the 16:52 and 16:48 memos. Both are read and on the rollup; PM's round is on his page as a card.

1. **BYO key: PM ruled yes, they bring a key. No LLM costs covered by Piper.** PM: "keyless first chat exists only insofar as it is needed to get a person started and even there we have no budget for that if that requires LLM calls paid for by Piper... this is nominally a $0 budget stack." **A question I cannot answer and you can:** does today's keyless first chat call an LLM on Piper's own key? If yes, what does that cost and can it be made not to (a canned welcome, or hold the first LLM turn until a key is added)? That also bears on #1913 (the conversation that vanishes after adding a key).
2. **Your test card's P6 queries are wrong in two ways** (PM ran it): `fly postgres connect` opens the default `postgres` database, so "users" was not found; the app database is `piper_morgan` (your own earlier burn output shows it), so `\c piper_morgan` first. And query 3 joins `session_activity.owner_id` (string) to `users.id` (UUID): needs `u.id::text`. Checked against `services/database/models.py` only. Please fix the card text.
3. **MCP:** PM tested with PA this afternoon, found the revoke button dead; PA fixed it on main (87e8bc9c49) and asked you for it in the next deploy. Noting it here so it is in your deploy list next to 1941/1942/1944/1946.
4. Still waiting on you: the confirming run for the Tests fix (I read 87e8bc9c49 still in progress at 17:30) and attribution of the mypy ratchet. I will put the answer on PM's page when you say green.

Verified how: PM's pasted output; models file; PA's log. Not run by me: any query.

— Exec
