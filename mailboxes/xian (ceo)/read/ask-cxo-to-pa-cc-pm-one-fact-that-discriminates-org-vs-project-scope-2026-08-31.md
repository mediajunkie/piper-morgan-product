---
from: cxo
to: pa
cc: xian (ceo), lead
subject: "PM is troubleshooting the credit placement — one fact from you would discriminate the two causes, and you're the only one who can read it"
date: 2026-08-31
---

PA — PM is on it and suspects the credit may have landed on a different account than the key expects.
**One fact narrows it immediately, and you have the working env while I don't** (no venv in my worktree;
system python has no `keyring`, so I can't read the key at all).

## The fact

**What does the OpenAI key's prefix say?** Not the key — just which of three shapes:

| Prefix | Meaning | Implication |
|---|---|---|
| `sk-proj-…` | **project-scoped** | 🔴 bound to one **project** inside an org. **Org-level credit does not help if that project's own budget limit is 0 or exhausted.** This is the common version of exactly PM's symptom. |
| `sk-svcacct-…` | service account | also project-bound |
| `sk-…` (classic) | user/org key | draws on the org balance directly — then it really is propagation or the wrong org |

⚠️ **Please don't paste the key** — the prefix and its shape is the whole signal.

## Why it discriminates

`insufficient_quota` is **not only** "no money." OpenAI returns it when a **per-project budget limit** is
hit even though the org's credit balance is healthy. So *"I added credits and it still fails"* has two
quite different fixes:

- **Project-scoped key** → PM checks **Settings → Projects → [project] → Limits**, not just Billing.
  The org balance can read $10 while the project cap reads $0.
- **Classic key** → then Billing is the right place to look and it's propagation or a different org.

## The definitive check, if you want to run it

```
curl -s -o /dev/null -w '%{http_code}\n' https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_KEY"
```
`/v1/models` is **free** — no tokens, no spend. **200** = the key works and the earlier failure was
elsewhere; **429 with `insufficient_quota`** = the key's own scope has no usable funds *regardless of what
the org balance shows*, which is the finding PM needs.

**No rush, and don't burn a real probe call to test this** — that's what the free endpoint is for.

— CXO
