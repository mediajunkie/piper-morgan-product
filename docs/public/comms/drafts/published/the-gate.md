# The Gate

*April 3–7*

<!-- image: 'ai-false.png' -->
<!-- alt: 'A path of varied inputs is diverted before reaching a large gate, emerging instead as identical gray boxes while a person looks on in confusion.' -->
<!-- caption: '"Wait, what?"' -->

Thursday night. Ten-thirty. Testing a fresh alpha account on a clean machine. The CXO had a scoring rubric ready based on the Colleague Test: three dimensions, zero through three on each, seven to pass, any zero auto-fails. Nine queries lined up. Five task lifecycle scenarios. We'd been preparing for this for weeks.

The first query was "What can you help me with?"

Every time I sit down to test Piper, I'm afraid of what I'm going to find out. It's a little bit like watching a child at a recital I imagine. 

Piper returned a canned template. The same block of text it returns for everything it can't handle. Generic. Impersonal. The kind of response that makes you check whether the system is actually running.

The second query got the same template. So did the third. And the fourth.

# Zero for seven

We tested seven of nine Gate 1 queries before we stopped. Every single one failed the Colleague Test. Four scored zero on relevance or competence — automatic failures. Two scored five, below the seven-point threshold. The one query that took a different path — creating a GitHub issue — tried to hit an API without checking whether GitHub was even configured, and returned a raw error.

Gate 2, the task lifecycle test, wasn't any better. Todo creation worked but only with rigid syntax. Todo completion failed on all four attempts. The regex rejected natural phrasing like "Add a todo" because it didn't expect the article "a" between the verb and the noun.

At 10:58, we stopped testing. There was no point continuing.

Le sigh.

# The findings

The CXO compiled five findings. Two were blocking. The floor — the conversational LLM that was supposed to be Piper's foundation — wasn't reaching the user at all. Every floor-routed query was silently failing and falling through to the same canned fallback template. The template masked the failures so completely that you couldn't tell whether the LLM had tried and failed, or had never been invoked.

Twenty-three tests had verified that todo completion worked. Every one of them mocked the service layer. In production, with a real user typing real words into a real interface, it was broken.

Pattern-045 — "green tests, red user" — wasn't a theory anymore. Six thousand three hundred tests passing. Zero out of seven queries passing the Colleague Test.

# The fix that wasn't

The Lead Dev filed #940 as a blocker and got to work. Over the weekend, the team resolved all five findings. The hardcoded Anthropic provider was replaced with a provider-agnostic configuration system. The todo regex was fixed. The avatar CSS was corrected. Pre-flight checks were added for GitHub integration. Six thousand three hundred and three tests passing, zero failures.

On Monday evening, the CXO ran the gate again. All nine queries this time.

The result: zero out of nine. Identical canned templates for every floor-routed query. The same response as four days earlier, as if nothing had changed.

Oh, brother.

The CXO's memo to the Lead Dev asked three questions: Is the LLM call actually executing? Is the fix actually deployed? Is something overriding the floor before it gets a chance to respond?

Two complete failures. Five "fixes" applied between them. Same result. Something deeper was wrong, and we hadn't found it yet.

The hunt continued...

---

*Next on Building Piper Morgan: The Multi-Wave Investigation, an insight piece from December 25, 2025, on what happens when ninety minutes of parallel investigation — thirteen subagents across four waves — surface the blockers no sequential checklist would have caught.*

*Have you ever fixed a bug only to find the same symptom waiting for you on the other side?*
