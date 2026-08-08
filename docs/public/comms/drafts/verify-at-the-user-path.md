---
image: ''
alt: ''
caption: ''
---

# Verify at the User Path, Not the Data Layer

*May 29–30, 2026*

There's a particular kind of green checkmark that lies to you. What it checked may be correct — the data is in the database, the server is up, the test passed — but the check is sitting in the wrong place. It's measuring something true that happens not to be the thing you actually care about: whether a person can use the feature. The data being correct and the person being able to reach it are two different claims, and the gap between them is where this whole lesson lives.

A while back I had my team build a feature called an Insight Journal, a page where you could browse the patterns the system had surfaced — and I was told it was complete and verified. The verification was real. The server was up, the health check was green, sample insights (for testing) were seeded in the database and you could see the rows. Then I actually tried to open the page, the way a user would, and it didn't exit. The command palette didn't recognize the menu command I was told to try. The direct URL returned an error. The checklist said the page existed but the person it was for could not load it.

# "It works" is a claim about a specific path

"It works" is never a standalone statement. It's always a claim about a *path* — a particular route from a person's intention to a result. And there are many paths through any system. The data layer is one path. The API is another. The rendered page a human loads in a browser is another. These paths share a lot of plumbing, but they are not the same path, and a check on one of them is not a check on the others.

When my agents verified the Insight Journal, they verified the data path. *Is the data there? Yes. Is the server responding? Yes.* Both true. But the user doesn't take the data path. The user types something into a command palette (the keyboard-driven menu for jumping around the app), or pastes a URL, and waits for a page to render. That path — the user's actual path — had a break in it that none of the data-layer checks could see, because none of them traveled down it.

This is the trap. The data-layer checks are *easy to write and satisfying to pass.* You can assert that a database row exists. You can assert that a server returns a 200 (the HTTP code for "OK"). These assertions are fast, they're stable, they go green reliably. The user-path check is harder — you have to actually render the page, simulate the click, look at what comes out the far end. So there's a natural gravity that pulls verification toward the easy checks and away from the path that matters. The most convincing green checks are often the ones furthest from the user.

# A 200 response is not the same as a rendered page

A `curl` (a command-line tool that fetches a URL) returning 200 tells you the server accepted the request and sent back *something*. It does not tell you that the something is the page the user needs. The server can return 200 with an error page. It can return 200 with a redirect to a login. It can return 200 with a template that failed to render and fell back to a stub. The 200 is a claim about the transport, not about the content.

And a clean database row tells you the data exists. It tells you nothing about whether the code that's supposed to fetch that row, hand it to a template, and render it into HTML actually does so without falling over. In our case the falling-over was almost comically specific — the page template had a self-reference that sent it into a loop, and separately the template engine was choking on tag syntax it found *inside an HTML comment*, which a human reading the file would skip right over. None of that is visible from the data layer. None of it is visible from a 200. It's only visible when you render the actual page and look at the actual output.

We fixed the bugs. That took care of  this page, this template, this loop. The more important lesson was about the *discipline*: before you say a user-facing surface works, render the real surface and assert on what the user would actually see. Not the row. Not the status code. The rendered thing, with realistic data in it, checked the way the user would experience it.

# Tests pass, users succeed — and those aren't the same claim

We now have a saying on this project: *tests passing is not the same as users succeeding.* A test suite is a set of paths through the system that someone decided to check. If those paths don't include the user's actual path, then a fully-green suite is fully compatible with a completely broken feature. The suite isn't lying. It's answering the question it was asked. The question just wasn't the right one.

What makes this insidious is that the green suite *feels* like evidence of user success. It's so easy to slide from "all the checks pass" to "the thing works" without noticing that you've changed the subject. The checks pass. Whether the thing works is a separate question, and the only way to answer it is to go stand where the user stands and look at what the user sees.

# How to tell which check you're actually running

When you're about to declare something works, ask: *which path did I verify, and is it the path the user takes?* If you verified that the data is present, you've verified the data path. Good — necessary, not sufficient. If you verified the server responds, you've verified the transport. Also good, also not sufficient. The user-path check is the one where you reproduce, as faithfully as you can, the sequence the human will actually perform — load the page, click the thing, read the result — and you assert on the result the human would read.

The tell is distance. The further your check sits from the user's hands, the more skeptical you should be of its green, *especially when the green is reassuring.* A reassuring check far from the user's path is exactly the configuration that lets a broken feature ship with confidence. The reassurance is the problem. It's doing the job of evidence without being evidence.

And this generalizes well past pages and templates. Any time you're verifying anything — a report a person will read, a workflow someone will run, an answer a user will receive — the same question applies. Did I check the thing the human actually touches, or did I check the thing that was easy to assert? Those drift apart constantly, and they drift apart in the direction of comfort, because the easy assertion is the one that's always available. The work is to resist the gravity and go all the way out to the edge — to the path where the person actually stands — and check the thing *there*, where it's harder and where it counts.

The page renders now. It passes, if barely. But the thing I'm keeping from the whole episode isn't the working page. It's the reminder that the most trustworthy-looking checkmark and the user's actual experience can sit a surprising distance apart, and that closing that distance is not optional polish. It's the verification.

---

*Next on Building Piper Morgan: "Over-Checking Has Dividends" — the corner you don't cut is the bug that never ships, and that dividend is invisible precisely because nothing went wrong.*

*Where in your own work does "it works" really mean "the data is there" — and when did you last actually stand where the user stands and load the thing yourself?*
