# Documents, from the person's side: CXO's prep for the MUX document-model discussion

- **Author**: CXO, 2026-11-27, for the week-1 discussion xian asked for (Exec 01M8F85S17).
- **Read with**: Arch's comparison, https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/current/document-mux-comparison.md (his page cites this one).
- **Source**: Arch's built picture, `docs/internal/architecture/current/document-implementation-map.md` (read whole), and `docs/internal/design/mux/objects-catalog.md` (the Document row). I read no source and ran nothing; every fact about the build is Arch's.
- **What this is**: for each of the map's six questions (section 6), what a person expects and the answer I would recommend. Recommendations, not rulings. The decisions are xian's, with PPM and Arch.

## What a person believes

"I gave Piper this file, so Piper knows it." Today a file a person uploads is stored and can be summarized or analyzed when they ask about it by name. Nothing indexes it, nothing searches it, and nothing relates it to a project or a conversation. The gap between the belief and the build is the honesty problem, not the missing feature.

## The six questions

1. **Which "document" does the vision mean?** Recommend: one thing to the person, **the file they uploaded**. The index is how Piper finds things in files; it never appears as a second kind of document in any sentence a person reads. Today there are two objects with no shared id. That is a build fact; the words should already be one-document words.
2. **Should an upload be indexed?** Recommend yes, eventually, because "find the file where I wrote about pricing" is what a person expects after uploading. Arch's comparison (linked below) frames the real choice as B (index after the local-embeddings work, 2226) or C (never; the words say so), because indexing now fails for most keys. The cost to say plainly to xian: it needs the person's own OpenAI key until 2226. (Correction, Arch 01M8F92T97: 2244 has been served since 11-26, so the index no longer empties at each deploy; its last row is xian's CLI check.) Until 2226, no served sentence may imply search over uploads.
3. **Should documents belong to projects or conversations?** Recommend projects, optional, set by the person ("add this to Launch"), and never silently bound to the conversation they were uploaded in. A document that vanishes from view when the conversation ends reads as lost.
4. **The summary reads the first 3,000 characters.** In hand: 2444, with the one-sentence disclosure. Reading in pieces waits on this discussion (PPM).
5. **`.docx` is accepted but not read.** In hand: 2443, read it, one table feeding the allow-list and the extractor, my words posted on 2443.
6. **Chat's "search documents" means Notion.** Recommend the reply says which place it searched, always: "I searched Notion" (or "your Notion workspace"), and when Notion is not connected, says so and says it does not search uploaded files. Today's reply when Notion is not connected is "can't search documents from chat yet", which is honest but does not tell a person who just uploaded a file why it can't find it. Wording after xian rules question 2.

## What I would ask xian to decide

- **Q2 and Q3 are the two real product decisions.** Index uploads or not, and project ownership or not. Everything else follows from them or is already in hand (4 and 5).
- **Sequence:** 2443 and 2444 are small and true regardless of the answers; they do not wait on this discussion except for the "read in pieces" option.

## What I would bring served

Nothing new is served for this. If useful in the room, two quotes from a seat: a `.docx` upload and summary before 2443 lands, and a long PDF's summary before 2444 lands, so the discussion has the person's actual screen, not the code. Web would run them; I judge the words.

## The person's steps, and what each one says today (added 2026-11-28)

The path a person walks with a file, in order. Each row: what they do, what they expect Piper to do, what it does today (Arch's map), and the one sentence that must be true. A row marked **words open** has no sentence I would sign yet.

| # | They do | They expect | Today | The sentence must say |
|---|---|---|---|---|
| 1 | Upload a file | Piper has it and tells them so | Stored; accepted types are one list, `.docx` accepted but not read (2443) | The file's name and that it is saved. Never "indexed", never "searchable" |
| 2 | Ask for a summary, by name | A summary of the whole file | First 3,000 characters (2444) | What part it read, in the summary's own first sentence (2444's disclosure) |
| 3 | Ask about the file without naming it ("what did my pricing doc say") | Piper finds it | No search over uploads | That it can't look across files yet, and that naming one works. **Words open** until xian rules Q2 |
| 4 | Say "search my documents" | Their files searched | Searches Notion only | Which place it searched, always; when Notion isn't connected, that it did not search uploaded files (Q6) |
| 5 | Add the file to a project ("add this to Launch") | The project shows it | No file-to-project link | A true refusal until Q3 is ruled; after a yes, one confirm line naming file and project. **Words open** |
| 6 | Come back tomorrow | The file is still there | Stored per account; the index emptied at deploy until 2244 (served 11-26) | Nothing, unless asked; then "saved on your account" and no more (PDR-102: no ownership or backup claim) |
| 7 | Delete the file | It is gone, and Piper no longer uses it | Not read for this page | Unchecked: a delete line is claimed only after a seat read. **Words open** |

Rows 3, 5 and 7 are the three where a person's belief outruns the build today. Rows 1, 2, 4 and 6 are covered by in-hand work (2443, 2444, Q6 wording) and need only the served reads below.

## Seat reads requested (Web), for the 12-01 room

1. A `.docx` upload on a seat account, then "summarize it": the whole reply quoted.
2. A long PDF (over 3,000 characters, ideally several pages), then "summarize it": the whole reply quoted, and whether it says what part it read.
3. Row 7: delete the uploaded file, then ask for it by name: both replies quoted.

I judge the words on the quotes; Web runs them. Nothing here is built or ruled by this page.

## Served on 11-28 (Web 01M8H9J72V, seat-tester-1, beta; judged in 01M8H9Z1PP)

- Row 1/2, .docx: the upload dialog allows Word (.docx); "summarize it" returned the refusal split into two bullets under a summary heading. Fails.
- Row 2, long PDF (8 sections, 7,486 characters): the summary covered sections 1 to 3, said "I read 'harbor-report.pdf' from your files" and "across three sections", and never said it read only the start. It also repeated itself. Fails the 2444 bar.
- Which-file question with two files: asked which, listed both. Passes.
- Row 7, delete then ask by name: "I didn't find 'harbor-report.pdf' in your uploads. Paste the text here and I'll work with it." Passes. The Remove dialog doesn't name the file; "can't be undone" awaits Lead's confirmation.
