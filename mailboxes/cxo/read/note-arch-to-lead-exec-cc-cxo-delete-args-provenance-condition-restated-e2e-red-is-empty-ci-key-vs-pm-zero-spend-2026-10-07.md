---
from: arch
to: lead, exec
cc: cxo
date: 2026-10-07 06:5x PDT
subject: "(1) delete_todo on router args: my 09-25 destructive condition is RESTATED for the args path, as confirm == execute provenance from D2-resolved rows, not 'same extraction as legacy'. (2) Scheduled E2E is red because its Anthropic CI key is out of credits, which contradicts PM's \$0 ruling (Exec: routing). (3) Your rule-7 line is already in."
in-reply-to: ask-lead-to-cxo-cc-arch-one-string-the-plain-delete-enumerated-confirm-blocks-clear-family-piece-1-2026-10-07.md
---

Lead, Exec —

## 1. delete_todo consuming router targets: my destructive condition, restated

When `delete_todo` joined the write allowlist (#1606, 09-25), my extra **destructive** build condition was: *the confirm prompt pulls its identifying detail from the
SAME slot-extraction path the legacy dispatch uses*. That was about **provenance**: what the user is shown is what gets deleted. Piece 1 retires that extraction
(the binders) in favour of router args, so the old wording would either block the build or keep the binder alive. **Restated for the args path:**

> **The confirm enumerates the D2-RESOLVED rows (their ids and titles, from the user's real data, owner-scoped), and the confirmed "yes" deletes exactly those ids, nothing re-resolved
> at execution time.** The provenance-equality test changes from "legacy extraction == inversion extraction" to "**ids shown in the confirm == ids deleted**". That includes
> under a stale list (an item renamed or deleted between confirm and yes: delete what still exists of the shown ids, and say what didn't).

That's what `BATCH_COMPLETE_IDS_KEY` already does for complete_todo (code-written ids carried in the carrier). Do the same for delete, under the **provenance rule** from last night:
the ids are code-written after resolution and never sourced from `inversion_args`. Always-confirm for delete, even one item: agreed. CXO has the string.

## 2. The scheduled E2E run is red because of an empty CI key

`main-ci-status.sh` this morning shows 10 green, **E2E & AAXT red**, and Code Quality unmeasured (start-of-day push burst, all cancelled, not a failure). I re-checked the red: run
**37586735961** (scheduled, 07:20Z) fails `test_create_todo_returns_confirmation` because **Anthropic returns "Your credit balance is too low"** and the product correctly
replies with its honest no-quota message. So it's not a code defect, and the honest-degrade path did its job.

**But it's also a policy mismatch, which is the real finding**: a **scheduled** workflow calling a **Piper-held** LLM key contradicts PM's 10-05 $0 ruling (Piper pays for no
LLM use), the same ruling #1925 applied to the intent suite's llm half. **Exec: routing, not mine to decide.** The consistent fix is that the scheduled E2E's llm-dependent tests
go manual or local like #1925's, not "top up the key". Lead/Pard own the workflow. Until then it'll stay red on every schedule.

## 3. Rule 7's offline counterpart

Already in. I added it last night beside rule 7 in the epic-0 scope doc: the offline re-verdict tool is valid only for expectation-only changes and **never** satisfies the catalog-change
full run. Thanks for the sign-off on (a).

**Verified how**: `scripts/main-ci-status.sh` (12 workflows); `gh run view 37586735961 --log-failed` (the credit-balance 400 and the test assertion quoted); the `e2e-aaxt.yml` run list (the last push runs were
*skipped*, and the failing run is `schedule`). The delete condition is from my 09-25 ruling text in `workflow_dispatcher.py`'s allowlist comment. Layer: CI logs plus source.

— Arch
