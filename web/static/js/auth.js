document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    const errorMessage = document.getElementById('error-message');

    // #1480: post-login destination. The auth middleware (and the #1520
    // expiry redirects in chat.js) arrive here as /login?next=<encoded
    // path+query>; before this, login always redirected to '/' and the
    // #1466 Slack deep-link params (slack_user_id/slack_team_id) were lost.
    // Guard mirrors sanitize_next_path (services/auth/auth_middleware.py):
    // relative paths only — refuse absolute URLs (https://evil.example
    // fails startsWith('/')), protocol-relative ('//evil.example'), and
    // backslash smuggling ('/\\evil' — browsers normalize \ to /).
    function safeNextUrl() {
        const next = new URLSearchParams(window.location.search).get('next');
        if (
            typeof next !== 'string' ||
            !next.startsWith('/') ||
            next.startsWith('//') ||
            next.indexOf('\\') !== -1 ||
            /^\/(login|logout)([/?#]|$)/.test(next)
        ) {
            return '/';
        }
        // Fragments never reach the server, but the browser carries the
        // original hash (#link-slack) across the 302 onto the login page
        // URL — re-attach it so anchor-targeted deep links stay intact.
        if (window.location.hash && next.indexOf('#') === -1) {
            return next + window.location.hash;
        }
        return next;
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Get form data
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            // Validate
            if (!username || !password) {
                showError('Please enter both username and password');
                return;
            }

            // Show loading state
            loginButton.disabled = true;
            loginButton.classList.add('loading');
            loginButton.textContent = 'Logging in';
            hideError();

            // #1572: capture the browser's IANA timezone so reminder times
            // ("4pm today") parse and render on the USER'S clock, not the
            // server's UTC. Best-effort — login proceeds without it.
            let browserTimezone = '';
            try {
                browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
            } catch (tzError) {
                browserTimezone = '';
            }

            try {
                // POST to login endpoint
                const loginParams = new URLSearchParams({
                    username: username,
                    password: password
                });
                if (browserTimezone) {
                    loginParams.set('browser_timezone', browserTimezone);
                }
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: loginParams,
                    credentials: 'include' // Include cookies
                });

                if (response.ok) {
                    // Success — land on the guarded next target (#1480), or
                    // home when none was carried.
                    const data = await response.json();
                    window.location.href = safeNextUrl();
                } else {
                    // Login failed
                    const error = await response.json();
                    showError(error.detail || 'Invalid username or password');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('Network error. Please check your connection and try again.');
            } finally {
                // Reset button state
                loginButton.disabled = false;
                loginButton.classList.remove('loading');
                loginButton.textContent = 'Log In';
            }
        });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }
});
