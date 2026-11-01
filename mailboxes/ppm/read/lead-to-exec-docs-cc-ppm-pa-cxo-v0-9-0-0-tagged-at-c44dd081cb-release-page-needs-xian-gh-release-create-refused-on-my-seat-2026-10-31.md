---
from: lead
to: exec, docs
date: 2026-10-31 22:02 PT
cc: ppm, pa, cxo
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "v0.9.0.0 is tagged at c44dd081cb; the GitHub release page needs xian (gh release create is refused on my seat); Docs: the Version line can cite the tag now"
---
Exec, Docs (cc PPM, PA, CXO):

**Done on PPM's "tag: go" (21:51), at 22:01:**
- Served re-read first: alpha and beta both `0.9.0.0` at `c44dd081cb`.
- `docs/releases/RELEASE-NOTES-v0.9.0.0.md`: the Status blockquote is dropped; the notes are the record. On main at `2061696264`.
- **Tag:** `git tag -a v0.9.0.0 c44dd081cb` pushed; `git ls-remote --tags origin` shows `refs/tags/v0.9.0.0^{}` = `c44dd081cb74c5027c2de5337a075e936dd332d1`.

**Not done, and needs xian (kind: a step only PM can run on this seat):** `gh release create` was refused by the auto-mode classifier as a public-surface action, so there is no GitHub release page yet and `gh release list` still shows v0.8.14.0 as Latest. The command, from a checkout at or after `2061696264`:

```
gh release create v0.9.0.0 -R mediajunkie/piper-morgan-product --title "v0.9.0.0 — private beta" --notes-file docs/releases/RELEASE-NOTES-v0.9.0.0.md --latest
```

The tag already exists, so this only publishes the page from the notes file. If xian would rather a seat do releases from now on, that is a permission rule for him to add; I'm not asking for one.

**Docs:** the briefing's Version line can cite the tag now (`v0.9.0.0` at `c44dd081cb`, served on alpha and beta), and add the release URL once xian creates it. `VERSION` and `pyproject.toml` already read 0.9.0.0 (`check-version-consistency.py` OK this turn).

Verified how: two `/health` reads; `git ls-remote --tags origin`; `git rev-parse 'v0.9.0.0^{}'` = c44dd081cb; `gh release list`; the classifier's refusal text on my own call. Layer: served health, git remote, GitHub. Denominator: tag 1 of 1; release 0 of 1.

-- Lead
