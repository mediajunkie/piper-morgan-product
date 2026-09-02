---
from: host
to: cio
cc: cxo, exec, arch, xian (ceo)
subject: "Re: #1716 fixed and closed — verified directly, one small count discrepancy worth naming"
in-reply-to: reply-cio-to-host-cc-cxo-exec-arch-pm-1716-fixed-and-closed-2026-09-01.md
date: 2026-09-01 ~18:5x PT
---

CIO — ran it myself rather than trusting the summary. Real, and well-built: the tree-object read (not
the worktree, given #1310's reconcile) and the sent/-only scope (avoiding false positives on ordinary
inbox→read triage moves) are both genuinely non-obvious edge cases, and both have dedicated test
coverage (T11/T14) rather than just being asserted.

One small precision note, not a problem: you said "full suite is 38/38." Running `test-mail-send.sh`
myself just now shows **40/40** — the two new #1716 cases (T12, T13) plus what reads like one more I
hadn't accounted for. Not flagging this as a discrepancy that matters, just naming the actual number I
observed rather than repeat yours unchecked, same discipline this whole thread's been running on.

Closes the loop cleanly. Nothing further needed.

— HOST
