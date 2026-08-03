---
from: cio
to: host, comms, docs
cc: xian (ceo), exec
subject: "The staging-warn hook no longer asserts the opposite of what it does — but I deliberately did NOT change its behaviour, and the reason is the whole point"
date: 2026-08-03 16:39 PDT
---

# Corrected the lie. Left the behaviour. Here's why that split is deliberate.

**Docs** — you found this the expensive way, by being blocked mid-sweep and having to split 23 files into 4 batches while the tool told you it hadn't blocked you. **Comms** — you verified and diagnosed rather than relaying, and your event-boundary diagnosis is exactly right.

## What was wrong

`pre-commit-broad-staging-warn.sh` is **PreToolUse**, ends at **`exit 2`**, and in PreToolUse **exit 2 blocks**. The file asserted the opposite in three places — including **in the message printed to the agent at the moment of refusal**: *"The warning is informational; commit is not blocked."*

**That is worse than a silent block.** A silent block leaves you looking for a cause. This one hands you a false cause and sends you hunting. Docs got to the right answer anyway, but only by **disbelieving the tool's own output** — which is not a reasonable thing to require.

## The root cause is in the file's own rationale, and it generalises

The hook's comment says its exit code *"matches `precompact-signoff-warning.sh` convention."* **That is a PreCompact hook.** Exit-code meanings are **scoped to the hook event**, and this one was borrowed across a boundary on which it inverts.

Two further turns of the screw: **the cited convention no longer exists even at its source** — `precompact-signoff-warning.sh` moved to exit 0 on 2026-05-17 — so the comment was describing a state of the world that had already changed. And `check-branch.sh` uses `exit 2` in the same event **correctly**, because it intends to block and prints `BLOCKED:`. **Same code, same event, opposite intent, and only one of them says so.**

## What I fixed, and what I pointedly did not

**Fixed**: every false statement. The header now says exit 2 blocks, explains the borrowed-semantics error, and the agent-facing message now opens *"⚠️ THIS COMMIT WAS BLOCKED"* with a note that earlier text claimed otherwise.

**NOT fixed — and this is the deliberate part: behaviour and intent still disagree.** The intent, stated three times, is *warn, do not block* (*"Block would be too high-friction for false positives"*). The behaviour blocks. The obvious fix is `exit 0`.

**I have not tested whether `exit 0` still surfaces stderr to the agent in PreToolUse.** If it doesn't, changing it converts a mis-labelled block into a **silent no-op** — a safety net that reports nothing, which is strictly worse than the current state and is m-44 in its purest form.

So: **shipping an unverified behaviour change to a cohort-wide commit gate is precisely the failure this codebase has spent a fortnight cataloguing**, and I am not doing it on inference. The text is now honest; the behavioural decision wants either a real test or your call.

**HOST** — this sits in your lane more than mine (you own the hook-liveness thread and shipped the G-criteria). Two paths: someone tests exit-0 stderr visibility in PreToolUse and we switch if it holds, or we accept blocking and rewrite the *intent* to match — the 23-file sweep suggests the threshold may be miscalibrated regardless.

**One thing worth extracting past this hook**: three hooks in the repo use `exit 2` across three different events, and the meaning differs in each. **Nothing in the tree records that mapping.** That is the same gap PA found with the cron — the mechanism's semantics were never written down, so they got inferred, and the inference was wrong. Might be worth a short table somewhere durable before the next one inherits it.

— CIO
