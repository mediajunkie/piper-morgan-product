/* #1280 — shared nav behavior, extracted from components/navigation.html so BOTH the top nav
   (legacy) and the left dark-rail (components/nav_rail.html) can use one source. Adapted for the
   rail: the ⌘K keydown is lifted out of the search-button guard (the rail has no button), and a
   conversation-list loader populates #nav-rail-chats when the rail is present. */
document.addEventListener('DOMContentLoaded', function() {
  // Trust-gated visibility (#420)
  // Get trust_stage from window (set by template from #419)
  const trustStage = window.trustStage || 1;

  // Show/hide nav items based on trust stage
  const trustGatedItems = document.querySelectorAll('.nav-item-trust-gated');
  trustGatedItems.forEach(item => {
    const minStage = parseInt(item.dataset.minTrustStage || '1', 10);
    if (trustStage >= minStage) {
      item.classList.add('trust-visible');
    } else {
      item.classList.remove('trust-visible');
    }
  });

  // Search trigger - opens command palette (#421)
  const searchTrigger = document.getElementById('nav-search-trigger');
  if (searchTrigger) {
    searchTrigger.addEventListener('click', function() {
      // Dispatch custom event for command palette to listen to
      const event = new CustomEvent('openCommandPalette');
      document.dispatchEvent(event);
      // Fallback: if no palette exists yet, show placeholder
      if (!window.commandPaletteExists) {
        console.log('Command palette not yet implemented - see #421');
      }
    });
  }

  // Keyboard shortcut: Cmd/Ctrl+K — registered UNCONDITIONALLY (#1280: the left rail has no
  // search button, so ⌘K must not depend on #nav-search-trigger existing).
  document.addEventListener('keydown', function(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      const event = new CustomEvent('openCommandPalette');
      document.dispatchEvent(event);
      if (!window.commandPaletteExists) {
        console.log('Command palette not yet implemented - see #421');
      }
    }
  });

  // History trigger (#425)
  const historyTrigger = document.getElementById('nav-history-trigger');
  if (historyTrigger) {
    historyTrigger.addEventListener('click', function() {
      // Open history sidebar if loaded
      if (window.HistorySidebar) {
        window.HistorySidebar.toggle();
      } else {
        console.log('History sidebar not yet loaded - see #425');
      }
    });

    // Keyboard shortcut: Cmd/Ctrl+H for history
    document.addEventListener('keydown', function(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'h' && !e.shiftKey) {
        e.preventDefault();
        if (window.HistorySidebar) {
          window.HistorySidebar.toggle();
        }
      }
    });
  }

  // Get user info if available in context (will be passed from server)
  const userButton = document.getElementById('user-menu-button');
  const userDropdown = document.getElementById('user-dropdown');
  const userAvatar = document.getElementById('user-avatar');
  const userName = document.getElementById('user-name');

  // Handle hamburger menu for mobile
  const hamburgerButton = document.getElementById('hamburger-button');
  const navMenu = document.getElementById('nav-menu');

  if (hamburgerButton && navMenu) {
    hamburgerButton.addEventListener('click', function(e) {
      e.stopPropagation();
      const isExpanded = hamburgerButton.getAttribute('aria-expanded') === 'true';
      hamburgerButton.setAttribute('aria-expanded', !isExpanded);
      navMenu.classList.toggle('active');
    });

    // Close menu when clicking on a nav link
    const navLinkElements = navMenu.querySelectorAll('.nav-link');
    navLinkElements.forEach(link => {
      link.addEventListener('click', function() {
        hamburgerButton.setAttribute('aria-expanded', 'false');
        navMenu.classList.remove('active');
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!hamburgerButton.contains(e.target) && !navMenu.contains(e.target)) {
        hamburgerButton.setAttribute('aria-expanded', 'false');
        navMenu.classList.remove('active');
      }
    });
  }

  // Handle Stuff dropdown
  const stuffButton = document.getElementById('stuff-dropdown-button');
  const stuffMenu = document.getElementById('stuff-dropdown-menu');

  if (stuffButton && stuffMenu) {
    stuffButton.addEventListener('click', function(e) {
      e.stopPropagation();
      const isExpanded = stuffButton.getAttribute('aria-expanded') === 'true';
      stuffButton.setAttribute('aria-expanded', !isExpanded);
      stuffMenu.hidden = isExpanded;
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!stuffButton.contains(e.target) && !stuffMenu.contains(e.target)) {
        stuffButton.setAttribute('aria-expanded', 'false');
        stuffMenu.hidden = true;
      }
    });

    // Close on escape key
    stuffButton.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        stuffButton.setAttribute('aria-expanded', 'false');
        stuffMenu.hidden = true;
      }
    });

    // Arrow key navigation in Stuff dropdown
    const stuffItems = stuffMenu.querySelectorAll('.nav-dropdown-item');
    let stuffFocus = -1;

    stuffButton.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        stuffButton.setAttribute('aria-expanded', 'true');
        stuffMenu.hidden = false;
        stuffFocus = 0;
        if (stuffItems[stuffFocus]) {
          stuffItems[stuffFocus].focus();
        }
      }
    });

    stuffItems.forEach((item, index) => {
      item.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          stuffFocus = (index + 1) % stuffItems.length;
          stuffItems[stuffFocus].focus();
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          stuffFocus = (index - 1 + stuffItems.length) % stuffItems.length;
          stuffItems[stuffFocus].focus();
        } else if (e.key === 'Escape') {
          stuffButton.setAttribute('aria-expanded', 'false');
          stuffMenu.hidden = true;
          stuffButton.focus();
        }
      });
    });
  }

  // Set active nav link based on current path
  const currentPath = window.location.pathname;
  const navLinks = {
    '/standup': 'nav-standup',  // "Check in"
    '/learning': 'nav-learning'
  };

  // Your stuff dropdown items (renamed from "My Work")
  const stuffLinks = {
    '/todos': 'nav-todos',      // "To-dos"
    '/projects': 'nav-projects', // "Projects"
    '/work-items': 'nav-work-items', // "Work Items" (#710)
    '/files': 'nav-files',       // "Documents"
    '/lists': 'nav-lists'        // "Collections"
  };

  for (const [path, id] of Object.entries(navLinks)) {
    const link = document.getElementById(id);
    if (link) {
      if (currentPath === path) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      } else {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
      }
    }
  }

  // Handle Stuff dropdown item active states
  for (const [path, id] of Object.entries(stuffLinks)) {
    const link = document.getElementById(id);
    if (link) {
      if (currentPath === path) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
        // Also highlight the Stuff button when a sub-item is active
        if (stuffButton) {
          stuffButton.style.color = 'var(--color-primary-decorative)';
        }
      } else {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
      }
    }
  }

  // Handle user dropdown menu
  if (userButton && userDropdown) {
    userButton.addEventListener('click', function(e) {
      e.stopPropagation();
      const isExpanded = userButton.getAttribute('aria-expanded') === 'true';
      userButton.setAttribute('aria-expanded', !isExpanded);
      userDropdown.hidden = isExpanded;
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
      userButton.setAttribute('aria-expanded', 'false');
      userDropdown.hidden = true;
    });

    // Keyboard support
    userButton.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        userButton.setAttribute('aria-expanded', 'false');
        userDropdown.hidden = true;
      }
    });

    // Arrow key navigation in dropdown
    const dropdownItems = userDropdown.querySelectorAll('.dropdown-item');
    let currentFocus = -1;

    userButton.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        currentFocus = 0;
        if (dropdownItems[currentFocus]) {
          dropdownItems[currentFocus].focus();
        }
      }
    });

    dropdownItems.forEach((item, index) => {
      item.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          currentFocus = (index + 1) % dropdownItems.length;
          dropdownItems[currentFocus].focus();
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          currentFocus = (index - 1 + dropdownItems.length) % dropdownItems.length;
          dropdownItems[currentFocus].focus();
        }
      });
    });
  }

  // Try to get user info from server context (if available)
  // This would be set by the server in a script tag
  if (window.currentUser) {
    if (window.currentUser.username) {
      userName.textContent = window.currentUser.username;
      const firstLetter = window.currentUser.username.charAt(0).toUpperCase();
      userAvatar.textContent = firstLetter;
    }
  }

  // #1280 — populate the left rail's conversation list (Slack-style, on every page). Runs only when
  // the rail is present (#nav-rail-chats). Clicking opens the conversation on home via
  // /?conversation=<id> (home reads that param), so it works from any page. textContent (not
  // innerHTML) keeps titles XSS-safe; failure leaves the honest "No conversations yet." placeholder.
  const railChats = document.getElementById('nav-rail-chats');
  if (railChats) {
    const activeConvId = new URLSearchParams(window.location.search).get('conversation');
    fetch('/api/v1/conversations?state=active&limit=8', { credentials: 'include' })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) {
        const convs = (data && data.conversations) ? data.conversations : [];
        if (!convs.length) return;  // keep the honest placeholder
        railChats.innerHTML = '';
        convs.forEach(function(c) {
          const a = document.createElement('a');
          a.className = 'nav-rail-chat-item';
          a.href = '/?conversation=' + encodeURIComponent(c.id);
          a.textContent = c.title || 'Untitled conversation';
          if (activeConvId && String(c.id) === String(activeConvId)) {
            a.classList.add('active');
            a.setAttribute('aria-current', 'page');
          }
          railChats.appendChild(a);
        });
      })
      .catch(function() { /* leave the placeholder; the rail's nav still works */ });
  }
});

// G8: Handle logout - POST to /api/v1/auth/logout
async function handleLogout(event) {
  event.preventDefault();

  try {
    const response = await fetch('/api/v1/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include' // Include authentication cookies
    });

    if (response.ok) {
      // Issue #787: Clear user-specific localStorage to prevent session bleed to next user
      // Must clear BEFORE redirect so new user gets fresh state
      try {
        localStorage.removeItem('piper_chat_session_id');
        localStorage.removeItem('piper_chat_history');
        localStorage.removeItem('piper_active_conversation_id');
      } catch (e) {
        // Ignore storage errors in private browsing
      }
      // Redirect to login or home page
      window.location.href = '/';
    } else {
      const data = await response.json();
      // #1170: Toast (global via base.html), not native alert
      (window.Toast ? Toast.error('Logout failed', data.detail || 'Unknown error') : console.error('Logout failed:', data.detail));
    }
  } catch (error) {
    console.error('Logout error:', error);
    // #1170: Toast (global via base.html), not native alert
    (window.Toast ? Toast.error('Logout failed', error.message) : console.error('Logout failed:', error));
  }
}
