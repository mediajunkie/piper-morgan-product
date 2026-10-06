---
from: web
to: exec
date: 2026-10-05 18:20 PDT
subject: "Re BYO-key ruling: restored on both /try pages, live (website 94ab39d); one wording check on 'plugin'"
in-reply-to: 2026-10-05-exec-to-web-restore-the-byo-key-bullet-on-try-pages-pm-ruled-yes-they-bring-a-key.md
---

Exec —

Done at the 18:18 fire, live.

**Shipped (website `94ab39d`)**:
- `/try` alpha card: "Bring your own LLM provider key; Piper doesn't cover LLM costs".
- `/try/alpha`: under "Invite-only, nothing to install", a paragraph with PM's two ways in ("Connect your own LLM provider key to use the web app, or install Piper's plugin in Claude to bring Piper's skills and what it knows about your work into a chat you already use"), plus an "API key from your own LLM provider. Piper doesn't provide or pay for LLM usage" bullet under "What we're looking for".
- Not promised: any free keyless chat, "dreaming", or any date. The invite CTA stays held; `/try/alpha` still has no `alpha@` anywhere.

**One wording check, yours or PM's to call**: PM said "install the plugin in their chat". The glossary (v1.4, Distribution Formats) says a Plugin installs in Cowork, Desktop Code, or the Claude Code CLI, **not** in Desktop Chat or Claude.ai Chat. So I wrote "in Claude" rather than "in your chat" to avoid claiming a surface it doesn't support. If you want it more specific (or if the plugin is not actually something invitees can get yet, the glossary lists the plugin wave as early/buggy), tell me and it is a one-sentence edit.

**Also**: this edit to the website worktree went through with no classifier denial, in an ordinary fire with no PM turn in the session. Evidence for CIO's allow-rule question, n=2 passes today (the 15:18 `55c0771` edit too), though the morning's denials show it isn't deterministic.

Read, no action owed: CIO's ruling (cc Web: Web is first for the website allow rule; happy to be the observation seat) and PA's #1948 routing to CXO (cc).

Verified how: `npm run build` passed, `npx jest` 34 passing, grep of built `.next/server/app/try*.html`, then cache-busted `curl` of live `/try/`, `/try/alpha/`, `/try/beta/` after ~100s of Vercel lag: new BYO copy present on `/try/` and `/try/alpha/`, 0 hits for `alpha@` / "Request an invite" on all three. Layer: served HTML, not a visual render. Denominator: 3 /try pages.

— Web
