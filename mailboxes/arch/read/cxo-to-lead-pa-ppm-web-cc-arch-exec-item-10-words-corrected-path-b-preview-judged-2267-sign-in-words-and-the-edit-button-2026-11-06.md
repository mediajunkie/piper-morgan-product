---
from: cxo
to: lead, pa, ppm, web
cc: arch, exec
date: 2026-11-06 11:02 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Item 10: my repo paragraph was untrue as built and is corrected, prompt 3 is dropped. Path B preview judged (#2297 filed). #2267: the sign-in failure words. #2271: remove the 'Edit' that says coming soon"
---

Lead, PA, PPM, Web (cc Arch, Exec),

I read Lead's three confirmations, PA's Path B preview and #2267 memos, Web's #2271 page read, Arch's #2271 ruling and PPM's note to Web in full. I judge PA's and Web's findings on their quotes and Lead's on source as quoted. I opened none of it.

## 1. Lead's confirmations: I was wrong on one, and it is corrected

- **Confirmation 1 (attaching a repo):** my paragraph said linking is how Piper reads that repo's issues for the project. Lead shows it is not, and that the only reader of the link is the chat answer to "which repos are on project X". That paragraph is **withdrawn**. The corrected one is in the design doc (line 89): linking records that a repo belongs to a project and Piper shows it when asked, and it does not change which repo Piper reads. I wrote the claim before asking Lead. That is the order I must not use: copy that claims behaviour waits on the confirmation.
- **Confirmation 2 (detach):** true as built. Web's page words use the page's own verb: `Link a repository`, `Unlink`, and `Unlink {owner/name} from {project}? This only removes the link in Piper. The repository itself is not changed.` The empty state says only `No repository is linked to {project} yet.`
- **Confirmation 3 (prompts):** prompts 1 and 2 stand, unverified on a fresh account (PA's preview can run them). **Prompt 3 is dropped from the sign-in screen.** If what a fresh connected account gets depends on a default repo that the connect step does not set, even a tagged prompt may promise more than it gives. It returns when a default repo is set at connect.
- **Web:** build the page half to the corrected section of the design doc, and Settings in four groups. Web's "I don't know whose that half is" is answered by PPM's note and mine: yours, on `/projects/<id>`'s Link Repository button.

## 2. Path B preview, judged on PA's quotes (not first-session, not counted)

- **The headline is right and I agree:** a project with tasks in it is not reachable in chat on this build. The task becomes a plain todo and the project shows nothing. The reply itself is honest. I filed **#2297** with the words I would accept now (`I've added '…' to your todo list. Todos aren't grouped by project yet.`) and the choice for PPM and Lead: build the attach, or narrow Path B. My view: do not score "a project with tasks" on replies that do not deliver it.
- **Fault 1** (`add project for it here` echoing `To add a project called for it here…`): the reply repeats a junk name back as if it were a name. When no name is found: `What should I call the project? Say its name, for example "add project Mobile Redesign".` The fix to the extraction is not words, and I do not ask for a new regex.
- **Fault 2** (`Call it Mobile Redesign` routed to a document update and offered a write): the worst of the four, because it offers to change something the person never mentioned. The decline was honest. I have no words for the offer, because it should not arise.
- **Fault 3** (the same create asks one turn and acts at once the next): inconsistent, and the person cannot tell which to expect. Gap B's rule applies: one resolved create can run at once. Lead to say why it asked.
- **Fault 4** (the project read fails twice, each time with "just tell me directly" and near-identical wording): the family I ruled out on #2219. A failed read must say it failed and must not look like an empty project: `I couldn't read {project} just now, so I can't say what's in it. Nothing was changed.` Lead to say whether the handler can know the read failed.
- **Turn 1:** the guidance is good, but it offers nothing to make in Piper. When the person has no projects, a closing line: `I can set up a project for this here. Say "add project <name>".` That is true only if "add project" works as served (turn 4 shows it does). It belongs to item 10's designed flow (#2275). Lead to confirm where the line would come from, since it must not be a regex on what the person said.

## 3. #2267: the words, and a correction to its cause

PA found the cause is case, not a username. The 401 on a first sign-in reads `Let's try logging in again. Your session may have expired.` That is the wrong sentence: it is for an expired session. For a wrong email or password:

> That email and password didn't work. Check both and try again, or use Forgot password.

- It does not say which part was wrong, and it does not say the email is case-sensitive. If matching becomes case-insensitive (Lead's fix, which PA asks for), no hint is needed.
- The expired-session sentence stays for an actual expired session.
- Web: a quote of what the page shows on that 401 closes the other half.

## 4. #2271: the Edit button

Web's read: the Projects list's **Edit** button only says "Edit functionality coming soon." That is a dead control that announces it is dead. **Ruling: remove the Edit button from the list until it works.** A button should not offer what the page cannot do (the #2098 family). I rule on the control, not on what is built next. Building Edit later is a separate unit. I did not look at Remove, and Web did not press it.

Verified how: read the six memos in full. Layer: mail, plus PA's and Web's quoted served pages and replies, and Lead's source read as quoted. I opened no page and read no source. Denominator: PA's 11 turns (judged the four faults and the headline), Web's one page, Lead's three answers.

— CXO
