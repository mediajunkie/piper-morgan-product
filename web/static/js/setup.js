// Setup Wizard JavaScript (Issue #390, #528)
(function() {
    'use strict';

    // State
    let currentStep = 1;
    let userId = null;
    let slackConnected = false;  // Issue #528: Track Slack OAuth status
    // #940: Track validation per-provider; any ONE LLM provider is sufficient
    const validatedProviders = { openai: false, anthropic: false, gemini: false };
    const apiKeys = { openai: null, anthropic: null, gemini: null, notion: null };
    const keychainKeys = { openai: false, anthropic: false, gemini: false, notion: false }; // Track which keys came from keychain

    // #940: Check if any LLM provider is validated (OpenAI or Anthropic or Gemini)
    function anyLlmProviderValid() {
        return validatedProviders.openai || validatedProviders.anthropic || validatedProviders.gemini;
    }

    // DOM elements
    const steps = document.querySelectorAll('.setup-step');
    const progressSteps = document.querySelectorAll('.setup-progress .step');
    const errorDiv = document.getElementById('error-message');

    // Utility functions
    function showError(message, title = 'Error') {
        if (typeof Toast !== 'undefined') {
            Toast.error(title, message);
        } else {
            // Fallback for when Toast not loaded
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
        }
    }

    function showStep(stepNum) {
        steps.forEach(s => s.classList.remove('active'));
        progressSteps.forEach((p, i) => {
            p.classList.remove('active', 'completed');
            if (i + 1 < stepNum) p.classList.add('completed');
            if (i + 1 === stepNum) p.classList.add('active');
        });
        document.getElementById(`step-${stepNum}`).classList.add('active');
        currentStep = stepNum;

        // Check keychain availability when entering step 2
        if (stepNum === 2) {
            checkKeychainAvailability();
        }
    }

    // Check if keys exist in keychain and show buttons. Only Notion has a
    // static, always-present .keychain-btn[data-provider="notion"] element.
    // openai/anthropic/gemini share one dynamic button (#keychain-llm-btn)
    // whose data-provider is only set once the LLM dropdown fires its own
    // `change` handler (see checkKeychainForProvider below) -- querying for
    // them here always misses (data-provider="" at this point), so they're
    // omitted rather than left as dead, always-losing lookups (#1105).
    async function checkKeychainAvailability() {
        const providers = ['notion'];
        for (const provider of providers) {
            try {
                const response = await fetch(`/api/v1/setup/check-keychain/${provider}`);
                const data = await response.json();
                const btn = document.querySelector(`.keychain-btn[data-provider="${provider}"]`);
                if (btn && data.exists) {
                    btn.classList.remove('hidden');
                }
            } catch (err) {
                // Silently fail - button stays hidden
                console.log(`Keychain check failed for ${provider}:`, err);
            }
        }
    }

    // Step 1: System Check
    document.getElementById('check-system-btn').addEventListener('click', async function() {
        this.disabled = true;
        this.textContent = 'Checking...';
        document.getElementById('step-1-description').textContent = 'Checking that all required services are running...';

        try {
            const statusDiv = document.getElementById('system-status');

            // Show progress animation while checking
            statusDiv.innerHTML = `
                <div class="service-status checking">⏳ Checking Docker...</div>
                <div class="service-status checking">⏳ Checking PostgreSQL...</div>
                <div class="service-status checking">⏳ Checking Redis...</div>
                <div class="service-status checking">⏳ Checking ChromaDB...</div>
                <div class="service-status checking">⏳ Checking Temporal...</div>
            `;

            const response = await fetch('/api/v1/setup/check-system', { method: 'POST' });
            const data = await response.json();

            // Animate results appearing sequentially
            const services = [
                { name: 'Docker', ready: data.docker_available },
                { name: 'PostgreSQL', ready: data.postgres_ready },
                { name: 'Redis', ready: data.redis_ready },
                { name: 'ChromaDB', ready: data.chromadb_ready },
                { name: 'Temporal (optional)', ready: data.temporal_ready },
            ];

            statusDiv.innerHTML = '';

            // Reveal each service result with 200ms delay for visual feedback
            for (let i = 0; i < services.length; i++) {
                const service = services[i];
                await new Promise(resolve => setTimeout(resolve, 200));

                const serviceEl = document.createElement('div');
                serviceEl.className = `service-status ${service.ready ? 'ready' : 'not-ready'}`;
                serviceEl.style.opacity = '0';
                serviceEl.style.transform = 'translateY(10px)';
                serviceEl.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                serviceEl.textContent = `${service.ready ? '✓' : '✗'} ${service.name}`;

                statusDiv.appendChild(serviceEl);

                // Trigger animation
                requestAnimationFrame(() => {
                    serviceEl.style.opacity = '1';
                    serviceEl.style.transform = 'translateY(0)';
                });
            }

            if (data.all_required_ready) {
                // Small delay before showing next button for satisfaction
                await new Promise(resolve => setTimeout(resolve, 400));
                document.getElementById('next-1').style.display = 'block';
                this.style.display = 'none';
            } else {
                showError('Required services are offline. Run: docker compose up -d', 'Services Not Running');
                this.disabled = false;
                this.textContent = 'Retry Check';
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to reach server. Please try again.', 'Connection Failed');
            }
            this.disabled = false;
            this.textContent = 'Retry Check';
        }
    });

    document.getElementById('next-1').addEventListener('click', () => showStep(2));

    // Back button handlers for navigation between steps
    const back2Btn = document.getElementById('back-2');
    if (back2Btn) {
        back2Btn.addEventListener('click', () => showStep(1));
    }

    const back3Btn = document.getElementById('back-3');
    if (back3Btn) {
        back3Btn.addEventListener('click', () => showStep(2));
    }

    // =========================================================================
    // Step 2: LLM Provider Selection + API Key (#940)
    // =========================================================================

    const llmProviderSelect = document.getElementById('llm-provider');
    const llmKeyGroup = document.getElementById('llm-key-group');
    const llmKeyInput = document.getElementById('llm-key');
    const llmKeyLabel = document.getElementById('llm-key-label');
    const validateLlmBtn = document.getElementById('validate-llm-btn');
    const keychainLlmBtn = document.getElementById('keychain-llm-btn');
    const llmStatusDiv = document.getElementById('llm-status');

    const providerPlaceholders = {
        openai: 'sk-...',
        anthropic: 'sk-ant-...',
    };
    const providerLabels = {
        openai: 'OpenAI API Key',
        anthropic: 'Anthropic API Key',
    };

    // Provider dropdown change — show key input
    if (llmProviderSelect) {
        llmProviderSelect.addEventListener('change', function() {
            const provider = this.value;
            if (!provider) return;

            // Show key input group
            llmKeyGroup.style.display = 'block';
            llmKeyInput.value = '';
            llmKeyInput.disabled = false;
            llmKeyInput.placeholder = providerPlaceholders[provider] || '';
            llmKeyLabel.textContent = providerLabels[provider] || 'API Key';
            validateLlmBtn.dataset.provider = provider;
            validateLlmBtn.disabled = false;
            keychainLlmBtn.dataset.provider = provider;
            llmStatusDiv.textContent = '';
            llmStatusDiv.className = 'validation-status';

            // Check keychain for this provider
            checkKeychainForProvider(provider);
        });
    }

    async function checkKeychainForProvider(provider) {
        try {
            const response = await fetch(`/api/v1/setup/check-keychain/${provider}`);
            const data = await response.json();
            if (data.exists) {
                keychainLlmBtn.classList.remove('hidden');
            } else {
                keychainLlmBtn.classList.add('hidden');
            }
        } catch (err) {
            keychainLlmBtn.classList.add('hidden');
        }
    }

    // Validate LLM key button
    if (validateLlmBtn) {
        validateLlmBtn.addEventListener('click', async function() {
            const provider = this.dataset.provider;
            const apiKey = llmKeyInput.value.trim();

            if (!apiKey) {
                llmStatusDiv.textContent = 'Please enter an API key';
                llmStatusDiv.className = 'validation-status invalid';
                return;
            }

            this.disabled = true;
            llmStatusDiv.textContent = 'Validating...';
            llmStatusDiv.className = 'validation-status';

            try {
                const response = await fetch('/api/v1/setup/validate-key', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();

                if (data.valid) {
                    llmStatusDiv.textContent = `✓ ${data.message}`;
                    llmStatusDiv.className = 'validation-status valid';
                    // Store in the hidden input for completeSetup() compatibility
                    document.getElementById(`${provider}-key`).value = apiKey;
                    apiKeys[provider] = apiKey;
                    keychainKeys[provider] = false;
                    validatedProviders[provider] = true;
                    document.getElementById('next-2').disabled = false;
                    // Lock the provider selector after successful validation
                    llmProviderSelect.disabled = true;
                } else {
                    llmStatusDiv.textContent = '✗ ' + data.message;
                    llmStatusDiv.className = 'validation-status invalid';
                    validatedProviders[provider] = false;
                    if (!anyLlmProviderValid()) {
                        document.getElementById('next-2').disabled = true;
                    }
                    this.disabled = false;
                }
            } catch (err) {
                llmStatusDiv.textContent = '✗ Validation failed';
                llmStatusDiv.className = 'validation-status invalid';
                if (!navigator.onLine) {
                    showError('Check your internet connection and try again.', 'No Connection');
                } else {
                    showError('Unable to validate API key. Please try again.', 'Validation Failed');
                }
                this.disabled = false;
            }
        });
    }

    // Keychain button for LLM provider
    if (keychainLlmBtn) {
        keychainLlmBtn.addEventListener('click', async function() {
            const provider = this.dataset.provider;

            this.disabled = true;
            llmStatusDiv.textContent = 'Retrieving from keychain...';
            llmStatusDiv.className = 'validation-status';

            try {
                const response = await fetch('/api/v1/setup/use-keychain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider })
                });
                const data = await response.json();

                if (data.success && data.valid) {
                    llmKeyInput.value = '••••••••••••••••';
                    llmKeyInput.disabled = true;
                    llmStatusDiv.textContent = '✓ ' + data.message;
                    llmStatusDiv.className = 'validation-status valid';
                    apiKeys[provider] = '__FROM_KEYCHAIN__';
                    keychainKeys[provider] = true;
                    this.classList.add('hidden');
                    validateLlmBtn.disabled = true;
                    validatedProviders[provider] = true;
                    document.getElementById('next-2').disabled = false;
                    llmProviderSelect.disabled = true;
                } else {
                    llmStatusDiv.textContent = '✗ ' + (data.message || 'Keychain retrieval failed');
                    llmStatusDiv.className = 'validation-status invalid';
                }
            } catch (err) {
                llmStatusDiv.textContent = '✗ Keychain access failed';
                llmStatusDiv.className = 'validation-status invalid';
                showError('Unable to access system keychain. Enter key manually instead.', 'Keychain Error');
            }
            this.disabled = false;
        });
    }

    // Notion key validation (kept separate — it's an integration, not LLM)
    document.querySelectorAll('.validate-key-btn').forEach(btn => {
        // Skip the LLM validate button (handled above)
        if (btn.id === 'validate-llm-btn') return;

        btn.addEventListener('click', async function() {
            const provider = this.dataset.provider;
            const input = document.getElementById(`${provider}-key`);
            const statusDiv = document.getElementById(`${provider}-status`);
            const apiKey = input.value.trim();

            if (!apiKey) {
                statusDiv.textContent = 'Please enter an API key';
                statusDiv.className = 'validation-status invalid';
                return;
            }

            this.disabled = true;
            statusDiv.textContent = 'Validating...';
            statusDiv.className = 'validation-status';

            try {
                const response = await fetch('/api/v1/setup/validate-key', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();

                if (data.valid) {
                    const message = data.workspace_name
                        ? `✓ Valid (Connected to '${data.workspace_name}')`
                        : `✓ ${data.message}`;
                    statusDiv.textContent = message;
                    statusDiv.className = 'validation-status valid';
                    apiKeys[provider] = apiKey;
                    keychainKeys[provider] = false;
                } else {
                    statusDiv.textContent = '✗ ' + data.message;
                    statusDiv.className = 'validation-status invalid';
                    this.disabled = false;
                }
            } catch (err) {
                statusDiv.textContent = '✗ Validation failed';
                statusDiv.className = 'validation-status invalid';
                this.disabled = false;
            }
        });
    });

    // Keychain buttons for non-LLM providers (Notion)
    document.querySelectorAll('.keychain-btn').forEach(btn => {
        if (btn.id === 'keychain-llm-btn') return;

        btn.addEventListener('click', async function() {
            const provider = this.dataset.provider;
            const input = document.getElementById(`${provider}-key`);
            const statusDiv = document.getElementById(`${provider}-status`);

            this.disabled = true;
            statusDiv.textContent = 'Retrieving from keychain...';
            statusDiv.className = 'validation-status';

            try {
                const response = await fetch('/api/v1/setup/use-keychain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider })
                });
                const data = await response.json();

                if (data.success && data.valid) {
                    input.value = '••••••••••••••••';
                    input.disabled = true;
                    statusDiv.textContent = '✓ ' + data.message;
                    statusDiv.className = 'validation-status valid';
                    apiKeys[provider] = '__FROM_KEYCHAIN__';
                    keychainKeys[provider] = true;
                    this.classList.add('hidden');
                    document.querySelector(`.validate-key-btn[data-provider="${provider}"]`).disabled = true;
                } else {
                    statusDiv.textContent = '✗ ' + (data.message || 'Failed');
                    statusDiv.className = 'validation-status invalid';
                }
            } catch (err) {
                statusDiv.textContent = '✗ Keychain access failed';
                statusDiv.className = 'validation-status invalid';
            }
            this.disabled = false;
        });
    });

    document.getElementById('next-2').addEventListener('click', () => showStep(3));

    // Step 3: Account Creation - Initialize form validation
    if (typeof FormValidation !== 'undefined' && typeof Validators !== 'undefined') {
        FormValidation.init('account-form', {
            username: [Validators.required(), Validators.minLength(3)],
            email: [Validators.required(), Validators.email()],
            password: [Validators.required(), Validators.minLength(8)],
            'password-confirm': [
                Validators.required(),
                Validators.custom(
                    (value) => value === document.getElementById('password').value,
                    'Passwords do not match'
                )
            ]
        });
    }

    document.getElementById('account-form').addEventListener('submit', async function(e) {
        e.preventDefault();

        // Use FormValidation if available
        if (typeof FormValidation !== 'undefined') {
            if (!FormValidation.validateForm('account-form')) {
                showError('Please fix the form errors before continuing.', 'Validation Error');
                return;
            }
        }

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const passwordConfirm = document.getElementById('password-confirm').value;
        // #1344: create-user REQUIRES an invite token — the wizard previously
        // omitted it, so every account creation failed with a 422.
        const inviteToken = document.getElementById('invite-token').value.trim();
        if (!inviteToken) {
            showError('Please enter your invite code — alpha access is invite-only.', 'Invite Code Required');
            return;
        }

        // Fallback password check if FormValidation not loaded
        if (typeof FormValidation === 'undefined' && password !== passwordConfirm) {
            showError('Passwords do not match.', 'Validation Error');
            return;
        }

        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';

        try {
            const response = await fetch('/api/v1/setup/create-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password, password_confirm: passwordConfirm, invite_token: inviteToken })
            });
            const data = await response.json();

            if (data.success) {
                userId = data.user_id;
                // Complete setup
                await completeSetup();
            } else {
                // Handle both success=false responses and HTTPException responses
                // HTTPException returns {detail: "..."}, success responses return {message: "..."}
                const errorMessage = data.message || data.detail || 'Failed to create account.';
                showError(errorMessage, 'Account Creation Failed');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create Account';
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to create account. Please try again.', 'Account Creation Failed');
            }
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });

    async function completeSetup() {
        try {
            // Don't send keys that came from keychain (they're already stored)
            const response = await fetch('/api/v1/setup/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    // #946: Send the user's chosen LLM provider
                    default_llm_provider: llmProviderSelect ? llmProviderSelect.value : null,
                    openai_key: keychainKeys.openai ? null : apiKeys.openai,
                    anthropic_key: keychainKeys.anthropic ? null : apiKeys.anthropic,
                    gemini_key: keychainKeys.gemini ? null : apiKeys.gemini,
                    notion_key: keychainKeys.notion ? null : apiKeys.notion
                })
            });
            const data = await response.json();

            if (data.success) {
                showStep(4);  // Step 4: Projects (Issue #860)
            } else {
                showError(data.message || 'Unable to complete setup.', 'Setup Failed');
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to complete setup. Please try again.', 'Setup Failed');
            }
        }
    }

    // Check initial setup status
    // Issue #608: Removed redirect to /login when setup_complete.
    // /setup should always be accessible for new user registration
    // (multi-user support for teams, shared machines, etc.)
    async function checkSetupStatus() {
        // No-op: setup wizard is always accessible
        // Users who already have an account can use the "Log In" link
    }

    // =========================================================================
    // Step 4: Projects Setup (Issue #860)
    // =========================================================================

    const setupProjects = [];  // Track projects added during setup

    function renderSetupProjects() {
        const listEl = document.getElementById('setup-projects-list');
        if (!listEl) return;

        if (setupProjects.length === 0) {
            listEl.innerHTML = '';
            return;
        }

        listEl.innerHTML = setupProjects.map((p, i) => `
            <div class="service-status ready" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <strong>${p.name}</strong>
                    ${p.repo ? ` — <span style="color: #6c757d;">${p.repo}</span>` : ''}
                </div>
                <button type="button" onclick="window._removeSetupProject(${i})"
                    style="background: none; border: none; color: #dc3545; cursor: pointer; font-size: 16px;"
                    title="Remove">✕</button>
            </div>
        `).join('');
    }

    // Expose remove function globally (called from inline onclick)
    window._removeSetupProject = function(index) {
        setupProjects.splice(index, 1);
        renderSetupProjects();
    };

    const addProjectBtn = document.getElementById('add-project-btn');
    if (addProjectBtn) {
        addProjectBtn.addEventListener('click', async function() {
            const nameInput = document.getElementById('setup-project-name');
            const repoInput = document.getElementById('setup-github-repo');
            const errorEl = document.getElementById('setup-project-error');

            const projectName = nameInput.value.trim();
            const githubRepo = repoInput.value.trim();

            // Validate
            if (!projectName) {
                errorEl.textContent = 'Project name is required.';
                errorEl.style.display = 'block';
                return;
            }

            if (githubRepo && !githubRepo.includes('/')) {
                errorEl.textContent = 'GitHub repo must be in owner/repo format.';
                errorEl.style.display = 'block';
                return;
            }

            errorEl.style.display = 'none';
            addProjectBtn.disabled = true;
            addProjectBtn.textContent = 'Adding...';

            try {
                const response = await fetch('/api/v1/setup/projects', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: userId,
                        project_name: projectName,
                        project_description: '',
                        github_repo: githubRepo || null
                    })
                });
                const data = await response.json();

                if (data.success) {
                    setupProjects.push({
                        id: data.project_id,
                        name: projectName,
                        repo: githubRepo || null
                    });
                    renderSetupProjects();
                    nameInput.value = '';
                    repoInput.value = '';
                    if (typeof Toast !== 'undefined') {
                        Toast.success('Project Added', data.message);
                    }
                } else {
                    const errorMessage = data.message || data.detail || 'Failed to create project.';
                    errorEl.textContent = errorMessage;
                    errorEl.style.display = 'block';
                }
            } catch (err) {
                errorEl.textContent = 'Unable to create project. Please try again.';
                errorEl.style.display = 'block';
            } finally {
                addProjectBtn.disabled = false;
                addProjectBtn.textContent = 'Add Project';
            }
        });
    }

    // Skip and Continue buttons for step 4
    const skipProjectsBtn = document.getElementById('skip-projects-btn');
    if (skipProjectsBtn) {
        skipProjectsBtn.addEventListener('click', () => showStep(5));
    }

    const next4Btn = document.getElementById('next-4');
    if (next4Btn) {
        next4Btn.addEventListener('click', () => showStep(5));
    }

    // =========================================================================
    // Slack App Credential Functions (Issue #576)
    // =========================================================================

    // Check if Slack app credentials are configured
    async function checkSlackCredentialsStatus() {
        try {
            const response = await fetch('/api/v1/settings/integrations/slack/app-credentials/status');
            if (!response.ok) {
                // If endpoint fails, show config form as fallback
                showSlackConfigNeeded();
                return false;
            }
            const data = await response.json();

            if (data.configured) {
                showSlackCredentialsConfigured();
                return true;
            } else {
                showSlackConfigNeeded();
                return false;
            }
        } catch (err) {
            console.log('Slack credentials status check failed:', err);
            // On error, show config form
            showSlackConfigNeeded();
            return false;
        }
    }

    // Show credential configuration form
    function showSlackConfigNeeded() {
        const configSection = document.getElementById('slack-config-needed');
        const notConnected = document.getElementById('slack-not-connected');
        const connected = document.getElementById('slack-connected');

        if (configSection) configSection.style.display = 'block';
        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'none';
    }

    // Show Connect button (credentials configured)
    function showSlackCredentialsConfigured() {
        const configSection = document.getElementById('slack-config-needed');
        const notConnected = document.getElementById('slack-not-connected');

        if (configSection) configSection.style.display = 'none';
        if (notConnected) notConnected.style.display = 'block';
    }

    // Save Slack app credentials
    async function saveSlackCredentials() {
        const clientId = document.getElementById('slack-client-id')?.value?.trim();
        const clientSecret = document.getElementById('slack-client-secret')?.value?.trim();
        const btn = document.getElementById('save-slack-credentials-btn');

        if (!clientId || !clientSecret) {
            showSlackError('Both Client ID and Client Secret are required');
            return;
        }

        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Saving...';
        }

        try {
            // Issue #772: Use setup-specific endpoint that doesn't require auth
            const response = await fetch('/api/v1/setup/slack-credentials', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    client_id: clientId,
                    client_secret: clientSecret
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Clear inputs
                document.getElementById('slack-client-id').value = '';
                document.getElementById('slack-client-secret').value = '';

                // Show success and switch to connect view
                if (typeof showToast === 'function') {
                    showToast('success', 'Slack app credentials saved');
                }
                showSlackCredentialsConfigured();
            } else {
                showSlackError(data.message || 'Failed to save credentials');
            }
        } catch (err) {
            showSlackError('Failed to save credentials. Please try again.');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Save Credentials';
            }
        }
    }

    // Event listener for save credentials button
    const saveSlackCredentialsBtn = document.getElementById('save-slack-credentials-btn');
    if (saveSlackCredentialsBtn) {
        saveSlackCredentialsBtn.addEventListener('click', saveSlackCredentials);
    }

    // =========================================================================
    // Slack OAuth Functions (Issue #528: ALPHA-SETUP-SLACK)
    // =========================================================================

    // Check for OAuth callback params in URL (after redirect from Slack)
    function checkSlackCallbackParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.get('slack_success') === 'true') {
            const workspace = params.get('slack_workspace') || 'Workspace';
            showSlackConnected(decodeURIComponent(workspace));
            // Clean URL by removing OAuth params
            window.history.replaceState({}, document.title, '/setup#step-2');
        } else if (params.get('slack_error')) {
            const error = params.get('slack_error');
            showSlackError(getSlackErrorMessage(error));
            window.history.replaceState({}, document.title, '/setup#step-2');
        }
    }

    // Check if Slack is already configured
    async function checkSlackStatus() {
        try {
            const response = await fetch('/api/v1/setup/slack/status');
            const data = await response.json();

            if (data.configured) {
                showSlackConnected(data.workspace_name || 'Connected');
            }
        } catch (err) {
            console.log('Slack status check failed:', err);
        }
    }

    // Start OAuth flow - redirects to Slack
    async function connectSlack() {
        const btn = document.getElementById('connect-slack-btn');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Connecting...';
        }

        try {
            const response = await fetch('/api/v1/setup/slack/oauth/start');
            const data = await response.json();

            if (data.auth_url) {
                // Redirect to Slack OAuth
                window.location.href = data.auth_url;
            } else {
                showSlackError('Failed to start OAuth flow');
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Connect to Slack';
                }
            }
        } catch (err) {
            showSlackError('Connection failed. Please try again.');
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Connect to Slack';
            }
        }
    }

    function showSlackConnected(workspace) {
        const notConnected = document.getElementById('slack-not-connected');
        const connected = document.getElementById('slack-connected');
        const workspaceName = document.getElementById('slack-workspace-name');
        const errorDiv = document.getElementById('slack-error');

        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'flex';
        if (workspaceName) workspaceName.textContent = `Connected to ${workspace}`;
        if (errorDiv) errorDiv.style.display = 'none';
        slackConnected = true;
    }

    function showSlackError(message) {
        const errorDiv = document.getElementById('slack-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    function getSlackErrorMessage(error) {
        const messages = {
            'access_denied': 'Authorization was denied. Please try again.',
            'missing_params': 'OAuth callback missing parameters.',
            'callback_failed': 'Failed to complete authorization.',
            'invalid_state': 'Session expired. Please try again.',
        };
        return messages[error] || 'An error occurred. Please try again.';
    }

    // Event listeners for Slack OAuth
    const connectSlackBtn = document.getElementById('connect-slack-btn');
    if (connectSlackBtn) {
        connectSlackBtn.addEventListener('click', connectSlack);
    }

    // Initialize Slack OAuth on page load
    // Issue #576: Check credentials first, then OAuth status
    checkSlackCallbackParams();
    checkSlackCredentialsStatus().then(credentialsConfigured => {
        if (credentialsConfigured) {
            // Only check OAuth status if credentials are configured
            checkSlackStatus();
        }
    });

    // =========================================================================
    // Google Calendar App Credential Functions (Issue #577)
    // =========================================================================

    // Check if Calendar app credentials are configured
    async function checkCalendarCredentialsStatus() {
        try {
            const response = await fetch('/api/v1/settings/integrations/calendar/app-credentials/status', {
                credentials: 'include'
            });
            if (!response.ok) {
                // If endpoint fails, show config form as fallback
                showCalendarConfigNeeded();
                return false;
            }
            const data = await response.json();

            if (data.configured) {
                showCalendarCredentialsConfigured();
                return true;
            } else {
                showCalendarConfigNeeded();
                return false;
            }
        } catch (err) {
            console.log('Calendar credentials status check failed:', err);
            // On error, show config form
            showCalendarConfigNeeded();
            return false;
        }
    }

    // Show credential configuration form
    function showCalendarConfigNeeded() {
        const configSection = document.getElementById('calendar-config-needed');
        const notConnected = document.getElementById('calendar-not-connected');
        const connected = document.getElementById('calendar-connected');

        if (configSection) configSection.style.display = 'block';
        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'none';
    }

    // Show Connect button (credentials configured)
    function showCalendarCredentialsConfigured() {
        const configSection = document.getElementById('calendar-config-needed');
        const notConnected = document.getElementById('calendar-not-connected');

        if (configSection) configSection.style.display = 'none';
        if (notConnected) notConnected.style.display = 'block';
    }

    // Save Calendar app credentials
    async function saveCalendarCredentials() {
        const clientId = document.getElementById('calendar-client-id')?.value?.trim();
        const clientSecret = document.getElementById('calendar-client-secret')?.value?.trim();
        const btn = document.getElementById('save-calendar-credentials-btn');

        if (!clientId || !clientSecret) {
            showCalendarError('Both Client ID and Client Secret are required');
            return;
        }

        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Saving...';
        }

        try {
            const response = await fetch('/api/v1/settings/integrations/calendar/app-credentials', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    client_id: clientId,
                    client_secret: clientSecret
                })
            });

            if (response.ok) {
                // Clear inputs
                document.getElementById('calendar-client-id').value = '';
                document.getElementById('calendar-client-secret').value = '';

                // Show success and switch to connect view
                if (typeof showToast === 'function') {
                    showToast('success', 'Google Calendar app credentials saved');
                }
                showCalendarCredentialsConfigured();
            } else {
                const error = await response.json();
                showCalendarError(error.detail || 'Failed to save credentials');
            }
        } catch (err) {
            showCalendarError('Failed to save credentials. Please try again.');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Save Credentials';
            }
        }
    }

    // Event listener for save calendar credentials button
    const saveCalendarCredentialsBtn = document.getElementById('save-calendar-credentials-btn');
    if (saveCalendarCredentialsBtn) {
        saveCalendarCredentialsBtn.addEventListener('click', saveCalendarCredentials);
    }

    // =========================================================================
    // Google Calendar OAuth Functions (Issue #529: ALPHA-SETUP-CALENDAR)
    // =========================================================================

    // Check for OAuth callback params in URL (after redirect from Google)
    function checkCalendarCallbackParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.get('calendar_success') === 'true') {
            const email = params.get('calendar_email') || 'Calendar';
            showCalendarConnected(decodeURIComponent(email));
            // Clean URL by removing OAuth params
            window.history.replaceState({}, document.title, '/setup#step-2');
        } else if (params.get('calendar_error')) {
            const error = params.get('calendar_error');
            showCalendarError(getCalendarErrorMessage(error));
            window.history.replaceState({}, document.title, '/setup#step-2');
        }
    }

    // Check if Calendar is already configured
    async function checkCalendarStatus() {
        try {
            const response = await fetch('/api/v1/setup/calendar/status');
            const data = await response.json();

            if (data.configured) {
                showCalendarConnected(data.email || 'Connected');
            }
        } catch (err) {
            console.log('Calendar status check failed:', err);
        }
    }

    // Start OAuth flow - redirects to Google
    async function connectCalendar() {
        const btn = document.getElementById('connect-calendar-btn');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Connecting...';
        }

        try {
            const response = await fetch('/api/v1/setup/calendar/oauth/start');
            const data = await response.json();

            if (data.auth_url) {
                // Redirect to Google OAuth
                window.location.href = data.auth_url;
            } else {
                showCalendarError('Failed to start OAuth flow');
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Connect Calendar';
                }
            }
        } catch (err) {
            showCalendarError('Connection failed. Please try again.');
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Connect Calendar';
            }
        }
    }

    function showCalendarConnected(email) {
        const notConnected = document.getElementById('calendar-not-connected');
        const connected = document.getElementById('calendar-connected');
        const emailSpan = document.getElementById('calendar-email');
        const errorDiv = document.getElementById('calendar-error');

        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'flex';
        if (emailSpan) emailSpan.textContent = `Connected: ${email}`;
        if (errorDiv) errorDiv.style.display = 'none';
    }

    function showCalendarError(message) {
        const errorDiv = document.getElementById('calendar-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    function getCalendarErrorMessage(error) {
        const messages = {
            'access_denied': 'Authorization was denied. Please try again.',
            'missing_params': 'OAuth callback missing parameters.',
            'callback_failed': 'Failed to complete authorization.',
        };
        return messages[error] || 'An error occurred. Please try again.';
    }

    // Event listeners for Calendar OAuth
    const connectCalendarBtn = document.getElementById('connect-calendar-btn');
    if (connectCalendarBtn) {
        connectCalendarBtn.addEventListener('click', connectCalendar);
    }

    // Initialize Calendar OAuth on page load
    // Issue #577: Check credentials first, then OAuth status
    checkCalendarCallbackParams();
    checkCalendarCredentialsStatus().then(credentialsConfigured => {
        if (credentialsConfigured) {
            // Only check OAuth status if credentials are configured
            checkCalendarStatus();
        }
    });

    checkSetupStatus();
})();
