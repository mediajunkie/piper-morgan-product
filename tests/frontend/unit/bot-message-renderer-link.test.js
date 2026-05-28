/**
 * Bot Message Renderer — Link Behavior Tests (#1123 LINK-NEW-TAB)
 *
 * Verifies external links open in new tabs and internal links stay same-tab.
 */

describe('#1123 LINK-NEW-TAB — renderBotMessage link behavior', () => {
  let renderBotMessage;

  beforeEach(() => {
    // Mock marked — we're testing the link-renderer LOGIC, not marked itself.
    // Capture the configured link renderer when marked.use() is called.
    let configuredLinkRenderer = null;
    const fakeMarked = {
      use: (opts) => {
        if (opts && opts.renderer && opts.renderer.link) {
          configuredLinkRenderer = opts.renderer.link;
        }
      },
      // Minimal parse: matches markdown links and replaces via the renderer
      parse: (text) => {
        if (!configuredLinkRenderer) return text;
        return text.replace(
          /\[([^\]]+)\]\(([^)]+)\)/g,
          (_, txt, href) => configuredLinkRenderer(href, null, txt)
        );
      },
    };
    global.marked = fakeMarked;

    // Load the renderer module's source and evaluate it
    const fs = require('fs');
    const path = require('path');
    const code = fs.readFileSync(
      path.join(__dirname, '../../../web/assets/bot-message-renderer.js'),
      'utf8'
    );
    // Wrap so top-level function declarations attach to a captured object
    const wrapped = new Function('marked', `
      ${code}
      return { renderBotMessage };
    `);
    renderBotMessage = wrapped(fakeMarked).renderBotMessage;
  });

  test('external https link gets target="_blank" and rel="noopener noreferrer"', () => {
    const html = renderBotMessage('Check [Notion](https://notion.so/abc) for more.');
    expect(html).toMatch(/href="https:\/\/notion\.so\/abc"/);
    expect(html).toMatch(/target="_blank"/);
    expect(html).toMatch(/rel="noopener noreferrer"/);
  });

  test('external http link also gets target="_blank"', () => {
    const html = renderBotMessage('See [example](http://example.com)');
    expect(html).toMatch(/target="_blank"/);
    expect(html).toMatch(/rel="noopener noreferrer"/);
  });

  test('internal absolute-path link does NOT get target="_blank"', () => {
    const html = renderBotMessage('Go to [Settings](/settings/notion)');
    expect(html).toMatch(/href="\/settings\/notion"/);
    expect(html).not.toMatch(/target="_blank"/);
  });

  test('relative link does NOT get target="_blank"', () => {
    const html = renderBotMessage('See [docs](docs/foo.md)');
    expect(html).not.toMatch(/target="_blank"/);
  });

  test('anchor link does NOT get target="_blank"', () => {
    const html = renderBotMessage('Jump to [section](#intro)');
    expect(html).not.toMatch(/target="_blank"/);
  });

  test('mixed message with internal + external links treats each correctly', () => {
    const html = renderBotMessage(
      'Open [Notion](https://notion.so/x) or visit [/settings](/settings)'
    );
    // External should have target=_blank
    expect(html).toMatch(/href="https:\/\/notion\.so\/x"[^>]*target="_blank"/);
    // Internal should NOT
    expect(html).toMatch(/href="\/settings"(?![^>]*target="_blank")/);
  });

  test('idempotent — calling renderBotMessage twice does not double-configure', () => {
    renderBotMessage('First call [a](https://a.com)');
    renderBotMessage('Second call [b](https://b.com)');
    expect(renderBotMessage._linkRendererConfigured).toBe(true);
  });
});
