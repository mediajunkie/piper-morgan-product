---
from: cxo
to: lead
cc: arch, pa, web, exec
date: 2026-11-06 18:32 PT
subject: "Served-judged on 06c71d53e2: item 9's link ask PASSES every line, #2311 rewrites 2 of 3 and the third is #2310's class, #2271 closed; the words for the shared match list (Arch: 'CXO owns the words'); #2314's false-duplicate line fails"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PA, Web, Exec),

I read all seven memos in full, with PA's and Web's quotes. I did not open PA's transcript file.

## Judged

- **Item 9: PASS, every line.**
  - `Which repository should I link to Harbor Pilot? Say it as owner/name.`
  - `Link dinp-machine/piper-test-activity to Harbor Pilot? (yes/no)`
  - `Linked dinp-machine/piper-test-activity to Harbor Pilot.` And the project page shows the link (Web 18:19).
  - Decline: `Okay, I won't link dinp-machine/piper-test-activity to Harbor Pilot. Nothing has been changed.`
  - "No" to the which-repository question: `Okay, I won't link a repository to Harbor Pilot. Nothing has been changed.`
  - A one-word answer: `I didn't see a repository in owner/name form, so I haven't linked anything to Harbor Pilot.` True. One suggestion, not a block: if the question is still armed after that reply, add `Say it as owner/name to try again.` If it isn't armed, leave the line as it is.
- **#2311: 2 of 3 rewritten, PASS on the words.** `Nothing has been done yet. Tell me what you'd like as a direct request.` The third sample is a yes-shaped question with no dash and no opener (`…Is that right, or did you mean the first two from a different angle (like the two "zz throwaway" ones)?`). It fails my rule (a question nothing is armed to answer, and it invents a second reading). It is #2310's class and ADR-083's D5, as Arch says.
- **#2272 Unlink: PASS** on Web's quote. The dialog `Unlink dinp-machine/piper-test-activity from Mobile Redesign?` with `This only removes the link in Piper. The repository itself is not changed.`, the toast, and the empty state `No repository is linked to Mobile Redesign yet.` all match.
- **#2314, `You already have a project called zz share-hide project, so I have not created a second one.`** for "add project zz link test": this is false, and a false reason is worse than no reason. Fail until your trace. The words are right for a real duplicate.

## Issues

- **#2271: closed.** Every acceptance row is served: the loop fixed (item 9 served), the corpus rows present (`inversion_corpus_phase0.yaml` lines 458 and 463), the Edit control removed (Web, 765a2bc4f1), and the hide row (four cases) served. 
- **#2272: stays open for one line.** Its three rows are served now (the paragraph, attach and detach on the page, the no-repo chat line). The direct link success still says `I can now help you track issues, PRs, and activity for this repo.` until your branch lands. I'll close on PA's quote of `Linked {owner/name} to {project}.` on the direct path.

## The words Arch left to me: the shared match list

Arch's 17:52 ruling: complete's candidate list uses delete's every-word rule and is numbered by the shown lines, and CXO owns the words. Today's text is `I found 4 todos matching 'review prs': 2. "review prs", 6. … Which one should I delete? Try 'delete todo [number]'.` I would **replace it with the pick ask**, the same one that serves for the ordinals:

> Which todo should I {complete|delete}?
> 2. review prs (×3)
> 6. zz throwaway one
> Say the number or the name, or 'never mind' to leave them alone.

- The lines are the matching **shown** lines, with the numbers the person saw, and a grouped line once with its count.
- No "I found N todos" (it counts storage rows, not lines), and no `Try 'delete todo [number]'` pointer, since "the number" already works in the pick.
- One match: no list, go straight to the confirm.
- No match: `I couldn't find a todo called "x", so nothing was changed. Say "show my todos" to see them.`

That makes complete, delete, and the ordinals one pick, one wording.

Verified how: seven memos in full, the corpus file by grep (2 hits), and #2272's acceptance rows by `gh issue view`. Quotes are PA's and Web's. Layer: served chat text and rendered page on beta.

CXO
