// G48: Page Transitions
// Provides smooth fade/slide animations when navigating between pages
// Handles link clicks and form submissions with transition effects
// WCAG 2.2 AA: Respects prefers-reduced-motion

const PageTransition = {
  // Configuration
  config: {
    duration: 150, // Duration of transition in milliseconds (reduced for snappier feel)
    type: 'fade', // 'fade' or 'slide'
    disableForReducedMotion: true,
  },

  // State
  isTransitioning: false,
  isReducedMotion: false,

  /**
   * Initialize page transitions
   * @param {Object} options - Configuration options
   */
  init(options = {}) {
    PageTransition.config = { ...PageTransition.config, ...options };

    // Check if user prefers reduced motion
    PageTransition.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Listen for reduced motion changes
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
      PageTransition.isReducedMotion = e.matches;
    });

    // Intercept link clicks
    document.addEventListener('click', PageTransition._handleLinkClick);

    // Intercept form submissions
    document.addEventListener('submit', PageTransition._handleFormSubmit);

    // Prevent browser back/forward transitions
    window.addEventListener('pageshow', PageTransition._handlePageShow);
    window.addEventListener('pagehide', PageTransition._handlePageHide);
  },

  /**
   * Show transition overlay and navigate
   * @param {string} url - URL to navigate to
   */
  transitionTo(url) {
    if (PageTransition.isTransitioning) return;
    if (PageTransition.isReducedMotion && PageTransition.config.disableForReducedMotion) {
      // Skip animation if reduced motion is enabled
      window.location.href = url;
      return;
    }

    PageTransition.isTransitioning = true;
    const overlay = document.getElementById('page-transition-overlay');

    if (!overlay) {
      window.location.href = url;
      return;
    }

    // #1859: navigate NOW. The old version faded the body out, waited
    // `duration`, then navigated — pure added latency on a full-page load,
    // and that fade-out was the first frame of the blank window PM sees.
    // The overlay stays up until the browser tears this document down.
    overlay.classList.add('active');
    window.location.href = url;
  },

  /**
   * Called when page loads to show entry animation
   */
  onPageEnter() {
    if (PageTransition.isReducedMotion && PageTransition.config.disableForReducedMotion) {
      return;
    }

    const overlay = document.getElementById('page-transition-overlay');
    if (overlay) {
      overlay.classList.remove('active');
    }
    // #1859: no `page-entering` any more — its keyframe started the NEW
    // document at opacity 0 for the first ~200 ms, which was the blank frame
    // itself. Content is never hidden on entry.
  },

  /**
   * Handle link clicks
   * @private
   */
  _handleLinkClick(event) {
    const link = event.target.closest('a');
    if (!link) return;

    // Skip special links
    if (
      link.target === '_blank' ||
      link.href === '' ||
      link.href === '#' ||
      link.href.startsWith('javascript:') ||
      link.href.startsWith('mailto:') ||
      link.href.startsWith('tel:')
    ) {
      return;
    }

    // Check if link is internal (same origin)
    const linkUrl = new URL(link.href);
    const currentUrl = new URL(window.location.href);

    if (linkUrl.origin !== currentUrl.origin) {
      return;
    }

    // Check for specific classes that should skip transition
    if (link.classList.contains('no-transition') || link.classList.contains('skip-link')) {
      return;
    }

    // Prevent default and show transition
    event.preventDefault();
    PageTransition.transitionTo(link.href);
  },

  /**
   * Handle form submissions
   * @private
   */
  _handleFormSubmit(event) {
    const form = event.target;

    // Skip if form has no-transition class
    if (form.classList.contains('no-transition')) {
      return;
    }

    // Skip if form opens in new tab/window
    if (form.target === '_blank') {
      return;
    }

    // Check if form method is POST (usually doesn't navigate)
    if (form.method.toUpperCase() === 'POST') {
      // For POST requests, still show transition briefly
      const overlay = document.getElementById('page-transition-overlay');
      if (overlay && !PageTransition.isReducedMotion) {
        overlay.classList.add('active');
        setTimeout(() => {
          overlay.classList.remove('active');
        }, PageTransition.config.duration);
      }
      return;
    }

    // For GET requests, show transition and navigate
    const action = form.getAttribute('action');
    if (action) {
      event.preventDefault();
      PageTransition.transitionTo(action);
    }
  },

  /**
   * Handle page show (browser back/forward)
   * @private
   */
  _handlePageShow(event) {
    if (event.persisted) {
      // Page was restored from back/forward cache
      PageTransition.onPageEnter();
    }
  },

  /**
   * Handle page hide (browser back/forward)
   * @private
   */
  _handlePageHide(event) {
    // Reset state for next navigation
    PageTransition.isTransitioning = false;
  },

  /**
   * Cleanup and remove transition system
   */
  destroy() {
    document.removeEventListener('click', PageTransition._handleLinkClick);
    document.removeEventListener('submit', PageTransition._handleFormSubmit);
    window.removeEventListener('pageshow', PageTransition._handlePageShow);
    window.removeEventListener('pagehide', PageTransition._handlePageHide);
  },
};

// Auto-initialize on page load if not reduced motion
document.addEventListener('DOMContentLoaded', () => {
  PageTransition.init();
  PageTransition.onPageEnter();
});
