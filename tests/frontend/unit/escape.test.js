/**
 * #1582 — web/static/js/escape.js: the shared escapeHtml/escapeAttr source
 * of truth consolidated out of 11 templates (2 already had this exact
 * quote-complete string-based implementation — todos.html/#1578,
 * files.html/#1581; 8 others carried a DOM-based `div.textContent ->
 * innerHTML` copy that did NOT escape quotes, an attribute-injection hole;
 * 1 had its own quote-complete regex-based copy).
 *
 * LAYER (m-43, named honestly): this suite `eval`s the REAL escape.js
 * source (not a reimplementation) in a jsdom global and exercises the
 * functions directly, plus proves the browser-facing surface
 * (window.PiperEscape + plain window.escapeHtml/escapeAttr globals) is
 * actually populated the way a `<script src="/static/js/escape.js">` tag
 * would populate it. It does not re-prove that any given template loads
 * this asset before calling it — that is the render-time assertion in
 * tests/unit/templates/test_todos_xss_escaping_1578.py and
 * test_files_xss_escaping_1581.py (source-text pin) and the runtime-DOM
 * suites (files-page-xss.test.js, todos-page-xss.test.js) that prepend this
 * same source into their evaluated wrapper.
 */

const fs = require('fs');
const path = require('path');

const SOURCE_PATH = path.join(__dirname, '../../../web/static/js/escape.js');
const SOURCE = fs.readFileSync(SOURCE_PATH, 'utf8');

// Attribute-injection payload from the #1581 finding: a quote-incomplete
// DOM-based escapeHtml (div.textContent -> innerHTML) left this able to
// close an attribute and plant a real onerror= handler.
const HOSTILE_ATTR = '" onerror="window.__pwned = true" data-x="';

describe('escape.js (#1582 shared asset)', () => {
  let helpers;

  beforeEach(() => {
    // Evaluate the REAL file, not a stub. `new Function` gives the source a
    // fresh top-level scope per test (matching how a <script src> tag
    // defines fresh top-level function declarations), and we return the
    // functions it declares — the same technique the page-render jsdom
    // suites use to extract inline <script> content.
    // eslint-disable-next-line no-new-func
    helpers = new Function(`
      ${SOURCE}
      return { escapeHtml, escapeAttr };
    `)();
  });

  test('escapeHtml escapes all five metacharacters (& < > " \')', () => {
    expect(helpers.escapeHtml('&')).toBe('&amp;');
    expect(helpers.escapeHtml('<')).toBe('&lt;');
    expect(helpers.escapeHtml('>')).toBe('&gt;');
    expect(helpers.escapeHtml('"')).toBe('&quot;');
    expect(helpers.escapeHtml("'")).toBe('&#39;');
    expect(helpers.escapeHtml(`a"b'c<d>e&f`)).toBe(
      'a&quot;b&#39;c&lt;d&gt;e&amp;f'
    );
  });

  test('escapeHtml handles null/undefined as empty string, not "null"/"undefined"', () => {
    expect(helpers.escapeHtml(null)).toBe('');
    expect(helpers.escapeHtml(undefined)).toBe('');
  });

  test('escapeHtml coerces non-string values (e.g. numbers) rather than dropping them', () => {
    expect(helpers.escapeHtml(0)).toBe('0');
    expect(helpers.escapeHtml(42)).toBe('42');
  });

  test('escapeAttr delegates to escapeHtml (same quote-complete coverage) — the #1581 fix', () => {
    expect(helpers.escapeAttr).toBeDefined();
    expect(helpers.escapeAttr('a"b\'c')).toBe(helpers.escapeHtml('a"b\'c'));
    expect(helpers.escapeAttr('a"b\'c')).toBe('a&quot;b&#39;c');
  });

  test('an attribute-injection payload is fully neutered (quotes included) — the #1581 regression class', () => {
    const escaped = helpers.escapeAttr(HOSTILE_ATTR);
    // round-trip through a real attribute to prove it, not just string-match
    const div = document.createElement('div');
    div.innerHTML = `<input aria-label="Select ${escaped} for bulk download">`;
    const input = div.querySelector('input');
    expect(input).toBeTruthy();
    expect(input.getAttribute('onerror')).toBeNull();
    expect(input.getAttribute('aria-label')).toBe(
      `Select ${HOSTILE_ATTR} for bulk download`
    );
  });

  test('escapeHtml output creates no elements when set via innerHTML (text-context safety)', () => {
    const hostile = '<img src=x onerror="window.__pwned = true">';
    const div = document.createElement('div');
    div.innerHTML = helpers.escapeHtml(hostile);
    expect(div.children).toHaveLength(0);
    expect(div.textContent).toBe(hostile);
  });

  describe('browser-facing globals (as a real <script src> tag would populate them)', () => {
    afterEach(() => {
      delete window.escapeHtml;
      delete window.escapeAttr;
      delete window.PiperEscape;
    });

    test('window.escapeHtml / window.escapeAttr are plain globals for existing per-template call sites', () => {
      // Indirect eval executes against the REALM'S global object (window in
      // jsdom) — the same effect a classic (non-module) <script src> tag has:
      // top-level function declarations become window properties.
      // eslint-disable-next-line no-eval
      (0, eval)(SOURCE);
      expect(typeof window.escapeHtml).toBe('function');
      expect(typeof window.escapeAttr).toBe('function');
      expect(window.escapeHtml('<')).toBe('&lt;');
      expect(window.escapeAttr('"')).toBe('&quot;');
    });

    test('window.PiperEscape exposes the same two functions namespaced', () => {
      // eslint-disable-next-line no-eval
      (0, eval)(SOURCE);
      expect(window.PiperEscape).toBeDefined();
      expect(window.PiperEscape.escapeHtml).toBe(window.escapeHtml);
      expect(window.PiperEscape.escapeAttr).toBe(window.escapeAttr);
      expect(window.PiperEscape.escapeHtml('&')).toBe('&amp;');
    });
  });
});
