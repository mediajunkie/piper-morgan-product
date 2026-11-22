---
image: ''
alt: ''
caption: ''
---

# Test the Page You Draw

*November 8–15, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Sat 2026-11-28 (insight, tentative per your 11-18 yes to the sketch). Title is a placeholder. You said on 11-20 it sounds awkward and you'll come up with a new one. Comms won't propose one unless you ask. It's needed before Sun 11-22's footer teases it.
Sources: the mining pass Nov 6-16 (11-17). Comms re-opened every quote below at source on 11-18. Files are docs/omnibus-logs/2026-11-DD-omnibus-log.md, cited "Nov DD lNN".
-->

## The principle (one line, yours to word)

A test that checks the code is not a test of what the person sees. Tests pass in the world the test builds, so build it from what the user gets.

## Two episodes, a week apart (facts verified)

**1. Nov 8: the fixtures agreed with the bug.**
- A new module (forgetting or changing a learned preference) read the value "done", while the path that clears a preference stores "complete". [Nov 8 l48]
- The tests had been seeded from the module's own words, so every test passed while real rows read as unknown. Arch put it on hold at 09:27. Lead called it Lead's own miss. [Nov 8 l48, l101]
- The lesson the team wrote down: "Read the producer's constants before seeding a fixture." [Nov 8 l101]
- It was fixed, served that afternoon, and closed the same day. [Nov 8 l48]

**2. Nov 15: you found it on your own screen.**
- At 18:57 you read three screens and reported that the Settings link "GitHub repositories" was a small text link you did not see, the GitHub card read "Settings", and there was no way to add a repository once one was installed. [Nov 15 l58]
- Your words, relayed at 19:11: "a floating link on that page violates the design and probably at least six other principles of this project or common sense". [Nov 15 l58]
- Lead found the cause at 19:17: the link had been put in the branch that draws Slack and Calendar, not the branch that draws GitHub. Lead's tests "ran a label function against a stub and read source text, and none drew a card." [Nov 15 l58]
- CXO moved the entry from a link to a card ("Manage repositories", "Add another repository"), and the fix landed that evening. [Nov 15 l58]
- The rule the team took from it: "A test that reads source text is not a drawn page." Drawn-card tests now run the page's own script and read the HTML it writes. [Nov 15 l105]

## Your angle, maybe

- Both test suites were green. Both were testing the team's idea of the product, not the product.
- The cheapest test of a screen is a person looking at it, and that person was you. The fix was to make the tests look the way you look.
- Product-manager reach: "the tests pass" and "the user can do it" are two claims. Ask which one you're hearing.

## Careful with these (accuracy)

- **Overlap:** "Check the Machine First" (11-01) is about agents checking the actual facts before debating. This one is about what the test itself draws. Keep the angle on the test.
- The logs record only your read of the Nov 15 screens. Don't say an outside tester hit it.
- Agents are "agents" or by role (Lead, Arch, CXO), never "people" or "someone".
- No issue numbers in prose.

---

*Next on Building Piper Morgan: [TEASE: Thu 12-03 "Ready or Not" (tentative, arc 2: the release decision, late October). Needs your final title before this goes to Docs.]*

*[Reader question, yours to write. A start: "When your tests last passed, what were they actually looking at?"]*
