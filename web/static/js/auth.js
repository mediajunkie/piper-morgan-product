document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    const errorMessage = document.getElementById('error-message');

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

            try {
                // POST to login endpoint
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        username: username,
                        password: password
                    }),
                    credentials: 'include' // Include cookies
                });

                if (response.ok) {
                    // Success - redirect to home
                    const data = await response.json();
                    window.location.href = '/';
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
