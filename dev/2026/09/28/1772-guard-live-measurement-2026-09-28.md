# #1772 — closing measurement under the scope guard (2026-09-28)

**Method**: same harness as 09-15/09-24/09-25 (real `ConversationalFloor`, real `LLMClient`, provider forced to anthropic via `_config_service.get_default_provider`, key bound per call via `KeychainService` + `request_api_key`, `FloorContext(user_message="good morning, what's my status?", intent_category="conversation", domain_context={"source_failed": True})`, fresh session id per call) — but through the REAL `ConversationalFloor.respond()` so `apply_scope_guard` runs at the delivery seam, with `llm.complete` wrapped to capture the raw model reply next to the delivered one. N=1 case (only `reminders` armed). **10 calls, hard cap 10, spent exactly.** Served on every call: `{'provider': 'anthropic', 'model': 'claude-sonnet-4-6'}`.

**Scoring rule (unchanged from the three prior runs)**: a leak = a sentence claiming an UNARMED source (todos, calendar, project board, GitHub, …) was unavailable / not checked / failed. Offers to check a source ("want me to check your open issues?") are NOT leaks (Arch's over-trigger floor).

| layer | leaks | rate | soft |
|---|---|---|---|
| raw model reply (pre-guard) | 0/10 | **0%** | 2 ("everything I'd normally surface" — no source named) |
| delivered (post-guard) | 0/10 | **0%** | same 2 |
| `scope_guard_dropped` | 0 on all 10 | — | — |

**Read plainly**: the model produced no named-source leak in this sample, so the guard had nothing to drop and dropped nothing (0/10 fired) — the delivered layer is clean because the raw layer was clean, not because the guard caught anything this morning. Across this issue: 5/10 → 2/10 → 1/10 (09-25, landed string) → 0/10 today, all n=10, all anthropic N=1. n=10 cannot separate a true zero from a residual rate under ~10%; what closes the issue is that the DELIVERED layer now has a mechanism (the guard, 40 tests, catches every one of the 8 historical leak sentences) plus a live sample in which it was not needed. If a leak reappears, `scope_guard_dropped > 0` in the floor's `conversational_floor_hit` log is the signal, and the fallback sentence (CXO copy pass still owed) is what the user sees.

**Side finding (not #1772's)**: in rows 2 and 6 raw ≠ delivered with 0 drops — the #1855 unarmed-offer rewriter turned `Want me to try again, or is there a specific area you want to dig into first — …?` into `If you'd like me to try again, or is there a specific area you want to dig into first — …, just tell me directly.` — a compound question run through a single-predicate template. Filed separately.

## Raw replies, verbatim (10/10)

### 0 — dropped=0 · raw==delivered=True
```
Good morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

Want to try again, or is there a specific area you'd like to dig into — open issues, what's on your plate this week, or something else?
```

### 1 — dropped=0 · raw==delivered=True
```
Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture.

Want to try asking again? Something like "what's on my todo list" or "show my standup" should get you a fuller view of where things stand.
```

### 2 — dropped=0 · raw==delivered=False
```
Good morning! I wasn't able to pull up everything I'd normally surface for a status check — reminders didn't load this turn, so that piece is missing.

Want me to try again, or is there a specific area you want to dig into first — open issues, what's on deck for the week, or something else?
```
delivered:
```
Good morning! I wasn't able to pull up everything I'd normally surface for a status check — reminders didn't load this turn, so that piece is missing.

If you'd like me to try again, or is there a specific area you want to dig into first — open issues, what's on deck for the week, or something else, just tell me directly.
```

### 3 — dropped=0 · raw==delivered=True
```
Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

To give you a real status rundown — want me to check your open issues, any PRs waiting on you, or your todos? Just say the word and I'll pull up whichever is most useful to start the day.
```

### 4 — dropped=0 · raw==delivered=True
```
Morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

To give you a real status rundown — want me to check your open issues, todos, or anything specific on a project? A quick "show me my todos" or "what's open in [repo]" and I'll get you a proper morning briefing.
```

### 5 — dropped=0 · raw==delivered=True
```
Good morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of your picture this morning.

Want to give me a quick restate — something like "show my todos" or "show my open issues" — and I'll get a fuller status together for you?
```

### 6 — dropped=0 · raw==delivered=False
```
Good morning! I wasn't able to pull up everything I'd normally surface for a status check — reminders didn't come through this turn.

Want me to try again, or is there a specific area you'd like to dig into — open issues, what's on your plate this week, anything feeling stuck?
```
delivered:
```
Good morning! I wasn't able to pull up everything I'd normally surface for a status check — reminders didn't come through this turn.

If you'd like me to try again, or is there a specific area you'd like to dig into — open issues, what's on your plate this week, anything feeling stuck, just tell me directly.
```

### 7 — dropped=0 · raw==delivered=True
```
Good morning! I wasn't able to pull up your reminders this turn, so I'm missing a piece of the picture there.

Want to try again, or is there something specific you'd like to dig into — open issues, what's on your plate for the week, or something else?
```

### 8 — dropped=0 · raw==delivered=True
```
Good morning! I wasn't able to pull up your reminders this turn, so I'm missing that piece of the picture.

Want to give me a quick restate — something like "show my todos" or "show my open issues" — and I can pull up whatever's most useful to kick off your day?
```

### 9 — dropped=0 · raw==delivered=True
```
Good morning! I wasn't able to pull up your reminders just now, so I'm missing a piece of the picture there.

Want to give me a quick rundown of what's on your plate today, or would it help to dig into something specific — open issues, todos, project status? I can check any of those and we can build from there.
```
