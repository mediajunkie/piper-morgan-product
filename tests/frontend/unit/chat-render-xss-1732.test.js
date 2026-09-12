/**
 * #1732 [SECURITY] — chat reply render boundary: attempted-exploit pins.
 *
 * Bot replies render via marked.parse(message) → element.innerHTML. Before
 * #1732 there was NO sanitizer on that path, while user-controlled text
 * (todo/reminder text, todo_handlers.py:_reminder_saved_message) is
 * interpolated into those messages server-side. The fix is a sanitizer at the
 * render chokepoint (renderBotMessage) using vendored, version-pinned
 * DOMPurify, failing CLOSED (entity-escape) when DOMPurify is absent.
 *
 * LAYER (named honestly): RUNTIME DOM via jsdom, through the REAL vendored
 * marked (15.0.12) + the REAL vendored DOMPurify (3.2.7) + the REAL renderer
 * source (web/assets/bot-message-renderer.js — the served copy; the divergent
 * CommonJS twin at web/ root that this suite used to also pin was deleted by
 * #1740, and its absence is pinned in
 * tests/unit/web/test_renderer_twin_absent_1740.py). Hostile output is
 * innerHTML'd into a real jsdom container. What it is NOT: a browser E2E
 * through the live server — Web's browser lane is the natural live verifier
 * (per the filing).
 */

const fs = require('fs');
const path = require('path');

const VENDOR = path.join(__dirname, '../../../web/static/vendor');
const MARKED = path.join(VENDOR, 'marked-15.0.12.min.js');
const PURIFY = path.join(VENDOR, 'purify-3.2.7.min.js');
const ASSETS_RENDERER = path.join(__dirname, '../../../web/assets/bot-message-renderer.js');

function realMarked() {
  // marked's UMD exports the same object the browser global gets ({parse, use, ...}).
  // Fresh copy per suite run isn't needed — the link renderer config is idempotent.
  const mod = require(MARKED);
  return mod.marked && mod.marked.parse ? mod.marked : mod;
}

function realDOMPurify() {
  // dompurify's UMD self-binds to the jsdom window present in this environment.
  let p = require(PURIFY);
  if (!p.sanitize && typeof p === 'function') p = p(window);
  expect(p.isSupported).toBe(true); // guard: an unsupported DOMPurify proves nothing (m-44)
  return p;
}

/** Load a renderer source with explicit marked/DOMPurify bindings. */
function loadRenderer(file, { purify } = {}) {
  const code = fs.readFileSync(file, 'utf8');
  // eslint-disable-next-line no-new-func
  const wrapped = new Function(
    'marked',
    'DOMPurify',
    'module',
    'window',
    `${code}\nreturn { renderBotMessage };`
  );
  return wrapped(realMarked(), purify, undefined, window).renderBotMessage;
}

/** Render a message through the renderer and mount it exactly as the app does. */
function mount(renderBotMessage, message, type = 'success') {
  const el = document.createElement('div');
  el.innerHTML = renderBotMessage(message, type, false); // the real sink shape
  document.body.appendChild(el);
  return el;
}

const PAYLOAD_SCRIPT = '<script>window.__pwned = true;</script>';
const PAYLOAD_ONERROR = '<img src=x onerror="window.__pwned = true">';
const PAYLOAD_JSHREF = '[click me](javascript:window.__pwned = true)';
// The markdown-restyle shape: raw hostile HTML riding INSIDE otherwise-normal
// markdown, so it survives parsing embedded in legit formatting.
const PAYLOAD_RESTYLE =
  '**Todo saved:** <iframe src="javascript:window.__pwned=true"></iframe> _done_';

describe('#1732 render boundary — served copy (web/assets) — with REAL marked + REAL DOMPurify', () => {
  let render;

  beforeEach(() => {
    delete window.__pwned;
    render = loadRenderer(ASSETS_RENDERER, { purify: realDOMPurify() });
  });

  test('script-tag payload emerges inert (no element, no execution)', () => {
    const el = mount(render, `Reminder saved: **${PAYLOAD_SCRIPT}**`);
    expect(el.querySelector('script')).toBeNull();
    expect(el.innerHTML).not.toMatch(/<script/i);
    expect(window.__pwned).toBeUndefined();
  });

  test('img-onerror payload loses its handler', () => {
    const el = mount(render, `Reminder saved: **${PAYLOAD_ONERROR}**`);
    expect(el.querySelector('[onerror]')).toBeNull();
    expect(el.innerHTML).not.toMatch(/onerror/i);
    expect(window.__pwned).toBeUndefined();
  });

  test('javascript: markdown link is neutralized', () => {
    const el = mount(render, PAYLOAD_JSHREF);
    for (const a of el.querySelectorAll('a')) {
      expect(a.getAttribute('href') || '').not.toMatch(/^\s*javascript:/i);
    }
    expect(window.__pwned).toBeUndefined();
  });

  test('markdown-restyle payload: hostile HTML inside legit markdown is stripped, formatting survives', () => {
    const el = mount(render, PAYLOAD_RESTYLE);
    expect(el.querySelector('iframe')).toBeNull();
    expect(el.querySelector('strong')).not.toBeNull(); // the legit markdown still renders
    expect(el.querySelector('em')).not.toBeNull();
    expect(window.__pwned).toBeUndefined();
  });

  test('error-type messages (raw, unparsed path) are sanitized too', () => {
    const el = mount(render, PAYLOAD_ONERROR, 'error');
    expect(el.querySelector('[onerror]')).toBeNull();
    expect(window.__pwned).toBeUndefined();
  });

  test('#1123 regression guard: external links KEEP target="_blank" + rel through the sanitizer', () => {
    const el = mount(render, 'Check [Notion](https://notion.so/abc) for more.');
    const a = el.querySelector('a[href="https://notion.so/abc"]');
    expect(a).not.toBeNull();
    expect(a.getAttribute('target')).toBe('_blank');
    expect(a.getAttribute('rel')).toBe('noopener noreferrer');
  });

  test('#1730 no-double-escape: copy-layer entity escaping renders ONCE, visibly correct', () => {
    // The 1730 decline-echo escapes at the copy layer server-side: the message
    // string already carries &lt;braindump&gt;. Through marked + DOMPurify it
    // must display as literal <braindump> — not &lt;braindump&gt; (double-escape)
    // and not an executed/stripped element.
    const el = mount(render, 'I did not run &lt;braindump&gt; just now.');
    expect(el.textContent).toContain('<braindump>');
    expect(el.textContent).not.toContain('&lt;');
    expect(el.querySelector('braindump')).toBeNull();
  });
});

describe('#1732 fail-closed: DOMPurify missing (never raw HTML through)', () => {
  test('served copy escapes to inert text without DOMPurify', () => {
    delete window.__pwned;
    const render = loadRenderer(ASSETS_RENDERER, { purify: undefined });
    const el = mount(render, `hi ${PAYLOAD_SCRIPT}`);
    expect(el.querySelector('script')).toBeNull();
    expect(window.__pwned).toBeUndefined();
    // Fail-closed means degraded-but-visible text, not silent raw HTML.
    expect(el.textContent).toContain('script');
  });
});
