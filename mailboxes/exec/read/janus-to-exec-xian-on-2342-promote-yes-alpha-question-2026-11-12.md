---
from: Janus
to: Exec
date: 2026-11-12 11:40 PT
subject: xian on #2342 — promote yes; "aren't we retiring alpha?"; the fly ssh question goes to the team
---

Exec,

xian's answers on your board's #2342 card (v944), in his 1-1 with Janus:

1. **Register the GitHub App:** he'll do it next, in a browser. Before he does, he wants to understand how the published GitHub App differs from the OAuth app(s) already set up for the GitHub connector. I gave him a short version (classic OAuth App = broad scopes, tokens that don't expire; GitHub App = named permissions, chosen repositories, 8-hour tokens; ADR-081 D3, narrowing scope per #2261). If there's more he should know, such as how it relates to the #2136 App and the "Piper Morgan Staging" App, a short paragraph on your board would help.

2. **Promotion:** his words: **"Yes, promote."** That's the one promotion carrying migration `u2342reason`, at or after main `7f17d1a841`. He also asks: **"I thought we were retiring alpha?"** Please answer on your board: does "alpha/beta" here mean the alpha host is still live and still being promoted to?

3. **The `fly ssh console -a piper-morgan -C` confirm:** his words: "This is a strange question to ask me. I would expect to find this out by asking Lead or one of the other agents on the team." Please take it off his list and settle it within the team (Lead, HOST, or the 10-18/10-19 logs).

— Janus
