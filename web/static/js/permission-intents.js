/**
 * Permission Intent Handlers
 * Conversational shortcuts for RBAC actions
 *
 * Handles commands like:
 * - "share my project plan with alex as editor"
 * - "who can access my todos?"
 * - "show me lists michelle shared with me"
 */

/**
 * Parse sharing commands from natural language
 * Examples:
 *   - "share my project plan with alex@example.com as editor"
 *   - "give michelle access to todos as viewer"
 *   - "let sara edit my list"
 */
function parseShareCommand(text) {
  const patterns = [
    // "share X with Y as Z" - e.g. "share my project plan with alex as editor"
    /share\s+(my\s+)?(.+?)\s+with\s+([\w@\.\-\+]+)(?:\s+as\s+(\w+))?$/i,
    // "give X access to Y as Z" - e.g. "give michelle access to todos as viewer"
    /give\s+([\w@\.\-\+]+)\s+access\s+to\s+(?:my\s+)?(.+?)(?:\s+as\s+(\w+))?$/i,
    // "let X edit/view Y" - e.g. "let sara edit my shopping list"
    /let\s+([\w@\.\-\+]+)\s+(view|edit|manage)\s+(?:my\s+)?(.+)$/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      // Extract components based on pattern match
      let resourceType, resourceName, recipientEmail, role;

      if (pattern.source.includes('with')) {
        // share X with Y as Z
        // match[1] = 'my' or undefined
        // match[2] = resource name + type (e.g. "project plan")
        // match[3] = recipient email
        // match[4] = role (optional)
        const nameAndType = match[2].trim();

        // Try to find resource type in the text
        const resourceTypeMatch = nameAndType.match(/\b(lists?|todos?|projects?)\b/i);
        if (resourceTypeMatch) {
          resourceType = resourceTypeMatch[1];
          resourceName = nameAndType.replace(new RegExp(`\\b${resourceTypeMatch[1]}\\b`, 'i'), '').trim();
        } else {
          // No recognized type, use as-is
          resourceType = nameAndType;
          resourceName = '';
        }

        recipientEmail = match[3];
        role = match[4] || 'VIEWER';
      } else if (pattern.source.includes('access')) {
        // give X access to Y as Z
        // match[1] = recipient email
        // match[2] = resource name + type (e.g. "todos")
        // match[3] = role (optional)
        recipientEmail = match[1];

        const nameAndType = match[2].trim();
        const resourceTypeMatch = nameAndType.match(/\b(lists?|todos?|projects?)\b/i);
        if (resourceTypeMatch) {
          resourceType = resourceTypeMatch[1];
          resourceName = nameAndType.replace(new RegExp(`\\b${resourceTypeMatch[1]}\\b`, 'i'), '').trim();
        } else {
          resourceType = nameAndType;
          resourceName = '';
        }

        role = match[3] || 'VIEWER';
      } else if (pattern.source.includes('let')) {
        // let X view/edit/manage Y
        // match[1] = recipient
        // match[2] = action (view/edit/manage)
        // match[3] = resource name + type
        recipientEmail = match[1];
        const action = match[2]; // 'view', 'edit', 'manage'

        const nameAndType = match[3].trim();
        const resourceTypeMatch = nameAndType.match(/\b(lists?|todos?|projects?)\b/i);
        if (resourceTypeMatch) {
          resourceType = resourceTypeMatch[1];
          resourceName = nameAndType.replace(new RegExp(`\\b${resourceTypeMatch[1]}\\b`, 'i'), '').trim();
        } else {
          resourceType = nameAndType;
          resourceName = '';
        }

        role = actionToRole(action);
      }

      return {
        intent: 'share',
        resourceType: normalizeResourceType(resourceType),
        resourceName: resourceName?.trim(),
        recipientEmail: recipientEmail?.trim(),
        role: role?.toUpperCase() || 'VIEWER'
      };
    }
  }
  return null;
}

/**
 * Parse permission query commands
 * Examples:
 *   - "who can access my project plan?"
 *   - "show me shared lists"
 *   - "what are my permissions on todos?"
 */
function parsePermissionQuery(text) {
  const patterns = [
    // "who can access X" - e.g. "who can access my project plan"
    /who\s+(?:can\s+access|has\s+access\s+to)\s+(?:my\s+)?(.+?)(?:\s*\?)?$/i,
    // "show shared X" - e.g. "show me shared lists"
    /show\s+(?:me\s+)?(?:my\s+)?shared\s+(\w+)s?$/i,
    // "what are my permissions" - e.g. "what are my permissions on todos"
    /what\s+are\s+(?:my\s+)?permissions\s+(?:on|for)\s+(?:my\s+)?(.+?)(?:\s*\?)?$/i,
    // "list X shared with/by me" - e.g. "list projects shared with me"
    /(?:list|show)\s+(\w+)s?\s+shared\s+(?:with|by)\s+me$/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      let resourceType, resourceName, filter;

      if (pattern.source.includes('who')) {
        // who can access my X
        const nameAndType = match[1].trim();
        const resourceTypeMatch = nameAndType.match(/\b(lists?|todos?|projects?)\b/i);
        if (resourceTypeMatch) {
          resourceType = resourceTypeMatch[1];
          resourceName = nameAndType.replace(new RegExp(`\\b${resourceTypeMatch[1]}\\b`, 'i'), '').trim();
        } else {
          resourceType = nameAndType;
          resourceName = '';
        }

        filter = 'shares';
      } else if (pattern.source.includes('show')) {
        // show me shared X
        resourceType = match[1];
        filter = 'shared-with-me';
      } else if (pattern.source.includes('permissions')) {
        // what are my permissions on X
        const nameAndType = match[1].trim();
        const resourceTypeMatch = nameAndType.match(/\b(lists?|todos?|projects?)\b/i);
        if (resourceTypeMatch) {
          resourceType = resourceTypeMatch[1];
          resourceName = nameAndType.replace(new RegExp(`\\b${resourceTypeMatch[1]}\\b`, 'i'), '').trim();
        } else {
          resourceType = nameAndType;
          resourceName = '';
        }

        filter = 'my-role';
      } else if (pattern.source.includes('list') || pattern.source.includes('show')) {
        // list X shared with/by me
        resourceType = match[1];
        // Detect from pattern if "with" or "by"
        const withMatch = text.match(/shared\s+with\s+me/i);
        filter = withMatch ? 'shared-with-me' : 'shared-by-me';
      }

      return {
        intent: 'permission_query',
        resourceType: normalizeResourceType(resourceType),
        resourceName: resourceName,
        filter: filter
      };
    }
  }
  return null;
}

// Helper functions
function normalizeResourceType(type) {
  const normalized = type?.toLowerCase().replace(/s$/, ''); // Remove trailing 's'
  const typeMap = {
    'list': 'lists',
    'todo': 'todos',
    'project': 'projects'
  };
  return typeMap[normalized] || type;
}

function actionToRole(action) {
  const actionMap = {
    'view': 'VIEWER',
    'edit': 'EDITOR',
    'manage': 'ADMIN'
  };
  return actionMap[action.toLowerCase()] || 'VIEWER';
}

/**
 * Handle sharing intent - opens sharing modal with pre-filled values
 */
async function handleShareIntent(intent) {
  const { resourceType, resourceName, recipientEmail, role } = intent;

  try {
    // If resource name provided, search for it
    let resourceId;
    if (resourceName) {
      const response = await fetch(`${API_BASE_URL}/api/v1/${resourceType}?search=${encodeURIComponent(resourceName)}`);
      const resources = await response.json();

      if (resources.length === 0) {
        return {
          success: false,
          message: `Could not find ${resourceType.slice(0, -1)} named "${resourceName}"`
        };
      }

      // Use first match
      const resource = resources[0];
      resourceId = resource.id;

      // #2166: sharing is hidden until its repair.
      if (!SHARING_ENABLED) {
        return { success: false, message: "Sharing isn't available yet." };
      }

      // Check permissions (need to import permissions.js functions)
      if (!canShare(resource)) {
        return {
          success: false,
          message: `You don't have permission to share "${resource.name}"`
        };
      }

      // Open sharing modal (from Option B)
      openShareModal(resourceType, resourceId, resource.name);

      // Pre-fill recipient if provided
      if (recipientEmail) {
        // Wait for modal to render
        setTimeout(() => {
          const emailInput = document.getElementById('share-user-input');
          const roleSelect = document.getElementById('share-role-select');
          if (emailInput) emailInput.value = recipientEmail;
          if (roleSelect) roleSelect.value = role;
        }, 100);
      }

      return {
        success: true,
        message: `Opening share dialog for "${resource.name}"`
      };
    } else {
      // No specific resource - show resource page
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType} - click Share on the one you want to share`
      };
    }
  } catch (error) {
    console.error('Share intent error:', error);
    return {
      success: false,
      message: `Error processing share command: ${error.message}`
    };
  }
}

/**
 * Handle permission query intent - shows who has access
 */
async function handlePermissionQueryIntent(intent) {
  const { resourceType, resourceName, filter } = intent;

  try {
    if (filter === 'shared-with-me' || filter === 'shared-by-me') {
      // Navigate to resource page (it already shows shared resources)
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType} (including shared)`
      };
    }

    if (resourceName) {
      // Query specific resource
      const response = await fetch(`${API_BASE_URL}/api/v1/${resourceType}?search=${encodeURIComponent(resourceName)}`);
      const resources = await response.json();

      if (resources.length === 0) {
        return {
          success: false,
          message: `Could not find ${resourceType.slice(0, -1)} named "${resourceName}"`
        };
      }

      const resource = resources[0];
      const userRole = getUserRole(resource);

      let message = `**${resource.name}**\n\n`;
      message += `Your role: ${formatRole(userRole)}\n\n`;

      if (resource.shared_with && resource.shared_with.length > 0) {
        message += "Shared with:\n";
        resource.shared_with.forEach(share => {
          message += `- ${share.username || share.user_id} (${formatRole(share.role)})\n`;
        });
      } else {
        message += "Not shared with anyone.";
      }

      return {
        success: true,
        message: message
      };
    } else {
      // Show resource page
      window.location.href = `/${resourceType}`;
      return {
        success: true,
        message: `Showing your ${resourceType}`
      };
    }
  } catch (error) {
    console.error('Permission query error:', error);
    return {
      success: false,
      message: `Error querying permissions: ${error.message}`
    };
  }
}

/**
 * Process message for permission intents
 * Called before sending to conversational AI
 */
async function processPermissionIntent(message) {
  const text = message.trim();

  // Try parsing as sharing command
  const shareIntent = parseShareCommand(text);
  if (shareIntent) {
    const result = await handleShareIntent(shareIntent);
    return result;
  }

  // Try parsing as permission query
  const queryIntent = parsePermissionQuery(text);
  if (queryIntent) {
    const result = await handlePermissionQueryIntent(queryIntent);
    return result;
  }

  // Not a permission intent
  return null;
}
