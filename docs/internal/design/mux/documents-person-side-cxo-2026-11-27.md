# Documents, from the person's side: CXO's prep for the MUX document-model discussion

- **Author**: CXO, 2026-11-27, for the week-1 discussion xian asked for (Exec 01M8F85S17).
- **Source**: Arch's built picture, `docs/internal/architecture/current/document-implementation-map.md` (read whole), and `docs/internal/design/mux/objects-catalog.md` (the Document row). I read no source and ran nothing; every fact about the build is Arch's.
- **What this is**: for each of the map's six questions (section 6), what a person expects and the answer I would recommend. Recommendations, not rulings. The decisions are xian's, with PPM and Arch.

## What a person believes

"I gave Piper this file, so Piper knows it." Today a file a person uploads is stored and can be summarized or analyzed when they ask about it by name. Nothing indexes it, nothing searches it, and nothing relates it to a project or a conversation. The gap between the belief and the build is the honesty problem, not the missing feature.

## The six questions

1. **Which "document" does the vision mean?** Recommend: one thing to the person, **the file they uploaded**. The index is how Piper finds things in files; it never appears as a second kind of document in any sentence a person reads. Today there are two objects with no shared id. That is a build fact; the words should already be one-document words.
2. **Should an upload be indexed?** Recommend yes, eventually, because "find the file where I wrote about pricing" is what a person expects after uploading. Two costs to say plainly to xian: it needs the person's own OpenAI key until the local-embeddings work (2226), and the index is emptied at each deploy until 2244. Until both are true, no served sentence may imply search over uploads.
3. **Should documents belong to projects or conversations?** Recommend projects, optional, set by the person ("add this to Launch"), and never silently bound to the conversation they were uploaded in. A document that vanishes from view when the conversation ends reads as lost.
4. **The summary reads the first 3,000 characters.** In hand: 2444, with the one-sentence disclosure. Reading in pieces waits on this discussion (PPM).
5. **`.docx` is accepted but not read.** In hand: 2443, read it, one table feeding the allow-list and the extractor, my words posted on 2443.
6. **Chat's "search documents" means Notion.** Recommend the reply says which place it searched, always: "I searched Notion" (or "your Notion workspace"), and when Notion is not connected, says so and says it does not search uploaded files. Today's reply when Notion is not connected is "can't search documents from chat yet", which is honest but does not tell a person who just uploaded a file why it can't find it. Wording after xian rules question 2.

## What I would ask xian to decide

- **Q2 and Q3 are the two real product decisions.** Index uploads or not, and project ownership or not. Everything else follows from them or is already in hand (4 and 5).
- **Sequence:** 2443 and 2444 are small and true regardless of the answers; they do not wait on this discussion except for the "read in pieces" option.

## What I would bring served

Nothing new is served for this. If useful in the room, two quotes from a seat: a `.docx` upload and summary before 2443 lands, and a long PDF's summary before 2444 lands, so the discussion has the person's actual screen, not the code. Web would run them; I judge the words.
