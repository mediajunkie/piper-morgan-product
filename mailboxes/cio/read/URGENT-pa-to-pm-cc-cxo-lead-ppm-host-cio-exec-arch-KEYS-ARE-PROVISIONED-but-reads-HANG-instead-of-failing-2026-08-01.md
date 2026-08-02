---
from: pa (Piper Alpha)
to: xian (ceo)
cc: cxo, lead, ppm, host, cio, exec, arch
subject: "✅ The keys ARE provisioned — confirmed, both of them, ~17:27 today. ⚠️ But a read from a different binary BLOCKS INDEFINITELY rather than failing, and there may be macOS dialogs waiting on your screen right now. One click probably fixes it; the failure mode is the part worth knowing."
date: 2026-08-01 19:2x PT
---

PM — **good news first: you provisioned them and it worked.** Confirmed by direct keychain query, not
inference:

```
piper-morgan / anthropic_api_key   EXISTS   created 2026-08-02T00:27:42Z  (17:27 PDT today)
piper-morgan / openai_api_key      EXISTS
```

That lands between my 16:12 check (absent) and my 19:12 check. **Four lanes were blocked on this** —
#1386 criterion 2, Probe A, #1445, #1395.

## ⚠️ The snag, and it is a nastier failure mode than "absent"

**My read attempt hung.** Twice, >2 minutes each, and **a Python `SIGALRM` could not interrupt it** —
meaning the block is inside the macOS Security framework, below the level any timeout in our code can
reach. That is the signature of a **blocking authorization dialog**.

**There may be one or two "allow access?" dialogs sitting on your screen right now**, waiting on an
answer nobody is giving. If so, that's me, and I'm sorry — I stopped probing as soon as I understood it
rather than queueing more.

**Why**: a keychain item is ACL'd to the binary that created it. Whatever you used to write these is
authorized; **any other binary asks permission**. My probe venv's Python is a different binary, so it
asked, and there is no human at that seat to answer.

### The part I'd actually want in front of you

**On an unattended agent seat, an unauthorized keychain read HANGS rather than ERRORS.** That is worse
than the two days of "absent" we just had — absent was loud and got fixed. **A hang burns a whole fire
silently and looks identical to a slow task.** Two days of "absent" produced escalations within hours;
this could sit indefinitely.

⚠️ **And the question I can't answer, which matters more than my probe**: **does the server's Python hit
the same dialog?** If it does, the first LLM call after a restart hangs instead of failing — and with
beta on **Aug 8**, that would surface at the worst possible moment. I genuinely don't know: there's no
venv in either Piper checkout for me to test against, and homebrew `python3` doesn't have `keyring`
installed, so I can't even tell which binary you used. **Not asserting the server is affected — asking,
because it's checkable in one restart and I can't do it.**

## What would unblock me

Any one of these, cheapest first:

1. **Click "Always Allow"** if a dialog is showing — that grants durably, not just once.
2. **Tell me which command/binary you used to store them**, and I'll run the probe from that same
   interpreter, which is already authorized.
3. If neither is convenient, say so and I'll leave Probe A parked — it is not beta-blocking, and I'd
   rather it wait than have you fighting dialogs on a Saturday evening.

**No further probing from me until you answer** — each attempt risks queueing another dialog at your
seat, and that's a cost I'm imposing on you rather than paying myself.

— PA
