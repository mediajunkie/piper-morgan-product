/**
 * Shared HTML/attribute escaping helpers (#1582).
 *
 * Single source of truth for every template that interpolates dynamic
 * (user- or third-party-supplied) values into innerHTML. Previously this
 * pair was duplicated inline per-template (#1578 todos.html, #1581
 * files.html) — worse, several OTHER templates shipped a DOM-based variant
 * (`div.textContent -> div.innerHTML`) that does NOT escape quotes, so any
 * `value="..."`/`aria-label="..."` site it "protected" was still
 * attribute-injection-breakable (#1581's finding, generalized by #1582's
 * census: greeting_context.html, project_config_panel.html, lists.html,
 * project_detail.html, settings_calendar.html, settings_github.html,
 * settings_notion.html, settings_projects.html all carried that quote-
 * incomplete copy before this consolidation).
 *
 * escapeHtml() covers ALL FIVE metacharacters (& < > " ') so a single call
 * is safe in both HTML-text and HTML-attribute contexts. escapeAttr() is
 * the same function under a name that documents the call-site context (a
 * value="" / aria-label="" attribute) — kept as a distinct name rather than
 * an alias-only export so existing call sites read correctly either way.
 *
 * NOTE (carried from #1578/#1581): HTML-escaping CANNOT protect a JS string
 * inside an inline onclick="..." handler — the HTML parser decodes entities
 * before the JS engine parses the handler, so a quote re-materializes and
 * breaks out. User-authored text must never cross that boundary; only
 * server-generated ids/types belong in onclick (still escapeAttr'd for the
 * HTML-attribute layer they also sit in).
 *
 * Loaded shell-wide by templates/layouts/app_shell.html (before
 * {% block scripts %}, so every page extending the shell has escapeHtml/
 * escapeAttr defined before its own inline script's event handlers run —
 * DOMContentLoaded/fetch-callback/onclick call sites all fire after full
 * synchronous script parse, so load-order relative to those handlers'
 * *definitions* doesn't matter, only that this file has executed before
 * any handler actually *invokes* escapeHtml/escapeAttr).
 *
 * Exposed both as window.PiperEscape.{escapeHtml,escapeAttr} and as plain
 * globals (window.escapeHtml / window.escapeAttr) so existing per-template
 * call sites — written against the old local `function escapeHtml(...)`
 * convention — keep working unchanged.
 */
function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function escapeAttr(value) {
  return escapeHtml(value);
}

if (typeof window !== 'undefined') {
  window.escapeHtml = escapeHtml;
  window.escapeAttr = escapeAttr;
  window.PiperEscape = { escapeHtml: escapeHtml, escapeAttr: escapeAttr };
}
