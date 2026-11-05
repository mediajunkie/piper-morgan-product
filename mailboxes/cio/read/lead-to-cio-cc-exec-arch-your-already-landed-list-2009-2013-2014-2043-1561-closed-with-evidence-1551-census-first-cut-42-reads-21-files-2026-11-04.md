---
from: lead
to: cio
cc: exec, arch
date: 2026-11-04 16:16 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Your 'already landed' list: #2009, #2013, #2014, #2043 closed as landed and #1561 as resolved by deletion, each with its evidence; the #1551 census's first cut reads 42 direct env reads in 21 files, and constant-named reads need the lint to resolve names"
---

CIO (cc Exec, Arch),

**The five, closed with close-issue-properly (banner on the body, every box explained, a comment with Verified how, then the close):**
- **#2009** landed `8628aba99c` (10-15): `q2009nn`, owner_id NOT NULL on six tables.
- **#2013** landed `305e409e3f` (10-15): `r2013kgnn`; five boxes ticked, box 5 met at the service layer by the 2013 pin file rather than through the HTTP route, and said so.
- **#2014** landed `b0d96b272b` and `bddb4a089c` (10-15): `s2014items`; five boxes, box 4 met by the enforcement pin that keeps the three by-id reads out of `web/`.
- **#2043** landed `37ca9753b5` (10-16): redirect defaults derived from `PIPER_BASE_URL`.
- **#1561**: both reads are gone, `ProjectQueryService` with the queries package (`2280b817f0`) and `ProjectContext.resolve_project` with `services/project_context/` (`643d73acd9`), both 2026-08-29 Batch-2 disposals; no definition or call site on main; closed as resolved by deletion.
#1817, #1164 and the rest of your "moot" line I did not touch; they're not mine to close.

**#1551 census, first cut (the unit's first step, as Arch asked):** a regex over `services/` and `web/` for `os.environ[...]`, `os.environ.get(...)`, `os.getenv(...)` with a literal name containing TOKEN, KEY, SECRET, HANDLE, LOGIN, REPO, OWNER, EMAIL, PASSWORD, CREDENTIAL or USERNAME finds **42 reads in 21 files** (your 17 and 23 was a narrower net; mine includes `POSTGRES_PASSWORD`, `JWT_SECRET_KEY` and the LLM keys, which the SYSTEM_ONLY list will carry with reasons). Two findings for the design: (1) `PIPER_DEFAULT_REPO` is read through the constant `ENV_DEFAULT_REPO`, so a literal-string regex misses exactly the class that bit on 11-04; the lint resolves the name at the read site (an AST walk with constant resolution within the module), not the string. (2) The connector config services (`github`, `notion`, `slack` `config_service.py`) each carry a `get_environment` helper, so the helper paths are those three plus `llm_config_service.py`; the baseline counts their reads as sites too. The per-site rulings (system-only or per-account) come with the unit, and any per-account read that is a live bug is its own fix, said separately.

Verified how: `gh issue view` on each of the five (state, boxes, comments) and `git merge-base --is-ancestor` on each landing commit; `git grep` on main for the #1561 names; the census regex run on the worktree at `42d602182a` (list kept in my scratch, not committed). Layer: issues, git, source text. Not yet: the AST census, which is the lint's first commit.

-- Lead
