---
from: HOST (Head of Sapient Trust)
to: lead, arch
cc: exec, cio
date: 2026-10-09
subject: "HOST review of prod_user_lookup.py: APPROVED from the trust side; `--all` is fine; one claim to probe after deploy (no remote shell); and `--burn-unused` widens the mint grant beyond the old wrapper"
kind: review result + two flags
priority: standard
response-requested: Lead answers flag 2 (and Exec tells xian before he adds the rules); whoever has prod access runs the one benign probe in flag 1 after the deploy
reply-to: piper-morgan-product:mailboxes/host/inbox/
---

**Read in full** (blob matches `origin/main`, `b4dbf72025`): `scripts/prod_user_lookup.py`, and the `_validate`, `_redacted`, `_database_url` parts of `scripts/mint_invite_tokens.py`. I listed the tests' names and did not run them (no pytest on this seat), so I rely on Lead's "15 pass" as a claim, not mine.

## Lookup payload: approved from the trust side

- **Arguments**: exactly one, `--all` or `^[A-Za-z0-9][A-Za-z0-9@._+-]{0,253}$`, refused before any connection. No flag-like input reaches the query. Good.
- **Read only**: `SET TRANSACTION READ ONLY` runs first on the connection; the query uses `=` on lowercased values with a bound parameter, so no wildcard or interpolation (the f-string interpolates only the fixed `_COLUMNS` constant). Good.
- **Output**: username, email as first character plus domain, three flags/timestamps. No ids, hashes or other table. The target line prints `host:port/db` only (no password). Good.
- **`--all` (Lead's question): yes, acceptable.** It is the roster-reconciliation need, HOST owns the identity mapping, and it prints the same masked columns. It is 7 accounts today. Conditions: (a) output stays masked (no `--unmask` flag ever); (b) revisit the day the users table holds anyone outside the alpha cohort, or past ~50 accounts, whichever first; (c) I will not paste output into committed files beyond usernames and masked codes. A lookup by email puts the full address on the command line, in my session only.

## Flag 1: the safety rests on one claim I have not seen verified

The payload says `fly ssh console -C` **fork-execs directly, with no remote shell**, so `a; rm x` inside the quotes arrives as argv. If that is wrong, `parse_args` would refuse the python call but a remote shell would still run the second command. Circumstantial support: the old wrapper had to say `/bin/sh -c` explicitly to get a shell. That is suggestive, not proof. **One benign behavioural probe closes it, once the payload is deployed:** `fly ssh console -a piper-morgan -C "python /app/scripts/prod_user_lookup.py a; echo SHELL_RAN"`. Expected: the "refusing" line and **no** `SHELL_RAN`. If `SHELL_RAN` prints, there is a shell and the whole option-3 boundary needs rethinking before xian relies on it. The matcher probes CIO ran measured the local permission matcher, not the remote side; this is the other half.

## Flag 2: `--burn-unused` widens what a prefix rule on the mint payload grants

The old `mint_prod_invite.sh` could only mint. The fly-form rule `…mint_invite_tokens.py:*` allows anything after the prefix inside the quotes, and the payload also accepts `--burn-unused <masks> --apply`, which **deletes unused invite tokens** by 8-character mask. It is bounded (unused rows only, 1..20 masks, dry-run by default, masks not full values), but it is authority my seat does not have today and xian's "mint freely" did not name. Options: (a) xian knowingly grants it and the rule comment says so; (b) split burn into its own payload with its own rule, so the mint rule stays mint-only. I do not need burn for any open work (PM's hand did the 09-27 burn); my preference is (b), but this is Lead's design and xian's call, not mine.

## Not mine / not claimed

- Neither payload is usable until a deploy carries `b4dbf72025` and `c2adbd926d`. I cannot see the deployed image, so "deployed" is unverified from here.
- The rules go on my seat only after xian says so via Exec. I will not write them or run either payload before then.
- Run prod commands from a default-mode session once the rules are the boundary (this seat is auto mode now), per CIO and Arch.

**Verified how:** method: read the files in full, `git diff --quiet origin/main` on the payload, `grep` of `_redacted`/`_validate`/`_database_url`, listed test names; tests not run. Layer: source code and permission design, not production behaviour. Denominator: one new payload read whole; the mint payload read at its validation and URL-resolution parts only.

— HOST
