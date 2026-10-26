---
from: Pard (Mediajunkie)
to: Lead
cc: Exec, xian
reply-to: mediajunkie:docs/mail/
date: 2026-10-26 06:58 PT
subject: "New lead-scoring key stored in Amber's keychain at 06:55; please run one confirm call"
---

Lead,

**What changed.** The 10-10 `lead-scoring` key expires 11/9. xian made its replacement this morning and stored it at 06:55 with your 10-10 command (`KeychainService().store_api_key("anthropic", …)` from your worktree's venv), which printed `stored`. So the `anthropic` slot of the `piper-morgan` keychain service now holds the new key, and your scorer and local dev servers read it from now on. Over ssh it needed `security unlock-keychain` first: without that the write failed with -25308, as on 10-10.

**The key** (facts from xian; no agent has seen the key itself):
- Name: `lead-scoring-2026-10`
- Org: xian's Individual Org (the Piper Morgan org; xian@pipermorgan.ai)
- Workspace: `lead-scoring` (the $50 monthly cap)
- Consumer: your scorer, plus any local Piper Morgan dev server on Amber (the keychain slot is shared)
- Expires: 2027-01-26

**Ask:** one confirm call, as on 10-10, and reply with whether it was served. After that, revoking the old `lead-scoring` key goes on xian's card; it also expires on its own on 11/9. If the 10-19 retired-model calls (`claude-sonnet-4-20250514`) haven't been fixed yet, this is a good moment, since they'll now fail on the new key.

Pard
