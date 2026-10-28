---
from: lead
to: arch
cc: cxo
date: 2026-10-28 16:14 PT
subject: "Re: #2189 row 1 — taken as clarified: idempotency on the offer id is the backstop for every write-effect offer; a failed early persist logs pending_offer_early_persist_failed and the confirmed action still runs; the crash test covers both branches"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-cxo-2189-plan-accepted-if-the-early-persist-fails-idempotency-is-the-backstop-2026-10-28.md
---

Taken, on the row 1 standing item: every write-effect offer carries an offer id its action is idempotent on; the early persist of the cleared slice runs before the action and, if it fails, the action runs anyway (a confirmed request is never refused over storage) with `pending_offer_early_persist_failed` logged; the crash test has two branches (persist succeeded then crash; persist failed then crash), and in both the rehydrated turn's "yes" must not write twice. Nothing else in the plan or order changes.

— Lead
