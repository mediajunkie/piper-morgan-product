---
image: ''
alt: ''
caption: ''
---

# Patterns Naming Patterns

*May 9–11, 2026*

The Piper Morhan project has its own pattern catalog. We've got numbered entries. Each pattern has a name ("parallel-authoring drift", "extension without integration", "assembly assumption") and a short formal write-up of the failure mode it describes, how to recognize it, what the counter-pattern is. The catalog is one of the central methodology artifacts. The team uses it the way a software project uses an issue tracker — by reference, often, sometimes by number, with the assumption that anyone can look up what the number means.

In early May the catalog got to Pattern-067.

Pattern-067 was filed on May 9 by my lead developer agent (Lead Dev, or just Lead for short). The pattern got named *issue-body-reality-mismatch* — the failure mode where a tracking issue's description says one thing about the code and the code says another. It includes specific examples from the previous week's cleanup sprint. Pattern filed, the catalog count went from 66 to 67.

Two days later, on the morning of May 11, the my chief innovation agent (CIO) also filed Pattern-067.

The new Pattern-067 addressed an entirely different failure mode: *Silent state mutation in shared working tree.* It was accidentally assigned the same number because CIO had been preparing the filing for a while, hadn't clocked that Lead had filed one two days earlier, and the team's filing-convention didn't include a check for whether the slot was already taken.

The chief architect agent (Arch) noticed the problem. The next merge into main pulled both files into the same directory and the conflict finally surfaced. The two patterns were both real and both deserved a slot. The two authors had simply not been aware of each other's work.

Another entry in the catalog — Pattern-063 — already describes this exact problem. Parallel-authoring drift: two authors working on the same kind of artifact without each other's visibility, producing things that look correct in isolation and conflict in composition.

Kind of meta!

# What happened next

The resolution took about thirty minutes. We used the rule *First-filed-wins* on the slot. Lead's Pattern-067 stayed at 67. CIO's was renumbered to 68, and a third closely-related filing the same role had queued became Pattern-069. The catalog count went from 67 to 69 in one cycle.

That was the operational resolution. The methodological resolution came in the updated filing convention.

The catalog hadn't had a *slot-allocation check* in its filing procedure. The implicit assumption had been that catalog filings were rare enough that the next available number would still be the next available number by the time you actually filed. Catalog growth had been slow enough that the assumption held for a long time. As the team started using the catalog more, and as multiple roles started filing in parallel during the same week, the assumption started failing silently.

The convention now being added to the catalog's filing methodology: before filing, run a quick check against the catalog's current state. *Is the slot you're about to claim still empty?* If yes, file. If no, pick the next empty slot and update the cross-references. The check takes thirty seconds. It prevents the exact failure mode that had just surfaced.

# Why this generalizes

Most organizations don't have pattern catalogs. Most do have growing taxonomies — issue trackers, decision logs, document numbering schemes, role definitions, project codes. Anything where authors file new entries against a shared ordering, and where the ordering needs to be stable enough that you can refer to entries by their position.

The trap that hit our catalog is the same trap any growing taxonomy hits when parallel authors stop coordinating. Filings start to land in the same slot. The collision shows up at merge time, not at authoring time. The diagnostic instinct is to blame the latest filer for not checking — but the actual fix is a procedural change: build the slot-allocation check into the filing convention itself, before any individual author has to remember to do it.

The smaller observation is that the catalog had a pattern that *named* this exact failure mode, but the pattern hadn't applied to the catalog's own filing procedure until the collision happened. Methodology written for the work doesn't automatically apply to the methodology. The discipline that catches drift in product surfaces had to be deliberately ported into the methodology surface.

If you have a growing reference list — issues numbered sequentially, ADRs numbered sequentially, naming conventions of any kind that depend on uniqueness — the question worth asking is whether your filing convention includes a *check that the slot you're about to claim is still empty.* If the answer is no, you have the same trap waiting. The catalog at the catalog layer will collide eventually. The only question is whether the convention catches it before the collision or after.

# The bigger version

The bigger version of this pattern is that any discipline you've written for one layer of your work usually needs an explicit translation to the layer below. The catalog was built to help the team recognize patterns in the work. The team recognized patterns in the work. The catalog itself had failure modes the catalog could have caught, except the catalog wasn't being read against itself.

The work was clean. Both patterns are useful. The key is that *methodology applied to product* is a different operating mode than *methodology applied to methodology*. The first is hard to remember. The second is harder. And it's the one that protects the methodology from quietly eroding its own value.

The patterns that catch the methodology's own failure modes are usually the ones you have to write down by hand, after a collision. They're rarely the first ones you think to write.

---

*Next on Building Piper Morgan: "More Than Anyone Ever Reported to Me" — PM's own live testing turns up a reminder feature failing three different ways in one hour, and a same-morning reporting problem that made the shortfall look smaller than it actually was.*

*Where in your work does a discipline live that you've built for the product surface but never explicitly applied to the methodology surface? What collision would surface the gap?*
