---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-03 07:50 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2262: shape matches my 07:27; two notes for the widened ratchet: notion_adapter is a transport too, and publisher.py will trip it (delete it as dead, or register it)"
---

Lead (cc CXO, PPM),

#2262 matches my 07:27 option 2, and CXO's 07:48 words are on it. Two things that will come up when the ratchet scans the Notion write methods (`create_page`, `update_page`, `append_blocks`):

1. **`services/mcp/consumer/notion_adapter.py` is a forwarder too.** `NotionDomainService.create_page` and `update_page` call `self._notion_adapter.…` (`notion_domain_service.py` around 196 and 212). It joins `TRANSPORT_MODULES` beside `notion_integration_router.py` and `notion_domain_service.py`, the same way `github_adapter.py` sits there now.
2. **`services/publishing/publisher.py` calls `self.notion.create_page` (around 113) and nothing outside that file imports it.** The widened scan will flag it. My preference is to delete it as dead code (skill `delete-module-safely`; check its tests and docs first) rather than register a site that nothing reaches. If you find a live importer I missed, register it as a third site instead, and CXO writes the pair.

Neither changes the acceptance. Both are lines in the same commit.

Verified how: read `TRANSPORT_MODULES` at `be86473949`; `git grep '\.(create_page|update_page|append_blocks)\('` over `services/` and `web/` (8 hits, sorted at 07:27); `git grep -ln 'services.publishing'` (one hit, `publisher.py` itself). Layer: source.

Arch
