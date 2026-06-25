---
image:
alt:
caption:
---

# The Hook and the Worktree

*May 13–15, 2026*

By the second week of May we'd written a procedure called *close-issue-properly* and turned it into a working skill the agents were supposed to invoke whenever they closed a GitHub issue. The procedure was short. Update the description checkboxes first. Then move the issue to closed. Then add a closing comment with evidence. The order mattered. Boxes checked first because a description with empty checkboxes after a *Closes #N* commit is permanently misleading. The closing-comment evidence reads as the audit trail.

Tuesday May 13 I asked Lead Dev to verify that recent closures had followed the skill.

The verification didn't take long. Thirteen of the last thirteen closed issues had unchecked description boxes. The skill existed. The skill named the right failure mode. The skill wasn't firing on any closure cycle the cohort had run for at least the prior several weeks.

# The remediation

Three layers landed the same day.

The first was a memory pin at the top of the project's living memory file: *Before any `Closes #N` commit or `gh issue close`, update description checkboxes first. Comment-only close leaves `[ ]` forever.* Memory pins are how recurring lessons travel between sessions. The pin's job is to surface the discipline at session start so it gets named before the close cycle begins.

The second layer was a pre-commit hook. The hook scanned the commit message for the *Closes #N* magic-string pattern and, when it found one, checked whether the referenced issue's description still had unchecked boxes. If yes, the hook blocked the commit with a message explaining how to fix it. The hook was narrow. It only fired on commits that actually asserted closure. It explained the fix when it fired.

The third layer was my own standing directive — captured for the memory file in the form I said it out loud: *we can't close issues improperly and then justify retroactively.* Memory pins prime sessions. Hooks block specific motions. The directive sets the posture.

Six of the thirteen audited closures turned out to have more than checkbox issues. The reopened scope was different from the closing comment. Each one got properly reopened with the gap named. By Wednesday May 14 the first clean application of the new discipline ran end-to-end. A real closure with description boxes checked, the hook silent because there was nothing to block, the closing-comment evidence intact.

That's the first arc of this piece. A procedure that wasn't firing got the structural backing it needed in three layers. The arc closed inside thirty-six hours.

# The second arc

Friday May 15 morning the product-management role (PPM, Piper Alpha) ran a sustained shipping sprint — fourteen commits in a few hours covering five substantive memos, a product-decision document iterating from v0.1 through v0.3, and a workstream review. The sprint happened on the project's shared `main` branch — the working tree everyone uses when they're not on a feature branch.

The sprint produced four distinct *foreign-state-capture* incidents. Each one was a different shape of the same failure mode. Adjacent inbox-to-read mailbox renames getting captured into PPM's commits via git's rename detection. A draft document wiped from PPM's working tree by another agent's concurrent rebase. Index entries getting dropped between staging and commit when a concurrent agent committed in the same window. CXO's tracked-but-unstaged deletions getting absorbed into PPM's session-log commit.

The cohort had a stack of memory pins from the prior five weeks for exactly this category of failure. *Git reset HEAD before staging.* *Verify branch identity before every commit.* *Read every line of `git diff --cached --name-only`.* *Run `git show --stat HEAD | head -30` post-commit and pre-push.* Each pin had landed in response to a specific incident. Each pin worked, in the sense that disciplined application of all of them simultaneously would have prevented the incident that motivated it.

PPM's morning made the limit visible. Layered discipline could *surface* foreign-state capture every time. None of it could *prevent* it. Capture only stopped happening when the working tree the agent was operating in stopped being shared with the other agents.

PPM filed two memos before noon. One pinned a new post-commit verification check ("run `git show --stat HEAD` immediately after every commit"). The other was the structural conclusion: *worktree-default for substantive agent work.* Each substantive session should start by creating a fresh dedicated `git worktree` — a separate checkout of the repo, on its own feature branch, with its own filesystem state. The shared `main` worktree should be reserved for short mailbox-discipline operations where the exposure window is small.

I ratified the directive at 7:13 AM via the chain PPM had filed it through. The documentation role landed the codification in the project's standing instructions by evening. The cohort started moving substantive work into dedicated worktrees that afternoon. The first-day data was small but consistent: roles that switched mid-day reported clean commits for the rest of the day.

# What the two arcs share

Both arcs end in the same shape. Discipline kept failing despite the agents knowing the discipline. The fix in each case was to change the environment so the failure became structurally harder rather than discipline-dependent.

The close-issue-properly procedure had been correct. The cohort had been agreeing to follow it. Closure cycles kept shipping without the boxes checked. The remediation that worked wasn't more reminders. It was a hook that blocked the specific commit pattern that asserted closure. The hook didn't make agents more disciplined. It made the *failure mode* impossible to reach via the path that had been producing it.

The commit-discipline memory pins had been correct. The cohort had been holding them as a stack. Foreign-state-capture incidents kept happening. The remediation that worked wasn't a sixth pin. It was an environmental separation that made the capture surface itself disappear. Other agents couldn't drift state into your commit if your commit was running against a working tree they weren't sharing.

The fancy way to describe this is *moving from discipline to architecture.* The plainer way is that procedures hold for as long as the agents stay disciplined, and infrastructure holds whether they do or not. Past a certain pass-rate ceiling on a recurring failure, the gain from more discipline saturates. The next gain has to come from a different layer.

# What this closed

Looking back at the prior three weeks, the same shape shows up at every layer of the project. Issue closures running ahead of evidence. Calibration metrics drifting from their reference state. Feature branches accumulating without merging. Voice-pass discipline operating janitorially because draft-time voice work wasn't being absorbed. Each case had a procedure. Each procedure was correct. Each procedure leaked at the rate procedures leak when the environment doesn't enforce them.

The arc that closed on May 15 wasn't really about issue closures or about worktrees specifically. It was about the cohort recognizing the saturation point — the moment where another reminder would not produce the next gain, and the gain has to come from changing the conditions instead.

The hook is a small piece of code that fires on a specific commit shape. The worktree directive is a small change to the default-mode for new sessions. Neither is glamorous. Both took an afternoon to design and an afternoon to land. They are, by any reasonable measure, the smallest possible infrastructure that does the work the prior discipline couldn't.

That's the thing worth carrying. The shape of *discipline-becoming-infrastructure* isn't usually a grand new system. It's a hook with an explanation message. It's a fresh directory tree. It's the right small change at the layer where the procedure had been leaking.

---

*Next on Building Piper Morgan: "The Triad Model" — the shape that kept showing up across design, methodology, and team structure.*

*Where in your work has a procedure been failing despite everyone knowing it? What would the small piece of infrastructure that closed the gap look like?*

[FACT-CHECK NOTE for PM: Sources verified against May 13, 14, 15 omnibus + memory pin canon. Key facts: May 13 Lead Dev close-issue-properly audit found 13-of-13 unchecked descriptions; three remediation layers same day — memory pin at top of MEMORY.md, #1083 pre-commit hook (Closes #N magic-string scan), PM standing directive "can't close issues improperly and then justify retroactively"; six of 13 reopened with scope-shaped gaps. May 14 first clean application. May 15 PPM 14-commit morning sprint produced 4 foreign-state-capture incidents (adjacent rename detection capture + draft wiped by concurrent rebase + git mv index drops + CXO deletions auto-captured); two memos filed — `feedback_verify_show_stat_post_commit_pre_push.md` (post-commit guard) + `feedback_worktree_default_for_substantive_work.md` (structural fix); PM ratified worktree-default at 7:13 AM via PPM relay; Docs codified in CLAUDE.md by evening. Five-week escalating commit-discipline memory stack: feedback_clear_index_before_staging_on_shared_main + feedback_branch_show_current_before_every_commit + feedback_diff_head_before_editing_shared_file + feedback_verify_show_stat_post_commit_pre_push + feedback_worktree_default_for_substantive_work.]

[SOURCE NEEDED for PM: The four foreign-state-capture incident shapes I named — I rendered them from memory and omnibus core themes; if the actual PPM memo enumerates them differently or in a different order, swap. Also flag if "first-day data: clean commits" is overstated — I have the directive-ratification timestamp but not a quantified day-one outcomes count.]
