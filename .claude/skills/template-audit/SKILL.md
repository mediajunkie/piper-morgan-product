---
name: template-audit
description: Run a mechanical template audit on a finished blog draft before sending the publish-ready signal to Docs. Use after PM's voice pass is complete. Produces a pass/fail report with specific flags. Blocks the publish-ready signal on any FAIL.
scope: comms
version: 1.12
created: 2026-06-19
updated: 2026-09-02
---

# template-audit

Mechanical pre-publish checklist for Comms. Runs against the **final draft** (after PM's voice pass). Every check must pass before sending the publish-ready memo to Docs.

**Critical**: run this AFTER PM's voice pass — not before, not during. PM's edits can introduce new jargon, change section headings, or rewrite paragraphs that break previously-clean checks. The miss that prompted this skill (Jun 19): "cohort" found 4× in *This One's Taken* after PM's voice pass; Comms' pre-pass grep had returned 0.

## When to Use

- After PM confirms their voice/edit pass is complete on a draft
- Before sending the publish-ready memo to Docs inbox
- Any time PM asks "is this ready to go to Docs?"

NOT for: draft-time discipline (that's in `draft-blog-post`) or Docs' final proof (that's Step 5 of the run-of-show). This is Step 3 only.

## Pre-Flight (before reading the draft)

1. Open `docs/internal/planning/comms/blog-post-template.md` — the structural reference
2. Open `docs/internal/planning/comms/xian-voice-tone-guide.md` — the voice reference
3. Pull the next scheduled post from `editorial-calendar.csv` — needed for footer tease verification

```bash
# Get the file's pubDate, then find the next post after it
grep -i "$(basename <draft> .md)" docs/internal/planning/comms/editorial-calendar.csv
# Find the next pubDate entry after this post's pubDate
```

## ⚠️ FIRST: check the theme. Four checks are calibrated for narratives and are WRONG on Weekly Ships.

**Look up `theme` on the calendar row before running anything.** Measured 2026-08-04 against the **6 most recent published Ships** — posts that shipped clean and are live on the site:

| check | Ships that would FAIL | why it's wrong for a Ship |
|---|---|---|
| **#1** caption non-empty | **6 of 6** | Ships carry no caption by convention (#044/#050 use the literal `N/A`) |
| **#6** footer tease present | **6 of 6** | Ships sit outside the tease chain entirely — see check #6 |
| **#13** word count ≤1,600 | **4 of 6** | Ship norm is **~1,630 words** (measured #049–#053: 1279 / 1384 / 1906 / 1827 / 1764). The 800–1,300 target is a *narrative and insight* range |
| **#15** no `#NNN` in prose | **6 of 6** | `#053`, `#054` are **Ship numbers**, not issue numbers, and they are conventional in Ship prose + the previous/next links |

**So a full audit against a Ship produces roughly four false FAILs every single time.** On `theme=ship`, mark these **N/A — by convention**, never FAIL. Every other check applies to Ships unchanged.

⚠️ **Why this is worth a table rather than four footnotes**: a mandatory gate that cries wolf on four of sixteen checks trains its own operator to discard failures by eye — and the discarding habit does not stay confined to the four that deserve it. That is the same dynamic CLAUDE.md documents for the sign-off checklist, where a step that reported thousands of unpushed commits every session got quietly substituted away by the people following it most carefully. **A check that is wrong in a knowable, repeating way is a check people learn to skim.**

## The Checklist

Run each check in order. Mark ✓ PASS or ✗ FAIL with a specific note on failures. **On a Ship, apply the calibration table above first.**

### 1. YAML frontmatter — all three fields present and non-empty

⚠️ **This check used `import yaml` until 2026-07-29 and was silently unrunnable on Amber for every role, in every location** — no `pyyaml`, and **no venv anywhere on the host** including the shared checkout (found by Comms on Ship #053, independently verified one level deeper by Docs). It emitted a `ModuleNotFoundError` traceback into a column of twelve passes, which is exactly what a pass looks like to a skimming reader. **It is the frontmatter check — the class that produced the caption `''` bug — so the hole sat in the one check whose absence had already cost us a real defect.** m-44 inside the audit tool itself.

**The version below has no third-party dependency and cannot lose one.** It only needs three keys, so it parses the block directly. It also prints an explicit verdict token per key rather than relying on the reader to interpret silence.

```bash
python3 - "<draft>" <<'PY'
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
if not m:
    print('FAIL: no frontmatter block'); sys.exit(0)
body = m.group(1)
fields = {}
for line in body.split('\n'):
    if re.match(r'^\s', line) or ':' not in line:
        continue                                   # skip continuations / non-kv lines
    k, _, v = line.partition(':')
    fields[k.strip()] = v.strip()
for k in ('image', 'alt', 'caption'):
    if k not in fields:
        print(f'FAIL: {k} key MISSING')
    elif not fields[k] or fields[k] in ("''", '""'):
        print(f'FAIL: {k} present but EMPTY')
    else:
        print(f'OK: {k} = {fields[k][:60]}')
PY
```

⚠️ **`caption` is legitimately empty on Weekly Ships** — verified across #047–#052, and #044/#050 use the literal `N/A`. So a `FAIL: caption present but EMPTY` on a `theme=ship` draft is **expected and not a blocker**; treat it as N/A-by-convention and say so in the report. On narratives and insights it is a real FAIL.

**If this check ever cannot run** — a `Traceback`, a missing interpreter, anything other than three verdict lines — **report it as `⚠ CANNOT RUN`, not as PASS, and verify the frontmatter by reading it.** A check that did not execute has measured nothing, and its silence is indistinguishable from a clean result (methodology-44). The same rule applies to check #14 below.

⚠️ **`\[PM\b` was added 2026-08-03 and it is the load-bearing half.** The prior pattern missed the two bracket forms actually in use — **`[PM: …]`** and **`[PM VOICE-PASS: …]`** — which are the conventions these drafts really carry, present in **5 drafts** at the time of the fix. Measured: the old pattern scored **0** against a draft with a live open bracket, so **this check — the one that BLOCKS the publish-ready signal on placeholders — was passing drafts with unresolved PM questions in them.** It was caught only because an ad-hoc grep during a pre-pass used a different pattern than the skill's own and disagreed with it. Verified: `\[PM\b` catches every real instance across the drafts directory with **zero false positives** — every match is a genuine editorial bracket. Note the skill's own check #14 already referenced `[PM: ...]` brackets, so the form was documented here while this check could not see it.

**Caption format check**: if caption starts with `'"`, it's a spoken-line format. Verify any apostrophe inside is doubled: `'"It''s fine."'` not `'"It's fine."'` (the latter breaks YAML). ⚠️ **The `''` doubling is correct ONLY inside single-quoted YAML.** Copying that form into markdown **body** text renders the doubled apostrophe literally — a real instance shipped in the Ship #053 draft as `*"OK, let''s see"*`. If a caption also appears in the body, it takes ordinary prose punctuation.

### 2. Title is H1, and title case

```bash
grep -n "^# " <draft> | head -3
```

First `#` heading should be the post title on the first non-frontmatter line. FAIL if missing or if it's `##`.

**Also verify title case.** Every published title across all three variants (Ships, narratives, insights) uses title case, not sentence case — measured across the 8 most recent Ships (#051–#058) and 10 most recent narratives/insights, 100% title case. Small words (a, an, the, and, but, or, nor, for, so, yet, to, in, on, at, by, of, as, up, vs, is) may stay lowercase mid-title; every other word, plus the first and last word regardless of length, must be capitalized.

```bash
python3 - "<draft>" <<'PY'
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
m = re.search(r'^# (.+)$', text, re.MULTILINE)
if not m:
    print('FAIL: no H1 title found'); sys.exit(0)
title = m.group(1)
title_for_check = re.sub(r'^Weekly Ship #\d+:\s*', '', title)
SMALL = {'a','an','the','and','but','or','nor','for','so','yet','to','in','on',
         'at','by','of','as','up','vs','is'}
words = re.findall(r"[A-Za-z][A-Za-z'-]*", title_for_check)
bad = []
for i, w in enumerate(words):
    if i == 0 or i == len(words) - 1:
        if not w[0].isupper():
            bad.append(w)
        continue
    if w.lower() in SMALL:
        continue
    if not w[0].isupper():
        bad.append(w)
if bad:
    print(f'FAIL: lowercase word(s) outside small-word list: {bad} — title: "{title}"')
else:
    print(f'OK: title case clean — "{title}"')
PY
```

Added 2026-09-02 after Ship #058 published as *"What we actually had"* (sentence case) — the defect survived Exec's draft, PM's own voice pass, this skill's own audit, and Docs' independent audit, all four layers checking sense and none checking case. PM caught it post-publish and fixed it directly. Same failure shape as check #11's origin: a real, consistent corpus-wide convention that nobody had made mechanically checkable.

### 3. Dateline — italicized, correct format, no stray draft dates

```bash
grep -n "^\*" <draft> | head -5
```

Look for `*Month DD–DD, YYYY*` (or `*Month DD, YYYY*` for single-day). FAIL if:
- No dateline
- Format wrong (e.g., `*March 2026*` without day range)
- A second date line appears above the dateline (stale draft date)

### 4. Section headings — `#` for top-level, `##` for subsections only

```bash
grep -n "^##\+" <draft>
```

Top-level sections must be `#`. `##` is allowed only for genuine subsections within a section. `###` and deeper: FAIL (not used in published prose).

### 5. No placeholder brackets

```bash
grep -nE "\[PM\b|\[CHRISTIAN|PLACEHOLDER|CONSIDER\]|ADD PERSONAL|FACT-CHECK|SOURCE NEEDED|TBD\]|\[alt text" <draft>
```

Any match = FAIL. All brackets must be filled or removed before publish.

### 6. Footer tease — present and matches editorial calendar

```bash
grep -n "Next on Building Piper Morgan" <draft>
```

Must be present **on narratives and insights**. The title in the tease must match the **next scheduled post** from the calendar (checked in pre-flight step 3) — not assumed, not the next narrative beat if an insight comes first.

⚠️ **Weekly Ships sit OUTSIDE the tease chain — two rules, both measured 2026-08-03, and getting this wrong causes ACTIVE DAMAGE rather than a miss:**

- **A Ship carries no footer tease at all.** `theme=ship` → check #6 is **N/A, not FAIL**. Measured: **6 of the 6 most recent Ships (#048–#053) have none.**
- **Narratives and insights tease past a Ship to the next non-Ship post.** Measured: **7 of 8** recent cases where a Ship fell next in the calendar. So when the calendar's literal next row is a Ship, the correct tease target is the row *after* it.

**Why this warning exists**: the sentence above used to end at "next scheduled post," full stop. Read literally against the calendar it would have had me "correct" *The List That Lies* (Aug 4) to tease Ship #054 (Aug 5) — **breaking a chain that was already right**, the day before it published. Unlike check #5's blindness, a wrongly-*directive* check doesn't just miss things; it manufactures the defect it claims to prevent. **A gate that is confidently wrong is worse than a gate that is silent.**

**Determine the target this way, not from the raw next row:**

```bash
python3 -c "
import csv
rows=sorted([r for r in csv.DictReader(open('docs/internal/planning/comms/editorial-calendar.csv')) if r['pubDate']],key=lambda r:r['pubDate'])
me='<this post title>'
i=next(n for n,r in enumerate(rows) if r['title']==me)
nxt=next((r for r in rows[i+1:] if r['theme']!='ship'), None)
print('tease target:', nxt['title'] if nxt else 'NONE — last in queue')"
```

### 7. Reader question — present

```bash
grep -n "^\*.*?\*$" <draft> | tail -5
```

The closing `*[question]?*` paragraph must be present after the `---` footer separator.

### 8. Zero semicolons in prose

```bash
grep -c ";" <draft>
```

Result must be 0. Any semicolon = FAIL (banned in published prose; split into two sentences).

### 9. No "load-bearing" in prose

```bash
grep -in "load-bearing" <draft>
```

Any match = FAIL (internal docbase term; public prose uses "critical" or rephrase).

### 10. No "cohort" in prose

```bash
grep -in "cohort" <draft>
```

Any match = FAIL. Public prose uses "team" (default) or "agent team" (agents-specific context). "Cohort" is fine in session logs, mail, and internal docs — not in published posts.

### 11. Agents referred to as "people"

```bash
grep -inE "\bpeople\b|\bsomeone\b|\banyone\b|\beveryone\b|\bnobody\b" <draft>
```

**Needs judgment, not a bare grep result** — most of these are legitimate. The only FAIL case is when the word stands in for a *named agent* (PA, Arch, PPM, CXO, Comms, etc., individually or as a group) rather than for a human — a tester, a reader, a user, or a genuinely generic unknown actor. Read each match in context:

- ✗ **FAIL**: "five people independently measure the wrong thing" when the five are PA/Arch/PPM/Comms/CXO. Fix: "five agents," or name the group ("the team," "every agent who...").
- ✗ **FAIL**: a section heading like "Everyone checked, and everyone was wrong" describing a specific set of named agents. Fix: "The team checked..." ("team" is the sanctioned public-prose collective noun — see check #10) or restate with "agents."
- ✓ **PASS**: "the gate wasn't actually protecting anyone yet" — "anyone" means testers/users, not agents.
- ✓ **PASS**: "from the point of view of someone trying to set up the connector" — a human configuring the product, not an agent.
- ✓ **PASS**: a closing reader-question ("the next time several people agree with you fast...") that deliberately generalizes to the reader's own world — these are supposed to reach past the agent-specific story, don't flatten them to "agents."

Caught 2026-09-01 (PM: "recent drafts have taken to referring to agents as 'people' — we may need to add that to the things you check"), found in 2 of 2 drafts checked that morning — one had just a footer instance, the other had it running through nearly every section, including a heading. Same family as check #10 ("cohort"): an internal-register word choice that reads wrong in public prose, but unlike #10 this one can't be a pure banned-string check because half its matches are correct as written.

### 12. AI-writing-tics / cliché constructions

```bash
grep -inE "(isn't|wasn't) [a-z][^.]{0,60}\. (It'?s|It was|They were)|wasn't [a-z][^.]{0,60}, it was|-fold\b" <draft>
```

This one needs judgment, not just the grep above — read the prose for the *rhetorical device*, not only the literal string. Known members of this family (grows over time; add here when a new one gets caught):

- **The negation-reveal cliché**: "It isn't X. It's Y." / "X wasn't Y, it was Z." A dramatic-sounding contrastive construction that reads as an AI tic once it appears more than once in a piece. It can hide in other surface phrasings too — "X was never the answer. Y was" is the same shape wearing different words. **Fix**: usually just state the affirmative directly and drop the negated setup — "It's Y" / "It was Z" / "Y was" — per PM's stated technique. Caught 2026-07-09 (PM: "rife... we need to tighten up the review you do") — found in 4 of 4 drafts checked that day, none caught by the pre-existing checklist. The grep above is a starting point, not a substitute for reading: its first version only matched `It's`/`Its` as the follow-up clause and missed 3 real instances phrased as "It was" in the very next draft checked — read every `wasn't`/`isn't` in context, don't just trust a clean grep result. ⭐ **PM's discriminator, given 2026-08-09 and it is the sharpest version we have**: *"Line 59 **doesn't lead with the negation**, which is part of the tic."* **The tic is LEADING with the denial** — *"It isn't X. It's Y."* A sentence that states its claim first and uses a negation to sharpen it (*"That's a portfolio observation, not a per-decision one"*) is **not** the tic and reads fine. **Check the word order, not the presence of a negative.** Don't over-apply: a plain factual negative ("the volume held scratch data that rebuilt cleanly") is NOT this pattern — only the tight deny-then-reveal construction is.
- **"-fold" as a crutch suffix** (e.g., "twofold," "manifold significance") — rephrase plainly.
- **"load-bearing"** — see #9.
- ⭐ **Fake-personal throat-clearing** (named by PM 2026-08-08, actively being stripped): a first-person preamble that *announces* an insight instead of delivering it — *"Now here's the thing I keep coming back to…"*, *"the thing I'm keeping from this whole episode is…"*, *"if there's one lesson here…"*. **Test: delete the preamble and read on. If the sentence survives intact, it was throat-clearing.** PM: *"no loss of info and an increase in clarity and tightness."* ⚠️ **Check BOTH ENDS FIRST — openers and closings.** PM extended this the same morning: *"Openers also have a lot of that 'set up' type prose that ends up being fat to cut."* The opener dialect is scene-setting that delays the first real sentence (*"before I get into what happened, some context…"*); **often the second paragraph is the real opener.** The middle is where the argument lives and gets attention; **the opener is written to warm up and the closing is written when tired.** Original note — both instances PM named were closers, and PM's own diagnosis was *"a sign I skimmed and didn't give the closing my full attention."* A closing is written last, read least, and is the most conspicuous paragraph in the piece.
```bash
grep -inE "here'?s the thing|the thing I'?m (keeping|taking)|what I keep coming back to|if there'?s one lesson|what strikes me" <draft>
```
- **"cohort"** — see #10.

Any confirmed instance of the reveal-cliché or "-fold" = FAIL.

### 13. Word count — within range

```bash
wc -w <draft>
```

⚠️ **MEASURED 2026-08-09: this range describes 2 of the last 14 published pieces.** Actual published narratives+insights: **min 597 · median 1,403 · max 2,564**. The `>1,600` flag fires on **6 of 14** — i.e. on posts that shipped and PM was happy with. **A 597-word beat and a 2,319-word beat both published without complaint.**

**So treat the number as a prompt, never a verdict**, and read the direction:
- 🔴 **LONG is the live concern.** PM has been actively cutting since 2026-08-01 (*"length is creeping up"*, *"trim the fat more aggressively"*). Flagging >1,600 is still useful — **as a question for PM, not a defect.**
- ✅ **SHORT is not a defect.** *What the Running System Found* (614) and *Almost Beta* (597) both published clean. **Do not pad a complete story to reach a floor** — that is the exact fat PM is removing.
- **The real test is whether the piece is complete**, not whether it hits a range: does it have its arc, and would cutting anything lose information?

Nominal target: ~800–1,300 words for narratives and insights (markdown word count includes some frontmatter noise — subtract ~10). FAIL if significantly over (>1,600) — flag for PM review, don't auto-block.

### 14. Acronym sweep

```bash
python3 scripts/check-acronyms.py <draft>
```

Any `⛔ FALSE-UNPACK` line = FAIL. Warnings are advisory — surface to PM if unexpected. (Skip if script not present; note the skip.) NO-GLOSS warnings matching text ONLY inside a `[PM: ...]` editorial bracket or a `[PLACEHOLDER ...]` footer note are false positives — check where the match actually falls before flagging.

### 15. Issue/commit references in narrative prose

```bash
grep -n "#[0-9]\{3,\}\|[a-f0-9]\{7,40\}" <draft>
```

Issue numbers (#824, #888) and commit hashes in narrative prose = FAIL unless they're inside a technical-detail section or coordinate reference (e.g., a metrics table). Replace with role-functional descriptions in running prose.

### 16. Typographic residue — doubled punctuation, orphaned markers, stray double spaces

```bash
grep -nE '(^|[^.])\.\.($|[^.])|[,;:!?]{2,}|,\.|\.,|[a-z][0-9]\)|  +[A-Za-z]' <draft>
```

Any match = FAIL. Catches the class of defect that survives a voice pass because it is invisible while reading for sense: **`architecture..`** (double period), **`skill1)`** (an orphaned footnote marker glued to a word), doubled commas, and a double space before a word.

⚠️ **The three-dot ellipsis is deliberately excluded** — `So you just... draft it` is a real stylistic device and appears in the corpus. A check that flags it would be noise, and noise is how a gate gets skimmed.

**Verified against three controls before shipping** (the discipline this skill keeps re-learning):
- **known-positive** — the pre-fix *Drained on Paper*: finds both real defects ✓
- **known-negative** — the published version: 0 ✓
- **false-positive sweep** — all 17 active drafts: **0** ✓

⚠️ **Scope, stated so nobody over-trusts it**: this catches the **mechanically greppable** half of proofreading only. Docs' step-5 proof caught four defects in *Drained on Paper*; **two were this class and two were not** — `unthethering` (a misspelling) and `mistakes`→`mistake` (number agreement). **Those need a reader, and step 5 is where they belong.** This check does not make Comms the proofreader.

★ **The narrower lesson, which cost the other one**: in that same audit I *did* catch a double space and *did* fix `two distinct issue`→`issues` — then never swept for either class. **A second number-agreement error was sitting four paragraphs away.** Fixing an instance is not fixing the class; when a defect type appears once, grep the whole document for it before moving on.

## Output Format

Report results as a compact table, then a verdict:

```
TEMPLATE AUDIT — <slug> — <date>

Check                        Result
─────────────────────────────────────
1. YAML frontmatter          ✓ PASS        ← use ⚠ CANNOT RUN if it didn't execute; never PASS
2. Title H1                  ✓ PASS
3. Dateline                  ✓ PASS
4. Section headings          ✓ PASS
5. No placeholders           ✗ FAIL — [CONSIDER] at line 49 still present
6. Footer tease              ✓ PASS — teases "Branch-or-Anchor" (Jun 23) ✓
7. Reader question           ✓ PASS
8. Zero semicolons           ✓ PASS (0)
9. No "load-bearing"         ✓ PASS
10. No "cohort"              ✗ FAIL — 4 instances (lines 13, 33, 49×2, 51)
11. Agents as "people"       ✓ PASS
12. AI-writing-tics          ✗ FAIL — negation-reveal cliché at lines 17, 29
13. Word count               ✓ PASS (1,104 words)
14. Acronym sweep            ✓ PASS
15. Issue refs in prose      ✓ PASS

VERDICT: FAIL (3 issues)
ACTION: Fix items 5, 10, 12 before sending publish-ready signal.
```

## On Failure

Fix each FAIL before sending the publish-ready memo. If a fix requires PM's voice (e.g., a placeholder that only PM can fill), flag it to PM and hold the signal — do not work around it.

On PASS: send the publish-ready memo to Docs inbox per the handoff protocol (Jun 18).

## Cross-references

- `docs/internal/planning/comms/blog-post-template.md` — the structural standard
- `docs/internal/planning/comms/xian-voice-tone-guide.md` — the voice standard
- `docs/internal/planning/comms/content-publishing-run-of-show.md` — step 3 of 7
- `docs/internal/planning/comms/editorial-calendar.csv` — footer tease source of truth
- `docs/internal/development/methodology-core/methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md` — why a check that cannot run must never report as PASS

---

*v1.2 — 2026-07-29. **Check #1 rewritten to have no third-party dependency**, after it was found silently unrunnable on Amber for every role in every location (no `pyyaml`, and no venv anywhere on the host including the shared checkout). It had been emitting a `ModuleNotFoundError` traceback into a column of twelve passes — the frontmatter check, i.e. the one class that had already produced a real shipped defect (the caption `''` bug). Found by Comms while auditing Weekly Ship #053; independently verified one level deeper by Docs, who established the venv is absent host-wide rather than worktree-local. The replacement parses the block directly (three keys don't need a YAML engine) and was behaviorally tested across four shapes before shipping: filled, empty-quoted `''`, YAML-escaped `''` apostrophe inside a caption, and no-frontmatter — all correct, no traceback. Also added: the explicit `⚠ CANNOT RUN` verdict token (a non-executing check must never occupy the PASS column, per m-44), the Ship-caption N/A-by-convention note, and the warning that `''` doubling is correct in YAML but renders literally in markdown body text.*

*v1.3 — 2026-08-03. **Check #5 widened to `\[PM\b`.** The placeholder gate could not see `[PM: …]` or `[PM VOICE-PASS: …]`, the two bracket forms these drafts actually use — so the check that blocks a publish-ready signal on unresolved PM questions was scoring 0 on drafts that had them. Found during a pre-pass when an ad-hoc grep disagreed with the skill's own pattern. Zero false positives across the drafts directory. Frontmatter version and footer bumped together, which is the defect v1.2 shipped with.*

*v1.4 — 2026-08-03. **Check #6 corrected: Weekly Ships sit outside the footer-tease chain.** The check said the tease must match "the next scheduled post" with no exception for Ships. Measured against actual practice: **6 of 6 recent Ships carry no tease**, and **7 of 8** narratives/insights whose next calendar row was a Ship teased *past* it to the following non-Ship post. Read literally, the old wording would have had me "fix" *The List That Lies* to tease Ship #054 — **corrupting a correct chain the day before it published.** Distinct from the v1.3 defect and worse in kind: check #5 was *blind* (it missed things), check #6 was *wrongly directive* (it would have manufactured the defect it claims to prevent). Added a calendar-derived query for the tease target so the rule isn't re-derived by eye. Second gate defect found in this skill in one day — both surfaced by running the gate against real queue state rather than reading it.*

*v1.5 — 2026-08-04. **Added the Ship-calibration table at the top of the checklist.** Four checks — #1 caption, #6 tease, #13 word count, #15 `#NNN` refs (numbers as of v1.11 renumbering; originally #12/#14) — are calibrated for narratives and produce **false FAILs on Weekly Ships**: measured against the 6 most recent published Ships, they'd fail **6/6, 6/6, 4/6, 6/6** respectively, on posts that shipped clean and are live. Ship word norm measured at **~1,630** (#049–#053), against the narrative target of 800–1,300. Two of the four (#1, #6) already had scattered N/A notes; word count and `#NNN` refs had none. **Consolidated into one theme-keyed table rather than a fourth footnote**, because the real hazard isn't any single false FAIL — it's that a gate crying wolf on four checks teaches its operator to discard failures by eye, and that habit doesn't stay confined to the four that earned it. Same dynamic CLAUDE.md records for the sign-off checklist. Found while pre-passing Ship #054.*

*v1.6 — 2026-08-07. **Added check #15, typographic residue.** Docs' step-5 proof caught **four** defects in *Drained on Paper* after my audit passed it: `architecture..`, `skill1)`, `unthethering`, `mistakes`→`mistake`. **Two of the four were mechanically greppable and this gate should have caught them** — same family as the double space it did catch. The other two need a reader and correctly belong to step 5. Pattern verified against a known-positive (pre-fix file: finds both), a known-negative (published file: 0) and a false-positive sweep (17 active drafts: 0), with the 3-dot ellipsis deliberately excluded after it produced the only false hit. **The sharper lesson is recorded in the check itself**: the same audit caught one number-agreement error and never swept for the class, leaving a second one four paragraphs away.*

*v1.7 — 2026-08-08. **Check #12 (AI-writing-tics; #11 at the time) gains fake-personal throat-clearing**, named by PM the same morning they stripped two instances from a closing paragraph they'd voice-passed. The shape: a first-person preamble that performs reflection instead of delivering it. **The load-bearing addition is WHERE to look — closings first.** Both instances were closers, and PM's own read was that it signalled a skimmed close. Also recorded in `xian-voice-tone-guide.md` with the delete-the-preamble test.*

*v1.8 — 2026-08-08. **Throat-clearing check extended to OPENERS**, per PM within the hour: *"Openers also have a lot of that 'set up' type prose that ends up being fat to cut."* Same shape, different dialect — scene-setting that delays the first real sentence, where the second paragraph is usually the real opener. **Both ends, not the middle**: the middle is where the argument lives and gets attention.*

*v1.9 — 2026-08-09. **Check #12 (AI-writing-tics; #11 at the time) gains PM's word-order discriminator.** Reviewing *Over-Checking Pays Dividends* I flagged *"That's a portfolio observation, not a per-decision one"* as the negation-reveal shape and left it for PM. PM's ruling names the actual boundary: **"it doesn't LEAD with the negation, which is part of the tic."** So the defect is **denial-first word order**, not the presence of a negation — a claim stated first and sharpened by a negative is fine. This retires a whole class of false positives the check was generating.*

*v1.10 — 2026-08-09. **Check #13 (word count; #12 at the time) recalibrated against reality.** The 800–1,300 target describes **2 of the last 14** published narratives/insights (min 597, median 1,403, max 2,564), and the >1,600 flag fires on **6 of 14** — posts that shipped fine. Found while pre-passing Beat 21 at 550 words: I nearly reported it as under-length when *Almost Beta* (597) and *What the Running System Found* (614) had published clean weeks earlier. **The fix is not a wider range but a direction**: long is the live concern PM is actively cutting; short is not a defect; **never pad a complete story to reach a floor.** Same mis-calibration family as the v1.5 Ship table — a check whose numbers didn't match what actually ships.*

*v1.11 — 2026-09-01. **New check #11, agents referred to as "people."** PM: "recent drafts have taken to referring to agents as 'people' — we may need to add that to the things you check." Found reviewing Beats 4 and 5 the same morning: one footer instance in Beat 4, and Beat 5 ("Repetition Isn't Convergence") had it running through nearly every section including a section heading ("Everyone checked, and everyone was wrong the same way"). **This check needs judgment, not a bare grep** — unlike #10 ("cohort"), roughly half of any match set is legitimate (a "someone" configuring the product, an "anyone" meaning testers, a deliberately human-generalizing reader question). The check documents worked examples of both FAIL and PASS so the judgment call is reproducible rather than ad hoc. Checks #12–#16 renumbered up by one to make room (was #11–#15); all internal cross-references and historical changelog number-mentions updated to match current numbering, with the original number noted in parens where a changelog entry describes a check by the number it had at the time.*

*v1.12 — 2026-09-02. **Check #2 gains title-case verification.** Ship #058 published as "What we actually had" — sentence case, against a corpus where the 8 most recent Ships and 10 most recent narratives/insights are 100% title case. The defect passed Exec's draft, PM's own voice pass, this skill's own audit, and Docs' independent post-publish audit — four layers, all checking sense, none checking case, because nothing had ever made the convention mechanically checkable. PM caught it after publish and fixed it directly. Added a small-word-aware title-case script to check #2 (the natural home, since both checks read the same H1 line) rather than opening a new numbered check and renumbering the other fifteen. Verified against three controls: the original defective title (flags "we," "actually," "had"), the corrected title (clean), and a false-positive sweep of 10 real published titles across all three variants (0 false positives). Same failure shape as v1.11's origin — and the irony wasn't lost: this is Ship #058's own learning-pattern theme ("no single layer was reliable enough alone") playing out inside the very checklist meant to catch it.*
