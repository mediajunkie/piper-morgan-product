/**
 * Form Validation System Tests
 *
 * Tests web/static/js/form-validation.js
 * Covers: FormValidation and Validators objects
 */

describe('Form Validation System', () => {
  beforeEach(() => {
    // Load form-validation.js
    global.loadScript('form-validation.js');
  });

  describe('FormValidation.init()', () => {
    test('initializes validation for a form', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="email" type="email">
          <button type="submit">Submit</button>
        </form>
      `;

      FormValidation.init('test-form', {
        email: [Validators.required()]
      });

      expect(FormValidation.validators['test-form']).toBeDefined();
      expect(FormValidation.validators['test-form'].email).toBeDefined();
    });

    test('handles missing form gracefully', () => {
      expect(() => {
        FormValidation.init('nonexistent-form', {});
      }).not.toThrow();
    });

    test('attaches event listeners to fields', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="username" type="text">
        </form>
      `;

      const addEventListenerSpy = jest.spyOn(
        document.querySelector('[name="username"]'),
        'addEventListener'
      );

      FormValidation.init('test-form', {
        username: [Validators.required()]
      });

      // Should add blur, input, and change listeners
      expect(addEventListenerSpy).toHaveBeenCalledWith('blur', expect.any(Function));
      expect(addEventListenerSpy).toHaveBeenCalledWith('input', expect.any(Function));
      expect(addEventListenerSpy).toHaveBeenCalledWith('change', expect.any(Function));
    });
  });

  describe('FormValidation.validateField()', () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <form id="test-form">
          <div class="field-container">
            <input name="email" type="email" value="">
          </div>
        </form>
      `;

      FormValidation.init('test-form', {
        email: [Validators.required(), Validators.email()]
      });
    });

    test('returns false for invalid field', () => {
      const result = FormValidation.validateField('test-form', 'email');
      expect(result).toBe(false);
    });

    test('returns true for valid field', () => {
      document.querySelector('[name="email"]').value = 'test@example.com';
      const result = FormValidation.validateField('test-form', 'email');
      expect(result).toBe(true);
    });

    test('sets aria-invalid attribute on invalid field', () => {
      FormValidation.validateField('test-form', 'email');

      const field = document.querySelector('[name="email"]');
      expect(field.getAttribute('aria-invalid')).toBe('true');
    });

    test('clears aria-invalid on valid field', () => {
      const field = document.querySelector('[name="email"]');
      field.value = 'valid@email.com';

      FormValidation.validateField('test-form', 'email');

      expect(field.getAttribute('aria-invalid')).toBe('false');
    });
  });

  describe('FormValidation.validateForm()', () => {
    test('returns true when all fields are valid', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="name" type="text" value="John">
          <input name="email" type="email" value="john@example.com">
        </form>
      `;

      FormValidation.init('test-form', {
        name: [Validators.required()],
        email: [Validators.required(), Validators.email()]
      });

      const result = FormValidation.validateForm('test-form');
      expect(result).toBe(true);
    });

    test('returns false when any field is invalid', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="name" type="text" value="">
          <input name="email" type="email" value="john@example.com">
        </form>
      `;

      FormValidation.init('test-form', {
        name: [Validators.required()],
        email: [Validators.required()]
      });

      const result = FormValidation.validateForm('test-form');
      expect(result).toBe(false);
    });
  });

  describe('FormValidation.clearErrors()', () => {
    test('clears all error messages', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="email" type="email" value="">
          <div class="error-message" style="display: block">Error here</div>
        </form>
      `;

      FormValidation.init('test-form', {
        email: [Validators.required()]
      });

      // Trigger validation to create error state
      FormValidation.validateField('test-form', 'email');

      // Clear errors
      FormValidation.clearErrors('test-form');

      const errorEl = document.querySelector('.error-message');
      expect(errorEl.style.display).toBe('none');
      expect(errorEl.textContent).toBe('');
    });

    test('resets aria-invalid on all fields', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="email" type="email" value="" aria-invalid="true">
        </form>
      `;

      FormValidation.init('test-form', {});
      FormValidation.clearErrors('test-form');

      const field = document.querySelector('[name="email"]');
      expect(field.getAttribute('aria-invalid')).toBe('false');
    });
  });

  describe('FormValidation.getErrors()', () => {
    test('returns errors object for form', () => {
      document.body.innerHTML = `
        <form id="test-form">
          <input name="email" type="email" value="">
        </form>
      `;

      FormValidation.init('test-form', {
        email: [Validators.required()]
      });

      FormValidation.validateField('test-form', 'email');

      const errors = FormValidation.getErrors('test-form');
      expect(errors.email).toBeDefined();
      expect(errors.email).toContain('We need your email');
    });
  });
});

describe('Validators', () => {
  describe('Validators.required()', () => {
    test('returns error for empty value', () => {
      const field = { value: '', type: 'text', name: 'username' };
      const result = Validators.required()(field);
      expect(result).toContain('We need your username');
    });

    test('returns error for whitespace-only value', () => {
      const field = { value: '   ', type: 'text', name: 'username' };
      const result = Validators.required()(field);
      expect(result).toContain('We need your username');
    });

    test('returns null for non-empty value', () => {
      const field = { value: 'John', type: 'text', name: 'username' };
      const result = Validators.required()(field);
      expect(result).toBeNull();
    });
  });

  describe('Validators.email()', () => {
    test('returns null for empty value (not required)', () => {
      const field = { value: '' };
      const result = Validators.email()(field);
      expect(result).toBeNull();
    });

    test('returns null for valid email', () => {
      const validEmails = [
        'test@example.com',
        'user.name@domain.org',
        'user+tag@example.co.uk'
      ];

      validEmails.forEach(email => {
        const field = { value: email };
        const result = Validators.email()(field);
        expect(result).toBeNull();
      });
    });

    test('returns error for invalid email', () => {
      const invalidEmails = [
        'notanemail',
        'missing@domain',
        '@nodomain.com',
        'spaces in@email.com'
      ];

      invalidEmails.forEach(email => {
        const field = { value: email };
        const result = Validators.email()(field);
        expect(result).toContain('valid email');
      });
    });
  });

  describe('Validators.min()', () => {
    test('returns null when value meets minimum', () => {
      const field = { value: '10' };
      const result = Validators.min(5)(field);
      expect(result).toBeNull();
    });

    test('returns error when value below minimum', () => {
      const field = { value: '3' };
      const result = Validators.min(5)(field);
      expect(result).toContain('Value needs to be at least 5');
    });
  });

  describe('Validators.max()', () => {
    test('returns null when value within maximum', () => {
      const field = { value: '5' };
      const result = Validators.max(10)(field);
      expect(result).toBeNull();
    });

    test('returns error when value exceeds maximum', () => {
      const field = { value: '15' };
      const result = Validators.max(10)(field);
      expect(result).toContain("Value can't exceed 10");
    });
  });

  describe('Validators.minLength()', () => {
    test('returns null when length meets requirement', () => {
      const field = { value: 'password123' };
      const result = Validators.minLength(8)(field);
      expect(result).toBeNull();
    });

    test('returns error when length too short', () => {
      const field = { value: 'short' };
      const result = Validators.minLength(8)(field);
      expect(result).toContain('Needs at least 8 characters');
    });
  });

  describe('Validators.custom()', () => {
    test('returns null when custom validator passes', () => {
      const isEven = (value) => parseInt(value) % 2 === 0;
      const field = { value: '4' };
      const result = Validators.custom(isEven, 'Must be even')(field);
      expect(result).toBeNull();
    });

    test('returns custom message when validator fails', () => {
      const isEven = (value) => parseInt(value) % 2 === 0;
      const field = { value: '3' };
      const result = Validators.custom(isEven, 'Must be even')(field);
      expect(result).toBe('Must be even');
    });
  });
});
