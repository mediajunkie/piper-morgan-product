/**
 * Jest Setup File
 *
 * Configures global mocks and DOM environment for testing
 * vanilla JavaScript from web/static/js/
 */

// Mock fetch globally
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
    status: 200
  })
);

// Mock localStorage
const localStorageMock = {
  store: {},
  getItem: jest.fn((key) => localStorageMock.store[key] || null),
  setItem: jest.fn((key, value) => {
    localStorageMock.store[key] = String(value);
  }),
  removeItem: jest.fn((key) => {
    delete localStorageMock.store[key];
  }),
  clear: jest.fn(() => {
    localStorageMock.store = {};
  }),
  get length() {
    return Object.keys(localStorageMock.store).length;
  },
  key: jest.fn((index) => Object.keys(localStorageMock.store)[index] || null)
};
Object.defineProperty(global, 'localStorage', { value: localStorageMock });

// Mock sessionStorage (same implementation)
const sessionStorageMock = {
  store: {},
  getItem: jest.fn((key) => sessionStorageMock.store[key] || null),
  setItem: jest.fn((key, value) => {
    sessionStorageMock.store[key] = String(value);
  }),
  removeItem: jest.fn((key) => {
    delete sessionStorageMock.store[key];
  }),
  clear: jest.fn(() => {
    sessionStorageMock.store = {};
  }),
  get length() {
    return Object.keys(sessionStorageMock.store).length;
  },
  key: jest.fn((index) => Object.keys(sessionStorageMock.store)[index] || null)
};
Object.defineProperty(global, 'sessionStorage', { value: sessionStorageMock });

// Mock console methods for cleaner test output (optional)
// Uncomment if you want to suppress console output during tests:
// global.console = {
//   ...console,
//   log: jest.fn(),
//   warn: jest.fn(),
//   error: jest.fn()
// };

// Reset all mocks and DOM before each test
beforeEach(() => {
  jest.clearAllMocks();
  document.body.innerHTML = '';
  document.head.innerHTML = '';
  localStorageMock.store = {};
  sessionStorageMock.store = {};
  global.fetch.mockClear();
});

// Clean up after each test
afterEach(() => {
  // Clear any timers
  jest.clearAllTimers();
});

/**
 * Helper to load a JS file and execute it in the current context
 * @param {string} relativePath - Path relative to web/static/js/
 * @returns {void}
 */
global.loadScript = (relativePath) => {
  const fs = require('fs');
  const path = require('path');
  const scriptPath = path.join(__dirname, '../../web/static/js', relativePath);
  const code = fs.readFileSync(scriptPath, 'utf8');

  // Parse the file to extract top-level const/let object declarations
  // and assign them to global scope
  // This handles patterns like: const Toast = { ... }

  // Create a function that returns the declared objects
  // Wrap the code to capture and export top-level const declarations
  const wrappedCode = `
    ${code}
    return {
      Toast: typeof Toast !== 'undefined' ? Toast : undefined,
      Dialog: typeof Dialog !== 'undefined' ? Dialog : undefined,
      FormValidation: typeof FormValidation !== 'undefined' ? FormValidation : undefined,
      Validators: typeof Validators !== 'undefined' ? Validators : undefined,
      parseApiDetail: typeof parseApiDetail !== 'undefined' ? parseApiDetail : undefined
    };
  `;

  try {
    const fn = new Function(wrappedCode);
    const exports = fn();

    // Assign exported objects to global scope
    Object.entries(exports).forEach(([name, value]) => {
      if (value !== undefined) {
        global[name] = value;
      }
    });
  } catch (err) {
    console.error(`Error loading script ${relativePath}:`, err.message);
    throw err;
  }
};

/**
 * Helper to create common DOM elements for testing
 */
global.createToastContainer = () => {
  // Create container
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.setAttribute('aria-live', 'polite');
  document.body.appendChild(container);

  // Create template
  const template = document.createElement('template');
  template.id = 'toast-template';
  template.innerHTML = `
    <div class="toast" role="alert" aria-atomic="true">
      <span class="toast-icon"></span>
      <div class="toast-content">
        <div class="toast-title"></div>
        <div class="toast-message"></div>
      </div>
      <button class="toast-close" aria-label="Close notification">&times;</button>
    </div>
  `;
  document.body.appendChild(template);
};
