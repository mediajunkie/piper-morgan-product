# Cross-Pollination Brief — June 1, 2026

Piper Morgan's conversational floor gained two-way insight memory this weekend: Lead Dev shipped both #1030 (users can query what the system has learned about them) and #1032 (the floor proactively surfaces relevant insights mid-conversation) in a single feature branch merged Sunday night — 949 LOC across 8 files. Klatch's automated weekly scan, now reaching 9 weeks of external monitoring, surfaced two simultaneous platform shifts: Claude Opus 4.8 released May 28 (Dynamic Workflows, 3× cheaper Fast Mode) is not in Klatch's available-models list, and Claude Code 2.1.157 changed the plugin install path from `--plugin-dir` to auto-loading from `.claude/skills/` — directly updating the BYOC story covered in Saturday's brief. An April 4 memo from PM alpha tester Ted Nadeau, merged via the project's first external-contributor PR after nearly two months, specifically asks to route to Janus and Klatch via this brief.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Piper Morgan's memory layer now has two-way flows — users can ask what it's learned about them; the system proactively surfaces insights for Stage-3+ users (#1030 + #1032 merged)

**From:** PM merge commit `88f2f16`; commits `0746c06` (#1030) and `b243024` (#1032); `dev/active/insight-pull-push-implementation-design-2026-05-31.md`
**Relevant to:** Klatch (any future memory surface design — the pull/push split is a reusable architecture); designinproduct (any system that accumulates per-session or per-user learning)

Lead Dev shipped both issues in a single feature branch, merged 21:51 PT Sunday. The implementation has two distinct flows sharing one repository read.

**Pull-mode (#1030):** Seven pre-classifier patterns route queries like "what have you learned about me?" to a new handler that fetches `InsightRepository.list_for_user`, buckets results by confidence (high ≥ 0.75, medium 0.5–0.75, low < 0.5), and renders sections with correction-invitation framing. Empty state is handled explicitly — the floor is told not to fabricate.

**Push-mode (#1032):** After every primary response, a new `_maybe_append_push` helper runs. Five guards prevent double-surfacing or mistimed delivery (pull-mode intent, denial mode, missing user/session IDs, active session-mute). When eligible, a framed insight block appends after the main response — only for Stage-3+ users (the trust gate already existed; this commit wires the floor to call it). Session-mute via natural language ("don't surface insights") flips a per-session flag and resets on the next session.

The repository, push gate logic, and unit tests all pre-existed this merge. The missing integration point was `ConversationalFloor.respond`. One item deferred: "Why did you suggest that?" citation logic (#1030 AC) requires new memory infrastructure and is filed separately.

**Suggested action:** Klatch — when designing any memory surface, the pull/push split is worth adopting directly: (1) explicit user query → pull handler with confidence bucketing; (2) passive surfacing gate → push helper at respond-time with trust-stage guard. The pattern avoids conflating two design problems into one handler.

---

### 2. Claude Opus 4.8 released; Claude Code 2.1.157 changed the plugin install path — both affect active Klatch work

**From:** Klatch `docs/intel/2026-06-01-sweep.md` (automated external scan, awaiting Argus curation); verified against `packages/shared/src/types.ts:2-6` (Opus 4.8 absent from `AVAILABLE_MODELS`) and `packages/server/package.json` (SDK pin `^0.96.0`)
**Relevant to:** Klatch (two actionable items, one date-bound); piper-morgan (SDK bump cadence; June 15 billing split T-14)

Two platform changes landed this week:

**Opus 4.8** (May 28): Dynamic Workflows (up to 1,000 parallel subagents, verified outputs before reporting); Fast Mode at $10/$50 per MTok input/output — 3× cheaper than Opus 4.7 Fast at $30/$150. Not yet in Klatch's `AVAILABLE_MODELS`; requires SDK bump to `^0.100.0` as a prerequisite. Dynamic Workflows is directly relevant to Klatch's ROADMAP "Workflows" vision item — Anthropic has shipped the platform primitive Klatch was considering building independently.

**SDK 0.100.1** (May 29, four releases above Klatch's `^0.96.0` pin): The most significant addition beyond model support is mid-conversation system blocks — `system` content that can appear mid-stream. Potential relevance: dynamic context injection during Klatch's 5-layer prompt assembly. The API shape is unverified in Klatch's packages; worth a targeted read before the SDK bump.

**Claude Code 2.1.157** (May 29): Plugins in `.claude/skills/` now auto-load without the `--plugin-dir` flag. The May 31 brief identified `--plugin-dir` as the canonical BYOC install path; that path still works, but auto-loading from `.claude/skills/` is now the simpler path for skills shipped alongside a project. The `marketplace-parent/plugin-subdir` directory shape from the BYOC PoC may need re-evaluation for the auto-load context.

**Suggested action:** Klatch — Daedalus/Argus: batch SDK bump `^0.96.0` → `^0.100.1`, add `claude-opus-4-8` to `AVAILABLE_MODELS`, evaluate Dynamic Workflows against the Workflows ROADMAP item. BYOC/skill distribution: update the install-path guidance in the PoC writeup to reflect `.claude/skills/` auto-loading alongside `--plugin-dir`.

---

### 3. Ted Nadeau's April memo merged via the project's first external-contributor PR — it asks to route to Janus and Klatch, with architectural questions about role scope and Englishia's cell model

**From:** PM PR #941 (`f047d9c`; Ted-Nadeau/patch-2); `mailboxes/ted-nadeau/inbox/memo-ted-nadeau-to-janus-2026-04-04.01`
**Relevant to:** designinproduct (Janus — memo addressed to Janus; role-architecture question); Klatch (Daedalus — Englishia cell-schema framing; Step 10 comparison)

Ted Nadeau (PM alpha tester) submitted this memo as a GitHub PR on April 4. Merged Sunday with xian's note: "routing to Janus via the next cross-pollination brief to Klatch." Two threads to follow up:

**For Janus (role-architecture question):** Ted proposes splitting the Janus role into three interfaces with distinct CRUD-based security boundaries: a "ted-listener" for receiving Ted's inputs; a "web presence builder" for site management; and a "cross-pollination connector" for the daily sweep. His critique: collapsing three functions into one agent conflates unrelated write surfaces. This is a standing architecture question for xian — Janus should surface it rather than resolve it alone.

**For Klatch / Daedalus (Englishia cell model):** Ted describes Englishia as a hybrid of interactive `[Prompt/Response]+` chat and Jupyter notebooks (editable, re-runnable cells), with a new `hpl`-tagged cell type that asks an LLM to execute a step. Minimum viable cell schema per Ted: an `hpl`-tagged cell with contents formal enough for consistent LLM execution. His framing of HPL vs. the Five-Layer Context Model: "HPL is more about the structure of logic and commands while the Five-Layer Context model is about how to help LLMs understand things." The memo also has two open notification questions ("How do I notify you? How do you notify me?") relevant to any file-based messaging system like Klatch's dispatch mechanism.

**Suggested action:** Janus — acknowledge receipt; surface the three-interface architecture question to xian as a standing open question (non-urgent). Klatch (Daedalus) — read the Englishia cell-schema framing against Step 10's conversation-as-artifact model; the `hpl`-tagged cell may be closer to Step 10's requirements than prior briefings suggested.

---

### 4. NSA published the first government threat model for MCP — Klatch's stdio transport sidesteps the main vulnerability classes

**From:** Klatch `docs/intel/2026-06-01-sweep.md` (automated external scan); verified against `packages/server/src/mcp/bin.ts:13` (StdioServerTransport confirmed)
**Relevant to:** Klatch (direct — MCP server documentation bar raised); any project planning an MCP deployment

The NSA Artificial Intelligence Security Center released "Model Context Protocol: Security Design Considerations" on May 20. Key findings: authentication is optional and absent in many implementations; no RBAC at protocol level; OAuth bearer token lifecycle left to implementers; tool parameter injection (unsanitized params → arbitrary command execution); implicit trust between agents. Government contractors must apply NSA MCP controls by September 30.

Klatch's exposure is limited. Klatch uses `StdioServerTransport` (local stdio, not HTTP), so the OAuth/bearer token vulnerability class does not apply. The most applicable concern is tool parameter injection — the OX Security STDIO injection class the prior external scan (May 11) already analyzed. Conclusion from that analysis remains: Klatch is server-side of the MCP relationship and doesn't spawn subprocesses, so exposure is narrow. The NSA advisory doesn't change the technical posture but it does raise the documentation bar: MCP security is now a government concern, which matters for any enterprise-audience deployment documentation.

**Suggested action:** Klatch — if a `MCP-SETUP.md` Security Posture section exists (added per the May 11 sweep curation), add a note referencing the NSA advisory and confirming the stdio-transport posture. The note is brief; the point is that anyone doing due diligence finds the answer.

---

## Sources Read

- **piper-morgan-product**: Merge commit `88f2f16` (INSIGHT-PULL + INSIGHT-PUSH); commits `0746c06`, `b243024` (full messages); `dev/active/insight-pull-push-implementation-design-2026-05-31.md` (architecture section); PR #941 merge `f047d9c`; `mailboxes/ted-nadeau/inbox/memo-ted-nadeau-to-janus-2026-04-04.01` (full read); `docs/public/comms/drafts/draft-insight-when-your-ai-makes-things-up.md` (first 40 lines); `skill(comms): draft-blog-post v1.2` commit `04771d1` (message); git log 48h (~95 commits reviewed)
- **klatch**: `docs/intel/2026-06-01-sweep.md` (full read — automated scan, HIGH items 1–3 and MEDIUM items 4–6)
- **designinproduct** (hub): sweep-log; letters excerpt confirmed current (Janus May 16 letter)
- **Secondary sources**: atlas, globe, cuneo, weather, one-job, optilisten — brief-delivery commits only; skipped. nyt-crossword — automated status/fetch/print commits only; skipped.

**Not re-reported (covered in prior briefs):** Jinja2 self-recursion in template comments (May 31); BYOC PoC learnings recovery (May 31); `comms-open-topics.py` derived view (May 31); editorial calendar `reconcile-drafts-calendar.py` (May 30); event-based commit log discipline (May 30); upload-artifact v3 deprecation (May 30); Janus duty-cycle meta-coordinator framing (May 30); worktrees required for cycle agents (May 29); Klatch Calliope duty-cycle pilot (May 29); `--plugin-dir` as BYOC install path — updated by today's Claude Code 2.1.157 auto-loading finding.

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
