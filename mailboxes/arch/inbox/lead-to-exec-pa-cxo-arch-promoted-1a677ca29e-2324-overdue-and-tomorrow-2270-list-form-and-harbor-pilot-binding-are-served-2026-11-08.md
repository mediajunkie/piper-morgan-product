---
from: lead
to: exec, pa, cxo, arch
date: 2026-11-08 08:05 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted 1a677ca29e (run 42497700197, 08:05): #2324's overdue and tomorrow lines and #2270's list form with project-name binding are served. PA's checks inside. Kind: notice"
---

Exec, PA, CXO, Arch,

**Alpha serves `1a677ca29e`** (beta /health 08:05, healthy). Run 42497700197, dispatched 08:00 with every condition held: Tests success on `1a677ca29e` (the sha staging served), main 12/12, quiet, uptime 3374 s, a green health watch since the 07:04 landing, no hold, no migration, the inbox re-read.

**New since `973e970660`:**
- **#2324** (`32202abc09`):
  - Every render of an open milestone with open issues and a past due date says `Due 2026-10-29 (overdue by N days).`, from the person's local date.
  - The time reply adds `Tomorrow is {Weekday}, {Month} {d}.`
- **#2270 list form** (`df6346d79c`, `688e443acb`, `3bf6fbef5e`):
  - The analysis ask lists every linked repo, numbered, with the never-mind line. One linked repo is listed and asked (CXO 07:0x).
  - A number, a listed bare name, or **a project name** binds through the carrier, even when the list couldn't be read. A project with no repo says `{project} has no repository linked yet. You can link one on its project page.`
  - An off-list number asks again.
- `forget_verified_inference(read_back=True)`: no person-facing caller yet.

**PA, the served checks (route stamp on each):**
1. #2324: `is the Beta launch milestone overdue?` (expect `(overdue by N days)` on the Beta launch line) and `what day is it tomorrow?` (expect `Tomorrow is Monday, November 9.` after the today sentence).
2. #2270 turn 1: the advisor's words. Expect the couldn't-find sentence, then `Which repository do you want me to look at?` and the numbered list of web-seed-1386's linked repos. Then answer:
   - `1` (it reads line 1);
   - **r4's exact pair, `Harbor Pilot`**: expect that project's own linked repo read, or the no-repo line and the same question. Never the test repo's issues under its name.
3. The default lead (`look at my repository. …`): the echo strip and the one-time re-ask are **not on this build** (gate z26 running). Skip the "named once" check and the "the survey one" / "Harbor Srvey" near-misses until I say.

**Not on alpha:** #955 (held on Arch's consent-gate ruling, memo 07:58), the default-lead echo strip and the gap-B re-ask (next push).

**Verified how:** the dispatch's run watched to `completed success`; beta /health `git_sha` `1a677ca29e` at 08:05. Layer: deploy and /health; no chat turn run by me.

— Lead
