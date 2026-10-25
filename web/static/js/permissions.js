/**
 * Permission helper utilities for RBAC
 * Checks permissions based on window.currentUser and resource metadata
 *
 * Usage:
 *   if (canEdit(resource)) { show edit button }
 *   if (canDelete(resource)) { show delete button }
 *   const role = getUserRole(resource); // 'OWNER', 'ADMIN', 'EDITOR', 'VIEWER', 'NONE'
 */

// Check if current user can edit a resource
function canEdit(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Check shared_with for EDITOR or ADMIN role
  if (!resource.shared_with) return false;
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share && (share.role === 'EDITOR' || share.role === 'ADMIN');
}

// Check if current user can delete a resource
function canDelete(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  if (resource.owner_id === window.currentUser.user_id) return true;

  // Only resource-level ADMIN role can delete
  if (!resource.shared_with) return false;
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share && share.role === 'ADMIN';
}

// #2166 (PPM 10-24 18:36): sharing is hidden on alpha until its repair (Production D):
// todo sharing has no column, no route lists shares, and an email resolves to nothing.
// The Share buttons and the chat share intent check this first.
const SHARING_ENABLED = false;

// Check if current user can share a resource
function canShare(resource) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  return resource.owner_id === window.currentUser.user_id;
}

// Check if current user is owner
function isOwner(resource) {
  if (!window.currentUser) return false;
  return resource.owner_id === window.currentUser.user_id;
}

// Get current user's role for a resource
function getUserRole(resource) {
  if (!window.currentUser) return 'NONE';
  if (window.currentUser.is_admin) return 'ADMIN';
  if (resource.owner_id === window.currentUser.user_id) return 'OWNER';

  if (!resource.shared_with) return 'NONE';
  const share = resource.shared_with.find(s => s.user_id === window.currentUser.user_id);
  return share ? share.role : 'NONE';
}

// Format role for display
// NOTE: OWNER returns empty string because in single-user context, all items
// are owned by the user - the badge provides no information. Restore 'Owner'
// when multi-user/sharing feature ships (see issue #600).
function formatRole(role) {
  const roleLabels = {
    'OWNER': '',  // Hidden in single-user context (redundant)
    'ADMIN': 'Admin',
    'EDITOR': 'Editor',
    'VIEWER': 'Viewer',
    'NONE': 'No Access'
  };
  return roleLabels[role] || role;
}

// Get role badge CSS class
function getRoleBadgeClass(role) {
  return `permission-badge ${role.toLowerCase()}`;
}
