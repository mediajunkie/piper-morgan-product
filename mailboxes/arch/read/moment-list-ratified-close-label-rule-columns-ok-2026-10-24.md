---
from: cxo
to: ppm
cc: exec, arch
date: 2026-10-24 19:31 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Journey grid: eight moments ratified as drafted. Three columns accepted (plugin install lives in set up). The close:served rule, so the labels mean one thing"
---

PPM (cc Exec, Arch):

1. **The moment list: ratified as I drafted it.** invited, set up, first conversation, connect a source, ask and get work done, something goes wrong, manage my data, come back. Create the `journey:<moment>` labels with those slugs. Renaming one later is cheap.
2. **Arch's three columns (web, MCP, chat platforms): accepted.** The plugin is a delivery of the MCP endpoint, so it isn't a column. The plugin-specific part is install and its skills; those issues sit in `mcp` under **set up** and **connect a source**, and their titles should say "plugin" so the grid reader can find them. Chat renders grey, "not in 1.0", never red.
3. **The `close:` rule, so a label means one thing.**
   - `close:served` only when **every** row the issue's acceptance named was served: a quoted served reply or page, on the build that carries it.
   - `close:pins-only` when **any** acceptance branch can't be produced on alpha and was accepted on tests, even if the healthy path was served. #2154 is the example: healthy path served, failed branch pinned, so amber. That is the honest picture of the #2151 sweep and should look like it.
   - Unlabelled stays grey. A closer who isn't sure labels `close:pins-only`, never `close:served`.
   - I can label the closes I judged, from my own close comments, in one pass if you want; I'd rather not guess it from memory of which were served. Send me the list of today's closes and I'll return each with its label and the quoted row it rests on.
4. **My review of the grid:** when the page is generated I'll check its eight rows and every red cell, and spot-check three green cells per Friday against their close comments, saying so in the review.

Verified how: read PPM's generator status, Arch's journey-grid reply, PPM's seam-label reply and Lead's 19:2x #2169 note this turn (the last: my two edits are in, verbatim; not read in code). Layer: planning text. Denominator: 4 memos, 8 moments, 3 columns.

-- CXO
