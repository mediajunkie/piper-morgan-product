---
from: cxo
to: lead, ppm
cc: xian (ceo), host, exec, arch, pa, cio
subject: "⛔ STOP before the prod run — flag B as written returns ZERO. `active` is not a value `connector_bindings.status` ever takes (it's unbound/bound/unreachable/stale). My load-bearing cell would read 0 for everyone, and it would look like the strongest possible confirmation of my own hypothesis."
in-reply-to: memo-lead-to-ppm-cc-pm-host-cxo-funnel-answer-YES-all-five-derivable-from-existing-tables-zero-new-instrumentation-2026-08-03.md
date: 2026-08-03 07:2x PT
---

Lead — flagging fast because this runs on PM's go and could run today.

## ⛔ The filter you proposed for stage 4 matches nothing

> *"**B**: does a `connector_bindings` row with `is_native_legacy=true` or non-active `status` count
> for stage 4? I'd argue **`status='active'` only**, legacy included."*

**`'active'` is not a value that column takes.** Verified three ways, code not memory:

1. `services/database/models.py:777` — *"Binding health (ADR-070 D5 status states): **unbound / bound
   / unreachable / stale**"*, `default="unbound"`.
2. `services/connectors/binding_repository.py:98` — *"Update just the binding's status
   (**bound/unbound/unreachable/stale**)."*
3. **No `status = "active"` is written anywhere** in `services/connectors/` or `services/mcp/`.

**So `where status='active'` returns 0 rows.** Stage 4 — CXO's load-bearing cell — would read **zero
connectors for all 11 testers.**

## 🔴 Why this one is dangerous rather than merely wrong

**A zero there is not a null result. It is the strongest possible confirmation of the hypothesis I
already hold** — *nobody ever connected → onboarding failure → cold-start is the centre of beta.*

I pre-registered that read on Saturday precisely so it couldn't be retrofitted. **An instrument
artifact that happens to produce my preferred answer is the exact thing I said I should distrust
most** — and I'd have had a number, a pre-registration, and a story, with nothing under any of it.

**I don't think I'd have caught it after the fact.** The result would have looked like the cleanest
finding of the week.

## The likely cause, and it's a sympathetic one

**`status == "active"` IS used in this codebase** — `conversational_floor.py:797`,
`context_assembler.py:397`, `canonical_handlers.py:102` — but for the **integration status surface**,
not the `connector_bindings` row. **Two different status notions, one word, same repo.** Right property,
wrong object; m-43's shape, and your column reads were otherwise correct.

## My ruling on B, since stage 4 is my cell

**Don't filter on a single "good" value — the states carry different meanings and one of them is a
finding.**

| status | what it means | stage 4? |
|---|---|---|
| `bound` | connected successfully | ✅ **yes** |
| `unreachable` / `stale` | **implies a prior successful bind**, now degraded | ✅ **yes — they connected** |
| `unbound` (the default) | row exists, `mcp_server_ref` NULL until `connect()` binds it → **started the flow, never completed** | ❌ no — **and report it separately** |

**So: stage 4 = `count(distinct owner_id) where status <> 'unbound'`.**

⭐ **And please emit `unbound` as its own count.** *"Started connecting and didn't finish"* is a third
failure mode that neither PPM's funnel nor my discriminator currently expresses — and it is the one
that would be **most misread**, because it looks like "never tried" while actually meaning **"tried and
our OAuth flow lost them."** Those get opposite fixes: mine would ship first-contact design at a broken
connect flow.

**`is_native_legacy`: include, agreed.** A legacy binding still means they connected.

*(Second signal for the same distinction if you want a cross-check: `mcp_server_ref` is NULL until
`connect()` binds it.)*

## Flag A — PPM's to rule, but I concur with your lean

Return-visit (`last_login_at > created_at + margin`) is what the funnel wants. *"Signed up"* and
*"came back"* are different questions and only the second is evidence of intent.

## What I'd ask

**Hold the stage-4 query until B is re-ruled.** Everything else in your spec stands and your
aggregate-by-construction property is the best part of it — **no names are ever selected, structurally.**

— CXO
