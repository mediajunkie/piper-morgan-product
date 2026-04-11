# The October Ghost

*Draft v1 - January 20, 2026*
*Work date: January 17, 2026*

---

**[HERO IMAGE: TBD - crisis/recovery themed]**

---

At 5:38 AM on a Friday, I woke up to an email from Google Cloud Platform.

"Your project has been suspended for hijacked resources."

My first thought: someone hacked us. My second thought: how bad is it? My third thought: coffee first, then crisis.

---

## The Alert

GCP's suspension notice was alarming but vague. "Hijacked resources" could mean anything from cryptocurrency mining to spam operations to something worse. The project was locked. Services were down. And I had no idea what had happened.

I spun up a Security Operations agent at 5:38 AM. First task: figure out what was affected.

The answer came back quickly: Gemini API. Google's AI service. We used it as a backup for certain operations—not our primary path, but integrated into the system. Someone had been using our API key.

---

## The Bleeding

By 5:48 AM, we'd confirmed the scope. The Gemini key was compromised. Usage was spiking in ways we hadn't caused. Someone else was running requests on our dime.

At 6:04 AM, we deleted the key via AI Studio. The bleeding stopped. Whatever they were doing, they couldn't do it anymore.

But that raised the harder question: how did they get the key in the first place?

---

## The Five Whys

**Why was the key compromised?**
→ Because it was exposed in a committed file.

**Why was it in a committed file?**
→ Because it appeared in `dev/server-startup.log`.

**Why was the key in a log file?**
→ Because httpx logs full URLs, and our Gemini calls included the key as a query parameter (`?key=...`).

**Why was that log file committed?**
→ Because `dev/` wasn't in our `.gitignore`.

**Why wasn't it caught before now?**
→ Because we had no automated secret scanning on the repository.

The root cause wasn't a hack. It wasn't sophisticated. It was a logging library doing exactly what logging libraries do—recording URLs—and us not realizing that URLs can contain secrets.

---

## The Timeline

We traced the leak to October 16, 2025. Three months of exposure.

Here's what likely happened: Someone—probably an automated scanner—found the key in our public repository. They started using it for their own Gemini API calls. Google detected the anomalous usage pattern and suspended the project.

In a way, Google's suspension was a favor. It forced us to discover a vulnerability we didn't know existed.

---

## The Fix (Five Layers)

One-layer fixes don't prevent recurrence. We implemented five:

**Layer 1: Immediate**
Added `dev/` to `.gitignore`. No more development logs in version control.

**Layer 2: Detection**
Deployed URL redaction filter to all HTTP loggers. Any URL containing sensitive patterns (`?key=`, `api_key=`, `token=`) gets redacted before logging.

**Layer 3: Scanning**
Ran `git secrets --scan-history` across the entire repository history. Found and flagged the October commit.

**Layer 4: Prevention**
Enabled GitHub's secret scanning on the repository. Future commits with exposed secrets will be blocked.

**Layer 5: Storage**
Migrated all API keys from Apple Notes (yes, really) to macOS Keychain with proper access controls.

Each layer addresses a different point of failure. Together, they make the same mistake much harder to repeat.

---

## The Lesson

The October Ghost wasn't a sophisticated attack. It was a combination of ordinary behaviors:
- A library logging URLs (normal)
- URLs containing API keys (unfortunately common)
- Development files getting committed (easy mistake)
- No scanning for secrets (oversight)
- Credentials stored in notes (convenient but insecure)

None of these individually is unusual. Together, they create a three-month window where anyone scanning public GitHub repositories could find and use your API key.

The fix wasn't heroic. It was systematic. Five layers, each addressing one link in the chain. Any one of them would have prevented or detected the leak.

---

## The Meta-Pattern

What struck me afterward was how the same methodology we use for debugging code worked for debugging security:

- **Five Whys** traced the root cause
- **Defense in depth** guided the multi-layer fix
- **Verification** (the git secrets scan) confirmed the scope
- **Documentation** (this post) captures the learning

Crisis response isn't different from regular development. It's just faster and higher stakes. The same systematic approaches apply.

---

## The Cost

We lost a few hours to the incident. The project suspension was lifted within a day after we appealed and showed our remediation steps. No user data was affected—Gemini doesn't handle our user data. The financial cost was some unauthorized API usage, probably minimal.

But we gained something: a security posture we should have had from day one. Five layers of protection that now exist because a ghost from October forced us to build them.

Sometimes the best improvements come from the worst surprises.

---

**[PM PLACEHOLDER: The 5:38 AM moment - what was the actual emotional experience of seeing that email?]**

**[PM PLACEHOLDER: Any detail on the appeal process or GCP's response?]**

**[PM PLACEHOLDER: Should we name the specific httpx behavior, or keep it general ("logging library")?]**

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development—including the parts where things go wrong.*

---

*Draft word count: ~900 words*
*Target: ~1,500-2,000 words*
*Status: First draft - needs PM review*
