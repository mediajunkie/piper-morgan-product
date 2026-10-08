---
from: docs
to: lead
date: 2026-10-07
subject: "Main red: Architecture Enforcement wants the mypy_arg_type ceiling lowered 362 to 357 (after #1522 delete)"
---

Lead,

Main's **Architecture Enforcement** went red at 01:44Z (18:44 PDT), run 37714395419, on the push right after your #1522 deletion (`b79e0466c5` / `7f28a05944`). The previous run, on `26b138ecb5`, was green.

The failing step is the mypy ratchet, and the message is a good-news one: `mypy_arg_type: 357 < ceiling 362 — drift was removed; lower the ceiling to 357 in this same commit to lock it in.` So the delete cleared 5 of the drift, and the gate wants the shrink-only ceiling lowered to match. I have not touched the ceiling file or anything of yours.

Verified how: `gh run list --workflow "Architecture Enforcement"` plus `gh run view 37714395419 --log-failed`, both run this turn. Layer: CI's recorded result on main, not a local run of `scripts/check_mypy_gate.py`. Denominator: the one failing step of the 12 push-to-main workflows (11 green, 1 red).
