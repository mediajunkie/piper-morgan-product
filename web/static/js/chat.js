// Chat Widget - Modular chat functionality
(function() {
  'use strict';

  const API_BASE_URL = window.API_BASE_URL || "";
  const chatWindow = document.getElementById("chat-window");
  let sessionId = null;

  // Issue #924: Chat avatar support
  const AVATAR_COLORS = [
    '#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#1abc9c',
    '#3498db', '#9b59b6', '#e91e63', '#00bcd4', '#ff5722'
  ];

  /**
   * Get a deterministic color from a username string.
   * Same username always gets the same color across sessions.
   */
  function getAvatarColor(name) {
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
  }

  /**
   * Create an avatar element for a chat message.
   * @param {boolean} isUser - Whether this is a user avatar
   * @returns {HTMLElement} Avatar element
   */
  function createAvatar(isUser) {
    const avatar = document.createElement('div');
    avatar.className = 'chat-avatar';

    if (isUser) {
      avatar.classList.add('user-avatar');
      const username = (window.currentUser && window.currentUser.username) || '?';
      const initial = username.charAt(0).toUpperCase();
      avatar.textContent = initial;
      avatar.style.backgroundColor = getAvatarColor(username);
      avatar.setAttribute('aria-label', username);
    } else {
      avatar.classList.add('piper-avatar');
      const img = document.createElement('img');
      img.src = '/assets/piper-avatar.svg';
      img.alt = 'Piper';
      img.width = 32;
      img.height = 32;
      avatar.appendChild(img);
    }

    return avatar;
  }

  // Storage keys for session persistence
  const STORAGE_KEYS = {
    SESSION_ID: 'piper_chat_session_id',
    CHAT_HISTORY: 'piper_chat_history',
    WIDGET_STATE: 'piper_chat_widget_expanded',
    // #1520: drafted message preserved across the expiry → re-login round trip
    DRAFT_MESSAGE: 'piper_chat_draft'
  };

  // Check if localStorage is available (graceful degradation for private browsing)
  let storageAvailable = false;
  try {
    const testKey = '__storage_test__';
    localStorage.setItem(testKey, testKey);
    localStorage.removeItem(testKey);
    storageAvailable = true;
  } catch (e) {
    console.warn('localStorage not available, session persistence disabled');
  }

  /**
   * Toggle chat widget expanded/collapsed state
   * Updates widget container class and manages focus/icon
   * Persists state to localStorage for cross-page consistency
   */
  function toggleChatWidget() {
    const container = document.querySelector('.chat-widget-container');
    if (container) {
      container.classList.toggle('expanded');
      const isExpanded = container.classList.contains('expanded');

      // Persist expanded state
      if (storageAvailable) {
        try {
          localStorage.setItem(STORAGE_KEYS.WIDGET_STATE, isExpanded ? 'true' : 'false');
        } catch (e) {
          // Ignore storage errors
        }
      }

      // Update toggle button icon when expanded
      const toggle = container.querySelector('.chat-widget-toggle');
      if (toggle) {
        toggle.innerHTML = isExpanded ? '✕' : '💬';
      }

      // Focus input when expanded for better UX
      if (isExpanded) {
        const input = container.querySelector('.chat-input');
        if (input) {
          // Use setTimeout to ensure focus after DOM update
          setTimeout(() => input.focus(), 50);
        }
      }
    }
  }

  // Make toggle globally available for onclick handlers
  window.toggleChatWidget = toggleChatWidget;

  /**
   * Generate a fallback session ID for browsers without crypto API
   */
  function generateSessionId() {
    return 'session-' + Math.random().toString(36).substr(2, 9) +
           '-' + Date.now().toString(36);
  }

  /**
   * Get or create a persistent session ID
   * Stored in localStorage for cross-page persistence
   */
  function getOrCreateSessionId() {
    if (storageAvailable) {
      try {
        const storedId = localStorage.getItem(STORAGE_KEYS.SESSION_ID);
        if (storedId) {
          return storedId;
        }
      } catch (e) {
        // Ignore storage errors
      }
    }

    // Create new session ID
    const newId = crypto.randomUUID ? crypto.randomUUID() : generateSessionId();

    // Persist if possible
    if (storageAvailable) {
      try {
        localStorage.setItem(STORAGE_KEYS.SESSION_ID, newId);
      } catch (e) {
        // Ignore storage errors
      }
    }

    return newId;
  }

  // Initialize session ID (persisted across pages)
  sessionId = getOrCreateSessionId();

  /**
   * Save chat history to localStorage
   * @param {Array} history - Array of message objects
   */
  function saveChatHistory(history) {
    if (!storageAvailable) return;
    try {
      // Limit history to last 50 messages to avoid quota issues
      const trimmedHistory = history.slice(-50);
      localStorage.setItem(STORAGE_KEYS.CHAT_HISTORY, JSON.stringify(trimmedHistory));
    } catch (e) {
      console.warn('Failed to save chat history:', e);
    }
  }

  /**
   * Load chat history from localStorage
   * @returns {Array} Array of message objects or empty array
   */
  function loadChatHistory() {
    if (!storageAvailable) return [];
    try {
      const stored = localStorage.getItem(STORAGE_KEYS.CHAT_HISTORY);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.warn('Failed to load chat history:', e);
      return [];
    }
  }

  /**
   * Clear chat history from localStorage
   */
  function clearChatHistory() {
    if (!storageAvailable) return;
    try {
      localStorage.removeItem(STORAGE_KEYS.CHAT_HISTORY);
    } catch (e) {
      // Ignore
    }
  }

  // Track messages for persistence
  let chatHistory = loadChatHistory();

  // Track last message timestamp for divider logic (Issue #564)
  let lastMessageTimestamp = null;

  /**
   * Append a message to the chat window
   * @param {string} html - The HTML content of the message
   * @param {boolean} isUser - Whether this is a user message
   * @param {boolean} persist - Whether to save to history (default true)
   * @param {number|string|null} timestamp - Message timestamp (default: now)
   * @returns {HTMLElement} The message element
   */
  function appendMessage(html, isUser = false, persist = true, timestamp = null) {
    // Determine timestamp to use (Issue #564)
    const msgTimestamp = timestamp || Date.now();

    // Check if we need date or session dividers (Issue #564)
    if (lastMessageTimestamp && typeof TimestampUtils !== 'undefined') {
      // Date divider takes precedence
      if (TimestampUtils.isDifferentDay(lastMessageTimestamp, msgTimestamp)) {
        const divider = document.createElement('div');
        divider.className = 'chat-date-divider';
        divider.innerHTML = `<span>${TimestampUtils.formatDateDivider(msgTimestamp)}</span>`;
        chatWindow.appendChild(divider);
      }
      // Session divider for same-day gaps > 8 hours
      else if (TimestampUtils.isSessionGap(lastMessageTimestamp, msgTimestamp)) {
        const divider = document.createElement('div');
        divider.className = 'chat-date-divider chat-session-divider';
        divider.innerHTML = '<span>Earlier today</span>';
        chatWindow.appendChild(divider);
      }
    }

    const msgContainer = document.createElement("div");
    msgContainer.className = "message-container";
    msgContainer.dataset.timestamp = msgTimestamp;

    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;

    // If it's a user message, use textContent; if bot message, use renderBotMessage for markdown
    // Issue #592: Use DDD domain service for consistent markdown rendering
    if (isUser) {
      msgDiv.textContent = html;
    } else {
      // Use renderBotMessage() from bot-message-renderer.js for consistent markdown parsing
      if (typeof renderBotMessage !== 'undefined') {
        msgDiv.innerHTML = renderBotMessage(html, 'success', false);
      } else {
        // Fallback if bot-message-renderer.js not loaded
        msgDiv.innerHTML = typeof marked !== 'undefined' ? marked.parse(html) : html;
      }
    }

    // Issue #924: Wrap message in a row with avatar
    const msgRow = document.createElement('div');
    msgRow.className = `message-row ${isUser ? 'user-row' : 'bot-row'}`;
    msgRow.appendChild(createAvatar(isUser));
    msgRow.appendChild(msgDiv);
    msgContainer.appendChild(msgRow);

    // Add hover timestamp tooltip (Issue #564)
    if (typeof TimestampUtils !== 'undefined') {
      const tooltip = document.createElement('div');
      tooltip.className = 'message-timestamp-tooltip';
      tooltip.textContent = TimestampUtils.formatHoverTime(msgTimestamp);
      msgContainer.appendChild(tooltip);

      // Add staleness indicator for messages > 7 days old (Issue #564)
      if (TimestampUtils.isStale(msgTimestamp)) {
        const staleDate = document.createElement('div');
        staleDate.className = 'message-stale-date';
        staleDate.textContent = TimestampUtils.formatHoverTime(msgTimestamp);
        msgContainer.appendChild(staleDate);
      }
    }

    chatWindow.appendChild(msgContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Update last message timestamp for divider logic
    lastMessageTimestamp = msgTimestamp;

    // Save to history for persistence (skip temporary messages like "Thinking..." or "Starting workflow...")
    if (persist && html && !html.includes('Thinking...') && !html.includes('Starting workflow...')) {
      chatHistory.push({ content: html, isUser, timestamp: msgTimestamp });
      saveChatHistory(chatHistory);
    }

    return msgDiv;
  }

  /**
   * #355: Add a "Save as artifact" button to a long assistant reply.
   * Persists the raw reply as a generated Artifact (POST /api/v1/artifacts),
   * which then appears in the /files browser. Gated to replies > 500 chars
   * (per #355) so short answers aren't cluttered.
   */
  function addSaveArtifactButton(botDiv, content) {
    if (!botDiv || !content || content.length <= 500) return;
    const btn = document.createElement('button');
    btn.className = 'save-artifact-btn';
    btn.type = 'button';
    btn.textContent = '💾 Save as artifact';
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      btn.textContent = 'Saving…';
      try {
        const resp = await fetch(`${API_BASE_URL}/api/v1/artifacts`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: content, source_conversation_id: sessionId }),
          credentials: 'include',
        });
        if (!resp.ok) throw new Error(`save failed (${resp.status})`);
        await resp.json();
        btn.textContent = '✓ Saved to your files';
        btn.classList.add('saved');
        if (typeof ToastMessages !== 'undefined') {
          ToastMessages.success('file_saved');
        }
      } catch (e) {
        console.error('Save artifact error:', e);
        btn.disabled = false;
        btn.textContent = '💾 Save as artifact';
        if (typeof ToastMessages !== 'undefined') {
          ToastMessages.error('save_error');
        }
        // #1170: dropped the native alert fallback — the toast + console.error above cover it
      }
    });
    botDiv.appendChild(btn);
  }

  /**
   * Restore chat history from localStorage
   * Called on initialization to restore previous conversation
   */
  function restoreChatHistory() {
    if (!chatWindow) return;
    const history = loadChatHistory();
    if (history.length === 0) return;

    // Clear any existing default messages
    chatWindow.innerHTML = '';

    // Reset last message timestamp for proper divider calculation (Issue #564)
    lastMessageTimestamp = null;

    // Restore each message with its original timestamp (Issue #564)
    history.forEach(msg => {
      appendMessage(msg.content, msg.isUser, false, msg.timestamp); // false = don't re-persist
    });
  }

  /**
   * Set an example from the examples list into the chat input
   * @param {HTMLElement} element - The example element clicked
   */
  function setExample(element) {
    const input = document.querySelector(".chat-input");
    if (input) {
      input.value = element.textContent.trim();
    }
  }

  /**
   * Poll workflow status until completion or timeout
   * @param {string} workflowId - The workflow ID to poll
   * @param {HTMLElement} elementToUpdate - The element to update with status
   */
  async function pollWorkflowStatus(workflowId, elementToUpdate) {
    let pollCount = 0;
    const maxPolls = 30; // Stop after 60 seconds (2s intervals)

    const intervalId = setInterval(async () => {
      pollCount++;

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/v1/workflows/${workflowId}`,
          { credentials: "include" }
        );

        if (!response.ok) {
          // If 404 and we've seen success before, assume it completed
          if (
            response.status === 404 &&
            elementToUpdate.textContent.includes("completed")
          ) {
            clearInterval(intervalId);
            return; // Keep the success message
          }

          // Otherwise show error and stop
          elementToUpdate.innerHTML = `<div class="result error">Error checking status.</div>`;
          clearInterval(intervalId);
          return;
        }

        const data = await response.json();
        // Use DDD handler for workflow responses
        if (data.status === "completed") {
          elementToUpdate.classList.remove("thinking");
          elementToUpdate.classList.add("reply");
          handleWorkflowResponse(data, elementToUpdate);
          clearInterval(intervalId);
        } else if (data.status === "failed") {
          elementToUpdate.classList.remove("thinking");
          elementToUpdate.classList.add("error");
          elementToUpdate.innerHTML = renderBotMessage(
            `Workflow Failed: ${data.message}`,
            "error",
            false
          );
          clearInterval(intervalId);
        }

        // Stop polling after max attempts
        if (pollCount >= maxPolls) {
          clearInterval(intervalId);
          elementToUpdate.innerHTML = `<div class="result error">Workflow status check timed out.</div>`;
        }
      } catch (error) {
        console.error("Polling error:", error);
        elementToUpdate.innerHTML = `<div class="result error">Could not connect to API to check status.</div>`;
        clearInterval(intervalId);
      }
    }, 2000); // Poll every 2 seconds
  }

  /**
   * Handle direct response from the API
   * Uses the bot message renderer if available
   */
  function handleDirectResponse(result, element) {
    if (typeof renderBotMessage === 'function') {
      // Use DDD bot message renderer if available
      // Issue #588: Use "success" type to ensure markdown is parsed (renderBotMessage only parses for "success")
      const html = renderBotMessage(result.message || result.reply || "", "success", false);
      element.innerHTML = html;
    } else {
      // Fallback: render markdown manually
      if (typeof marked !== 'undefined') {
        element.innerHTML = marked.parse(result.message || result.reply || "");
      } else {
        element.textContent = result.message || result.reply || "";
      }
    }
  }

  /**
   * Handle error response from the API
   */
  function handleErrorResponse(error, element) {
    const errorMsg = error.message || "An unknown error occurred";
    element.innerHTML = `<div class="result error">${errorMsg}</div>`;
    element.classList.add("error");
  }

  /**
   * Restore widget expanded state from localStorage
   */
  function restoreWidgetState() {
    if (!storageAvailable) return;
    try {
      const wasExpanded = localStorage.getItem(STORAGE_KEYS.WIDGET_STATE);
      if (wasExpanded === 'true') {
        const container = document.querySelector('.chat-widget-container');
        if (container) {
          container.classList.add('expanded');
          const toggle = container.querySelector('.chat-widget-toggle');
          if (toggle) {
            toggle.innerHTML = '✕';
          }
        }
      }
    } catch (e) {
      // Ignore
    }
  }

  /**
   * #1520: Attempt a silent access-token refresh via the #857 endpoint.
   * Returns true when the session was renewed (httponly cookies rotated
   * server-side — nothing to store client-side).
   */
  async function tryRefreshSession() {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });
      return res.ok;
    } catch (e) {
      return false;
    }
  }

  /**
   * #1520: Make session expiry VISIBLE and preserve the drafted message.
   * Called only after a silent refresh attempt has failed — the session is
   * genuinely over. Honest copy: the session expired; sign in again. Never
   * blames a missing API key (that copy belongs to anonymous callers only).
   */
  function handleSessionExpired(message, form) {
    // Preserve the draft: back into the input, and stashed for after re-login.
    const input = form && form.querySelector(".chat-input");
    if (input && !input.value) {
      input.value = message;
    }
    if (storageAvailable && message) {
      try {
        localStorage.setItem(STORAGE_KEYS.DRAFT_MESSAGE, message);
      } catch (e) {
        // Storage full/unavailable — the input restore above still holds it.
      }
    }

    // Visible, honest notice in the chat window.
    const notice = appendMessage(
      "Your session has expired, so that message wasn't processed. " +
        "Redirecting you to sign in again — your message is saved and " +
        "will be restored.",
      false
    );
    notice.classList.add("error");

    // Reuse the session-timeout modal's expired state when available.
    if (typeof SessionTimeout !== "undefined" && SessionTimeout.autoLogout) {
      SessionTimeout.autoLogout();
    } else {
      setTimeout(() => {
        // #1480: carry the current page through the re-login round trip so
        // login lands back here (auth.js reads + guards the next param).
        window.location.href = "/login?next=" + encodeURIComponent(loginReturnTarget());
      }, 3000);
    }
  }

  /**
   * #1480: where re-login should land — the full current location including
   * query and fragment. The fragment survives because auth.js's redirect is
   * client-side; the open-redirect guard lives at the consuming end
   * (sanitize_next_path server-side, safeNextUrl in auth.js).
   */
  function loginReturnTarget() {
    return window.location.pathname + window.location.search + window.location.hash;
  }

  /**
   * #1520: Restore a draft preserved across the expiry → re-login round trip.
   */
  function restoreDraftMessage(form) {
    if (!storageAvailable) return;
    try {
      const draft = localStorage.getItem(STORAGE_KEYS.DRAFT_MESSAGE);
      if (draft) {
        const input = form.querySelector(".chat-input");
        if (input && !input.value) {
          input.value = draft;
        }
        localStorage.removeItem(STORAGE_KEYS.DRAFT_MESSAGE);
      }
    } catch (e) {
      // Ignore — draft restore is best-effort.
    }
  }

  /**
   * Initialize the chat widget
   */
  function initChat() {
    const form = document.getElementById("chatForm");
    if (!form) return; // Chat form not found, widget not initialized

    // Restore previous state
    restoreChatHistory();
    restoreWidgetState();
    restoreDraftMessage(form); // #1520: draft preserved across re-login

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = form.querySelector(".chat-input");
      const message = input.value.trim();
      if (!message) return;

      appendMessage(message, true);
      input.value = "";

      // Show a temporary 'thinking' message
      const thinkingDiv = appendMessage("Thinking...");
      thinkingDiv.classList.add("thinking");

      try {
        // First, try to process as a permission intent
        if (typeof processPermissionIntent === 'function') {
          const permissionResult = await processPermissionIntent(message);
          if (permissionResult) {
            // Permission intent was handled
            if (permissionResult.success) {
              const botDiv = appendMessage(permissionResult.message, false);
              botDiv.classList.add("reply");
            } else {
              const errorDiv = appendMessage(permissionResult.message, false);
              errorDiv.classList.add("error");
            }
            // Remove entire message-container (avatar + row), not just the inner .message div
            const thinkingContainer1 = thinkingDiv.closest('.message-container');
            if (thinkingContainer1) thinkingContainer1.remove(); else thinkingDiv.remove();
            return;
          }
        }

        // Not a permission intent, send to conversational AI
        const sendIntent = () =>
          fetch(`${API_BASE_URL}/api/v1/intent`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              message: message,
              session_id: sessionId,
            }),
            credentials: "include",
          });

        let response = await sendIntent();
        let result = await response.json();

        // #1520: expired session — try ONE silent refresh (#857) and resend
        // before surfacing anything. Active users should never notice expiry.
        if (result && result.error_type === "session_expired") {
          if (await tryRefreshSession()) {
            response = await sendIntent();
            result = await response.json();
          }
        }

        if (result && result.error_type === "session_expired") {
          // Refresh failed — the session is genuinely over. Visible + honest,
          // draft preserved (#1520).
          const thinkingContainer0 = thinkingDiv.closest('.message-container');
          if (thinkingContainer0) thinkingContainer0.remove(); else thinkingDiv.remove();
          handleSessionExpired(message, form);
          return;
        }

        if (!response.ok) {
          throw new Error(result.detail || "An API error occurred");
        }

        // Replace the 'thinking' message with a new bot message (with 'reply' class)
        const botDiv = appendMessage("", false);
        botDiv.classList.add("reply");
        handleDirectResponse(result, botDiv);
        // #355: offer to save long replies as an artifact (raw markdown content).
        addSaveArtifactButton(botDiv, result.message || result.reply || "");
        // Remove the old thinking message (entire container including avatar)
        const thinkingContainer2 = thinkingDiv.closest('.message-container');
        if (thinkingContainer2) thinkingContainer2.remove(); else thinkingDiv.remove();

        // Issue #248/#375: Render preference suggestions if detected
        if (result.preferences && typeof renderPreferenceSuggestions === 'function') {
          renderPreferenceSuggestions(result.preferences, botDiv);
        }

        // Issue #676: Only show workflow status when valid workflow_id exists
        // Check for non-empty string to avoid spurious "Starting workflow..." messages
        // Issue #875: Don't poll if the response contains an error (workflow never started)
        // Issue #878: Don't poll for clarification/validation responses (no async work started)
        if (result.workflow_id && result.workflow_id.trim() !== '' && !result.error && !result.requires_clarification) {
          // If a workflow was started, create a new message bubble to poll for its status
          const statusDiv = appendMessage("Starting workflow...");
          statusDiv.classList.add("thinking");
          pollWorkflowStatus(result.workflow_id, statusDiv);
        }

        if (result.session_id) {
          sessionId = result.session_id;
        }

        // Issue #787: Refresh sidebar when a new conversation is auto-created
        // (data-only since #1522 step 1 — kept for home's auto-select state)
        if (result.conversation_created && typeof loadConversations === 'function') {
          loadConversations();
        }

        // #1477: announce the exchange so the left rail (nav.js) refreshes —
        // the current conversation gets its row from the FIRST turn, not the
        // next full page load. The #787 hook above renders nothing since
        // #1522 step 1; this event is what refreshes the visible surface.
        document.dispatchEvent(new CustomEvent('piper:conversation-updated', {
          detail: { conversationId: sessionId, created: !!result.conversation_created }
        }));

        // Issue #840: Detect expired auth token and redirect to login
        if (result.auth_expired) {
          const warningDiv = appendMessage(
            "Your session has expired. Redirecting to login so you can continue with full features...",
            false
          );
          warningDiv.classList.add("reply");
          setTimeout(() => {
            // #1480: carry the current page as next (see loginReturnTarget).
            window.location.href = "/login?next=" + encodeURIComponent(loginReturnTarget());
          }, 2000);
        }
      } catch (error) {
        // Replace the 'thinking' message with a new error message (with 'error' class)
        const errorDiv = appendMessage("", false);
        errorDiv.classList.add("error");
        handleErrorResponse(error, errorDiv);
        // Remove the old thinking message (entire container including avatar)
        const thinkingContainer3 = thinkingDiv.closest('.message-container');
        if (thinkingContainer3) thinkingContainer3.remove(); else thinkingDiv.remove();
      }
    });
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChat);
  } else {
    initChat();
  }

  // Export for testing if needed
  window.ChatWidget = {
    appendMessage,
    setExample,
    pollWorkflowStatus,
    handleDirectResponse,
    handleErrorResponse,
    clearHistory: clearChatHistory,
    getSessionId: () => sessionId,
    setSessionId: (id) => {
      // Issue #581: Allow sidebar to sync conversation selection to chat
      sessionId = id;
      // Persist to localStorage for refresh/bookmark scenarios
      if (storageAvailable && id) {
        localStorage.setItem(STORAGE_KEYS.SESSION_ID, id);
      }
    },
    init: initChat
  };
})();
