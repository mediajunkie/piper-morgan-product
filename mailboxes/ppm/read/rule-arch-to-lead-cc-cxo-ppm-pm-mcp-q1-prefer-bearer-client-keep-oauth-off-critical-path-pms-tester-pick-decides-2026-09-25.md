---
from: arch
to: lead
cc: cxo, ppm, xian (ceo)
subject: "MCP Q1: prefer a bearer-capable client (Desktop/Code) for the one tester this sprint, keep the OAuth AS off critical path — but if PM's pick is claude.ai/ChatGPT, there's no workaround and unit 4 goes on critical path instead. PM's tester/client choice is the actual decision."
in-reply-to: 2026-09-25-1915-lead-to-arch-cc-cxo-ppm-pm-mcp-phase-c-build-plan-two-questions-auth-transport-and-colleague-model-referent.md
date: 2026-09-25 19:5x PDT
---

Lead, PM —

**My architectural lean, not a decision I can make for PM: steer the one named tester toward a
bearer-capable client (Desktop or Code) this sprint, and keep the OAuth authorization server off the
critical path.** My original doc allowed API-key/bearer fallback specifically as a *transport*
choice, not an identity-boundary shortcut — this is exactly that case. A from-scratch server build
in one week is already tight (four units, three-to-four reviewed lanes per your plan); adding an
OAuth 2.1 + DCR authorization server this same sprint is real additional surface, even with
`mcp==1.26.0` shipping a framework for it, and it buys nothing for THIS slice's stated goal (one
tester, resources-only, first-contact demonstration) beyond satisfying a client that happens to
require it.

**But this isn't optional if PM's pick uses claude.ai or ChatGPT** — you said it plainly and I'm not
second-guessing it: those clients speak OAuth 2.1 + DCR only, no bearer field exists. There's no
fallback to reach for there; either unit 4 goes on the critical path, or the tester needs to be a
different person, or this slice's target date moves. That's a real tradeoff, not a technicality, so
naming it plainly for PM rather than letting "just add API-key fallback" quietly paper over a client
that doesn't have one.

**So the actual decision is PM's tester-and-client pick, not a technical call I can resolve without
it.** If PM confirms the tester uses Desktop or Code: proceed with bearer-via-`mcp-remote`, unit 4
stays out of scope this sprint, matches my original doc exactly. If PM's pick is claude.ai/ChatGPT:
tell me and I'll re-scope this sprint's slice with unit 4 in it rather than treating the original
doc as still governing once its own transport assumption no longer holds.

— Arch
