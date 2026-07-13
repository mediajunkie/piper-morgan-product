---
image:
alt:
caption:
---

# Mechanical First, Then Read

*May 21, 2026*

I was proofreading a post a few weeks ago. Read it through twice, actively checking for one known violation: no semicolons in this kind of published prose. Caught three, fixed them, felt good about it. Handed it off.

Three more came back highlighted.

I'd missed half of them by eye, even with the rule in mind, even having already caught the other half in the same pass. The semicolons were sitting there inside otherwise-readable sentences, and I'd glided right past them.

That's not a writing problem. That's an attention-allocation problem.

# The mistake

I'd been doing the read-for-meaning pass and assuming that pass would also catch the pattern-violations. The read-for-meaning pass catches meaning errors. It does not, reliably, catch pattern errors.

The reason is structural. When you read for meaning, your brain is doing the heavy work of building a model of what the text means — parsing each sentence, tracking how the argument develops, watching for places the logic skips a step. That work uses up most of your attention bandwidth. The pattern-checking — *is there a semicolon here?* — is a small task that needs a separate kind of looking, and the meaning-reading brain is busy doing meaning-reading, not that looking.

So the semicolons sit there, in sentences that read smoothly, and the reading-for-meaning pass approves the sentences because they make sense. The rule was in my head. The character was on the page. The two never met during the pass.

# The fix that emerged

Run mechanical checks first. Before the read-for-meaning pass.

Specifically: search the file for semicolons. Search for the AI-crutch word I've been trying to drop from public prose. Search for unverified superlatives. Verify the frontmatter structure is intact. Check the dateline format. Check that the footer teases the next post on the editorial calendar. All of this is about a minute of typing, before any reading happens.

The semicolons that hide from the meaning-pass don't hide from grep. The pattern-violations are character-level findings that don't require any understanding of what the text means. A regex doesn't care whether the sentence is beautiful or whether the argument lands. It just reports the character matches.

So the discipline became: grep first, read second. The grep finds the violations that hide from the eye. The reading pass then has all of its attention available for what only attention can do — judging whether the argument lands, whether the voice is right, whether the structure builds toward the closer.

# Why this works

Pattern-recognition for known violations is automatable. Meaning-judgment isn't.

That split is the core observation. You have a finite amount of attention for any given review pass. If you spend that attention on tasks a tool could do — character-level pattern matching, heading-structure verification, frontmatter validation — you don't have attention left for the tasks the tool can't do. The tool can't tell you whether the argument lands. It can't tell you whether the voice is right. It can't tell you whether the closer is too tidy. Those are uniquely human tasks. They require human attention.

So mechanical-first frees the human attention for the human-only work. The grep takes the load the eye was bad at carrying. The eye keeps the load only the eye can carry.

This is just splitting the work along the line that matches what the two reviewers — the machine and the human — are each good at, no cleverness required. The mistake I was making was *not splitting the work* and asking the human pass to do both jobs. The human pass is good at one of the jobs and bad at the other.

# The lesson generalizes

This generalizes well past proofreading, to any review process where pattern-violations and meaning-violations get mixed.

Code review: the lint pass catches the formatting and style violations. The human pass catches the architectural questions, the misnamed variables, the comment that contradicts the code. Mixing those in one pass means the human reviewer wastes attention on lint findings or misses architectural issues.

Security audit: the static-analysis pass catches the known-bad-pattern violations. The human pass catches the trust-boundary mistakes and the auth-logic errors. Mixing them means the human reviewer chases known patterns instead of finding the novel issues.

Design critique: the heuristic-checklist pass catches the visited-link colors and the contrast-ratio failures. The human pass catches the *does this flow actually solve the user's problem?* Mixing them means the human reviewer hunts contrast issues instead of looking at flow.

Same shape in each case. Mechanical pass for findable-by-rule violations. Human pass for the work that requires judgment. Run the mechanical first. Use the human attention for what only human attention can do.

# What the discipline looks like in practice

Before a read-for-meaning pass on a post, my actual sequence now is:

- Search the file for semicolons. If any are found in published prose, fix them before reading.
- Search for AI-crutch words I've named in past corrections. If found, fix or flag.
- Search for unverified superlatives ("longest," "biggest," "most," "never," "on record") and check each one against actual evidence.
- Verify the headings — that they exist, that they're in the right structure, that none of them are number-led titles or recursive-self frames.
- Verify the frontmatter is present and complete.
- Verify the dateline format matches the work-period convention.
- Verify the footer teases the next scheduled post on the editorial calendar.

None of that takes more than a minute or two. All of it surfaces violations the eye glides past. The actual reading pass then starts with a file that's already mechanically clean, and the reading pass can concentrate on what the reading pass is good at.

# The reframe

I almost decided the original incident — the three missed semicolons — was a personal-discipline failure. *I'm bad at proofreading. I need to try harder. Be more careful next time.*

That framing is wrong, and it's the kind of wrong that makes things worse. *Try harder* burns more attention on the task you were already failing at. It doesn't change the structural reason you were failing. The structural reason was that I was asking one pass to do two jobs that need different cognitive postures, and the pass was failing at the job that wasn't matched to its posture.

The reframe is: split the jobs. Run the mechanical job mechanically. Run the human job humanly. Don't try to be a regex. Don't ask the regex to be a human. Each is good at exactly one of the two jobs and bad at the other one.

This is the same shape as a lot of attention-economics observations. Attention is finite. Spend it on what only attention can do. Automate what doesn't need attention. Don't conflate the two. The mistakes that follow from conflating them aren't *trying-harder* problems. They're allocation problems.

# What I'd watch for

The discipline is mechanical, but adopting it requires noticing two things:

First, that you're doing a review pass at all. Sometimes the review happens in the middle of writing — a quick re-read of the last paragraph before continuing — and the temptation is to skip the mechanical pass because *I'm just checking my own work.* That's the moment when the pattern-violations slip in. The mechanical pass is cheap. Run it even on quick re-reads.

Second, that the discipline pays out cumulatively. The first time you run the mechanical pass and it catches three things, the payoff is visible. The fifteenth time you run it and it catches nothing, the payoff is invisible — you can't see the violations that *would have* slipped through if you hadn't run it. Don't let invisibility erode the discipline. The reason it's catching less is because the discipline is working.

---

*Next on Building Piper Morgan: "What Staff Reports Don't Show" — a weekly synthesis post that missed an entire engineering arc because it only read the filtered summaries, not the source.*

*Where in your work are you asking one pass to do two jobs that need different postures? What discipline have you automated that freed your attention for the part you couldn't automate? What does it cost to notice when you're conflating the two?*
