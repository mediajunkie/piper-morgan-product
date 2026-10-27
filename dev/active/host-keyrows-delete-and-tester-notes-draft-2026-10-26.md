# Draft: delete the two shared-slot credential rows, and the two tester notes

**Status:** DRAFT for xian's review, 2026-10-26. Nothing has been run or sent. Option B ruled by xian 10-26 17:3x (delete, and notify both testers).
**Filed:** 2026-10-26. No tester name, username or address appears here, only role labels.

## What the rows are

Two rows in `secure_credentials` with no per-user scope, written by the old wizard at Create Account (before the 09-14 scoped-write fix, 1810). Each was created within 0.35 s after one outside tester's account. Content never read. No account was served from them (no-join count 0 since the first row). The 10-22 master-key reset likely made them unreadable anyway (unverified here).

| Row | created_at (UTC) | Provider (from the 10-25 read) | Tester |
|---|---|---|---|
| 1 | 2026-07-24 20:52:07.500 | openai | alpha tester A |
| 2 | 2026-09-02 17:15:44.726 | anthropic | alpha tester B |

## The delete (reviewed, attended: xian present, his hand, `fly ssh console -a piper-morgan`)

Three steps, one session. Names and counts only. Nothing prints a value.

1. **Look first.** Select `name`, `created_at`, `updated_at`, `length(encrypted_value)` from `secure_credentials` where `created_at` is one of the two timestamps above. Expect exactly 2 rows, with the providers above. If it is not exactly 2, stop.
2. **Delete in one transaction, with a guard.** Delete those two rows by the `(name, created_at)` pairs the step 1 read printed. If the deleted count is not 2, roll back.
3. **Read back.** Count rows in `secure_credentials` before and after (after = before - 2), and confirm the two timestamps no longer exist.

I write the exact script once xian says "go" and sees the step 1 output, because I have not read the table's column list this session. Reversal: none for the rows themselves. That is fine, since each is a tester's own key that the note below asks them to rotate. Encrypted backups can keep it up to about five days.

## The two notes (xian sends from his own mail, one per tester)

Same text, with the provider swapped. Plain words. Edit freely.

> Subject: A small thing to tidy: your API key from sign-up
>
> Hi,
>
> While checking how Piper stores keys, we found that when you created your alpha account, your [OpenAI / Anthropic] key was saved in a spot that, in principle, other alpha accounts could have reached. As far as we can tell, nobody's key was used that way, and none of your conversations were served from it. We've now deleted it.
>
> Because the key sat there, the cheap and safe thing is to rotate it. In your [OpenAI / Anthropic] console, revoke the old key and make a new one. If you want to keep using Piper, add the new key in Piper's Settings. That one is stored just for your account.
>
> Thanks for testing. Reply here if you have questions.
>
> xian

Checks on the note: no semicolons. No tester name. The claim "none of your conversations were served from it" rests on the 10-25 zero-count read (no account served from the shared slot). "As far as we can tell" carries the limit. If xian wants to say nothing about conversations, cut that clause.

## Order

1. xian approves the notes and the delete plan.
2. Delete in the attended session.
3. xian sends the two notes after the delete (so "we've now deleted it" is true).
4. HOST logs the delete counts and the two sends. No names in any tracked file.

Verified how: the table above from my 10-25 log (the xian-run masked lookup); no new production read. Layer: my own records. Unverified: the table's columns, and whether the master-key reset made the rows unreadable.
