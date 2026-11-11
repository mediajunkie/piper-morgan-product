---
image: 'never-green-in-a-thousand-runs-proud-spare-two-flat-tires.jpg'
alt: 'A cheerful AI mechanic proudly presents a fully inflated spare tire while a puzzled woman gestures toward the car beside them, its tires visibly flat.'
caption: '"This one passes every time!"'
---

# Never Green in a Thousand Runs

*September 9–11, 2026*

In early September I felt nervous about our progress toward the MVP milestone. It felt like we were taking one step forward, two steps back. Meanwhile, we were relying on a report of "green tests" that only covered four of our seven test workflows, and excluded one that had never yet been green once in a thousand runs.

# The pile that wouldn't shrink

I carved out time on September 9 for some live testing, something I cannot delegate, and after a series of verification passes we closed six issues by midday, while the backlog still grew. My tests were finding new issues and fixes were discovering new issues or deeper patterns.

My chief of staff agent (Exec) summarized it in the "attention rollup" artifact they maintain for me, noting that the sprint backlog went from 28 to 34, as it "grew by six while PM closed six" (they often refer to me as simply PM, the human product manager they all work for).

# The work that didn't start

Exec also noted some "never started" work that was still being postponed. This got me wondering. What is blocking that work? Why has it not yet started? How can I be blocking it yet if it hasn't yet even started? How can you have any pudding if you don't eat your meat? Well, not that.

My lead developer agent peeked at the issue and took the blame, saying they had been blocking it themselves, not I. A faulty duty-cycle mechanism tied the backlog-intake to an idle state that never came.

Exec and I also discussed how to escalate items to me if they sit unaddressed for too long and Exec spread the work among the agent team.

In discussing how I didn't feel I had a good grip on where we stood and whether we were really making progress or just slipping sideways, I said something about how I needed to understand "the state of the forest and not just the most recently noticed trees."

This led to a productive conversation that improved how we track and measure throughput.

# Evergreen vs. never green

Several times in this period Lead shared reports about how the CI (continuous integration) test belt was "fully green" but when Lead took a closer look, they realized that their reports had been partial at best and misleading at worst.

It turns out two workflows were red on every visible run but were not being included in the summary. For at least one of these (a set of end-to-end or "E2E" tests) the two provider test keys (for Anthropic and OpenAI) that I had set up were both dead.

One was out of credit and the other was invalid (probably expired), but nobody had told me. I'm the only person on the project, so it's up to me to mint new credentials like API keys.

One thing that had masked the key problem was that local test runs had been able to fall back to a key in the keychain of my Mac Studio, even though that was not the intent.

By that evening six of seven workflows were now green, with the seventh still blocked by the need for me to "rotate a secret" (update a credential).

# It's not you, it's me

My agent team is getting a lot better at doing work thoroughly and reporting on it accurately, but the mechanisms that drive them still have gaps that can lead to completely ignoring relevant information and sometimes missing the forest for the trees.

Along the way, at every stage of improvement, there are times when it comes down to me asking a question, noticing a problem, or wondering why something doesn't smell right.

It doesn't really let me off the hook when an agent calls themselves out for overlooking something or making an incomplete claim, since I realize that in the end ultimately it all comes down to how good a job I am doing of establishing instructions and the rules.

---

*Next on Building Piper Morgan: "The Server Has No Key," in which I have to lay down the law to prevent my personal key being made available as a fallback for testers.*

*When your reports say everything is green, are you confident that everyone agrees on what "everything" means?*
