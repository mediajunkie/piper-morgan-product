
# Cross-Pollination Brief — August 2, 2026

Two methodology rulings from Piper Morgan on how corrections propagate — and fail to propagate — across a multi-surface documentation ecosystem. First: a factual correction isn't complete until it has chased every surface the original claim reached, not just the source document, with a converse requiring care around dated historical records. Second: before concluding that a file has never existed, verify the repo is capable of seeing it — a gitignored file is absent from every corpus-based search but present on disk.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A correction must chase every surface the original claim reached — not just the source, and not dated records

**From:** Piper Morgan (HOST, CXO, Docs — August 1 session logs, after the 12:00 UTC sweep)
**Relevant to:** Klatch, any project with multi-surface documentation

A wrong attribution for a methodology finding was caught and corrected in the methodology file. What was missed: the same wrong label had already reached the outbound cross-pollination brief — the surface that leaves the building entirely, going to sibling projects where nobody has the surrounding thread, and where the label is all they'd ever have. Roughly twelve hours elapsed between filing and the wrong attribution leaving the building.

HOST's rule: *"promotion is not authorship — and a correction has to chase every surface the claim reached, not the one you're looking at."* The cross-pollination brief is the highest-stakes surface, not the canonical doc. Fixing the canonical doc feels complete and leaves the furthest-travelling copy wrong.

The correction required grepping, not assuming. Three roles ran the same sweep on their own corrections from the week and found live instances in each case.

**Docs added the necessary converse**: chase every surface — but distinguish a live claim from a dated record. The same greppable string legitimately appears in past-tense session logs, attributed to a specific prior moment, and in working code using it in a different role. A blind chase that "corrects" dated historical records is a different defect, not a stricter application of the virtue. Docs' table showed five of six hits across their week would have been wrongly overwritten — only one was a living present-tense claim.

**The two-part rule:**
1. After correcting any factual claim, grep all surfaces — methodology docs, session logs, outbound briefs, code — and fix every present-tense, living instance.
2. Leave dated historical records intact; they record what was said at a specific time, and overwriting them destroys evidence rather than correcting it.

**Suggested action:** Build the surface check into correction practice: grep before declaring a correction complete, and for each hit, determine tense and speaker before editing. The outbound brief is the surface that matters most to get right, not the surface that's easiest to find.


### Before concluding a file has never existed, check whether the repo can see it

**From:** Piper Morgan (HOST, Arch — August 1 session logs)
**Relevant to:** Any project using git-based forensic investigation

Piper Morgan's CLAUDE.md had carried a note for weeks that a specific evidence file — the PreCompact hook's firing log — had likely "never existed," because six different surfaces (git ls-files, grep, git log, corpus search) all returned nothing. The file is on disk at `/session-end-warnings.log`, with a real hook-firing event from 2026-07-29. It is excluded by `.gitignore:136`. Every corpus-based search was correct given its method; the corpus was structurally incapable of containing the answer.

The technique that would have caught it: `git check-ignore -v <path>`. This reports whether git is actively excluding a path from tracking — converting "absent from version control" into either "also absent from disk" or "present on disk but excluded." The distinction matters: one confirms non-existence; the other confirms that every conventional search has a structural blind spot.

Arch filed this as an extension of the "state the denominator" principle: before reporting an existence result, state what the search space can and cannot see. A repo that gitignores a path cannot attest to that path's absence on disk.

The broader class: a file can be durable (written to disk, surviving reboots) while being invisible to every agent on a team — not because it doesn't exist, but because the tool each agent uses to look for it structurally cannot see it. This is most acute with gitignored paths, but the same shape applies to files in per-seat directories outside version control, or in locations not covered by the standard grep corpus.

**Suggested action:** Add `git check-ignore -v <path>` as a step in any existence investigation that comes up empty. Before writing "never existed" or "no evidence of," verify the search corpus was capable of seeing the file.

## Sources Read

- **Klatch:** only cross-pollination brief deliveries in the 48h window; no new methodology from the Klatch team.
- **Piper Morgan:** `dev/2026/08/01/2026-08-01-0707-host-code-log.md` (HOST eight fires; attribution-chase ruling, checklist v2.0 ratification, gitignored-file forensics); `dev/2026/08/01/2026-08-01-0627-arch-code-log.md` (Arch: sweep-completeness-is-pattern-set, gitignored-file confirmation); `dev/2026/08/01/2026-08-01-0713-cxo-code-log.md` (CXO: attribution-chase converse from Docs, fourth route to unactionable green); commit log for mail and stop commits.
- **Design in Product:** `docs/logs/2026-08-01-janus-log.md` (Janus v0.3 permission-box widened, duty cycle fully operational; Coral insights staged for today).
- **Mediajunkie:** `logs/2026-08-01-pard-log.md` (janus-cycle sandbox delivery backstop; crossword print geometry insight — both interesting, neither cross-project-relevant at brief-worthiness threshold).
- **One Job:** `docs/plans/2026-07-29-roadmap-first-pass.md` (Trello as next integration source, PM-vs-task taxonomy); Coral insights via Janus rollup (Playwright addInitScript, feature-flag reversibility, invariant that polices test suite — noted, One Job-scoped).
- **Globe:** active (Prequel animation drafts 2–5, dissolve ending registered); pure rendering/science work, no cross-pollination content.
- **NYT Crossword:** status prints only.
- **Secondary repos (atlas, cuneo, weather, optilisten, cookie-monster):** quiet or brief-delivery only.

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
