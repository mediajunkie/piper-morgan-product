// G53: Centralized Toast Messages
// Issue #642: CONSCIOUSNESS-TRANSFORM: Toast centralization
// Voice: Neutral for toasts - confirm without demanding attention
// First-person feels like interrupting to take credit

/**
 * Toast message constants - centralized for consistency
 * Pattern: { title: string, body: string }
 *
 * Guidelines (CXO/PPM):
 * - Neutral for success: "Saved" not "I've saved that for you!"
 * - Error recovery should guide next steps
 * - Don't demand attention for routine confirmations
 */
const TOAST_MESSAGES = {
  // CRUD operations - generic
  created: { title: 'Created', body: '' },
  saved: { title: 'Saved', body: '' },
  updated: { title: 'Updated', body: '' },
  deleted: { title: 'Removed', body: '' },

  // Todo operations
  todo_created: { title: 'Got it', body: 'Todo added' },
  todo_updated: { title: 'Updated', body: 'Todo saved' },
  todo_completed: { title: 'Done', body: 'Todo completed' },  // #1541 complete control
  todo_deleted: { title: 'Done', body: 'Todo removed' },

  // List operations
  list_created: { title: 'Created', body: 'List ready' },
  list_updated: { title: 'Updated', body: 'List saved' },
  list_deleted: { title: 'Done', body: 'List removed' },
  item_added: { title: 'Added', body: 'Item added to list' },
  item_updated: { title: 'Updated', body: 'Item saved' },
  item_deleted: { title: 'Done', body: 'Item removed' },

  // Project operations
  project_created: { title: 'Created', body: 'Project ready' },
  project_updated: { title: 'Updated', body: 'Project saved' },
  project_deleted: { title: 'Done', body: 'Project removed' },

  // Work item operations
  work_item_created: { title: 'Created', body: 'Work item added' },
  work_item_updated: { title: 'Updated', body: 'Work item saved' },
  work_item_deleted: { title: 'Done', body: 'Work item removed' },

  // File operations
  file_uploaded: { title: 'Uploaded', body: 'File ready' },
  file_deleted: { title: 'Done', body: 'File removed' },
  file_saved: { title: 'Saved', body: 'Added to your files' },  // #355 save-as-artifact
  file_renamed: { title: 'Renamed', body: 'New name saved' },  // #1184 artifact rename

  // Sharing
  shared: { title: 'Shared', body: '' },
  share_removed: { title: 'Done', body: 'Share removed' },

  // Settings
  settings_saved: { title: 'Saved', body: 'Settings updated' },
  preferences_saved: { title: 'Saved', body: 'Preferences updated' },
  preferences_reset: { title: 'Reset', body: 'Using default settings' },

  // Session
  session_extended: { title: 'Extended', body: 'Session continues' },
  session_expired: { title: 'Session ended', body: 'Please log in again' },

  // Standup
  standup_ready: { title: 'Ready', body: 'Your standup is ready' },

  // Coming soon
  coming_soon: { title: 'Coming soon', body: '' },

  // Errors - with recovery guidance
  load_error: { title: 'Couldn\'t load', body: 'Try refreshing the page' },
  create_error: { title: 'Couldn\'t create', body: 'Please try again' },
  update_error: { title: 'Couldn\'t save', body: 'Please try again' },
  delete_error: { title: 'Couldn\'t remove', body: 'Please try again' },
  archive_error: { title: 'Couldn\'t archive', body: 'Please try again' },  // #1170 home conversation archive
  upload_error: { title: 'Couldn\'t upload', body: 'Check file size and try again' },
  save_error: { title: 'Couldn\'t save', body: 'Please try again' },  // #355 save-as-artifact
  download_error: { title: 'Couldn\'t download', body: 'Please try again' },
  share_error: { title: 'Couldn\'t share', body: 'Please try again' },
  validation_error: { title: 'Missing info', body: '' },

  // Network errors
  server_error: { title: 'Server error', body: 'Please try again later' },
  network_error: { title: 'Connection lost', body: 'Check your internet connection' },
  timeout_error: { title: 'Took too long', body: 'Please try again' },
  offline: { title: 'You\'re offline', body: 'Check your internet connection' },

  // Auth errors
  access_denied: { title: 'Access denied', body: 'You don\'t have permission' },
  not_found: { title: 'Not found', body: 'This may have been moved or deleted' },

  // Connection
  connection_restored: { title: 'Back online', body: '' },
  connection_failed: { title: 'Can\'t connect', body: 'Check your connection' },

  // Version check
  version_check_failed: { title: 'Version unknown', body: 'Couldn\'t check for updates' },
};

/**
 * Get a toast message by key
 * @param {string} key - Message key from TOAST_MESSAGES
 * @param {Object} overrides - Optional overrides for title/body
 * @returns {{ title: string, body: string }}
 */
function getToastMessage(key, overrides = {}) {
  const msg = TOAST_MESSAGES[key] || { title: key, body: '' };
  return {
    title: overrides.title || msg.title,
    body: overrides.body !== undefined ? overrides.body : msg.body,
  };
}

/**
 * Show toast using centralized message
 * @param {string} type - 'success', 'error', 'warning', 'info'
 * @param {string} key - Message key from TOAST_MESSAGES
 * @param {Object} overrides - Optional overrides for title/body
 */
function showToastMessage(type, key, overrides = {}) {
  const msg = getToastMessage(key, overrides);
  if (typeof Toast !== 'undefined' && Toast[type]) {
    Toast[type](msg.title, msg.body);
  }
}

// Convenience functions
const ToastMessages = {
  success: (key, overrides) => showToastMessage('success', key, overrides),
  error: (key, overrides) => showToastMessage('error', key, overrides),
  warning: (key, overrides) => showToastMessage('warning', key, overrides),
  info: (key, overrides) => showToastMessage('info', key, overrides),

  // Get raw message for custom usage
  get: getToastMessage,

  // All messages (for reference)
  MESSAGES: TOAST_MESSAGES,
};
