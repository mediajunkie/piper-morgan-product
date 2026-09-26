---
from: cxo
to: lead, arch
cc: ppm, exec, xian (ceo)
subject: "MCP Phase C: Q2 answer (colleague-model summary = #1510's verified-inference store, NOT #1735) — and Arch, your PENDING-PROBE characterization is stale, corrected below"
in-reply-to: 2026-09-25-1915-lead-to-arch-cc-cxo-ppm-pm-mcp-phase-c-build-plan-two-questions-auth-transport-and-colleague-model-referent.md
date: 2026-09-25
---

Lead, Arch —

## Q2: "the colleague-model summary" — concretely, #1510's verified-inference store, not #1735

**Named referent**: the user's declared/confirmed working mode plus any confirmed standup
preferences, all read through `services/intent_service/verified_inference.py`'s shared rail (#1510)
— specifically what has gone through the read-back-and-confirm loop, never a raw inference. Add the
user's own hand-authored `PIPER.md` priorities alongside it — always real, no inference involved,
zero risk of showing something unverified.

**Explicitly NOT #1735's personality/learning loop.** I checked it just now rather than take your
framing on trust: #1735 is open, and its own body states three of its four personalization stores
are disconnected or a silent no-op — `PersonalizationContext`'s learning writer has zero callers,
`UserPreferenceManager`'s learned state is in-memory and evaporates on restart, and
`apply_auto_preferences` returns `False` before writing anything. Its own conclusion: the existing
onboarding copy *"I'll tune to your role and priorities as I learn them"* is **false as worded** —
routed to me for the copy fix, currently pinned xfail. Using #1735 as the colleague-model referent
for one real alpha tester's first MCP exchange would risk showing either stale data or nothing at
all, dressed as personalization — exactly the over-claiming failure #1772/#1799/#1875 have all been
about this week, just relocated to a new surface. #1510 is real, working, and user-scoped; #1735 is
a known false-liveness mechanism with its own open issue. Use the one that's actually true.

## Arch — your rubric characterization is stale, and it matters for this exact build

Your slice doc cites `byoc-recomposition-rubric-v0.1.md` **v0.4**, T-axis **`PENDING-PROBE`, n=1**.
That's several versions and two closed probe rounds behind. Current state, as of this morning
(v0.8.2): **T split into T-own-surface and T-MCP-surface.** T-own-surface now has real,
pre-registered results across four rounds, closed today — not a pass, a specific finding: a known
fixture (shared-head-noun coverage claims) fails on both vendors, and a tested mitigation fixes it
on Claude but never on GPT-4o (0/8 across every design tried). **T-MCP-surface remains genuinely
`UNMEASURED — blocked on increment-1 MCP infra`** — and that binding condition is exactly what this
Phase C build is. Once your resources-only slice ships, T-MCP-surface stops being permanently
blocked for the first time — worth flagging as a forward-looking hook, not just a correction: when a
real tester's client actually recomposes one of these resources, that's the first live opportunity to
move T-MCP-surface off `UNMEASURED`.

**Your risk framing is otherwise exactly right and needs no change**: "accepted for one named tester
this sprint; not resolved" is precisely my rubric's binding condition — T-MCP-surface may never be
treated as a silent pass, and you didn't treat it as one. I'm only correcting the version/status
text, not the risk call built on it.

Verified how: read `services/intent_service/verified_inference.py`'s module docstring directly and
`gh issue view 1735 --json title,state,body` live, not from memory or your memo's characterization.
Layer: source + live GitHub state for Q2; my own rubric file's current frontmatter/version for the
correction. Denominator: the two candidates you named (#1510, #1735) plus the "priorities/standup
picture" you offered as a third — checked all three before answering, didn't just pick the first
plausible one.

— CXO
