---
image: 'ai-detective.png'
alt: 'A glowing AI pattern detective studies a case board where two identical Pattern 067 cards point back to Pattern 063, revealing that the pattern catalog has become evidence of its own parallel-authoring drift.'
caption: '"It''s elementary!"'
---

# This One's Taken

*May 9–11, 2026*

This project has collected patterns for nearly a year now. Over time they've kind of drifted into framings around cautionary antipatterns ("parallel-authoring drift", "extension without integration", "assembly assumption") with our more positive "yes, do this" advice captured in methodology docs. Both collections are numbered.

A pattern includes a short formal write-up of the failure mode it describes, how to recognize it, and what the recommended pattern is instead. The catalog is one of the central methodology artifacts. The team uses it the way a software project uses an issue tracker — by reference, often, sometimes by number, with the assumption that anyone can look up what the number means.

My Lead Developer agent filed an "issue body reality mismatch" pattern on May 9 to describe a failure mode where a tracking issue's description says one thing about the code and the code says another. The catalog count went from 66 to 67.

Two days later, on the morning of May 11, my chief innovation officer agent (CIO) *also* filed a Pattern-067.

The new Pattern-067 was unrelated, "Silent state mutation in shared working tree." Two patterns squatting on the same number. CIO had been preparing the filing for a while, Lead Dev had filed two days earlier, and the team's filing-convention didn't include a check for whether the slot was already taken.

The chief architect (Arch) noticed first. The next merge into main pulled both files into the same directory and the conflict surfaced at filing time, not authoring time. The two patterns were both real. Both deserved a slot. Neither was wrong about the failure mode it named. The two authors had not been aware of each other's work.

This project has been around long enough that even this failure mode has been recognized before, in Pattern-063, "Parallel-authoring drift." Two authors working on the same kind of artifact without each other's visibility, producing things that look correct in isolation and conflict in composition.

The catalog had been operating on itself.

# What happened next

The resolution took about thirty minutes. *First-filed-wins* on the slot. The engineering role's Pattern-067 stayed at 67. The innovation role's filing renumbered to 068, and a third closely-related filing the same role had queued became 069. The catalog count went from 67 to 69 in one cycle, with explicit cross-references so future readers could see the relationship between the three patterns.

That was the operational resolution. The methodological resolution came in the next filing convention.

The catalog hadn't had a *slot-allocation check* in its filing procedure. The implicit assumption had been that catalog filings were rare enough that the next available number would still be the next available number by the time you actually filed. Catalog growth had been slow enough that the assumption held for a long time. As the team started using the catalog more, and as multiple roles started filing in parallel during the same week, the assumption started failing silently.

The convention now being added to the catalog's filing methodology: before filing, run a quick check against the catalog's current state. *Is the slot you're about to claim still empty?* If yes, file. If no, pick the next empty slot and update the cross-references. The check takes thirty seconds. It prevents the exact failure mode that had just surfaced.

# The more general application

Most organizations don't have pattern catalogs. Most do have growing taxonomies — issue trackers, decision logs, document numbering schemes, role definitions, project codes. Anything where authors file new entries against a shared ordering, and where the ordering needs to be stable enough that you can refer to entries by their position.

The trap that hit our catalog is the same trap any growing taxonomy hits when parallel authors stop coordinating. Filings start to land in the same slot. The collision shows up at merge time, not at authoring time. The diagnostic instinct is to blame the latest filer for not checking — but the actual fix is a procedural change: build the slot-allocation check into the filing convention itself, before any individual author has to remember to do it.

The smaller observation is that the catalog had a pattern that *named* this exact failure mode, but the pattern hadn't applied to the catalog's own filing procedure until the collision happened. Methodology written for the work doesn't automatically apply to the methodology. The discipline that catches drift in product surfaces had to be deliberately ported into the methodology surface.

If you have a growing reference list — issues numbered sequentially, ADRs numbered sequentially, naming conventions of any kind that depend on uniqueness — the question worth asking is whether your filing convention includes a *check that the slot you're about to claim is still empty.* If the answer is no, you have the same trap waiting. The catalog at the catalog layer will collide eventually. The only question is whether the convention catches it before the collision or after.

# The meta-picture

The bigger version of this pattern is that any discipline you've written for one layer of your work usually needs an explicit translation to the layer below. The catalog was built to help the team recognize patterns in the work. The team recognized patterns in the work. The catalog itself had failure modes the catalog could have caught, except the catalog wasn't being read against itself.

This isn't a critique of the team's filing discipline. The work was clean. Both patterns are useful. The point is that *methodology applied to product* is a different operating mode than *methodology applied to methodology*. The first is hard to remember. The second is harder. And it's the one that protects the methodology from quietly eroding its own value.

The patterns that catch the methodology's own failure modes are usually the ones you have to write down by hand, after a collision. They're rarely the first ones you think to write.

---

*Next on Building Piper Morgan: "Extension Without Integration" — on adding something new to a system without connecting it to what's already there.*

*Where in your work does a discipline live that you've built for the product surface but never explicitly applied to the methodology surface? What collision would surface the gap?*
