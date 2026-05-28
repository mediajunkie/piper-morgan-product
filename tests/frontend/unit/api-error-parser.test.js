/**
 * API Error Parser Tests
 *
 * Tests web/static/js/api-error-parser.js parseApiDetail() function.
 * Covers the FastAPI 422-shape vs. plain-string vs. fallback rendering
 * surfaced by #1119 FRONTEND-ERROR-RENDER.
 */

describe('parseApiDetail', () => {
  beforeEach(() => {
    global.loadScript('api-error-parser.js');
  });

  describe('plain string detail (HTTPException shape)', () => {
    test('returns the string verbatim', () => {
      expect(parseApiDetail('Invalid API key', 'fallback')).toBe('Invalid API key');
    });

    test('returns the string even with leading/trailing whitespace if non-empty', () => {
      expect(parseApiDetail('  Invalid token  ', 'fallback')).toBe('  Invalid token  ');
    });

    test('returns fallback for empty string', () => {
      expect(parseApiDetail('', 'fallback')).toBe('fallback');
    });

    test('returns fallback for whitespace-only string', () => {
      expect(parseApiDetail('   ', 'fallback')).toBe('fallback');
    });
  });

  describe('FastAPI 422 array detail shape', () => {
    test('formats single validation error with loc.path: msg', () => {
      const detail = [{ loc: ['body', 'api_key'], msg: 'field required', type: 'value_error.missing' }];
      expect(parseApiDetail(detail, 'fallback')).toBe('Validation error — body.api_key: field required');
    });

    test('joins multiple validation errors with semicolons', () => {
      const detail = [
        { loc: ['body', 'api_key'], msg: 'field required' },
        { loc: ['body', 'workspace'], msg: 'must be alphanumeric' }
      ];
      const out = parseApiDetail(detail, 'fallback');
      expect(out).toContain('body.api_key: field required');
      expect(out).toContain('body.workspace: must be alphanumeric');
      expect(out).toContain('; ');
    });

    test('handles missing loc gracefully (msg only)', () => {
      const detail = [{ msg: 'some error' }];
      expect(parseApiDetail(detail, 'fallback')).toBe('Validation error — some error');
    });

    test('handles missing msg with "invalid" placeholder', () => {
      const detail = [{ loc: ['body', 'foo'] }];
      expect(parseApiDetail(detail, 'fallback')).toBe('Validation error — body.foo: invalid');
    });

    test('filters falsy loc segments', () => {
      const detail = [{ loc: ['body', null, '', 'api_key'], msg: 'field required' }];
      expect(parseApiDetail(detail, 'fallback')).toBe('Validation error — body.api_key: field required');
    });

    test('returns fallback for empty array', () => {
      expect(parseApiDetail([], 'fallback')).toBe('fallback');
    });
  });

  describe('object detail with msg property', () => {
    test('returns the msg property', () => {
      expect(parseApiDetail({ msg: 'something went wrong' }, 'fallback')).toBe('something went wrong');
    });
  });

  describe('missing or null detail', () => {
    test('undefined → fallback', () => {
      expect(parseApiDetail(undefined, 'fallback')).toBe('fallback');
    });

    test('null → fallback', () => {
      expect(parseApiDetail(null, 'fallback')).toBe('fallback');
    });

    test('no fallback provided → generic message', () => {
      expect(parseApiDetail(null)).toBe('Request failed');
    });
  });

  describe('regression — the [object Object] bug specifically', () => {
    test('FastAPI 422 array does NOT stringify as "[object Object]"', () => {
      const detail = [{ loc: ['query', 'api_key'], msg: 'field required' }];
      const result = parseApiDetail(detail, 'Failed to save');
      expect(result).not.toContain('[object Object]');
      expect(result).toContain('field required');
    });

    test('Multi-element 422 array does NOT stringify as "[object Object],[object Object]"', () => {
      const detail = [
        { loc: ['body', 'a'], msg: 'a-err' },
        { loc: ['body', 'b'], msg: 'b-err' }
      ];
      const result = parseApiDetail(detail, 'fallback');
      expect(result).not.toContain('[object Object]');
      expect(result).toContain('a-err');
      expect(result).toContain('b-err');
    });
  });
});
