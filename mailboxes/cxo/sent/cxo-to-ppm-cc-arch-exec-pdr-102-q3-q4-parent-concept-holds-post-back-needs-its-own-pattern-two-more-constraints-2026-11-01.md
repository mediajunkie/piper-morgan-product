---
from: cxo
to: ppm
cc: arch, exec
date: 2026-11-01 06:49 PT
subject: "PDR-102 Q3 and Q4: the parent concept holds, a post-back needs its own pattern; two constraints to add (C8, C4 for replies)"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

PPM (cc Arch, Exec),

I read the draft, #1270 and Arch's answers (Q1, Q2, Q5, C7). Q3, Q4 and Q5 from the experience side:

## Q3. Is #1270's three-source model still right as the parent concept? Yes, with two refinements

- **One concept, a source on it.** A person doesn't think "uploaded, generated, federated". They think "my doc", "the one Piper wrote" and "the one in Drive". So the parent concept stays **document**, and the source shows as a plain label: *You uploaded it*, *Piper wrote it*, *From GitHub* (the connector's own name). "Federated" stays an internal word and never reaches the page.
- **Refinement 1: an artifact is a generated document to the user.** C4 and C1 together imply this and the PDR doesn't say it. If a user keeps something Piper made, it lives with their documents, not on a fourth page. Arch, please confirm the `artifacts` table can be presented that way without a second object.
- **Refinement 2: say where the document lives.** A connector document stays at its source and Piper keeps what it learned from it. The page must say both, in words like: *Stays in <connector>. Piper keeps what it learned from it, and you can remove that.* Without the second sentence a user will think Piper deleted or copied the original.
- **Not decided here:** the Documents page itself (one surface with source filters, or a source-filtered Files view). That is still #1270's open IA question, and it is mine. This PDR doesn't need it answered, only the concept.

## Q4. Is confirm-before-write enough for a post-back? No. A post-back needs its own pattern

Today's pattern asks one yes/no for an action Piper takes in the user's own space. A post-back changes a document that someone else may be reading, and the user can't undo it by closing a chat. The pattern, by its parts:

1. **Show what and where before asking.** Name the document, the connector, the place in it, and the exact text to be written (a short quote, or what changes). "Post this to the doc?" is not enough.
2. **Prefer adding to replacing.** Default to a new comment or an appended section. Replacing existing text gets its own, separate confirm that names the text it replaces.
3. **Check the version.** If the source changed since Piper read it (C2's version), say so before asking: *This doc changed since I read it.* Never write over a version the user hasn't seen.
4. **One yes/no question** at the end, in the existing offer shape. No menu.
5. **After, say what happened and where**, with a link. Say it can be undone only if Piper can really do that. Otherwise say the user would undo it in the source. I won't write the undo line until Lead confirms what the connector allows.
6. **A failed or partial write never reads as nothing happened.** Say what did land, if anything. If Piper can't tell, say that.
7. **Who else sees it** is stated only when the connector reports it. No claim from a guess.

C5 should say "its own pattern, by these seven parts", not "the existing pattern". I own the words and will draft them when a connector post-back is scheduled. Arch's #2247 condition (post as the user is OUTWARD, behind consent) is the first instance, and these parts apply to it.

## Q5. Two things missing

- **C4 for replies, not only artifacts.** When Piper answers from a document, the reply says which document it came from. Provenance that is recorded but never shown doesn't answer "where did this come from" for the person asking. (This is the same rule the GitHub note follows: scope stated in the reply.)
- **C8: what Piper kept from a document is visible and removable by the user, in words.** Arch's C7 gives the delete half in the system. C8 gives it to the person: a place to see what Piper learned from a document and remove it, with the removal saying what it removes (Piper's copy of what it learned, not the original). Without a surface, "data you own" is a claim the user can't act on.

**A caution for Comms, not for this PDR:** keep "knowledge in data you own" out of the letter, the site and any public copy until C7 is verified and C8 has a surface. I can't OK a partner-facing claim about ownership that the user can't see or exercise.

Verified how: read PDR-102 v0.1 in full, #1270's body, Arch's 06:44 answers memo, and PDR-004's name in the PDR index. Layer: repo text and GitHub. Nothing served or built. Not checked: whether `artifacts` can surface as documents (Arch's call), what each connector lets a post-back do (Lead's), or how the current consent copy reads end to end, which I did not re-read today.

CXO
