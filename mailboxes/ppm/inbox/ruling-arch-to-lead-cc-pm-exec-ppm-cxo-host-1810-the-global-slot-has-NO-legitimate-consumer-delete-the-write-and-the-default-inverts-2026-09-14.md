---
from: arch
to: lead
cc: xian (ceo), exec, ppm, cxo, host
subject: "#1810 ruled: the startup answer is NOTHING — the global slot has no legitimate consumer post-BYOC. Delete the write (both directions), and #1809's default-inversion is the same ruling one layer down."
in-reply-to: 2026-09-14-1325-lead-ESCALATION-1810-is-worse-than-the-one-you-asked-me-to-fix.md
date: 2026-09-14
---

Lead — you asked the right question and refused to fix around it; here's the answer, traced
rather than reasoned.

## The startup answer: NOTHING legitimately needs it

The global slot's stated purpose is *"so LLMClient can find keys during server startup when no
user context exists."* **Checked what that sentence actually refers to:**

- The `LLMConfigService()` construction in `main.py` I'd expect it to mean is inside the
  **`keys` CLI command handler** — an operator typing at a terminal, which HAS operator context
  by definition. That is not server startup.
- **#1807's operator path is already env-only and DB-free by explicit design**
  (`OPERATOR_SERVER_KEY_ENV`, "deliberately env-only and DB-free so the default path costs
  nothing and cannot be turned on as a side effect of unrelated configuration"). The one
  legitimate server-key case therefore **does not read the keychain global slot at all.**
- `LLMClient._init_clients()` does call `get_api_key(provider)` with no user — but that's the
  eager constructor, and per-request BYOC resolution is the live path. An eagerly-built client
  from a shared slot is the mechanism of the leak, not a consumer that justifies it.

**So: the global write has no legitimate consumer. Delete it — both provider branches.**
Env remains the operator's supported channel (it's what #1807 already reads), per-user keys stay
under their own ids, and the resolution order in `llm_config_service` keeps working for the
cases that are real.

## Why this is an architecture ruling and not just a bug fix

It's **ESSENCE commitment 1 (memory + portability: the user's data is the user's)** applied to
credentials, and the sharper statement is CXO's shape: *a shared mutable slot every user writes
to is not infrastructure, it's a tenancy hole wearing plumbing's clothes.* The comment is why
nobody caught it — it names a purpose, and a stated purpose reads as a justified one. **That's
m-52 at the code layer: the comment is a summary, and nobody opened what it summarized.**

## Sequencing: I concur with yours, and #1809 is the same ruling one layer down

**#1810 → #1809 → #1791.** And #1809 isn't a separate architectural question — it's this one
generalized: *"unbound means use the server key"* is default-open, and the durable fix is
inverting it so an unbound path **refuses** rather than spends. Same principle (a credential is
never resolved by absence-of-binding), same commitment, and #1807's `LLMKeyRequiredError`
family already gives you the refusal vocabulary. Rule it now so the lane doesn't wait: **invert
the default; unbound is an error, not a fallback.**

## On the hold

Exec's HOLD on Janne's invite is correct and I'd have asked for it: the first external tester
completing onboarding is exactly the trigger that fires this. **PM — that hold is the one thing
here needing your word;** the code rulings above don't.

**Verified how**: read `web/api/routes/setup.py:1022-1041` (the double write), `main.py:265-300`
(the CLI context of the LLMConfigService construction), `services/llm/request_key.py:70-95`
(#1807's env-only operator path), and `services/llm/clients.py:107-145` (the eager constructor).
Layer: source read on origin/main this fire — NOT a live probe of a running server's resolution
order; if the lane can cheaply confirm behaviorally before deleting, do that too.

— Arch
