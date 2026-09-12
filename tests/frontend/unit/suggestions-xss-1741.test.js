/**
 * #1741 [SECURITY] — pattern-suggestions UI: attempted-exploit pins.
 *
 * renderSuggestions/renderSuggestionCard interpolate pattern-derived data
 * (pattern_id, pattern_type, and a reasoning string built from
 * pattern_data.reasoning / description / action_params.title — plausibly
 * user-authored, e.g. an issue title captured into a learned
 * create_github_issue pattern) into HTML appended to element.innerHTML. This
 * surface was deliberately left OUTSIDE the #1732 DOMPurify chokepoint because
 * its markup carries inline onclick handlers by design (DOMPurify would strip
 * them and break the accept/reject/execute buttons). It gets the #1578
 * treatment instead: escapeHtml/escapeAttr per interpolation, numeric fields
 * coerced to numbers, and user-adjacent text never in onclick JS-string
 * context — only the server-generated pattern id crosses that boundary.
 *
 * LAYER (named honestly): RUNTIME DOM via jsdom — hostile suggestion objects
 * rendered through the REAL served renderer source (web/assets/) and
 * innerHTML'd into a real jsdom container, exactly the app's sink shape
 * (handleDirectResponse appends renderSuggestions output to
 * element.innerHTML). The full-path test additionally runs through the REAL
 * vendored marked (15.0.12) + DOMPurify (3.2.7) via handleDirectResponse.
 * What it is NOT: a browser E2E through the live server.
 */

const fs = require('fs');
const path = require('path');

const VENDOR = path.join(__dirname, '../../../web/static/vendor');
const MARKED = path.join(VENDOR, 'marked-15.0.12.min.js');
const PURIFY = path.join(VENDOR, 'purify-3.2.7.min.js');
const ASSETS_RENDERER = path.join(__dirname, '../../../web/assets/bot-message-renderer.js');

function realMarked() {
  const mod = require(MARKED);
  return mod.marked && mod.marked.parse ? mod.marked : mod;
}

function realDOMPurify() {
  let p = require(PURIFY);
  if (!p.sanitize && typeof p === 'function') p = p(window);
  expect(p.isSupported).toBe(true); // guard: an unsupported DOMPurify proves nothing (m-44)
  return p;
}

/** Load the renderer source with explicit marked/DOMPurify bindings. */
function loadRenderer({ marked, purify } = {}) {
  const code = fs.readFileSync(ASSETS_RENDERER, 'utf8');
  // eslint-disable-next-line no-new-func
  const wrapped = new Function(
    'marked',
    'DOMPurify',
    'module',
    'window',
    `${code}\nreturn { renderBotMessage, renderSuggestions, renderSuggestionCard, handleDirectResponse };`
  );
  return wrapped(marked, purify, undefined, window);
}

/** Mount suggestions exactly as handleDirectResponse does: innerHTML +=. */
function mountSuggestions(renderSuggestions, suggestions) {
  const el = document.createElement('div');
  el.innerHTML = '<div class="result success">ok</div>';
  el.innerHTML += renderSuggestions(suggestions); // the real sink shape
  document.body.appendChild(el);
  return el;
}

function suggestion(overrides = {}) {
  return {
    pattern_id: '4f8b2c1a-9d3e-4a5b-8c7d-6e5f4a3b2c1d',
    pattern_type: 'issue_creation',
    confidence: 0.87,
    usage_count: 3,
    pattern_data: { reasoning: 'You often create issues after standup' },
    ...overrides,
  };
}

const PAYLOAD_ONERROR = '<img src=x onerror="window.__pwned = true">';
const PAYLOAD_SCRIPT = '<script>window.__pwned = true;</script>';

beforeEach(() => {
  document.body.innerHTML = '';
  delete window.__pwned;
  // Suppress the first-time onboarding tooltip so cards are the whole surface.
  localStorage.setItem('piper_suggestions_seen', 'true');
});

describe('#1741 suggestions render boundary — hostile pattern data is neutralized in the OUTPUT', () => {
  let R;

  beforeEach(() => {
    R = loadRenderer(); // no marked/DOMPurify: the suggestions path must be safe on its own
  });

  test('hostile pattern_data.reasoning emerges as inert text (no element, no handler, no execution)', () => {
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({ pattern_data: { reasoning: PAYLOAD_ONERROR } }),
    ]);
    expect(el.querySelector('.suggestion-reasoning img')).toBeNull();
    expect(el.querySelector('[onerror]')).toBeNull();
    // Escaped, not dropped: the text survives visibly.
    expect(el.querySelector('.suggestion-reasoning').textContent).toContain('<img src=x');
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile action_params.title (the derived-reasoning path, the issue-cited vector) is inert', () => {
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({
        pattern_data: {
          action_type: 'create_github_issue',
          action_params: { title: PAYLOAD_SCRIPT },
        },
      }),
    ]);
    expect(el.querySelector('script')).toBeNull();
    expect(el.innerHTML).not.toMatch(/<script/i);
    expect(el.querySelector('.suggestion-reasoning').textContent).toContain(
      'Create GitHub Issue:'
    );
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile pattern_type is inert in the meta line', () => {
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({ pattern_type: PAYLOAD_ONERROR }),
    ]);
    expect(el.querySelector('.suggestion-meta img')).toBeNull();
    expect(el.querySelector('[onerror]')).toBeNull();
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile pattern_id cannot break out of the data attribute (no new attributes materialize)', () => {
    const hostileId = 'x" onmouseover="window.__pwned = true';
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({ pattern_id: hostileId }),
    ]);
    expect(el.querySelector('[onmouseover]')).toBeNull();
    // The escaping is entity-level: the parser round-trips the value as TEXT.
    const card = el.querySelector('.suggestion-card');
    expect(card.getAttribute('data-pattern-id')).toBe(hostileId);
    expect(window.__pwned).toBeUndefined();
  });

  test('user-adjacent text NEVER appears in onclick JS-string context (the #1578 invariant)', () => {
    // HTML-escaping cannot protect onclick (entities decode before the JS
    // engine parses the handler) — so the pin is absence, not escaping.
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({
        pattern_data: { reasoning: "evil'); window.__pwned = true; ('" },
      }),
    ]);
    for (const btn of el.querySelectorAll('[onclick]')) {
      expect(btn.getAttribute('onclick')).not.toContain('__pwned');
    }
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile usage_count / confidence strings are coerced to numbers, never rendered as markup', () => {
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({ usage_count: PAYLOAD_ONERROR, confidence: PAYLOAD_ONERROR }),
    ]);
    expect(el.querySelector('[onerror]')).toBeNull();
    expect(el.querySelector('.suggestion-usage').textContent).toContain('Used 0 times');
    expect(el.querySelector('.confidence-label').textContent).toContain('0% confidence');
    expect(window.__pwned).toBeUndefined();
  });
});

describe('#1741 regression guards — benign suggestions still render a working UI', () => {
  let R;

  beforeEach(() => {
    R = loadRenderer();
  });

  test('benign card keeps its content, buttons, and id-bearing onclick handlers', () => {
    const el = mountSuggestions(R.renderSuggestions, [suggestion()]);
    const card = el.querySelector('.suggestion-card');
    expect(card).not.toBeNull();
    expect(card.getAttribute('data-pattern-id')).toBe(
      '4f8b2c1a-9d3e-4a5b-8c7d-6e5f4a3b2c1d'
    );
    expect(el.querySelector('.suggestion-reasoning').textContent).toContain(
      'You often create issues after standup'
    );
    expect(el.querySelector('.suggestion-type').textContent.trim()).toBe('issue creation');
    expect(el.querySelector('.confidence-label').textContent).toContain('87% confidence');
    // The inline handlers this surface exists for (why it bypasses DOMPurify):
    const accept = el.querySelector('.suggestion-btn.accept');
    expect(accept).not.toBeNull();
    expect(accept.getAttribute('onclick')).toBe(
      "handleSuggestionFeedback('4f8b2c1a-9d3e-4a5b-8c7d-6e5f4a3b2c1d', 'accept')"
    );
    expect(el.querySelector('.suggestion-btn.reject')).not.toBeNull();
    expect(el.querySelector('.suggestion-btn.dismiss')).not.toBeNull();
  });

  test('auto-triggered card keeps Execute/Skip/Disable handlers', () => {
    const el = mountSuggestions(R.renderSuggestions, [
      suggestion({ auto_triggered: true }),
    ]);
    expect(
      el.querySelector('.suggestion-btn.execute').getAttribute('onclick')
    ).toBe("handleExecute('4f8b2c1a-9d3e-4a5b-8c7d-6e5f4a3b2c1d')");
    expect(el.querySelector('.suggestion-btn.skip')).not.toBeNull();
    expect(el.querySelector('.suggestion-btn.disable')).not.toBeNull();
  });
});

describe('#1741 full path — handleDirectResponse with REAL marked + REAL DOMPurify', () => {
  test('message goes through the #1732 chokepoint; suggestions render hostile-inert WITH handlers intact', () => {
    delete window.__pwned;
    const R = loadRenderer({ marked: realMarked(), purify: realDOMPurify() });
    const el = document.createElement('div');
    document.body.appendChild(el);

    R.handleDirectResponse(
      {
        message: `Done! ${PAYLOAD_SCRIPT}`,
        suggestions: [suggestion({ pattern_data: { reasoning: PAYLOAD_ONERROR } })],
      },
      el
    );

    // #1732 half: the chat message is sanitized.
    expect(el.querySelector('script')).toBeNull();
    // #1741 half: the suggestion payload is inert...
    expect(el.querySelector('[onerror]')).toBeNull();
    // ...while the intentional inline handlers SURVIVE (they never crossed
    // DOMPurify — the reason this surface needed its own fix).
    expect(el.querySelector('.suggestion-btn.accept').getAttribute('onclick')).toContain(
      'handleSuggestionFeedback'
    );
    expect(window.__pwned).toBeUndefined();
  });
});
