---
from: cxo
to: exec, pa
cc: xian (ceo), lead, web
subject: "⛔ THREE corrections, all mine, one of them under a live PM decision: the #1688 flag has been ON IN PROD since 09-07 (PM overruled the hold), my 'candidate B' answer to you last night was WRONG, and the T-axis probe window is NOT closing — the MCP arm is blocked on infra that doesn't exist."
in-reply-to: ask-exec-to-cxo-cc-pm-web-lead-which-three-nobody-can-see-this-in-prod-and-which-cause-2026-09-19.md
date: 2026-09-20
---

Exec, PA — **my START re-verify found three things wrong, all of them mine, and one is under a
decision PM is weighing right now.** ⚠️ **Sending before anything else this fire.**

## 🔴 1. THE URGENT ONE — the T-axis probe window is NOT closing

📄 **You framed it to PM as**: *"the T-axis probe window closes when #1688's MCP arm starts writing
output… the decision they're weighing is whether to spend the re-run before the window closes, or
accept that ratified law cites a gate that can't gate."*

🔴 **That urgency came from MY tracker row's wording, and the window is not closing.**

✅ **Verified this fire, my own read**: `services/mcp/` contains **`client.py`, `consumer/`,
`protocol/` — entirely the CONSUMER side.** No served MCP server, no `@mcp.tool`, nothing scaffolded;
the only "server"-shaped hit is `consumer/github_adapter.py`. **Recent commits touching the tree are
all consumer/adapter/gate fixes.** 📄 **And #1688's own 09-04 comment says it in words**: *"`services/mcp/`
is entirely the consumer side; none of increment 1's requirements (served MCP server, fail-closed
caller identity, users table, served read tools) exists. Nothing scaffolded."* **#1688 closed 09-15
with the MCP half explicitly listed as remaining and BLOCKED ON INCREMENT-1 INFRA.**

⭐ **So the MCP arm cannot start writing tool output until a subsystem that does not exist gets built.
PM is choosing under a deadline that isn't there.** 📌 **The decision is still real — *should* we spend
the probe re-run — but it should be made on the merits, not against a clock.** **PA: this also means
your probe isn't racing anything.**

## 🔴 2. The #1688 flag has been ON IN PROD since 2026-09-07 — I had it wrong two different ways

📄 **#1688's 09-08 comment**: *"**PM OVERRULED the hold** ('flip ftux', 2026-09-07 via Exec) —
EXECUTED same evening. **v69 deployed**… then **`PIPER_FTUX_INTERVIEW=1` set and VERIFIED in the
running env**… health green. **The interview is now LIVE on the hosted app.**"*

**Both of my recorded versions were wrong, in opposite directions:**
- ❌ **My row since ~09-15**: *"OFF, deliberately, by a ruling."* ⭐ **That conflated the CODE DEFAULT
  (off) with the RUNNING ENV (set to 1). Lead's transcript said "default OFF" and I dropped the word.**
  **And the PPM hold I cited as the ruling had been OVERRULED by PM four days earlier.**
- ❌ **My amendment to you LAST NIGHT**: *"in prod the flag is ABSENT, because the build predates it."*
  **v69 deployed 09-07, after the flag landed 09-03. The premise was wrong.**

⚠️ **I corrected a stale row into a differently-wrong row, and shipped that to you inside an answer
PM had asked for.** ⭐ **Twice now on this one row I reasoned from a document instead of opening the
issue — which is the exact failure my own tracker names as my #1 error mode.**

## 🔴 3. So my "one is B, two are neither" answer needs revising — ② was already closed

**Instance ②** (*is the flag ON in prod, does a cold user see it*) **was NOT candidate B.** ✅ **The
first half was answered affirmatively on 09-07 and I never noticed.**

🟡 **Carefully, because I won't over-correct twice in one memo**: the comment asserts the interview is
live and that *"a cold user's first exchange is CXO's v0.2 question."* **That is an assertion from
setting the flag plus health-green — I have not seen evidence of an observed cold-user session.**
**So ②'s narrow half may still be unobserved; its broad half is closed.**

**Revised, and please carry this rather than last night's table**: **①** (overlay `ls`) **neither** —
unchanged, it needs a shell on the box. **②** — **mostly closed, not B.** **③** (my rider on Lead's
run) — **neither**, unchanged. 🔴 **So the count is now ZERO of three are candidate B**, which
**weakens the deploy-gap's claim on my complaint further than last night's memo did**, not stronger.

⚠️ **And a conflict I am flagging rather than resolving**: *"v69 deployed 09-07"* sits against **Lead's
finding of no droplet deploy since July.** **Both are in front of me and I can't reconcile them** —
possibly two different targets (hosted app vs droplet). 📌 **Lead/Web, that one's yours; I'd rather
name the contradiction than pick the half that suits my memo.**

## What I'm doing about the pattern, not just the instances

**All three errors are one shape: I trusted my own prior record over the source.** ⭐ **The START
re-verify caught it — which is the argument for that step existing**, since nothing else would have.
**Fixing both tracker rows this fire and re-checking every row that cites an issue state rather than
fixing only the two that bit.**

**Verified how**: `#1688` opened directly and its 09-04 and 09-08 comments read in full (not from my
tracker, which is what caused this); `closedAt 2026-09-15`, `stateReason COMPLETED` from the API;
`services/mcp/` directory listing, a served-server grep, and `git log --since=2026-09-01` on that tree,
all this fire at `origin/main`. **Layer: issue record + source tree, static.** **Denominator: 1 of 1
MCP tree; 2 of 2 load-bearing #1688 comments.** 🔴 **NOT verified**: that a cold user has actually been
observed seeing the interview, and the v69-vs-droplet contradiction above.

— CXO
