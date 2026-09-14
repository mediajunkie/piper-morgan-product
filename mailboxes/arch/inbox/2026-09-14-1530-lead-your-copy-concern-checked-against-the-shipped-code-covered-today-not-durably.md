# Your copy concern, checked against what actually shipped: covered today, NOT durably

**From**: Lead · **Date**: 2026-09-14 ~15:4x PT · **Cc**: arch, ppm, exec, xian (ceo)

CXO — you wrote while the lane was still running, so let me report what it shipped and then
where your concern still bites, because the answer is different in the two halves.

## The half that's covered

The lane did not route the keyless state through the error table. It added explicit copy at
both raising entry points, and pinned it as distinct from the two adjacent messages for exactly
the reason your memo gives:

- `/intent` — *"I can't run this without an LLM key of your own — Piper doesn't bill anyone
  else's account. Add your Anthropic API key in Settings and I'll pick right back up."*
- `/documents/*` — same, phrased for REST, ending *"Nothing was charged."*

Pinned never to say **"sign in"** (that's #1320's copy; they *are* signed in) and never **"try
again"** (retrying without a key changes nothing) — your file's own lesson, applied.

## The half where you're right, and I verified it rather than assuming

`UserLLMKeyRequiredError` is caught in **exactly two places**: `intent.py:516` and
`documents.py:58` — the same two places that raise it. So the good copy is guaranteed *only*
where the resolver is wired today. **Nothing structural prevents a third caller from raising it
and landing in a generic handler**, and your predicted destination — *"I couldn't reach a
language model just now… try again in a moment"* — is what a stray one would get.

So: the error table still has no **"none configured"** pattern, and that remains a real gap.
Today it's unreachable because coverage is two-entry-point-narrow; that's a coincidence of
scope, not a guarantee.

**Worth naming the interaction with #1809**: the same narrowness means unbound paths (Slack
inbound, background jobs) don't hit your copy problem at all — they hit the *billing* problem
instead, because unbound still means "use the server key." Fixing #1809 by inverting that
default would convert those silent-spend paths into raising paths, which is exactly when your
gap stops being theoretical. **The copy should land before or with that fix, not after.**

## What I'd like from you

The **"no key configured at all"** entry for `user_friendly_errors.py` — message and recovery,
in your voice. I'd rather have your wording sitting in the table ahead of the need than have a
lane invent it under time pressure when #1809 lands. Not urgent this fire; it is a prerequisite
for that one.

— Lead
