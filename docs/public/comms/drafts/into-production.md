---
image: ''
alt: 'An explorer kneels just beyond the doorway of a tidy workshop, calmly gathering small hardware pieces shaken loose by the uneven ground, illustrating how a new environment reveals hidden assumptions.'
caption: ''
---

# Into Production

*June 6–7, 2026*

The production branch had been last updated on March 4. The main branch, where I push all the newest code, had moved 4,139 commits ahead of it in the time since. This included the M1 and M2 Minimum Valuable Product (MVP) sprints, most of M3, the migration wave and the duty-cycle launch. Everything that had happened in the previous three months was running in development and staging and shared test environments. Nothing had been cut for production since March.

On Saturday morning, my product assistant agent (Piper Alpha, or PA) ran the production release. The new tag went onto the June 3 commit — the last verified release checkpoint, where the retest of the "canonical queries" test suite had come back green and the M2 close had been confirmed. Production fast-forwarded from March 4 all the way to v0.8.7. The gap between "running in development" and "running in production" was now zero.

Except it wasn't, because my plan was to provide a hosted version of Piper Morgan for my alpha testers. This was always in the cards, but up to now testing Piper meant cloning my repo and running the code locally. Not for the faint of heart! The plan for hosting the alpha involved setting up a DigitalOcean "droplet," and the droplet required Linux, and, well... Piper had never up to now had to run on Linux.

# Seven problems nobody knew about

The backend had been developed and tested on my Mac. Linux runs differently in specific, predictable ways — but you don't know which specific ways until you try. PA provisioned the droplet and started working through the deploy.

Seven portability issues surfaced, one at a time. An orchestration container trying to copy in a script that had never actually been tracked in the repository. A Mac-specific package that didn't exist on Ubuntu. An `.env` file with permissions that Linux refused to read. A SQLite version too old for what the database layer needed. A container that couldn't write to its own data directory because of a permissions mismatch. A server binding to 127.0.0.1 that would never accept external connections on a droplet. A database migration tool pointing at entirely the wrong host.

Each one was small. Each one was invisible until the moment Linux ran into it and stopped. The code had been carrying assumptions about its environment — assumptions that were accurate, in the environment where the code was written. The assumptions just weren't written down anywhere. The move to the new environment made them visible, one by one, because they stopped being true.

By late Saturday evening, all seven were fixed. The /health endpoint returned 200. The /intent endpoint returned 200. Thirty-six database tables were migrated. The backend was running.

# The next morning

At 7:13 UTC on Sunday, I dropped the Anthropic API key into the server configuration. The hosted backend went live — a real language model answering real questions at an external IP.

At 7:48 UTC, alpha.pipermorgan.ai went up. Caddy as the edge proxy. Let's Encrypt for the TLS certificate. Basic authentication as a gate. The system was now reachable from the open internet.

I ran the full install on my own machine. The Claude Desktop plugin (a skunkworks project PA has been running for me) connected. The bundled runtime installed. The gated endpoint responded. A question got a real answer. The test passed.

# The first external tester

Later that Sunday, the alpha plugin distribution package went out to an tester.

She wasn't in the room when the system was built. She hadn't watched the audits run or the bugs get fixed or the seven Linux problems get diagnosed and cleared. She just received a package, installed it, and tried it out.

The thing I've been building was now running on hardware I didn't own, responding to requests over the open internet, being used by someone who didn't build it. The last three months of development work had finally crossed into production.

The distance from "working" to "deployed" is seven problems you didn't know you had until you tried. The distance from "deployed" to "live" is a TLS certificate and a test. The distance from "live" to "being used" is one person who opens the thing and runs it without you in the room.

---

*Next on Building Piper Morgan: "Mechanical First, Then Read" — why the mechanical checks come before reading for meaning, and what that order quietly saves.*

*What's the most revealing thing you've learned from running a system in production vs. in development? What had you been carrying that the environment hadn't told you yet?*
