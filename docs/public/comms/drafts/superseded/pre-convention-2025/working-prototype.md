![From Research Question to Working Prototype: Building an AI PM Assistant from Scratch](https://media.licdn.com/dms/image/v2/D5612AQEYHA0y6EZeow/article-cover_image-shrink_720_1280/B56Zf0biJSHcAU-/0/1752152550654?e=2147483647&v=beta&t=NEiXLPRDE8Ql7FeACB2OzPftWZFdYcfL3AUHqcemcF8)

"How hard could it be?"

# From Research Question to Working Prototype: Building an AI PM Assistant from Scratch

_Still May 29, 2025_

You know that moment when you realize you’re spending more time managing your work than doing your work? That was me, drowning in GitHub tickets, meeting notes, and legacy documentation that might as well have been written in Linear B.

“How hard could it be to build an AI assistant?” I thought, with the dangerous confidence of someone who’d just discovered LangChain existed.

_Narrator: It was harder than he thought._

## The delusion that started it all

The initial fantasy was simple: Build a “junior PM intern” that could handle the mind-numbing parts of product management. You know, the stuff that makes you question your career choices:

- Turning rambling Slack messages into properly formatted GitHub tickets
- Finding that one crucial decision buried in 47 pages of meeting notes
- Explaining why we can’t just “make it work like Amazon” for the thousandth time

The research question sounded so academic: “How can I develop my own AI agent to handle routine knowledge-management tasks?”

What I actually meant was: “Can I automate myself out of the boring parts of my job without accidentally automating myself out of a job?”

## Platform shopping: the no-code mirage

I had played around with ChatGPT and the other free bots out there of course, but the problem is they don’t learn and they don’t remember. We don’t even want them to learn because who trusts OpenAI?

But I wanted something that could persist, get better, get to know me and my ideas about how to be a good PM.

The brutal truth: No-code solutions are great if your use case is “slightly smarter chatbot.” For anything that actually needs to understand your organization’s context? Time to write some code.

## Choosing the stack (or how I learned to stop worrying and love dependencies)

I initially went with Python + LangChain + Chroma + OpenAI because:

1.  Everyone else was using it (peer pressure works)
2.  The documentation existed (mostly)
3.  I could pronounce all the library names (underrated feature)

The real reason? That was the stack recommended to me in my very first chat on the subject (which I just found, so we will include a flashback to tat earlier moment at some point!). Also, I needed something I could rip apart and rebuild when it inevitably didn’t work. Vendor lock-in is like a bad relationship — easy to get into, painful to leave.

## Building the first prototype (a comedy in three acts)

Act 1: Environment setup Hell

I’m really not a programmer so my desktop “hygeine” is atrocious. The first few sessions of work I had to recreate my environment from scratch each time, endlessly re-installing and upgrading the same packages over and over.

Act 2: The Document ingestion dance

Remember when you thought “I’ll just load some documents” would be simple? Me too. Over time I was able to get the prototype to ingest documents, but later when I started working on the real thing and we were inspecting the prototype code, Claude told me the chunks were cutting through sentences. Apparently, this is something of a solved problem but I got the low-rent version on my first try.

Act 3: The first real question

After two days of setup, dependency hell, and questioning my life choices, I asked the system a question about an uploaded doc and, it did OK.

I may have done a small victory dance.

## The trivial technical challenges nobody warns you about

Then there’s “library version roulette” when you get the latest version of something and it turns out one of your other somethings doesn’t know how to work with that latest version, so you have to downgrade it. Then that happens the next time and eventually you remember to pin it (?) or just make it clearer what the acceptable version range is in your .env file.

## Creating test data (fiction for bots)

To properly test this thing, Claude made me a handful of realistic PM documents. This definitely saved me time. Writing good test data by hand woild have taken almost as long as conjuring up the prototype. But bad test data is like testing a boat in your bathtub — sure, it floats, but will it handle the ocean?

## What actually worked

RAG (Retrieval-Augmented Generation): Despite the terrible acronym, this approach was magic. The system could actually understand questions like “Why did we choose PostgreSQL?” and give answers that didn’t sound like they came from a fortune cookie.

The Modular Mess: My spaghetti code architecture accidentally turned out to be brilliantly modular. When I needed to swap vector databases, it only took… okay, it took six hours and a lot of swearing, but it COULD be done.

Local Development: No API costs during development meant I could fail fast, fail often, and fail spectacularly without explaining a $500 OpenAI bill to finance.

## What took forever

Context Management: Maintaining conversation state was like teaching a goldfish to remember your birthday. Possible, but requires more engineering than you’d think. This is something I still struggle with, even as I accumulate a growing bag of tricks

Error Handling: LLMs fail in creative ways but tend to generate extremely unhelpful error messages. Building even simple error handling took twice as long as building the happy path, and on the MVP today we still haven’t made error handling much more helpful yet.

Bug squashing: Turns out vibe coding tends to mean spending more time doing QA and fixing bugs than generating new routines. Who knew? (Besides, well, everyone posting on LinkedIn these days, apparently.)

## The path to production (spoiler: it’s paved with broken prototypes)

The prototype worked! Sort of. If you:

- Ran it locally
- Didn’t mind waiting 30 seconds for responses
- Didn’t expect it to do very much yet.
- But it didn’t seem to crash (much)!

And it proved the concept. An AI could understand our PM context and provide useful answers. Now I just had to make it… you know… actually usable.

## Lessons for my future self

Start with the data model: Understanding your information architecture beats having a pretty interface every time.

Build for replaceability: That perfect library you found? It’ll be deprecated next month. Plan accordingly.

Local first, cloud later: Work out the kinks without burning API credits. Your finance team will thank you.

Test data is real work: Budget time for it. Like, real time. Not “I’ll throw something together” time.

Document everything: Future you will not remember why you chose that specific chunking strategy at 2 AM on a Tuesday. This is a lesson I am learning incrementally.

## The moment of truth

The CLI (command-line interface) prototype validated something important: AI could actually help with PM work. Not by being magic, but by maybe by being a really bright intern who never forgot what was in the documentation.

But a command-line tool that only did one trick wasn’t going to shave much time off my day. Time to build something real.

## The bottom line

Building a working prototype taught me that AI development is 10% machine learning and 90% dealing with the same problems we’ve always had: data quality, system integration, and user experience.

The prototype wasn’t pretty. It wasn’t fast. It occasionally made no sense. But it worked just well enough to prove it was worth doing right.

Next up: How adding a web interface and GitHub integration turned my simple prototype into a complex disaster (and then into something actually useful).

---

_Next up in Building Piper Morgan: From primitive CLI to web app!_

_(Ever made a prototype that barely worked but still taught you exactly what needed to be fixed? Tell me about it, I’m all ears!)_
