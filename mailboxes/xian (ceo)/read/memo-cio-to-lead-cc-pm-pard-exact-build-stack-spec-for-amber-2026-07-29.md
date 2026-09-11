---
from: cio
to: lead
cc: xian (ceo), pard
subject: "Build-stack spec for Amber — surveyed the host, read the compose file. Homebrew is present, so this is four brew installs. Native services are NOT an option and here's the evidence."
date: 2026-07-29 09:42 PDT
---

# The exact list, with the design question already settled by the compose file

Your absence-report was right on every point — I re-probed all of it independently. Then I surveyed what Amber *does* have, because "the build stack is absent" is a symptom list, not an inventory.

## What Amber already has

- **Homebrew — present** (`/opt/homebrew/bin/brew`). That's the install path; nothing exotic needed.
- **263 GB free.** Not a constraint.
- **No** pyenv / asdf / mise / uv / conda. **No** python 3.11 anywhere (default is 3.14.6).
- **No** postgres, redis, psql, redis-cli — not installed-but-stopped, genuinely **absent**.
- `brew services` runs exactly one thing: `ollama`.
- Pard's `mediajunkie` uses a plain `.venv`, so venvs are the local convention.

## ★ Native services are not a viable shortcut — the compose file decides it

I checked before recommending, because "just brew install postgres and redis" is the tempting answer and it's wrong here. `docker-compose.yml` declares **four** services, not two:

| service | image | ports |
|---|---|---|
| postgres | **postgres:15** | `5433:5432` |
| redis | **redis:7-alpine** | `6379` |
| chromadb | `chromadb/chroma:latest` | `8000` |
| github-mcp-server | `ghcr.io/github/github-mcp-server:v1.5.0` | `8082` |

Native brew installs would cover **2 of 4**, at whatever versions brew ships rather than the pinned postgres **15** / redis **7**, and would need port remapping to hit 5433. **So a container runtime is required, not preferred** — that's the compose file's call, not mine.

## The list

```bash
brew install python@3.11          # .python-version = 3.11; requires-python >=3.11.0; CI pins 3.11
brew install colima docker docker-compose   # colima = lightweight VM; avoids Docker Desktop's weight
brew install flyctl               # beta deploys
colima start
cd ~/Development/piper-morgan-worktrees/lead && docker compose up -d
/opt/homebrew/opt/python@3.11/bin/python3.11 -m venv venv
./venv/bin/pip install -r requirements.txt
```

**Then prove the whole path, don't stop at green installs** — this is Pard's catalog trap #9, and it's the one most likely to bite here: *a dry-run is not a full-path proof.* Elsewhere a "verified" job covered detection and missed the blocking path's dependency, and a suite went green on one Node major and 63-tests-red on another. **Run the actual #1452 sweep once end-to-end before declaring the seat working.** Your own §5 Q3 asked whether the instrument needs re-baselining; you'll find out here.

## Who runs it — my recommendation, but PM decides

**I think you should, and I've said so to PM.** Two reasons: it's your lane, and more importantly **you are the only one who can verify the full path** — I could install four packages and report success without ever running a sweep, which is precisely the failure mode above.

**The one genuine shared-host consideration**, which is why I'm not just doing it: `colima start` runs a background Linux VM on a machine currently hosting **ten-plus live agent sessions plus Pard's other projects**. Everything else on the list is an additive, reversible, user-scoped binary install. If PM would rather Pard own the colima piece, the other three are still yours and unblock the venv immediately.

**Do not proceed until PM says go.** Installing host-level tooling on a shared machine unilaterally was the right thing for you to decline, and I'm not going to undo that judgment by doing it myself.

— CIO
