// G52: Session Timeout Handling
// Tracks user idle time and warns before session expiry
// Provides graceful logout and session extension
// Configuration can be customized per deployment

const SessionTimeout = {
  // Configuration (override these in init)
  totalSessionMinutes: 30, // Total session duration
  warningMinutesBefore: 5, // Warn this many minutes before expiry
  idleMinutesBeforeWarning: 25, // Show warning after this many idle minutes
  warningIntervalSeconds: 1, // Update countdown every N seconds
  logoutUrl: '/logout', // URL to redirect to on logout
  // #1384: "Continue Working" was a placebo — it reset only the client timer
  // while the 30-min JWT marched on. The #857 refresh endpoint (httponly
  // refresh_token cookie, rotates on use) is the real extension.
  extendUrl: '/api/v1/auth/refresh',

  // Internal state
  sessionStartTime: null,
  lastActivityTime: null,
  timeoutHandle: null,
  countdownHandle: null,
  modalOpen: false,
  sessionExpired: false,

  /**
   * Initialize session timeout tracking
   * @param {Object} config - Configuration options
   */
  init(config = {}) {
    // Merge config
    Object.assign(SessionTimeout, config);

    SessionTimeout.sessionStartTime = Date.now();
    SessionTimeout.lastActivityTime = Date.now();

    // Track user activity
    // #1384: the modal copy promises "Move your mouse ... to stay signed in"
    // but mousemove was never tracked (and 'touch' is not a DOM event — the
    // touchstart listener silently never fired). mousemove is throttled so a
    // busy pointer doesn't spam the timestamp.
    document.addEventListener('mousedown', () => SessionTimeout.recordActivity());
    document.addEventListener('keydown', () => SessionTimeout.recordActivity());
    document.addEventListener('touchstart', () => SessionTimeout.recordActivity());
    document.addEventListener('scroll', () => SessionTimeout.recordActivity());
    let lastMove = 0;
    document.addEventListener('mousemove', () => {
      const now = Date.now();
      if (now - lastMove > 5000) {
        lastMove = now;
        SessionTimeout.recordActivity();
      }
    });

    // #1384: bind the modal buttons here (template carries no inline onclick).
    const bind = (id, fn) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('click', fn);
    };
    bind('session-timeout-extend', () => SessionTimeout.extend());
    bind('session-timeout-logout', () => SessionTimeout.logout());
    bind('session-timeout-close', () => SessionTimeout.dismiss());

    // Start idle timeout check
    SessionTimeout.startIdleCheck();
  },

  /**
   * Record user activity and reset idle timer
   */
  recordActivity() {
    SessionTimeout.lastActivityTime = Date.now();

    // If modal was shown, dismiss it (user is active)
    if (SessionTimeout.modalOpen) {
      SessionTimeout.dismiss();
    }
  },

  /**
   * Start checking for idle timeout
   */
  startIdleCheck() {
    // Check idle status every 10 seconds
    const checkInterval = setInterval(() => {
      const minutesIdle = (Date.now() - SessionTimeout.lastActivityTime) / 1000 / 60;
      const minutesUntilExpiry =
        SessionTimeout.totalSessionMinutes - minutesIdle;

      // Show warning if within warning window
      if (
        minutesUntilExpiry <= SessionTimeout.warningMinutesBefore &&
        minutesUntilExpiry > 0 &&
        !SessionTimeout.modalOpen
      ) {
        SessionTimeout.showWarning(minutesUntilExpiry);
      }

      // Auto-logout if time expired
      if (minutesUntilExpiry <= 0 && !SessionTimeout.sessionExpired) {
        SessionTimeout.sessionExpired = true;
        SessionTimeout.autoLogout();
      }
    }, 10000); // Check every 10 seconds

    SessionTimeout.timeoutHandle = checkInterval;
  },

  /**
   * Show session timeout warning modal
   * @param {number} minutesRemaining - Minutes until session expires
   */
  showWarning(minutesRemaining) {
    const modal = document.getElementById('session-timeout-modal');
    if (!modal) return;

    SessionTimeout.modalOpen = true;

    // Update countdown display
    SessionTimeout.updateCountdown();

    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');

    // Focus close button for accessibility
    const closeBtn = modal.querySelector('.session-timeout-close');
    if (closeBtn) closeBtn.focus();

    // Announce to screen readers
    if (typeof Toast !== 'undefined' && Toast.warning) {
      Toast.warning(
        'Session Expiring',
        `Your session expires in ${Math.round(minutesRemaining)} minutes. Click to continue.`
      );
    }

    // Start countdown updates
    SessionTimeout.startCountdown();
  },

  /**
   * Update countdown display
   */
  updateCountdown() {
    const minutesIdle = (Date.now() - SessionTimeout.lastActivityTime) / 1000 / 60;
    const minutesRemaining = SessionTimeout.totalSessionMinutes - minutesIdle;

    if (minutesRemaining <= 0) {
      SessionTimeout.autoLogout();
      return;
    }

    const minutes = Math.floor(minutesRemaining);
    const seconds = Math.floor((minutesRemaining % 1) * 60);

    const countdownEl = document.getElementById('timeout-countdown');
    if (countdownEl) {
      countdownEl.textContent =
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
  },

  /**
   * Start updating countdown timer
   */
  startCountdown() {
    if (SessionTimeout.countdownHandle) clearInterval(SessionTimeout.countdownHandle);

    SessionTimeout.countdownHandle = setInterval(() => {
      SessionTimeout.updateCountdown();
    }, SessionTimeout.warningIntervalSeconds * 1000);
  },

  /**
   * Stop countdown timer
   */
  stopCountdown() {
    if (SessionTimeout.countdownHandle) {
      clearInterval(SessionTimeout.countdownHandle);
      SessionTimeout.countdownHandle = null;
    }
  },

  /**
   * Extend session (dismiss warning and continue)
   */
  async extend() {
    SessionTimeout.lastActivityTime = Date.now();
    SessionTimeout.dismiss();

    // #1384: actually extend the server-side session. Cookie-based (#857);
    // on failure be honest — a dead refresh token means the session WILL end.
    if (SessionTimeout.extendUrl) {
      try {
        const res = await fetch(SessionTimeout.extendUrl, {
          method: 'POST',
          credentials: 'same-origin',
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        if (typeof Toast !== 'undefined' && Toast.success) {
          Toast.success('Session Extended', 'Your session has been extended.');
        }
      } catch (e) {
        console.error('Failed to extend session:', e);
        if (typeof Toast !== 'undefined' && Toast.warning) {
          Toast.warning(
            'Could Not Extend Session',
            'Your session could not be renewed — save your work and log in again soon.'
          );
        }
      }
    }
  },

  /**
   * Dismiss warning modal
   */
  dismiss() {
    const modal = document.getElementById('session-timeout-modal');
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
    }

    SessionTimeout.modalOpen = false;
    SessionTimeout.stopCountdown();
  },

  /**
   * Logout immediately
   */
  logout() {
    SessionTimeout.sessionExpired = true;
    SessionTimeout.dismiss();

    // Clear session data
    // Issue #787: Clear all user-specific localStorage to prevent session bleed
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('sessionId');
      localStorage.removeItem('piper_chat_session_id');
      localStorage.removeItem('piper_chat_history');
      localStorage.removeItem('piper_active_conversation_id');
    }

    // Redirect to login/logout page
    window.location.href = SessionTimeout.logoutUrl;
  },

  /**
   * Auto-logout when time expires
   */
  autoLogout() {
    const modal = document.getElementById('session-timeout-modal');
    if (modal) {
      // Update message
      const title = modal.querySelector('.session-timeout-title');
      if (title) {
        title.textContent = 'Your Session Has Expired';
      }

      const message = modal.querySelector('.session-timeout-message');
      if (message) {
        message.innerHTML =
          'Your session has expired for security. Please log in again to continue.';
      }

      // Hide action buttons
      const actions = modal.querySelector('.session-timeout-actions');
      if (actions) {
        actions.style.display = 'none';
      }

      // Show modal
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
    }

    // Redirect after 5 seconds
    setTimeout(() => {
      SessionTimeout.logout();
    }, 5000);
  },
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => SessionTimeout.init());
} else {
  SessionTimeout.init();
}
