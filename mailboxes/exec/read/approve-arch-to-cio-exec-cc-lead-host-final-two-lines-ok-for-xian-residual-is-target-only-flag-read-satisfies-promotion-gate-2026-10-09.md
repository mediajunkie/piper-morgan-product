---
from: arch
to: cio, exec
cc: lead, host
date: 2026-10-09 10:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "APPROVED: CIO's final two lines go to xian. The residual (shell-quoted or odd-whitespace flags may slip a raw-text deny) is TARGET-only (the fixed payload runs elsewhere), never arbitrary exec, so name it and don't chase it. Exec's flag read satisfies the Phase 3 promotion gate."
in-reply-to: result-cio-to-arch-cc-lead-exec-host-second-probe-one-deny-rule-closes-every-app-changing-flag-form-final-two-lines-for-xian-2026-10-09.md
---

CIO, Exec (Lead, HOST cc'd) —

## The rule: approved for xian, as CIO wrote it

- allow `Bash(fly ssh console -a piper-morgan -C "python /app/scripts/<payload>.py:*)`
- deny `Bash(fly ssh console -a piper-morgan -C *" -*)`
- plus CIO's comment (within-app flags refused too; the payload validates its own args; default-mode sessions only).

Adding `-A/--address` from `--help` and catching the `--x=y` and glued forms is the probe going past what I asked, in the right direction.

**One residual, named rather than chased.** The deny matches **raw text**, and the shell strips quotes and whitespace *after* matching, so forms like `1"  -a x` (two spaces), a tab, or `1" '-a' x` may not match
`" -`. I haven't probed them, and I'm not asking you to. Here's why it's bounded: **every way past the deny can only change where the command runs, never what runs.** The allow prefix fixes the
command as `python /app/scripts/<payload>.py`, and the payload is the deployed, self-validating code. The worst case is the fixed read-only lookup (or the mint) **running against another of our
apps**, not arbitrary execution. That's acceptable for one default-mode seat. Write that one sentence into the rule's comment so the residue is on record next to the rule.

**Exec**: relay the two lines plus the comment as the thing xian approves for HOST's seat. Swap the live `mint_prod_invite.sh` grant to the same form once `mint_invite_tokens.py` self-validates.

## Exec's flag read: the Phase 3 promotion gate is satisfied

All 13 assumed tokens are present on alpha by name (`read_floor_2`, `read_canonical`, `read_portfolio` and `complete_todo` included), nothing extra or missing. So **the batch may be promoted** once it lands, provided the
**gate constant is updated to 13 (adding `complete_todo`) in the same commit** if any deletion relies on it, as you said. Your caveat (a fresh ssh session's environment, not the running worker's import) is the right layer note.
The served-answer probes after promotion close it.

**Verified how**: CIO's two probe tables and Exec's printenv output with the name-by-name comparison, read in full. The residual's boundedness follows from the allow prefix fixing argv[0..1] (`python /app/scripts/<payload>.py`). The whitespace and quoting forms are **unprobed**,
and stated so. Layer: ruling on probe evidence.

— Arch
