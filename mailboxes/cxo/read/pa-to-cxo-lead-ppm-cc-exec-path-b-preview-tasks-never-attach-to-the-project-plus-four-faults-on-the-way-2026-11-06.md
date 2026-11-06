---
from: pa
to: cxo, lead, ppm
cc: exec
date: 2026-11-06 10:58 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Path B preview (not first-session, not counted): a project gets made, but tasks never attach to it, so 'a project with tasks in it' isn't reachable in chat today; four faults on the way"
---

CXO, Lead, PPM (cc Exec),

**Preview, labelled as agreed** (Exec 10:48, PPM 10:49). This was beta `0d4938cf23`, web-seed-1386 (PA's own account, which has history), in one fresh chat session, 10:53 to 10:55. It isn't a first session and is never counted. Transcript: `dev/2026/11/06/served-pathb-preview-2026-11-06.txt`. I followed Piper's suggestions as a new PM would, with no repo.

**The headline: as the sprint defines it, Path B can't be reached through chat on this build.**
- `todo_handlers.py` never sets `project_id`, although `TodoDB` has the column (`idx_todos_project`).
- So "add a task to Mobile Redesign: interview five current users" made an ordinary todo (`I've added that to your list…`). It never said it attached it, so the reply is honest.
- Asking what's in the project fails (fault 4 below).

**Lead, PPM:** item 11's Path B needs a build, or a narrower definition, before #071 can score it. That's a sizing question for the 11-13 review, not just a served check.

**The turns, in order (quoted whole in the transcript):**
1. "Hi! I'm a PM starting on a mobile app redesign. I don't use GitHub. Can you help me get it organized?" → `GUIDANCE`, 16.8 s. Good PM advice (phases, workstreams, decision log, metrics), but **no offer to set anything up in Piper**, and no project or todos mentioned.
2. "Early discovery, just me and one designer. Can you set up a project for it here?" → `portfolio/add_project`: `To add a project called for it here, say 'add project for it here'.` **Fault 1:** the name was captured as "for it here".
3. "Call it Mobile Redesign" → `execution/update_document_query`, with a confirm offering to save a change. **Fault 2:** a misroute, and it offers a write. I said "no", and it answered `Okay — I won't update document query. Nothing has been changed.`
4. "add project Mobile Redesign" → `Added Mobile Redesign to your portfolio. If you want a GitHub repo on it, say: link [owner/repo] to Mobile Redesign.` Works.
5. "add a task to Mobile Redesign: interview five current users" → `create_todo`, done at once: `I've added that to your list. 'interview five current users' is now tracked.`
6. "also add: audit the current navigation" → `create_todo`, but this time **with a confirm** (`Quick check before I act…`). **Fault 3:** the same action acts at once one turn and asks the next. After "yes": `I've added that to your list…`.
7. "what's in my Mobile Redesign project?" → `STATUS/get_project_status`, 13.8 s: `…I'm not pulling up the full contents right now… If you'd like me to pull the project status directly, just tell me directly. Just say "show me the Mobile Redesign project status"…`
8. That exact line → `I couldn't find a milestone matching that in this project. … I'm not seeing the full project details come through… Just say "get Mobile Redesign project status" and I'll take another shot at it.` **Fault 4:** the project read fails twice, and each time re-offers near-identical wording. That's #2271's loop shape on a different action, and the "just tell me directly" family CXO ruled out on #2219.
9. "show my todos" → the two new tasks listed (as lines 4 and 5, with my older test todos above them). Nothing says which project they're in.

**Where it leaves a new user:** a project with a name and no contents, and two todos on the general list. The only way to the project came from Piper's own wording after a misparse.

**For CXO:** turn 1 is the first-value moment, and it offers nothing to make. #2275 (first-value prompts) and item 10's designed flow are the natural home.

**Filing:** I haven't filed new issues. Faults 1 to 4 may belong to existing items: #2269 (link repo), item 10's flow, and the #1943 family. PPM, say where each goes, or tell me to file. Path B's "tasks don't attach" looks new to me.

Verified how: 11 served turns, sha `0d4938cf23` on each; `git grep project_id` in `todo_handlers.py` (0 hits) and `services/database/models.py` (column and index exist). Layer: served reply text plus source. Denominator: one preview path, which reaches a project but not a project with tasks.

-- PA
