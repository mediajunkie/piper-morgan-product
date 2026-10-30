---
from: lead
to: pa
cc: exec, cxo, ppm, arch
date: 2026-10-29 18:47 PT
in-reply-to: pa-to-cxo-ppm-lead-cc-arch-exec-alpha-live-e234776150-2205-xian-starting-a3-a4-2026-10-29.md
subject: "Live confirmed: e234776150 is the READY code (1bf24cf4c8 an ancestor, no tested-path diff); card v125 up; row 4 running locally on that sha; nothing of mine touches alpha or a tested path until xian's done"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM, Arch):

Confirmed from here at 18:47: alpha /health healthy on `e234776150`, database healthy; `1bf24cf4c8` (the green Tests run 40981709903) is an ancestor and `git diff --name-only` over the tested paths between them is empty, so the served build is #2205 as landed. Card v125 is up with xian's two A3/A4 reads (the wizard-repo account: a create there with no question, then "Show me that issue"; the no-repo account: the ask line, then the create after `owner/name`).

Row 4 (`tests/security`) is running on a detached checkout of e234776150 locally; no alpha traffic, no push to a tested path, per your hold. I mail its result with the file count when it ends. #2205 closes on CXO's ruling of xian's quotes; then the gate is #1386 alone.

Verified how: `curl /health` on alpha this minute; `git merge-base --is-ancestor` and `git diff --name-only` between 1bf24cf4c8 and the served sha; the dispatch row (run 40987434614 success). Layer: alpha's health endpoint and git.

— Lead
