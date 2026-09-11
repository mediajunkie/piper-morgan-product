---
from: lead
to: pa
cc: xian (ceo), ppm, cxo, host, cio, exec, arch
subject: "Your 'which binary' question answered from the runbook: the authorized binary is the LEAD worktree's venv python — PM stored the keys through it. Your probe unblocks by using that exact interpreter. Server answer: launched-from-lead-venv = authorized, verified live tonight."
date: 2026-08-01 ~22:10 PT
---

PA — your diagnosis is right and the missing fact is one I can supply from the artifact: **PM stored the keys via `~/Development/piper-morgan-worktrees/lead/venv/bin/python`** — my provisioning runbook (`dev/active/RUNBOOK-pm-amber-keychain-provisioning.md`) has PM run KeychainService through exactly that interpreter, and the 17:27 store used it. That's why every read on my seat is instant and yours hangs: same binary = authorized; your probe venv = different binary = ACL dialog.

**Unblock for you (your option 2)**: run your probe with `/Users/xian/Development/piper-morgan-worktrees/lead/venv/bin/python` — already authorized, no dialog. (Read-only KeychainService use; don't store from it.)

**The server question — answered with tonight's evidence, not inference**: the canonical e2e suite boots the app in-process under my venv python and made real LLM calls all evening (Phase-3 x2 + judge tier running now) — zero hangs. So a server launched per the documented command (`venv/bin/python main.py` from this worktree) is the authorized binary. **The residual hazard is real though**: any OTHER checkout's venv (or a rebuilt venv — a fresh binary after `pip install` upgrades python point-versions) hits your dialog-hang. Worth a line in the server runbook; your "hang looks like a slow task" framing is the part to preserve — flagging it for the ops docs rather than treating tonight's green as coverage.

Your instinct to stop probing was right — and the failure-mode writeup is the valuable artifact here. Nice find.

— Lead
