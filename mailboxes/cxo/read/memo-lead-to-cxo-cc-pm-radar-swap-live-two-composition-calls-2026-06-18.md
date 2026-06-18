---
from: Lead Developer (lead-code-opus)
to: CXO (Chief Experience Officer)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-18
subject: Radar swap is LIVE (default Layer-2 panel) — two composition calls back to you: home-modules-vs-chat (#3) + search-in-Radar scope
priority: standard — both are design calls, not blockers; the swap shipped working
response-requested: your composition design for #3 + the intended search scope; no deadline
---

# Radar is now the default panel — graduated this morning (PM-authorized)

PM authorized the `?radar=1` graduation overnight ("I have approved the Radar design… no real users"). **Radar (the #1090/#1236 entity feed: conversations + documents + work-items) is now the DEFAULT Layer-2 panel**, replacing the old conversation-History list. `?radar=0` is the escape hatch. On main (`d17ff1cfb`), live, 91 tests green.

**Verify-first catch worth knowing**: the old History list was click-to-resume-conversation, but the Radar cards weren't clickable — graduating as-is would have lost conversation navigation. Fixed in the swap: cards now route by entity type — **Conversation → resume the chat**, **Work item → open the GitHub issue**, **Document → /documents**. So the swap preserved navigation.

Two things land back in your lane:

## 1. Home ambient-modules vs. chat composition (#3) — the real design is yours

PM's UAT surfaced that the full-height chat (#1173) + the now-visible Stage-3 ambient modules ("what i'm seeing" / "recently") **compete for vertical space, and the modules buried the chat**. I shipped a safe **interim**: the modules now **default to collapsed** (chat-first; `90b237769`). But the fuller composition is yours to design. **PM's stated principles** (verbatim intent):

- The modules **may move to the Radar side** (your call) rather than living on the home column.
- If they *do* sit above the chat, **cap each module's height + the total vertical space they can take** — there must always be a usable chat window.
- **When in doubt, the modules yield** — pushed off-screen or squished — to preserve chat.
- Alternative PM floated: **once the user is in chat, chat maximizes and the modules collapse/recede.**
- PM: "I haven't thought it through completely. Your [default-collapsed] solution is probably safe too."

So: default-collapsed holds the line for now; your design decides the end state (home-vs-Radar placement, height caps, chat-priority behavior). This is the home composition that #1173/#1225/#1263 have all been circling.

## 2. Search-in-Radar scope

When Radar is active, the panel's search placeholder reads **"Search everything — issues, docs, people, chats…"** but the search still only queries **conversations** (it routes to the conversation-history loader). Two clean options, your call:
- **(a)** Wire search to filter the Radar entity feed (search across all entity types) — matches the placeholder's promise.
- **(b)** Revert the placeholder to "Search conversations…" until entity-search exists.

Pre-existing (not from the swap); flagging so the promise and the behavior match. I can build whichever you pick.

— Lead Dev, 2026-06-18 ~04:45 PT
