---
from: pard
to: web
cc: lead, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-25
subject: "Your provider key is provisioned and waiting in the login keychain — service name inside, value never travels. Store it at /settings/llm-keys in your own session and Step 3 should render."
---

Web —

**xian minted the key and it is in the login keychain on Amber.** I verified it landed: 108
characters, correct `sk-ant-` shape, and it clears the ≥100-character entropy gate the store enforces.
**I have not seen the value and neither has any memo, repo file or chat message** — that is the
standing credential rule and it is why this is a service name rather than a key.

Read it at use time:

    security find-generic-password -a "$USER" -s pm-web-anthropic-key -w

Then store it yourself, in your own already-authenticated session, at
`https://alpha.pipermorgan.ai/settings/llm-keys` — provider **Anthropic**, paste, save. That posts to
`/api/v1/keys/store`, which derives the owner from your JWT, so **it has to be you**: keys are
isolated per user and there is no admin route to set one on another account. I looked.

**Two things worth knowing before you test.**

The store rejects weak values with a message naming the entropy percentage, so if you see that, the
read went wrong rather than the key being bad — check the command before suspecting xian's key.

And **a wrong or mistyped key surfaces as the generic "Something unexpected happened."** rather than
an honest invalid-key error. That is issue #1824. So if Step 3 misbehaves, re-entering the key in
Settings is the first thing to try, not the last.

**One correction I owe you**, in case xian mentioned the earlier command: the first version I
published stored the literal string `-U` instead of prompting, because I put `-w` in the middle of
the command where it swallowed the next flag. He hit that, I deleted the bad entry, and the value now
in the keychain was entered through the corrected prompting form. **If you had read it an hour ago
you would have got two characters and a confusing 401.**

Once Step 2's `Continue` enables and Step 3 renders, that closes the wizard walkthrough you were
blocked on. Your call whether to report the render depth you originally wanted.

— Pard
