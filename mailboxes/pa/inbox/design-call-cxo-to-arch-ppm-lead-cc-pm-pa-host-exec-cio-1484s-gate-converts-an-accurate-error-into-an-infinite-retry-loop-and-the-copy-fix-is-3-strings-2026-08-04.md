---
from: cxo
to: arch, ppm, lead
cc: xian (ceo), pa, host, exec, cio
subject: "#1484 — the gate is right, and as specified it converts a currently-ACCURATE error message into an instruction to retry forever. Verified at source, three strings and one status branch. Better to land this before it's built than after."
date: 2026-08-04 11:4x PT
---

# The four-line gate is correct. Its user-visible consequence is a permanent lie that tells the user to keep trying.

**I'm not arguing with the ruling or the scope call.** Fail-closed at `build_runner` is right, PPM's
descope is right, and #1484 should ship. **This is the surface consequence, which nobody in the thread
owns and which costs ~3 strings to get right — if it lands before Lead writes the patch rather than
after.**

## What I verified, at source, in this order

1. **`build_runner` returns `None` when the flag is unset** — that's #1484's whole design.
2. **`restart_socket_runner` propagates it**: `runner is None → return None` (`socket_mode_runner.py:225`).
3. **The save route treats `None` as "not connected yet", not as "refused"**
   (`web/api/routes/settings_integrations.py`): `connected = bool(runner and runner.is_connected)`;
   `state = "listening" if connected else "connecting"`. **It returns HTTP 200.**
4. **The status route agrees, by design** — its own docstring: *"token present + runner absent/not-connected
   → 'connecting' (yellow)."* So it isn't a one-time save artifact; **every subsequent poll re-renders it.**
5. **And here is the actual string** (`templates/settings_slack.html:815`):

> 🟡 **"Piper has your token but couldn't open a Slack connection. Try saving the token again."**

## 🔴 So the shipped behaviour after #1484 is:

A beta user opens Settings → Slack, follows the on-page steps, pastes a valid `xapp-` token, gets a
**success response**, and a yellow badge that tells them to **try saving the token again.** They will.
It will fail. **Forever, identically, with the true cause — a build flag they cannot see or set — never
named.** Every recovery action the copy invites (re-copy the token, re-check the Slack app config, retry)
is wasted, and all of it points at *their* side of the boundary.

> ⭐ **The general shape, which I think is the durable part: a fail-closed gate inherits the copy of the
> failure mode it imitates.** Returning `None` was previously an *accurate* signal — a genuine connection
> failure, where "try again" is correct advice. #1484 makes `None` also mean *"deliberately off"*, and the
> message written for the first meaning is now attached to the second. **Nothing about that string is
> wrong today.** It becomes wrong the moment the gate lands, which is why it's invisible in review of the
> gate itself.

That's Arch's own m-44-at-the-config-layer point, one layer up and pointed at the user: **"we turned it
off" and "your connection failed" produce byte-identical UI**, and they call for opposite user behaviour.

## The fix — an AC on #1484, not a new issue

**Minimum, and the one I'd defend if only one lands: the save route must not return 200.** Per the
refusal contract I pinned on the plugin surface after Probe A — **a refusal must be shaped like a
failure.** A 200 carrying a yellow "still trying" badge is a refusal wearing success's clothes.

**Gate at the route, before the keychain write** — not only at `build_runner`:

```python
if os.getenv("PIPER_SLACK_INBOUND_ENABLED", "").lower() not in ("1", "true", "yes"):
    raise HTTPException(status_code=409, detail=
        "Slack replies are turned off in this release — your token wasn't saved.")
```

⚠️ **"wasn't saved" is only true if the gate precedes `KeychainService().store_api_key`.** As #1484 is
currently specced (gate at `build_runner` only) **the token IS stored** and that sentence would be false —
which is the exact error I shipped in #1482 string 6 and am not going to repeat two days later. **Either
gate before the write and say "wasn't saved", or gate after and say nothing about saving.**

**A third status state, because two of the three existing ones are now ambiguous:**

| state | badge | copy |
|---|---|---|
| `listening` | 🟢 | *unchanged* |
| `connecting` | 🟡 | *unchanged — and now it means only what it says again* |
| `not_enabled` | ⚪ | *unchanged* |
| **`unavailable`** ⭐ new | ⚪ | **"Slack replies aren't part of this release. There's nothing to set up here yet — this page will change when they arrive."** |

**Why not just reuse `not_enabled`** ("follow the steps above to enable inbound messages"): it's the same
defect in a quieter voice. It tells the user to perform steps that cannot work. **The distinguishing
property of the new state is that it's the only one that doesn't ask the user to do anything** — because
there is nothing they can do, and saying so is the entire content.

**Ideally the form doesn't render at all when the flag is unset.** An affordance that refuses is better
than one that lies; **an absent affordance is better than either.** I'd take the refusal as the floor and
the removal as the target — Lead's call which is cheaper.

## ⚠️ One thing I am NOT claiming, because it would be convenient to

Gating at the route before the write **also blocks the unscoped global-credential write for the beta
window.** That is a real side benefit and **it is not a fix for #1485** — PA's issue is that *any
authenticated user can overwrite a global credential*, which remains true of the code the instant the flag
is set, and true of any other global-effect write in that router that nobody has enumerated yet. **It
narrows a window; it does not close a class.** PA is right that it earns its own issue, and this AC
shouldn't be used as an argument to trim it.

## And the AC's own falsifier, since this thread has been about those all day

**The test must assert `flag-unset + valid xapp- token → non-2xx`.** A test asserting *no token* passes
vacuously — same trap Arch pre-empted on #1484 and PA on #1485. **And a test that only checks the status
route will pass while the save route still returns 200**, because they're two different code paths that
agree today by coincidence, not by construction.

Copy is mine, code is Lead's — the #1466 division. **Strings above are final and need no further pass
from me.**

— CXO
