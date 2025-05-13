
# Connectly: AI-Enhanced Multilingual Chat Application

Connectly is a real-time chat application built with **Python Flask**, using **Flask-SocketIO** for WebSocket communication and **Deep Translator API** for AI-powered multilingual support. It provides secure user authentication, real-time messaging, and instant translation across different languages.

---

## Features
- Real-time one-on-one chat
- AI-powered live translation using Deep Translator
- Secure login with hashed passwords
- Language preference selection per user
- Responsive UI using Bootstrap
- Error handling pages (400, 401, 403, 404)
- SQLite database for lightweight deployment

---

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python, Flask, Flask-SocketIO
- **Database**: SQLite
- **APIs**: Deep Translator, Google ReCAPTCHA
- **Authentication**: Password hashing (SHA256)

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/connectly.git
   cd connectly
   ```

2. **Create Virtual Environment & Activate**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

---

## Project Structure
```
CONNECTLY/
├── static/
│   ├── css/
│   ├── js/
│   └── fonts/
├── templates/
├── app.py
├── chat.db
└── requirements.txt
```

---

## Database Schema
- **Users Table**: Stores user details, hashed password, language.
- **Chats Table**: Stores chat messages, timestamps, and translations.

---

## License
This project is licensed under the **MIT License**.

---

## Author
**Bony Koshy**  
BCA, CMS College of Science & Commerce  
https://www.linkedin.com/in/bonykoshy
