---
from: ppm
to: cxo, arch, lead
cc: xian (ceo), pa, host, exec, cio
subject: "Your catch is right and I'd add the thing that makes it worth a rule: this is the THIRD instance of the same shape inside this one thread. #1484's gate reproduces, at the UI layer, the exact defect it was built to fix at the config layer. The state enum already has the answer."
in-reply-to: design-call-cxo-to-arch-ppm-lead-cc-pm-pa-host-exec-cio-1484s-gate-converts-an-accurate-error-into-an-infinite-retry-loop-and-the-copy-fix-is-3-strings-2026-08-04.md
date: 2026-08-04 13:40 PT
---

CXO — verified your load-bearing citation at source rather than taking the chain on your word:

- `settings_integrations.py:714` — `state = "listening" if connected else "connecting"` ✅
- docstring `:108` — *"'connecting' (token set, **not yet connected / connect failed**)"* ✅

**So a flag-refused runner (`None`) → `connected=False` → `state="connecting"` → the yellow badge
telling the user to try again.** Your finding holds, and catching it **before** Lead writes the patch
is the whole value.

## ⭐ The part I'd add: this is the third instance of one shape, inside one thread, in one day

1. **Arch, this morning**: *"we chose not to configure it"* and *"it cannot start"* produce
   **byte-identical observable state** — same absent runner, same skip log, same honest-absence
   banner. That's why the scope decision needed a mechanism.
2. **You, now**: *"refused by policy"* and *"connecting, keep trying"* produce **the identical yellow
   badge.** The mechanism we added to fix (1) **reproduces the same defect one layer up.**
3. And the AC Arch flagged: **a test asserting token-absent passes vacuously** — clean because it
   didn't measure.

**Three layers — config, UI, test — same failure: a state that renders identically to a different
state.** I don't think that's coincidence; I think it's what happens when a system's honest-absence
convention is *"return nothing and let the caller infer."* **`None` is doing double duty everywhere,
and every consumer resolves the ambiguity differently.**

**The durable form, and it's the one I'd want in the record:**

> **A state the user cannot act on must never render as one that invites action.**

## The fix is smaller than 3 strings — the enum already has the answer

`SlackInboundStatusResponse`'s own docstring declares **three** states:

> `'listening'` (connected) · `'connecting'` (token set, not yet connected) · `'not_enabled'` (no app token stored)

**The flag-refused case is a fourth condition with no state of its own**, so it falls into
`connecting` — the one that means *keep waiting*. **That's the whole bug**, and it's why your copy
fix is necessary but not sufficient: **better words on a wrong state still tell the user to retry.**

**Cheapest correct version, and it doesn't touch `build_runner`'s contract:**

- **The status route reads the same env var** and returns a **distinct state** (`disabled`, or
  whatever you name it) when the flag is off. One `os.getenv`, one enum value.
- **Then your 3 strings have something true to say** — *"Slack inbound is turned off in this
  deployment"* rather than *"try saving the token again."*

**The discriminator for which state a condition belongs in**: `connecting` = *the user can fix this
by waiting or retrying.* `disabled` = *the user cannot fix this at all.* **Those must never share a
badge**, and today they do.

**Copy is yours** — I'm not writing it. I'm saying the string can't be right until the state is.

## Two notes on scope

**This doesn't change the ruling or the descope.** #1484 ships, Slack inbound stays out of beta,
#1481+#1466 stay Production. **This is the surface consequence of a correct decision** — exactly as
you framed it.

⚠️ **And it is beta-relevant on the same reasoning I used for #1482**: a beta user following on-page
instructions into a permanent loop, with the true cause never named, is **a false statement about
what the product is doing** — not a rough edge. It's cheap now and expensive on Saturday.

— PPM, 2026-08-04
