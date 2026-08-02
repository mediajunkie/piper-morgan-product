> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# G26: Spacing System
**WCAG 2.2 AA Compliance**: 8px grid-based spacing for consistent, accessible layouts

---

## Overview

The spacing system is built on an **8px base unit**. All spacing values are multiples of 8px, creating visual harmony and consistency across the entire application.

### Why 8px?
- Aligns with most design systems (Material Design, Ant Design, Bootstrap)
- Works well with modern screen DPI values
- Provides enough granularity for precise layouts
- Easier for developers to memorize and use
- Improves visual hierarchy and balance

---

## Spacing Scale

```
--space-xs   = 4px   (0.5x)  Micro spacing
--space-sm   = 8px   (1x)    Small spacing
--space-md   = 16px  (2x)    Medium spacing
--space-lg   = 24px  (3x)    Large spacing
--space-xl   = 32px  (4x)    Extra large spacing
--space-2xl  = 40px  (5x)    2x extra large
--space-3xl  = 48px  (6x)    3x extra large
--space-4xl  = 56px  (7x)    4x extra large
--space-5xl  = 64px  (8x)    5x extra large
```

### When to Use Each

| Scale | Use Case | Example |
|-------|----------|---------|
| **xs (4px)** | Micro spacing between inline elements | Icon + text in button |
| **sm (8px)** | Tight spacing within components | Button padding, small gaps |
| **md (16px)** | Standard component spacing | Form field spacing, card padding |
| **lg (24px)** | Section padding, larger margins | Container padding, sidebar spacing |
| **xl (32px)** | Major section spacing | Between main content areas |
| **2xl+ (40px+)** | Large layouts | Page margins, major sections |

---

## CSS Variables

All spacing values are defined as CSS custom properties (variables) for easy customization:

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;
  --space-3xl: 48px;
  --space-4xl: 56px;
  --space-5xl: 64px;
}
```

### Overriding Spacing

You can override spacing in specific contexts:

```css
/* Tighter spacing in mobile */
@media (max-width: 768px) {
  :root {
    --space-lg: 16px;
    --space-xl: 24px;
  }
}

/* Dark mode specific spacing */
@media (prefers-color-scheme: dark) {
  .dark-container {
    padding: var(--space-xl);
  }
}
```

---

## Padding Utilities

### All Sides
```html
<div class="p-sm">Small padding all sides (8px)</div>
<div class="p-md">Medium padding all sides (16px)</div>
<div class="p-lg">Large padding all sides (24px)</div>
```

### Horizontal Padding
```html
<div class="px-sm">Padding left & right (8px)</div>
<div class="px-md">Padding left & right (16px)</div>
```

### Vertical Padding
```html
<div class="py-sm">Padding top & bottom (8px)</div>
<div class="py-lg">Padding top & bottom (24px)</div>
```

### Individual Sides
```html
<div class="pt-md">Padding top only (16px)</div>
<div class="pb-lg">Padding bottom only (24px)</div>
<div class="pl-sm">Padding left only (8px)</div>
<div class="pr-xl">Padding right only (32px)</div>
```

---

## Margin Utilities

### All Sides
```html
<div class="m-sm">Small margin all sides (8px)</div>
<div class="m-lg">Large margin all sides (24px)</div>
```

### Horizontal Margin
```html
<div class="mx-sm">Margin left & right (8px)</div>
<div class="mx-auto">Center horizontally</div>
```

### Vertical Margin
```html
<div class="my-md">Margin top & bottom (16px)</div>
```

### Individual Sides
```html
<div class="mt-lg">Margin top only (24px)</div>
<div class="mb-md">Margin bottom only (16px)</div>
<div class="ml-sm">Margin left only (8px)</div>
<div class="mr-xl">Margin right only (32px)</div>
```

---

## Gap Utilities (Flexbox & Grid)

### Standard Gap
```html
<div style="display: flex;" class="gap-md">
  <item>Item 1</item>
  <item>Item 2</item>
</div>
```

### Row Gap (Grid/Flex Direction Column)
```html
<div style="display: flex; flex-direction: column;" class="row-gap-lg">
  <item>Item 1</item>
  <item>Item 2</item>
</div>
```

### Column Gap (Grid)
```html
<div style="display: grid; grid-template-columns: 1fr 1fr;" class="col-gap-md">
  <item>Item 1</item>
  <item>Item 2</item>
</div>
```

---

## Common Patterns

### Containers
```html
<div class="container-padding">
  <!-- 24px padding on desktop, 16px on mobile -->
</div>
```

### Cards
```html
<div class="card card-padding card-margin" style="display: flex;" class="card-gap">
  <img src="..." />
  <div>Content</div>
</div>
```

### Forms
```html
<div class="form-group-spacing">
  <label>Field Label</label>
  <input class="form-field-spacing" />
  <label>Another Field</label>
  <input />
</div>

<div class="form-padding">
  <!-- Form content with 24px padding -->
</div>
```

### Sections
```html
<section class="section-padding section-margin">
  <h2 class="heading-margin">Section Title</h2>
  <!-- Section content -->
</section>
```

### Button Groups
```html
<div style="display: flex;" class="button-group-gap">
  <button class="button-padding">Cancel</button>
  <button class="button-padding">Save</button>
</div>
```

### Lists
```html
<ul style="list-style: none; padding: 0;">
  <li class="list-item-padding list-item-spacing">Item 1</li>
  <li class="list-item-padding list-item-spacing">Item 2</li>
  <li class="list-item-padding list-item-spacing">Item 3</li>
</ul>
```

### Navigation
```html
<nav class="nav-padding">
  <a href="/" class="nav-item-spacing">Home</a>
  <a href="/about" class="nav-item-spacing">About</a>
</nav>
```

### Headings & Titles
```html
<div class="container">
  <h1 class="heading-margin">Page Title</h1>
  <h2 class="title-margin">Section Title</h2>
  <p class="subtitle-margin">Subtitle</p>
</div>
```

---

## Responsive Behavior

### Desktop Layout
- Full spacing at 768px+
- More breathing room, generous margins
- Larger gaps between elements

### Mobile Layout (< 768px)
- Reduced spacing to fit smaller screens
- Tighter padding and margins
- Smaller gaps in grids and flexbox

```css
/* Automatic adjustment at 768px */
@media (max-width: 768px) {
  .p-xl { padding: var(--space-lg); } /* 32px → 24px */
  .gap-lg { gap: var(--space-md); }    /* 24px → 16px */
}
```

---

## Touch Target Sizing (WCAG)

For mobile and touch devices, ensure interactive elements meet the 48px minimum:

```css
/* Automatic 48px minimum on touch devices */
@media (hover: none) and (pointer: coarse) {
  button {
    min-height: 48px;
    min-width: 48px;
    padding: var(--space-md); /* 16px padding */
  }
}
```

**Result**: 16px padding × 2 + 16px content = 48px minimum touch target ✓

---

## Real-World Examples

### Card Layout
```html
<div class="card p-lg">              <!-- 24px padding -->
  <h3 class="mb-md">Title</h3>       <!-- 16px margin bottom -->
  <p class="mb-lg">Description</p>   <!-- 24px margin bottom -->
  <div class="gap-sm" style="display: flex;">
    <button>Action 1</button>        <!-- 8px gap between -->
    <button>Action 2</button>
  </div>
</div>
```

### Form Layout
```html
<form class="form-padding">           <!-- 24px padding -->
  <div class="form-group-spacing">    <!-- 24px margin bottom -->
    <label class="block mb-sm">Email</label>  <!-- 8px margin -->
    <input type="email" class="form-field-spacing" />
  </div>
  <div class="form-group-spacing">
    <label class="block mb-sm">Password</label>
    <input type="password" />
  </div>
  <div class="gap-md" style="display: flex;">
    <button type="button">Cancel</button>    <!-- 16px gap -->
    <button type="submit">Sign In</button>
  </div>
</form>
```

### Section Layout
```html
<section class="section-padding my-3xl">  <!-- 24px padding + 48px margins -->
  <h2 class="heading-margin">Section</h2> <!-- 24px bottom margin -->
  <p class="mb-lg">Introduction text</p>   <!-- 24px margin -->
  <div class="gap-lg" style="display: grid; grid-template-columns: 1fr 1fr;">
    <card>Item 1</card>                    <!-- 24px gap -->
    <card>Item 2</card>
  </div>
</section>
```

---

## Spacing Guidelines

### ✅ DO:
- Always use the spacing scale (don't pick arbitrary values)
- Use CSS variables (var(--space-md)) instead of hardcoding
- Respect responsive adjustments (smaller on mobile)
- Maintain consistent spacing patterns
- Use gap for flexbox/grid (not margins)
- Stack spacing: margin + padding = total breathing room

### ❌ DON'T:
- Use arbitrary spacing (15px, 21px, etc.)
- Hardcode pixel values (use variables instead)
- Mix spacing scales (5px padding + 24px margin)
- Forget mobile responsive adjustments
- Over-space elements (less is more)
- Use negative margins to "fix" spacing

---

## Testing & Verification

### Visual Testing
1. Open each page at different screen sizes (320px, 768px, 1920px)
2. Check that spacing looks balanced and consistent
3. Verify mobile spacing is tighter than desktop
4. Confirm no overlap or cramping

### Code Review Checklist
- [ ] All padding/margin uses spacing variables
- [ ] Spacing scale is consistent with specification
- [ ] Mobile media queries adjust spacing down
- [ ] Form fields have at least 16px padding
- [ ] Touch targets are at least 48px (mobile)
- [ ] Cards and sections have balanced spacing

### Browser DevTools
```javascript
// Check CSS variable values
getComputedStyle(element).getPropertyValue('--space-md') // "16px"

// Inspect spacing on any element
element.style.padding // "var(--space-lg)" or "24px"
```

---

## Customization

### Override for Specific Component
```css
.my-component {
  --space-md: 20px;  /* Override just for this component */
  padding: var(--space-md);
}
```

### Theme Variations
```css
/* Compact theme */
.compact {
  --space-sm: 4px;
  --space-md: 8px;
  --space-lg: 12px;
}

/* Spacious theme */
.spacious {
  --space-md: 24px;
  --space-lg: 32px;
  --space-xl: 48px;
}
```

---

## Resources

- [Material Design Spacing](https://material.io/design/layout/spacing-methods.html)
- [Tailwind CSS Spacing](https://tailwindcss.com/docs/padding)
- [8-Point Grid System](https://builttoadapt.io/8-point-grid-systems-50283f4b3765)
- [Web Accessibility: Spacing](https://www.a11y-101.com/design/spacing)

---

## Integration Checklist

- [ ] `spacing.css` linked on all pages
- [ ] All components use spacing utilities
- [ ] Variables defined in `:root`
- [ ] Mobile breakpoints adjust spacing
- [ ] Touch targets are 48px minimum
- [ ] Spacing is documented in component READMEs
- [ ] Team trained on spacing system
- [ ] Design system uses consistent values

---

## Sign-Off

**Created**: 2025-11-15
**Specification**: WCAG 2.2 AA + Material Design compatibility
**Status**: Ready for implementation

The spacing system is now ready to be applied across all components and pages for maximum consistency and accessibility.
