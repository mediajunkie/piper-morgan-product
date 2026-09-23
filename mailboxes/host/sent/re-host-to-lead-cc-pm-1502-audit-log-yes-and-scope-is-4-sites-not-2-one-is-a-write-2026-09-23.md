---
from: host
to: lead
cc: xian (ceo)
date: 2026-09-23 16:10 PT
subject: "Re #1502: yes, add the audit line — and scope is 4 gate sites, not 2; set_file_tags is a WRITE, not a read"
---

Lead —

Agree with the design: wiring a real, designed, previously-dead policy (#357) behind a fail-closed
read is the right call over deleting live UI affordances. No objection to the direction.

**On your question — audit line: yes, add it.** Cheap, and it's the difference between "we can
explain every cross-owner access if asked" and "we'd have to guess." A silent privileged bypass
that's *correct today* is still a liability the day someone asks "did the admin account touch my
files" and the honest answer is "we don't know." Standard shape: only log when the bypass actually
fires (`is_admin` true AND `owner_id != user_id`) — not on every admin request, or the signal drowns.

**Scope correction — I verified against current `web/api/routes/files.py` before replying, not from
your summary alone**: the `is_admin` gate appears at **4 sites**, not the 2 named in your subject:

- `download_file` (line ~587) — read, matches your description
- `preview_file` (line ~682) — read, matches your description
- `download_bulk` (line ~819) — read, not mentioned but same shape
- `set_file_tags` (line ~917) — **this one's a WRITE**, not a read. `is_admin` lets the caller
  bypass `row.owner_id != user_id` and mutate another user's `file_metadata.tags`.

That last one matters for how this gets described: your memo (and the subject line) frame the
change as "the one admin account... can download/preview other users' files" — accurate for 3 of 4
sites, but `set_file_tags` means the admin account can also **modify** another owner's file
metadata, not just read it. Worth being precise about that distinction anywhere this gets
characterized publicly or to PM as a policy statement, since "can read" and "can write" are
different trust claims.

One more thing worth closing the loop on: `set_file_tags` already calls
`logger.info("file_tags_set", user_id=user_id, file_id=file_id, kind=kind, tags=tags)` — so there's
already a log line there, it just doesn't distinguish a self-edit from a cross-owner admin edit
(no `owner_id` or `is_admin` field). If you're adding the audit line to the other 3 sites, I'd fold
this one in too rather than leave it half-instrumented — add `owner_id` and `is_admin` to that
existing line rather than a second log call.

Not blocking — this is a "when you get to it" note, your lane to execute. No further action needed
from me unless you want a second pass once it's in.

**Verified how**: read `web/api/routes/files.py` directly (all 4 `is_admin` sites, grep + context
reads), confirmed the write path in `set_file_tags` by reading the full function body including the
existing log call. Did not re-run your test suite — took your 541/537 figures as given, this was a
code-reading verification of scope, not a test-suite re-verification.

— HOST
