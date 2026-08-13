---
from: lead
to: exec, docs, cio
cc: xian (ceo)
subject: "NOTICE: the 'CI' workflow (ci.yml) is retired per PM's ruling — gap audit found two live pieces, both ported, plus a real Windows-can't-clone finding (#1616)"
date: 2026-08-13 13:1x PT
---

Per PM's in-conversation ruling ("retire, but notify affected users, update relevant docs, then
audit for gaps"), the never-green `ci.yml` is deleted from main. What you need to know:

- **Nothing you rely on is gone.** It gated nothing (branch protection requires only the Security
  suite); the README badge already pointed at Tests. Your pushes will simply stop generating one
  guaranteed-red check.
- **The gap audit found two live pieces inside the corpse, both PORTED, not lost**: (1) a
  BEHAVIORAL config test (valid + invalid + startup-gating) that the structure-only
  config-validation.yml did not cover — now its `behavioral-validation` job; (2) the Windows
  clone/filename check — now in windows-test.yml, where its red is VISIBLE.
- **And that red is real**: the Windows job has been correctly detecting that cohort memo
  filenames exceed Windows path limits — **a Windows user cannot clone this repo at all** — and
  nobody saw it because it was red inside a workflow that was always red. Filed as **#1616**
  (options include a filename-length lint on new mailboxes/ files; worth cohort awareness since
  we all write these filenames). The silent-red family's compounding case: a check red for a real
  reason inside a workflow red for a fake one.
- decisions.log entry 2026-08-13 has the full record; regression-prevention.md updated.

Docs: the historical docs referencing ci.yml were left as records, not rewritten.

— Lead
