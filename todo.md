# Connectly Project To-Do List

## 🚨 Critical Security Issues

- [ ] **Fix Plain Text Passwords**: Implement password hashing (e.g., using `werkzeug.security`) in `app.py` for both registration and login routes. Never store raw passwords.
- [ ] **Verify Google ReCAPTCHA**: Add backend validation in the `register` route to verify the captcha token sent from the frontend. Currently, it is displayed but ignored.
- [ ] **Secure Secret Key**: Replace the hardcoded `app.secret_key = "your_secret_key"` with an environment variable (e.g., `os.environ.get('SECRET_KEY')`) to prevent session forgery.
- [ ] **Remove Sensitive Data**: Delete `chat.db` from the repository history and ensure it is listed in `.gitignore` to prevent leaking user data.

## 🐛 Functional Bugs & Logic

- [ ] **Fix Register Page JS**: Update `static/js/register.js` to select the container by class (`.form-container`) instead of ID (`#container`), or update the HTML ID to match.
- [ ] **Add CSRF Protection**: Implement `Flask-WTF`'s `CSRFProtect` to secure forms in `register.html` and `login.html` against Cross-Site Request Forgery.
- [ ] **Clean Up Imports**: Remove duplicate `import sqlite3` statements in `app.py`.

## ⚠️ Best Practices & Configuration

- [ ] **Disable Debug Mode**: Ensure `debug=True` is disabled in `socketio.run()` for production environments to prevent arbitrary code execution vulnerabilities.
- [ ] **Improve Room Logic**: Refactor the room name parsing logic (`room.split('_')[1:]`) in `app.py` to be more robust against usernames containing underscores or future group chat naming conventions.
- [ ] **Database Migrations**: Replace the `try-except` block in `init_db` with a proper migration tool like `Flask-Migrate` for handling schema changes (e.g., adding columns).
- [ ] **Add .gitignore**: Create a `.gitignore` file to exclude `__pycache__`, `*.db`, `.env`, and IDE settings.
