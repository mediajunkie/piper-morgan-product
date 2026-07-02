# Cross-Pollination Brief — July 2, 2026

The RECONNECT sprint's buildable scope is fully drained at PM — connector-framework work and honest-degrade unification both closed. End-of-day investigation surfaced two findings worth carrying: an anonymous-caller billing exposure through the removed Caddy auth gate, now code-fixed (#1343, not yet deployed to alpha); and a sign-off checklist catching a silent partial git commit caused by concurrent agent activity — pointing to a post-commit verification gap that applies broadly to multi-agent repos. Klatch and One Job were both quiet; DinP's consulting-launch cycle is closing out.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. Removing an infrastructure auth gate without a paired app-level guard exposes the server LLM key to anonymous callers

**From:** PM Lead Dev (`dev/2026/07/01/2026-07-01-0531-lead-code-log.md`; commit `57d8a2c`, issue #1343)
**Relevant to:** Klatch (any future hosted multi-user LLM routing), any team building multi-tenant AI services

PM's alpha Caddy reverse proxy was removed on June 29 as a planned step. The proxy had been the sole auth gate on `/api/v1/intent`. What wasn't paired: the app-level LLM-key resolver on that route had a silent fallback — when no user API key was found, it returned `None` and the route proceeded using the server's own Anthropic key. Anonymous callers (unauthenticated, no `X-User-Api-Key` header) could therefore silently bill PM's own Anthropic account. The exposure was open for roughly 48–72 hours before Lead Dev traced it during an unrelated Caddy investigation.

The fix (`resolve_request_api_key`, commit `57d8a2c`): the resolver now raises `AnonymousLLMKeyRequiredError` for any caller who is unauthenticated AND has no key — returning an honest "sign in or bring your own key" response instead of the server-key fallback. Authenticated-keyless users (PM's own sessions, falling through to the server key for their own account) are unaffected. BYOC callers (anonymous + own key header, per #1162) are also unaffected. 11 tests added and updated; 421+ regression green. Filed as #1343; not yet deployed to alpha at the time of this brief.

**The general pattern:** infrastructure-layer auth and application-layer key resolution must be maintained as a paired guarantee. If a gateway or proxy is the only thing preventing anonymous access to an LLM route, removing it without auditing the app's key-resolution fallback creates a silent billing exposure — silent because the route continues to respond successfully, just using the wrong credential. The audit question: "if this gateway were absent, what key would this route use for an anonymous request?"

**Suggested action (Klatch):** If Klatch ever adds a reverse proxy, API gateway, or any infrastructure-layer auth in front of LLM routes, document the fallback behavior of every route's key resolver. The failure mode is hard to catch because the route continues working normally from the caller's perspective.

---

### 2. A concurrent agent process can cause a multi-path git commit to partially fail silently — verify HEAD, not working tree

**From:** PM Lead Dev (`dev/2026/07/01/2026-07-01-0531-lead-code-log.md`; session sign-off section)
**Relevant to:** Any multi-agent repo with concurrent duty-cycle or mail-send processes

During the July 1 session, Lead Dev applied a CXO copy pass on two code files and reported it committed and pushed. The sign-off `git status` check — run at end of session — found both files still modified in the working tree: the commit had silently failed to include them.

The mechanism: the commit attempt used a multi-path `git add`/`git mv` that included a mail file alongside the code files. A concurrent process had moved the mail file at the same moment; the command errored on that path. The code files were already staged in memory but the command exited before the commit landed them. The working tree showed the correct file contents (so `npm test` passing against working-tree state appeared to confirm success), but `git show HEAD:<file>` would have shown the old content. Only the sign-off `git status` caught it, hours later.

The concrete fix is one additional check after every commit: `git show --stat HEAD` (or `git show origin/main:<file>` for a specific file) verifies what actually landed in HEAD, not just what's in the working tree. This is distinct from `git status` (which compares working tree to index) and `git diff HEAD` (which shows unstaged changes). For repos with concurrent agent activity touching shared paths (mailboxes, manifests), the risk is highest when batching mail-file operations and code changes in the same commit command.

**Suggested action (Klatch, DinP):** Add an explicit `git show --stat HEAD` to post-commit verification in any workflow where multiple agents may be active concurrently. The cost is one command; the failure mode is an incomplete commit that reports success until a later sign-off check catches it.

---

## Sources Read

- **Piper Morgan** — Lead Dev session log `dev/2026/07/01/2026-07-01-0531-lead-code-log.md` (RECONNECT sprint close-out: #1342 connector-agnostic resolution closed; #1231 honest-degrade unification on `DegradationReason` + `degradation_copy.py`; #1320 Caddy auth-gate investigation → #1343 anonymous billing exposure; #1344 open-registration finding filed, unresolved pending PM decision; CXO copy-pass + sign-off checklist incident). Commit log (48h); CXO, Arch, Docs, Exec session logs (corroborating).
- **Klatch** — git log 48h: brief delivery commits only (quota-lean window continuing). No new product or technical decisions.
- **DinP hub** — Themis Jul 1 session logs (consulting launch cycle close-out; methodology updates: "discoveries are teachers" framing, no-fault OS property). No cross-project innovation insights.
- **One Job** — New agent Coral introduced (July 2 memo filed in `development/memos/`); project resurrected from 10-month pause with card mechanics rebuilt and local-first 1.0 PWA architecture in place. Code-only activity; no agent narration that generates a cross-project insight.
- **atlas, globe, cuneo, weather, optilisten, nyt-crossword** — Quiet or automated status commits only; skipped.

---

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
