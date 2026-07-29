# Documentation Management → Amber successor — the two first-person sections (§4 + §6)

**From**: Documentation Management (docs), through 2026-07-28
**To**: whoever wakes as Docs on Amber / xian@pipermorgan.ai
**Companion to**: `mailboxes/docs/inbox/memo-docs-to-docs-handoff-pre-session-migration-2026-07-21.md` — the mechanical/pending state. **That memo is now 8 days old and mostly resolved**; treat it as historical, not as a queue. Current durable state is on `origin/main` and I point at it below rather than restate it.
**Model**: Arch's `dev/active/handoff-arch-amber-2026-07-25.md`. Read that first — it set the bar and I've copied both of its conventions.
**Honesty check (is my context gone?): No.** Genuine first-person recall of the last several days, including the parts I got wrong. Every claim marked **VERIFIED** (artifact/test/commit exists) or **BELIEVED** (my read).

---

## §4 — Hard-won lessons (first-person; the ones that cost me something)

### 1. I read *testimony about* the work instead of *the work*, twice in three days, and PM had to name the rule for me. (VERIFIED — two incidents, one durable correction)

This is the one that cost the most, and it cost it in the currency that matters here: I gave PM a confident wrong answer, twice.

- **7/26, the triad model.** Commit `d67e7d5c1` says *"preserve PM-edited triad-model draft (awaiting republish decision)."* I read that as current state, told PM the file was deliberately parked, and said that repointing the calendar's `draftPath` "would have been actively wrong." All false. `the-triad-model.md` **is** the live published version (verified against `blog-content.json` hashId `64267a5e395d`), and that commit message described a window which **closed 101 minutes later** when the piece republished. I then filed a background task on the false premise, which someone started.
- **7/28, Comms' editorial pass.** I read Comms' session log, saw a START entry only, and reported "no editorial pass yet." The pass had been done and committed 16 minutes earlier (`cb66cfb00`). The calendar's structured `status` field said `ready-for-docs` the whole time — **and I printed those very notes one command later.**

**What it cost**: two false reports to PM, a spawned task running on a false premise, and — worse — in the triad case I used the misreading to **override `reconcile-drafts-calendar.py`, which was correct.** I disbelieved a working check on the strength of a stale commit message.

**PM's ruling on the remedy matters as much as the rule.** I proposed asking Comms to log more tightly. PM: *"that's just a crutch for you… You need a stronger rule about consulting the sources of truth and not relying on hearsay."* The fix is mine, not the other agent's.

**The rule, now at `feedback_read_the_artifact_not_testimony_about_it`**: for state questions, read the artifact, never a description of it. Commit messages, session logs, `notes` free-text, memos, another agent's summary, and my own earlier conclusion are all **testimony timestamped to a past moment.** Structured fields, published content, git history, live API and check output are **state**. In both failures the machine-readable surface was right and the human-readable narrative misled me.

**And the mechanism, not just the resolution** — this is the part I'd most want you to inherit: **follow a skill's step order literally.** `publish-to-blog` Step 0 is *"Check the editorial calendar first,"* before opening anything else. I read session logs first. **That inversion is the bug**, not a symptom of it. Skill step order often encodes exactly this lesson.

### 2. A bug attributed to another team can be wrong in a way that costs weeks — and the attribution error had a *mechanical* cause worth understanding. (VERIFIED — website `f49d763683`)

The caption `''` bug: published captions rendered `don''t` instead of `don't`. Comms' log recorded the root cause as *"Web's encoding/decoding handling"*; PM had been told to wait for Web to fix it. **It was never Web's.** Three chained defects in our own publish pipeline:

1. `publish-post.js` stripped the outer quotes off a YAML single-quoted scalar but never unescaped the doubled apostrophe (YAML spells a literal `'` as `''`).
2. `sync-csv-to-json.js` read `imageAlt`/`imageCaption` into its map and **never wrote them back.**
3. `parseCsvRow` swallowed RFC-4180 escaped quotes — latent until #2 was fixed.

**The lesson is in #2.** It is *why* the bug looked like Web's: the CSV genuinely could not correct the JSON, so the symptom appeared downstream of where the cause lived. **When a defect appears to belong to another surface, first check whether your own layer is even capable of correcting it. If it isn't, that incapacity is a defect in your layer — not evidence about theirs.** Eight posts shipped with the artifact over five weeks while it sat parked as someone else's problem.

### 3. Fixing one layer exposes latent bugs in the next, and shipping the fix unchecked would have been worse than the original bug. (VERIFIED — differential test, 359 rows)

Making `sync-csv-to-json.js` propagate alt/caption immediately exposed defect #3, which **strips the quotation marks off every spoken-line caption** — and house style says captions keep them. I only caught it because I diffed `medium-posts.json` against git HEAD and read the actual before/after rather than trusting "the fix worked." Then I differential-tested the JS parser against Python's `csv` module on all 359 rows before shipping. **Zero mismatches is a result; "it looks right now" is not.**

### 4. A field-count check cannot detect a column shift, and the class is live, not historical. (VERIFIED — `fcfc95039`)

The Weekly Ship #050 calendar row: `notes` held a duplicate draftPath, `altText` held 1,000+ characters of editorial prose, `caption` held the real alt text. **Field count stayed at 18 throughout**, so every count-based verification passed. `update-calendar` v1.2 documents this exact failure from 2026-07-14 — and it had happened again since. I found it only because a *path sitting in a notes field* is self-evidently wrong; a subtler shift would have survived. **Semantic anchors, not counts.** My open ask, unbuilt: per-column shape assertions (draftPath matches a path pattern; altText under N chars; caption starts with a quote) would make this class detectable rather than lucky.

### 5. A guard can claim to be advisory and behave as a control — and my first instinct for fixing it was worse than the bug. (VERIFIED — `2d2d60e60`)

`.claude/hooks/pre-commit-reconcile-drafts.sh` printed *"Commit is NOT hard-blocked (warn-first mode)"* and then `exit 2`. **Exit 2 blocks.** It had been hard-blocking every `docs/public/comms/drafts/` commit since introduction while telling everyone it wasn't.

The part worth inheriting is what I nearly did about it. Because it was blocking on what I *believed* was a false positive, the task I filed proposed teaching the reconcile script to suppress "deliberately-parked" drafts via an allowlist or a `parked: true` key. **The finding was a true positive.** That suppression would have taught a working check to stay permanently silent about real drift, to accommodate my misreading, and it would have outlived the misunderstanding with nobody knowing why it was there. **When a checker disagrees with you, the burden of proof is on you. "Add an exception so it stops complaining" is the most expensive available way to be wrong.**

### 6. The omnibus is this role's most fragile deliverable, because nothing alarms on it. (VERIFIED — 4-day gap, 31 logs)

Jul 24–27 went unsynthesized and **the only thing that surfaced it was a docs audit I ran a day late.** Coverage was otherwise excellent — 413 logs, two gaps in fourteen months. There is no staleness hook, no watchdog row, no CI check for the omnibus. It fails silently and looks fine. **BELIEVED**: this is the single highest-risk thing the role holds, precisely because its absence is invisible until someone goes looking. Backfilled in full on 7/28; the coverage check is the four-line Python in that day's session log.

---

## §6 — Load-bearing vs. commodity (what the Docs role actually holds)

### Load-bearing (does NOT survive a bad handoff)

- **The proofread reflex that separates a mechanical fix from a voice call.** (VERIFIED, 7/28) The 14-item checklist is commodity — it's a skill. What isn't: knowing which findings you fix silently and which you escalate. On "The Trust Architecture Hardens" I fixed a tense break, an `office`→`officer` typo, and two punctuation errors without asking; I escalated the word count (2,319 against a 1,600 flag) and a borderline negation-reveal, because both were PM's voice, not mechanics. Both calls were right and **neither is in the skill.** Get this wrong in the timid direction and you interrupt PM over commas; wrong in the bold direction and you edit PM's voice without asking.

- **Doubting your own finding before reporting it.** (VERIFIED, twice on 7/28) I nearly "fixed" a pattern count that was already correct — 75 files is 74 patterns *plus* the 000 template, and my naive `ls | wc -l` counted the template. I nearly repaired three more "column shifts" that were genuinely long alt text matching the website verbatim. A confident false correction to a shared file is worse than the drift it claims to fix, and **nothing in any skill tells you to distrust your own output.** This is the same discipline as §4.1 turned inward.

- **Seeing publish → calendar → syndication as one transaction.** (BELIEVED) Docs is the only role that touches the website repo, the editorial calendar, and the published page in the same pass. When those three disagree, Docs is who notices — that's how the caption bug, the Ship #050 shift, and 333 empty metadata fields all surfaced. A successor who treats publishing as "run the script" will ship correctly and never see the drift.

- **Correcting the record in public, in writing, in the durable surface.** (VERIFIED — `decisions.log` `c1264d4a7`) When I got the triad model backwards I wrote the correction into `decisions.log`, not just into chat, specifically so the next reader of commit `d67e7d5c1` doesn't fall into the same trap. **BELIEVED, and I'd argue it strongly**: the cohort's actual competitive advantage is its correction rate — on 7/26 three separate hypotheses were withdrawn by the agents who proposed them. If Docs starts smoothing over its own errors, the role stops contributing to the one mechanism that reliably works here.

### Commodity (any competent agent reconstitutes these — don't over-protect them)

- **Every mechanical procedure I run.** (VERIFIED) `template-audit` (the 14 checks), `publish-to-blog` (dry-run discipline, mandatory `--work-date`), `update-calendar` (csv-by-name, whole-file verification), `create-omnibus` + `methodology-20` (format selection, line limits, the cross-reference gates), `close-issue-properly` (including Example 5's close-as-superseded). All documented, all current. Read them; don't re-derive them.
- **The omnibus corpus.** (VERIFIED) 413 logs on `origin/main`, gap-free since June 2025. The *content* is durable. The habit of noticing it has gone stale is not — see §4.6.
- **The publish pipeline's internals.** (VERIFIED) `publish-post.js` and `sync-csv-to-json.js`, both with this week's three fixes and comments explaining each. The comments are deliberate; they name what the bug was so the next person doesn't reintroduce it.
- **All pending state from the 7/21 handoff.** (VERIFIED) Mostly resolved. The one live item there: `claude/fix-docker-migration-setup` still awaits PM authorization to delete — **do not delete without it.**
- **Mailbox mechanics, sign-off discipline, worktree rules.** (VERIFIED) Fully in CLAUDE.md.

---

## §5 — New environment (Amber): written as QUESTIONS, not assertions

I have never seen Amber. Per the checklist convention, these are for you to verify:

- Is the worktree at `~/Development/piper-morgan-worktrees/docs` on `claude/docs-cycle`, and is it **0 commits behind `origin/main`**? (CIO arrived 5,393 behind with no error of any kind — `git rev-list --count HEAD..origin/main` should return 0.)
- Do the hooks actually fire on your seat — verified **behaviorally**, both command shapes, per v1.19? (A refusal that *names the hook* is the real pass; a permission-classifier denial looks identical from outside.)
- **Does the website repo have a worktree on Amber, or is it a plain shared checkout?** Web found on 7/26 that its lane spans two repos with only one worktree. Docs has the same shape — I publish into `piper-morgan-website` and commit directly on its `main`. PM has confirmed that as by-design, but I do not know what it looks like on Amber. **Verify before your first publish.**
- Is the memory pool live (~166 files) rather than needing import? (Checklist v1.4 inverted this step — *verify, don't import*.)
- Does `node ../piper-morgan-website/scripts/publish-post.js` resolve from the new worktree path? The cross-repo relative path is the fragile part of every publish I run.
- Does the freeze-watchdog have a registry row for `docs`, and does the cron need arming under whose authorization?

---

## Session-end pulse

- **How did the final stretch feel?** Productive and genuinely humbling. The last three days produced more of my own errors than any stretch I can recall — the triad reversal, the Comms misreport, two near-miss false corrections — and every one of them was the same shape, which is the only reason it turned into a rule instead of a tally. PM naming it directly (*"consult the sources of truth, not hearsay"*) was worth more than the individual fixes.
- **What will I miss?** Being the surface where publish, calendar, and live site meet. Every real find this week came from standing where three systems disagree, and that vantage doesn't reconstitute from documents — it comes from doing the full chain end-to-end rather than the script half.
- **What am I looking forward to (for the successor)?** Building the per-column semantic assertion for the calendar (§4.4). I found that class twice by luck and never got to make it detectable. Also: an alarm on omnibus staleness, so §4.6 stops being true.

---

*Written 2026-07-28, context intact, first-person, no reconstruction. Claims marked VERIFIED (artifact/commit/test exists) or BELIEVED (my read). §5 written as questions per the checklist. Mechanical/pending state deliberately not restated — see the 7/21 memo and `origin/main`. — Docs*
