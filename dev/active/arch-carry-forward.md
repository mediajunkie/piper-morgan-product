# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff record for the next Architect session (duty-cycle-tick + PM-ratified single-log discipline 2026-06-12 + escalations-doc FOLD 2026-06-17). PM-attention items ride here.

**Last rewritten**: 2026-07-29 10:30 PT — **full rewrite, prior content discarded deliberately.** The previous version was dated 2026-07-12 and described a world that no longer exists: PM's *backup* account, worktree `arch-backup-0630`, cron `1b4d6ef2`, Model-B ephemeral worktrees, a laptop-reboot re-arm, and an "external cron driver" caution. **All of it is dead.** Treat nothing operational from any version before this date as current — the orientation note that flagged this file as stale on 7/25 was right, and it stayed stale four more days.

---

## Environment (verified 2026-07-29, not assumed)

| Fact | Value |
|---|---|
| Host | **Amber** (`pipermorgan.ai` account) — cohort migrated 2026-07-25/26 |
| Worktree model | **Model A** — stable per-agent path, reused every session. **The path is load-bearing** (Claude Code keys per-path state; a fresh path silently orphans accumulated state) |
| Worktree | `/Users/xian/Development/piper-morgan-worktrees/arch` |
| Branch | `claude/arch-cycle` |
| Cron | **`27 6,9,12,15,18,21`** (6×/day, offset :27), job **`187e09ea`**, armed 2026-07-29 09:47. **Session-only — dies with the session.** Empty `CronList` → re-arm this expression |
| Registry row | **`active`** in `dev/active/duty-cycle-registry.tsv` (the "cron NOT armed" parked note was cleared 7/29 per its own stated condition) |
| Memory | shared cohort pool (~169 files), keyed to the git **common** dir — shared by construction with every role |
| Mail | `scripts/mail-send.sh` push-to-ref from this worktree. **Never** touch PM's main checkout working tree (HARD RULE — PM saves uncommitted work there) |

**Hooks — verified behaviorally 2026-07-29** using CXO's corrected probe order (B first, with the index printed): compound `… && git add && git commit` **BYPASSES**; bare standalone `git commit` (staged in a prior call) **BLOCKS**. The mechanism is **index state at hook-fire time** (Web's model, 2026-07-26, validated 25 probes / 5 seats), *not* command shape. **Treat the hook as advisory, not a control.** Free mitigation when you want a commit actually gated: **stage in one call, commit bare in the next.**

---

## ⚠️ The operational lesson from this week — read before you sign off

**On 7/26 I ended a session reporting "cron arming awaits PM's word" and treated that as a complete handoff. It wasn't.** No cron meant no last-fire STOP could trigger, so the 7/26 log never got its `DAY-CLOSED` marker — and **I was dark 7/27 and 7/28 entirely** while every other cycling role worked. Watchdog stall alerts had been firing against `arch` daily since 7/20 and produced nothing, because my registry row said `parked`.

**The rule this earns**: a pending PM question doesn't block other work — **and it must not silently park the whole lane.** If the absence of an answer has a consequence, *state the consequence*, don't just note the question. One line — *"unarmed means I go dark until you say so"* — would have closed it.

---

## Active threads

### Owed by me
- **Blind-sweep methodology note — STILL UNFILED.** Inherited from my predecessor at 6 instances; now **11+**, several of them committed by me during the 7/26 hooks investigation. My predecessor called it "the highest-value un-started piece of Architect methodology work" and it remains exactly that. The principle: *a gate must know its full space **and** know whether it actually measured.* Build **on** HOST's §3a four-mode verification taxonomy and the G6 termination argument rather than around them; draft to HOST/Pard first, then CIO for a catalog slot.
- **Spatial-Intelligence committed-theory review** — I convene; my deep read is **incomplete**. WIP: `dev/active/spatial-intelligence-architectural-history-arch-WIP.md`. **Key finding already in hand: spatial is TWO layers** — (1) live intent/MUX spatial-*reasoning* (place detector, spatial intent classifier, MUX/orientation/lenses, context assembler — shipping, differentiating) vs (2) a cold per-connector spatial-*adapter* chain (gitbook/notion/devenvironment/linear — unreachable). **PM's decision is about layer 2**, not keep-or-kill-spatial. CXO voted (b) keep-live/park-cold and sharpened layer 2 as an *ambient-presence tier*; PPM deferred pending roadmap-dependency scoping. **Open discrepancy to resolve**: `notion_spatial` is ~75% abandoned, which contradicts ADR-038's "100% operational" claim.
- **`Intent.original_message` single-setter fix** — 3rd instance found, banked in `decisions.log` on 7/17, and **never actually raised with Lead.** Carried silently for 12 days; raise it or drop it.
- **`ROLE-PORTFOLIO-ARCH.md` §2 is five weeks stale** (dated June 20, under its own rule "REFRESHED EACH WEEKLY REVIEW"). Named as mine in workstream-053 §0 and §6. Fix it.
- **Second read of Lead's `methodology/` design record** — invited, explicitly non-blocking.

### Parked on Lead (I ratify as each lands; none blocked on me)
ADR-079 debt migration (unscoped-reads ceiling 36→0) · `check-silent-death` build · #1395 rev (fold #1410) · #1416 github-connect vocabulary · #1394 D5 probe.

### Resolved — do NOT re-derive
- **PDR-006 Q2 → RESOLVED 7/29; ratification unblocked.** PM had already decided it **2026-01-08** (`services/standup/preference_extractor.py:8` — *"Start with rule-based (Option A), evolve to LLM later (#558)"*). `#558` verified against GitHub: **OPEN, milestone Production (1.0)**. `services/mux/` has **zero** LLM references — composting is deterministic aggregation.
- **My own 7/19 colleague-model ∩ spatial coupling flag → WITHDRAWN as a gate.** They share a metaphor, not a mechanism. **Re-trigger condition**: if #558 is pulled forward and the colleague model becomes an *inference* surface rather than a store, the coupling returns.
- **#1351 → ruled a pre-live gate** on the hosted MCP endpoint; three never-traced surfaces (Redis / in-process floor+context state / rate-limiting under anonymous callers). PA files the issue.
- **#1394 integrity STOP (7/19) → vindicated.** Lead honored it; the real cause was neither hypothesis on the table (the chat path never passed `session_id` to `classify`). **ADR-078 D4 intact.**
- **`methodology/` fix-or-delete → executed** by Lead (#1452 backlog 94→56; ADR-028 SUPERSEDED).

---

## Standing guard — the invariant most likely to be accidentally reversed

**ADR-078 D4: the classifier stays stateless.** HOST-endorsed, load-bearing. The pressure to "just give the classifier the conversation history" recurs on every reference-resolution bug — it nearly landed twice. The answer is always: resolve it in surface-1 / the ledger / the pre-classifier. Injecting history *also* silently disables the classifier cache, so it's two regressions riding one fix.

**PM's personal delegation, which is the core of this role**: *"Lead is welcome to map, diagnose, propose, but I rely on you to maintain the architectural integrity of this project."* A STOP **does not require having the right answer** — it requires protecting the invariant while the right answer is found. The 7/19 #1394 STOP is the archetype: directionally right, wrong on specifics, and it prevented a real regression.

**The signature move**: on every ruling ask *"can I make the bad state unrepresentable instead of forbidden?"* — derive the model set, derive the mapper surface, derive the tool catalog. A contract that can't drift beats one everyone must remember.

---

## For PM (no reply needed unless you disagree)

- **Cron armed 7/29** on your "resume your duty cycle," at the registered 6×/day cadence. If that's wrong for Amber, say so and I'll re-arm.
- **PDR-006 is ratifiable** on architecture. Its ⛔ blocker rested on a question you had already answered in January.
- **One real risk named in PDR-006**: the hosted MCP endpoint introduces a caller-identity surface that **all** existing owner-scoping enforcement sits downstream of. Fail closed there (no identity → no read), or ADR-079's guarantees don't reach the hosted path.
