# PDR-102: Piper's Document Model, and Knowledge in Data You Own

**Status:** Draft v0.2 (PPM, 2026-11-01). Arch's answers folded in (06:45; decisions.log 06:44). CXO's still to come (Q3, Q4). Not ratified.
**Source:** xian, in his PPM session of 2026-10-31 (decisions.log 18:46 and 18:51 PT, PPM lines).
**Tier:** 1xx, feature and capability. It sets a direction and the constraints that keep it reachable. It schedules nothing, and it admits nothing to a milestone.
**Stakeholders:** xian (owner of the vision), Arch (how), CXO (how it feels), Lead (builds), PA (MCP surface), Pard (local-model experiments on Amber).

---

## What xian said

Quoted from his chat messages; two typos are corrected and one sentence start is capitalized.

On #2226 (document search embeddings), 10-31:

> Piper learns what you want it to learn and that knowledge accrues in data you own, not on a vendor's server. That is a goal and not something we need to achieve or provide on day one but it shouldn't be viewed as some exotic idea or even really scope creep but more a matter of when. I'd rather not even rely on OpenAI, tbh, in the meantime.

On documents, the same evening:

> Piper's document model is nuanced about how it (a) creates docs, (b) ingests docs, (c) edits docs via connector, and synthesizes all of that to make artifacts, ideally with roundtrip posting back when working from a source doc via connector etc. Again, this is the vision, not the MVP, but it needs to be kept as the future we are aiming for and making possible. Local models are getting tighter all the time, too, and we can confer with Pard who is running experiments for me on Amber as new things emerge and we think of experiments to do.

## The decision proposed

1. **The target.** Piper works with documents in five ways:
   - it **creates** them;
   - it **ingests** them (uploads, and documents read through connectors);
   - it **edits** them in place through connectors;
   - it **synthesizes** across them into artifacts;
   - when an artifact started from a connector document, it **posts back** to that source (roundtrip).
2. **Ownership.** What Piper learns from a user's documents (chunks, embeddings, summaries, extracted facts) is the user's data. It lives in Piper's store under that user's account, and it leaves or is deleted with the account. It doesn't depend on a vendor holding the only copy.
3. **Status.** This is the vision, not the MVP or the 1.0 promise. Work toward it ships when xian schedules it. Until then, new work must not close it off (the constraints below).

## Constraints on work done now (so the future stays possible)

These bind any new document-touching design, at any milestone. Each is a product rule. Arch says how, or says one can't hold.

- **C1. Document is the parent concept, with a source.** A document is uploaded, generated, or read through a connector. This is xian's 06-17 model on #1270 (uploaded, generated, federated). New code keeps the source on the record and doesn't add a fourth page or object that splits the concept again.
- **C2. A connector document keeps its address.** Anything ingested through a connector keeps which connector, which item, and which version it came from. Without that, roundtrip posting can't happen later. An anonymous copy is the one shape that closes off (c) and roundtrip for good.
  - *Arch, 11-01:* uploads meet C2 once #2226's condition (m) lands. The knowledge id becomes the owner's `uploaded_files.id`, with a full content hash as the version. Today the id is a file hash shared across accounts, which is latent because the web upload route doesn't ingest yet. Connector documents can't meet C2 with today's schema: `documents.source` is a free string. **Trigger:** Arch writes an ADR (typed source plus connector, external id and version) when the first connector-ingest unit is placed. #2226 and #1624 don't need it.
- **C3. Derived knowledge is the user's and stays in Piper.** Embeddings and other derived data are computed and stored inside Piper, in durable storage (#2244 first), under the account. No new dependency on a hosted embedding vendor. This applies xian's 10-31 #2226 ruling: local embeddings, no OpenAI. Arch's int8 MiniLM conditions (decisions.log 18:50) are the first instance.
- **C4. A generated artifact records what it came from.** That means the source documents and their versions. It makes "where did this come from" answerable, and it's what a roundtrip needs.
  - *Arch, 11-01:* holds with no ADR. The first unit that persists a document-derived artifact records `derived_from` (document id and version) in the artifact, with a pin test. #1624's summarize answers in chat and doesn't persist one, so it isn't that unit unless its scope changes.
- **C5. Writing to someone else's system is always the user's choice.** Edits and post-backs through a connector follow the existing confirm-before-write pattern and the trust gradient (PDR-004). Piper never writes back silently. CXO owns the words.
- **C6. No design assumes one model vendor.** Where a model reads or writes documents, the choice of model stays swappable, so a local model can take a part when one is good enough. Pard's experiments on Amber are the way to find out when; the cohort brings him an experiment when one suggests itself.
  - *Arch, 11-01:* true for generative calls across hosted vendors (Anthropic, OpenAI, Gemini per user, #2131). A local provider would be a new provider member, not a redesign. **One single-vendor point remains: embeddings are OpenAI-only today.** #2226's local MiniLM closes it. Unverified: whether the analyzer's JSON response format works on every provider.
- **C7. Derived knowledge has its source's scope and lifetime** (Arch's proposal, 11-01). Chunks, embeddings and summaries are readable by exactly who can read the document. #1238's owner scoping already does this on reads. They're deleted when the document or the account is deleted. Without C7, C3's "your data" has no delete half. Unverified: whether an account delete removes its vector-store chunks today (`documents.owner_id` has no declared cascade). Whoever builds #2226 checks and pins it.

## Where today's issues sit against the five capabilities

From issue titles and bodies read 11-01. This isn't a plan or an order.

| Capability | Open issues that touch it | Today |
|---|---|---|
| Create | #712, #713 (document viewer and lifecycle), #1270 (object model) | Not built as a document concept |
| Ingest | #2226 (search, waits for local embeddings), #2244 (vector store on the volume), #1704 (MCP document knowledge base), #302 (document processing) | Upload works. Search from chat doesn't (letter line 6) |
| Edit through a connector | #2238 and #2203 (Notion), #2247 (Slack as a source; read only) | None yet. Notion and Slack aren't offered in the beta |
| Synthesize | #1624 (chat summarize, never worked end to end), #302 | Not working in chat |
| Roundtrip | none filed | No issue. It's vision-only until xian schedules it |

## What this PDR does not decide

- **Dates, milestones or sprint placement.** Those are xian's. #2226's timing is still his call.
- **Formats, stores, model choice, chunking.** Those are Arch's. C3 cites his 10-31 ruling and doesn't extend it.
- **How the Documents surface looks and reads.** That's CXO's, including #1270's information architecture.
- **Which connectors get edit rights first.**

## Questions for review

1. ~~**Arch:** can C2 (source address) and C4 (provenance) hold with today's upload and knowledge tables? Or does one need an ADR before the next document-touching unit lands (#2226, #1624)?~~ Answered 11-01 (under C2 and C4).
2. ~~**Arch:** is C6 already true where models touch documents, or is there a single-vendor assumption to record?~~ Answered 11-01 (under C6).
3. **CXO:** is #1270's three-source model still right as the parent concept, so C1 can cite it? It was blocked on CXO and PPM alignment in June, and PPM's half is now this PDR's C1.
4. **CXO:** for C5, is the existing confirm-before-write wording enough for a post-back, or does a post-back need its own pattern? (It changes a document someone else may also be reading.)
5. **Both:** is there a constraint missing that would close the future off and that today's work could break? Arch proposed C7 (11-01). CXO's view is open.

## Next steps

- Arch and CXO review (mail 11-01). PPM folds their answers into v0.2.
- Then it goes to xian through Exec for ratification. He's the owner of the vision.
- Once ratified, PPM checks new document-touching issues against C1–C7 when placing them, and notes the constraint on the issue.

Verified how (v0.2): Arch's memo of 06:45 read in full. His code reads are his; PPM didn't re-run them. Verified how (v0.1): the two quotes are xian's chat words of 10-31, as recorded in the PPM session log and the decisions.log lines 18:46 and 18:51 (read 11-01). #1270, #302, #712 and #1624 bodies read with `gh issue view` 11-01. The other issues are from titles in `gh issue list --search "document in:title"` 11-01, plus #2238, #2203, #2244 and #2247 read on 10-31. Layer: repo text and GitHub. Nothing was built or measured.
