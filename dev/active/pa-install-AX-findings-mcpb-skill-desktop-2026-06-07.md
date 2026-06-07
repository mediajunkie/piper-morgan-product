# Install AX findings — comparable-tool walkthrough on Desktop/Chat (2026-06-07)

**Source**: PM walked a non-technical user through installing a comparable third-party tool (an MCPB+skill
privacy/anonymization tool for legal/medical work) into Claude Desktop. ~1 hour; required a technical
helper. Rich AX + competitive intel for how Piper BYOC should be installable and which packaging fits
which surface. (Personal details omitted by design.)

## Headline packaging learning: `.mcpb` + `.skill` self-install one-click on Desktop — and on the CHAT side that's currently *smoother than a plugin*
- **`.mcpb` bundle**: download → it opens Claude Desktop → click **Install** → lands under **Extensions**.
  One-click self-install.
- **`.skill` bundle**: Customize → Skills → create → **upload** (drag/drop) → added. One-click-ish.
- On Desktop **chat**, you install **both separately** (the MCPB *and* the skill) — "they haven't focused
  on this part yet." **Cowork/Code take ONE plugin blob** that bundles everything.
- Desktop-chat **plugin** support is **emerging-but-incomplete**: chat now *sees* plugins but says it
  "doesn't know how to use them" (consistent with #15178).

→ **Surface-dependent packaging.** The *plugin* is right for Cowork/Code (and the marketplace future), but
for **Desktop-chat today, `.mcpb` + `.skill` is the smoother one-click path** than our plugin (which also
hit the Desktop description-length validation cap). **Worth considering an `.mcpb`+`.skill` packaging of
Piper for the Desktop-chat audience**, not only the plugin zip. Track plugin-on-chat maturing (#15178).

## Friction catalog (for "how should Piper be installable / presentable")
Observed pain points for a non-technical user (all real, all ours to avoid):
- **Browser vs Desktop-app** confusion (tool needs the app; she was in a browser).
- **Chat / Cowork / Code tab** confusion (didn't know the three surfaces exist).
- "**Install from GitHub**" reads as geeky / intimidating.
- The MCPB install's **permission warning** ("grant extension everything on your computer") is scary.
- **Two-step install** (MCPB *then* skill) confusing — she thought she was done after the MCPB.
- A **separate File System extension** was a surprise third install nobody flagged.
- **Connected-folders is buried** — settings vs customize vs connectors vs extensions; even the *expert
  helper* struggled ("they need help with information architecture").
- A surprise **~634MB model download** mid-flow.
- "**Send any short message to continue**" / "tell me you're done" hand-holding prompts confused her.
- **Approve-every-action** permissions = tedious.
- **drag-attach bypasses the tool** (raw doc hits Claude before the shield) → must use a connected
  folder. A *security-critical* UX subtlety.
- **Terminal / full-path** steps crept in (make a marker file, give absolute paths) — too geeky.
- **PDF vs docx** handling gap (needed an extra piece for PDF).
- Net: **~1 hour + a technical helper**; she said she couldn't have done it alone.

## The encouraging part: Piper's hosted alpha *dodges the worst of it*
The hardest parts of that install are parts **Piper's hosted alpha doesn't have**:
- **No File System extension / connected folder** — ask/consult hit the hosted backend, not local files.
- **No multi-hundred-MB model download** — inference is hosted.
- **No folder-path / terminal** step.
- **One artifact** (our distribution bundle) + bundled uv + hosted endpoint → install-and-go.

→ **Piper-hosted is structurally simpler to install than this comparable local-MCP tool.** A real
advantage — lean into it. The friction that made their install an hour is friction we designed out by
hosting + bundling.

## Implications / actions
1. **Consider `.mcpb`+`.skill` packaging for Desktop-chat** (surface-dependent), alongside the plugin for
   Cowork/Code. The plugin is the long-game (marketplace); MCPB+skill is the smoother chat-today path.
2. **INSTRUCTIONS.html + COVER-NOTE matter** — install IA is confusing even for experts; be explicit on
   the exact click-path per surface.
3. **Near-zero-step is the bar.** A non-technical user can't self-install a tool like this alone today.
   Our hosting-simplicity gets us closer; keep minimizing steps (bundled-uv + the connect-step direction).
4. **drag-attach-bypasses-the-tool** is a security-UX lesson if Piper ever handles files directly.

## Refs
- #15178 (Desktop plugin skill-load); the BYOC distribution docs; INSTRUCTIONS.html / COVER-NOTE in the
  alpha distribution bundle.
