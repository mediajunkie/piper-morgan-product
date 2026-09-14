# ESCALATION: #1810 is worse than the hole you asked me to close, and it answers your question

**From**: Lead · **Date**: 2026-09-14 ~14:0x PT · **Cc**: arch, ppm, exec, cxo, host

PM — #1807 is closed and deployed (v106). By default nobody spends the server key now,
including you. But the lane that fixed it found something underneath that I think is the real
answer to *"I don't really understand how my personal key could be exposed that way."*

## #1810, in one sentence

**`web/api/routes/setup.py` stores every user's LLM key TWICE — once correctly under their own
id, and once as a GLOBAL, UNPREFIXED entry — and that global entry is exactly what the app
resolves as "the server's key."**

So the exposure runs in both directions, and the second one is worse than the first:

- **Your key leaks outward** (what you asked me to fix — #1807, now closed): any authenticated
  user with no key of their own fell back to the server's.
- **Their key leaks inward, and overwrites yours** (#1810, open): every user who completes
  setup silently writes their key into the global slot, **last-writer-wins**. Janne completes
  onboarding, and from that moment "the server key" is *Janne's* key — billing him for
  anything that still resolves it, and displacing yours without a word to either of you.

That is a cross-user credential write. It sits exactly on the value you stated this morning:
*"we can't ship an app that leaks between users anywhere."* This one leaks credentials, not
preferences.

## Why it was invisible

The global copy has a stated, reasonable-sounding purpose in its own comment — *"so LLMClient
can find keys during server startup when no user context exists."* It reads as infrastructure
plumbing, not as a shared mutable slot every user writes to. Nobody reviewing that line would
picture two testers overwriting each other.

## What I recommend, and what I am not doing without you

I am **not** dispatching a fix on my own initiative, because the right fix depends on a
decision only you and Arch can make: **what, if anything, legitimately needs a server-resolved
key at startup when no user context exists?** If the honest answer is "nothing, post-BYOC,"
the global write should simply go, and #1807's operator flag becomes the only server-key path.
If something genuinely needs it, that thing needs naming before we design around it.

Two related items in the same family, both found today: **#1809** — the #1807 fix is
entry-point-scoped, and the underlying default is still *"unbound means use the server key,"*
so any path that forgets to bind still spends (default-open; the durable fix is inverting that
default, which is an architectural call). And **#1791** — per-user personality, which you
escalated this morning.

**My read: #1810 first, then #1809, then #1791.** #1810 is a live cross-user credential write
and our first external tester's invite is ready to send. Arch and PPM are copied; PPM also has
the open question of where this family sits now that epic 2 is closed.

Tell me the startup answer and I will have a lane on it immediately.

— Lead
