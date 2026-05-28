/**
 * DDD Bot Message Renderer - Domain service for consistent message rendering
 */

/**
 * #1123 LINK-NEW-TAB: external links emitted by Piper open in a new tab so
 * the user's chat context isn't replaced. Internal/relative links stay
 * same-tab (those are intra-app navigation like /settings/...).
 *
 * Configured once on first use; idempotent. Marked supports a custom renderer
 * via marked.use({ renderer: ... }) (modern) or new marked.Renderer() (legacy).
 * Try the modern path first; fall back to legacy.
 */
function _ensureLinkRendererConfigured() {
    if (typeof marked === 'undefined') return;
    if (renderBotMessage._linkRendererConfigured) return;
    const linkRenderer = (href, title, text) => {
        // The `href` may already be the full string or marked may pass an
        // object depending on version. Normalize.
        let url = href;
        let titleStr = title;
        let textStr = text;
        if (href && typeof href === 'object' && href.href) {
            url = href.href;
            titleStr = href.title;
            textStr = href.text || text;
        }
        const safeUrl = String(url || '');
        const titleAttr = titleStr ? ` title="${titleStr}"` : '';
        const isExternal = /^https?:\/\//i.test(safeUrl);
        if (isExternal) {
            return `<a href="${safeUrl}"${titleAttr} target="_blank" rel="noopener noreferrer">${textStr || safeUrl}</a>`;
        }
        return `<a href="${safeUrl}"${titleAttr}>${textStr || safeUrl}</a>`;
    };
    try {
        if (typeof marked.use === 'function') {
            marked.use({ renderer: { link: linkRenderer } });
        } else {
            const renderer = new marked.Renderer();
            renderer.link = linkRenderer;
            marked.setOptions({ renderer });
        }
        renderBotMessage._linkRendererConfigured = true;
    } catch (e) {
        console.warn('Marked link-renderer config failed; falling back to default:', e);
    }
}

/**
 * Render bot message with consistent formatting
 * @param {string} content - The message content
 * @param {string} type - 'success', 'error', 'thinking'
 * @param {boolean} isThinking - Whether this is a thinking/loading state
 * @returns {string} - Rendered HTML
 */
function renderBotMessage(content, type = 'success', isThinking = false) {
    if (!content) return '';
    if (isThinking) return content; // Don't process thinking messages

    // Domain logic: Apply markdown only to success messages
    let processedContent = content;
    if (type === 'success' && typeof marked !== 'undefined') {
        try {
            _ensureLinkRendererConfigured();
            processedContent = marked.parse(content);
        } catch (error) {
            console.warn('Markdown parsing failed:', error);
            processedContent = content; // Fallback to raw content
        }
    }

    // Domain logic: Apply consistent CSS classes
    const cssClasses = ['result', type];
    if (isThinking) cssClasses.push('thinking');

    return `<div class="${cssClasses.join(' ')}">${processedContent}</div>`;
}

/**
 * Handle direct API responses
 * @param {Object} result - API response object
 * @param {HTMLElement} element - DOM element to update
 */
function handleDirectResponse(result, element) {
    console.log('Direct response:', result.message);
    element.innerHTML = renderBotMessage(result.message, 'success', false);

    // Phase 3: Render pattern suggestions if present
    if (result.suggestions && result.suggestions.length > 0) {
        element.innerHTML += renderSuggestions(result.suggestions);

        // Auto-show onboarding tooltip if first time
        setTimeout(() => {
            const tooltip = document.querySelector('.onboarding-tooltip');
            if (tooltip) {
                tooltip.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 100);
    }
}

/**
 * Render pattern suggestions UI (Phase 3)
 * @param {Array} suggestions - Array of suggestion objects
 * @returns {string} - Rendered HTML
 */
function renderSuggestions(suggestions) {
    const count = suggestions.length;
    const plural = count === 1 ? '' : 's';

    // Check if user has seen suggestions before (Phase 3.3)
    const showOnboarding = !hasSeenSuggestions();

    let html = '<div class="suggestions-container">';

    // Onboarding tooltip (first-time only)
    if (showOnboarding) {
        html += renderOnboardingTooltip();
    }

    // Main suggestions UI
    html += `
            <div class="suggestions-badge" onclick="toggleSuggestionsPanel()">
                💡 ${count} pattern suggestion${plural}
                <span class="badge-chevron">▼</span>
            </div>
            <div class="suggestions-panel" id="suggestions-panel" style="display: none;">
                <div class="suggestions-header">
                    <strong>Suggested Actions</strong>
                    <span class="suggestions-subtitle">Based on your past patterns</span>
                </div>
                ${suggestions.map((s, idx) => renderSuggestionCard(s, idx)).join('')}
            </div>
        </div>
    `;

    return html;
}

/**
 * Render individual suggestion card (Phase 3)
 * @param {Object} suggestion - Suggestion object
 * @param {number} index - Card index
 * @returns {string} - Rendered HTML
 */
function renderSuggestionCard(suggestion, index) {
    // Issue #485: Defensive null checks for malformed responses
    if (!suggestion || typeof suggestion !== 'object') {
        console.warn('renderSuggestionCard: Invalid suggestion object', suggestion);
        return '';
    }

    const confidence = Math.round((suggestion.confidence || 0) * 100);
    const patternType = (suggestion.pattern_type || 'unknown').replace('_', ' ').toLowerCase();
    const usageText = `Used ${suggestion.usage_count} time${suggestion.usage_count === 1 ? '' : 's'}`;

    // Phase 4: Check for auto-triggered flag
    const isAutoTriggered = suggestion.auto_triggered || false;

    // Bug #76n: Extract action details from pattern_data for better descriptions
    let reasoning = suggestion.pattern_data?.reasoning || suggestion.pattern_data?.description;

    // If no reasoning/description, try to generate from action details
    if (!reasoning) {
        const actionType = suggestion.pattern_data?.action_type;
        const actionParams = suggestion.pattern_data?.action_params;

        if (actionType === 'create_github_issue' && actionParams?.title) {
            reasoning = `Create GitHub Issue: ${actionParams.title}`;
        } else if (actionType && actionParams) {
            // Generic action description
            const actionName = actionType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            reasoning = `${actionName}`;
        } else {
            // Fallback to generic pattern type
            reasoning = `${patternType} pattern detected`;
        }
    }

    // Phase 4: Visual styling based on type
    const icon = isAutoTriggered ? '⚡' : '💡';
    const cardClass = isAutoTriggered ? 'auto-triggered' : '';
    const badgeClass = isAutoTriggered ? 'auto-badge' : 'manual-badge';
    const badgeText = isAutoTriggered ? 'Auto-detected' : 'Suggested';

    return `
        <div class="suggestion-card ${cardClass}" data-pattern-id="${suggestion.pattern_id}">
            <div class="suggestion-content">
                <div class="suggestion-header">
                    <span class="suggestion-icon">${icon}</span>
                    <span class="suggestion-badge ${badgeClass}">${badgeText}</span>
                </div>
                <div class="suggestion-reasoning">${reasoning}</div>
                <div class="suggestion-meta">
                    <span class="suggestion-type">${patternType}</span>
                    <span class="suggestion-usage">${usageText}</span>
                </div>
                <div class="confidence-bar-container">
                    <div class="confidence-bar" style="width: ${confidence}%"></div>
                    <span class="confidence-label">${confidence}% confidence</span>
                </div>
            </div>
            <div class="suggestion-actions">
                ${isAutoTriggered ? `
                    <button class="suggestion-btn execute" onclick="handleExecute('${suggestion.pattern_id}')">
                        ▶ Execute Now
                    </button>
                    <button class="suggestion-btn skip" onclick="handleSkip('${suggestion.pattern_id}')">
                        Skip This Time
                    </button>
                    <button class="suggestion-btn disable" onclick="handleDisable('${suggestion.pattern_id}')">
                        Disable Pattern
                    </button>
                ` : `
                    <button class="suggestion-btn accept" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'accept')">
                        ✓ Accept
                    </button>
                    <button class="suggestion-btn reject" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'reject')">
                        ✗ Reject
                    </button>
                    <button class="suggestion-btn dismiss" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'dismiss')">
                        Dismiss
                    </button>
                `}
            </div>
        </div>
    `;
}

/**
 * Toggle suggestions panel visibility (Phase 3)
 */
function toggleSuggestionsPanel() {
    const panel = document.getElementById('suggestions-panel');
    const badge = document.querySelector('.suggestions-badge');
    const chevron = document.querySelector('.badge-chevron');

    if (panel.style.display === 'none') {
        panel.style.display = 'block';
        chevron.textContent = '▲';
        badge.classList.add('expanded');
    } else {
        panel.style.display = 'none';
        chevron.textContent = '▼';
        badge.classList.remove('expanded');
    }
}

/**
 * Handle suggestion feedback (Phase 3)
 * @param {string} patternId - Pattern UUID
 * @param {string} action - 'accept', 'reject', or 'dismiss'
 */
async function handleSuggestionFeedback(patternId, action) {
    console.log(`Suggestion feedback: ${action} for pattern ${patternId}`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/learning/patterns/${patternId}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        });

        if (!response.ok) {
            throw new Error('Feedback submission failed');
        }

        const result = await response.json();

        // Remove the suggestion card with animation
        const card = document.querySelector(`[data-pattern-id="${patternId}"]`);
        if (card) {
            card.style.opacity = '0.5';
            card.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                card.remove();

                // Update badge count
                const remaining = document.querySelectorAll('.suggestion-card').length;
                if (remaining === 0) {
                    document.querySelector('.suggestions-container').remove();
                } else {
                    const badge = document.querySelector('.suggestions-badge');
                    const plural = remaining === 1 ? '' : 's';
                    badge.innerHTML = `💡 ${remaining} pattern suggestion${plural} <span class="badge-chevron">▲</span>`;
                }
            }, 300);
        }

        // Show feedback toast
        showFeedbackToast(action);

    } catch (error) {
        console.error('Feedback error:', error);
        alert('Failed to submit feedback. Please try again.');
    }
}

/**
 * Phase 4: Handle Execute button for proactive suggestions
 * @param {string} patternId - Pattern UUID
 */
async function handleExecute(patternId) {
    console.log(`Executing proactive pattern: ${patternId}`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/learning/patterns/${patternId}/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Pattern execution failed');
        }

        const result = await response.json();

        // Remove the suggestion card
        removeSuggestionCard(patternId);

        // Show success message
        showFeedbackToast('execute', result.message || 'Action executed successfully!');

    } catch (error) {
        console.error('Execute error:', error);
        alert('Failed to execute action. Please try again.');
    }
}

/**
 * Phase 4: Handle Skip button for proactive suggestions
 * @param {string} patternId - Pattern UUID
 */
async function handleSkip(patternId) {
    console.log(`Skipping proactive pattern: ${patternId}`);

    // Just dismiss without feedback (neutral action)
    removeSuggestionCard(patternId);
    showFeedbackToast('skip');
}

/**
 * Phase 4: Handle Disable button for proactive suggestions
 * @param {string} patternId - Pattern UUID
 */
async function handleDisable(patternId) {
    console.log(`Disabling proactive pattern: ${patternId}`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/learning/patterns/${patternId}/disable`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error('Pattern disable failed');
        }

        // Remove the suggestion card
        removeSuggestionCard(patternId);

        // Show success message
        showFeedbackToast('disable');

    } catch (error) {
        console.error('Disable error:', error);
        alert('Failed to disable pattern. Please try again.');
    }
}

/**
 * Phase 4: Helper to remove suggestion card with animation
 * @param {string} patternId - Pattern UUID
 */
function removeSuggestionCard(patternId) {
    const card = document.querySelector(`[data-pattern-id="${patternId}"]`);
    if (card) {
        card.style.opacity = '0.5';
        card.style.transition = 'opacity 0.3s';
        setTimeout(() => {
            card.remove();

            // Update badge count
            const remaining = document.querySelectorAll('.suggestion-card').length;
            if (remaining === 0) {
                const container = document.querySelector('.suggestions-container');
                if (container) container.remove();
            } else {
                const badge = document.querySelector('.suggestions-badge');
                if (badge) {
                    const plural = remaining === 1 ? '' : 's';
                    badge.innerHTML = `💡 ${remaining} pattern suggestion${plural} <span class="badge-chevron">▲</span>`;
                }
            }
        }, 300);
    }
}

/**
 * Show feedback toast message (Phase 3)
 * @param {string} action - Feedback action
 * @param {string} customMessage - Optional custom message
 */
function showFeedbackToast(action, customMessage) {
    const messages = {
        accept: '✓ Pattern accepted - confidence increased',
        reject: '✗ Pattern rejected - confidence decreased',
        dismiss: 'Pattern dismissed',
        execute: '▶ Action executed successfully!',
        skip: 'Skipped for now',
        disable: 'Pattern disabled - won\'t suggest again'
    };

    const toast = document.createElement('div');
    toast.className = 'feedback-toast';
    toast.textContent = customMessage || messages[action] || 'Action completed';
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

/**
 * Handle workflow completion responses
 * @param {Object} data - Workflow data object
 * @param {HTMLElement} element - DOM element to update
 */
function handleWorkflowResponse(data, element) {
    console.log('Workflow response:', data.message);

    if (data.type === 'analyze_file' || data.type === 'generate_report') {
        const message = data.message || 'File analysis completed successfully!';
        element.innerHTML = renderBotMessage(message, 'success', false);
    } else {
        // GitHub issue logic (keep existing special case)
        const finalResult = data.tasks && data.tasks[data.tasks.length - 1]?.result?.issue;
        if (finalResult && finalResult.url) {
            element.innerHTML = `
                <div class="result success">
                    <strong>✅ GitHub Issue Created!</strong><br>
                    <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
                    <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
                </div>`;
        } else {
            const message = data.message || 'Workflow completed successfully!';
            element.innerHTML = renderBotMessage(message, 'success', false);
        }
    }
}

/**
 * Handle error responses
 * @param {Error} error - Error object
 * @param {HTMLElement} element - DOM element to update
 */
function handleErrorResponse(error, element) {
    console.error('Error response:', error.message);
    element.innerHTML = renderBotMessage(error.message, 'error', false);
}

/**
 * Phase 3.3: Onboarding Helpers
 */

/**
 * Check if user has seen suggestions before
 * @returns {boolean}
 */
function hasSeenSuggestions() {
    return localStorage.getItem('piper_suggestions_seen') === 'true';
}

/**
 * Mark suggestions as seen
 */
function markSuggestionsAsSeen() {
    localStorage.setItem('piper_suggestions_seen', 'true');
}

/**
 * Render onboarding tooltip (Phase 3.3)
 * @returns {string} - Rendered HTML
 */
function renderOnboardingTooltip() {
    return `
        <div class="onboarding-tooltip">
            <div class="tooltip-header">
                <span class="tooltip-icon">💡</span>
                <h4>New: Pattern Suggestions</h4>
            </div>
            <p>Piper noticed patterns in how you work and can suggest helpful next steps. You're always in control.</p>
            <div class="tooltip-actions">
                <button onclick="dismissOnboarding()">Got it</button>
                <button onclick="showLearnMore()">Learn more</button>
            </div>
        </div>
    `;
}

/**
 * Dismiss onboarding tooltip
 */
function dismissOnboarding() {
    markSuggestionsAsSeen();
    const tooltip = document.querySelector('.onboarding-tooltip');
    if (tooltip) {
        tooltip.style.opacity = '0';
        tooltip.style.transition = 'opacity 0.3s ease';
        setTimeout(() => tooltip.remove(), 300);
    }
}

/**
 * Show "Learn More" modal
 */
function showLearnMore() {
    dismissOnboarding();

    const modal = document.createElement('div');
    modal.className = 'learn-more-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeLearnMoreModal()"></div>
        <div class="modal-content">
            <h3>How Pattern Suggestions Work</h3>

            <div class="learn-section">
                <h4>🔍 Pattern Detection</h4>
                <p>Piper observes when you repeatedly do similar actions (like creating issues after standup).</p>
            </div>

            <div class="learn-section">
                <h4>📊 Confidence</h4>
                <p>The percentage shows how confident Piper is based on how often the pattern succeeds.</p>
            </div>

            <div class="learn-section">
                <h4>✓ Feedback</h4>
                <p>Accept helpful suggestions to see more like them. Reject unhelpful ones to improve Piper's learning.</p>
            </div>

            <div class="learn-section">
                <h4>🔒 Privacy</h4>
                <p>Your patterns are private. Only you see them.</p>
            </div>

            <button onclick="closeLearnMoreModal()">Got it!</button>
        </div>
    `;
    document.body.appendChild(modal);
}

/**
 * Close "Learn More" modal
 */
function closeLearnMoreModal() {
    const modal = document.querySelector('.learn-more-modal');
    if (modal) {
        modal.remove();
    }
}
