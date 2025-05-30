
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

## Preview

### Landing Page
![Index](screenshots/index.png)

### Register Page
![Register](screenshots/register.png)

### Login Page
![Login](screenshots/login.png)

### Chat List
![Chat List](screenshots/chat_list.png)

### Sidebar View
![Sidebar](screenshots/side_bar.png)

### Chat Search
![Search](screenshots/search_list.png)

### Chat Interface
![Chat Page](screenshots/Chat_Page.png)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/BonyKoshy/Connectly.git
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
<!-- Modern Icon Button Contact Section -->

<div style="display: flex; gap: 1rem; align-items: center;">
  <!-- Email -->
  <a href="mailto:bonykoshy@gmail.com" title="Email">
    <img src="https://img.icons8.com/ios-filled/50/006bed/new-post.png" width="32" height="32" alt="Email Icon"/>
  </a>

  <!-- LinkedIn -->
  <a href="https://linkedin.com/in/bonykoshy" target="_blank" title="LinkedIn">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="32" height="32" alt="LinkedIn Icon"/>
  </a>

  <!-- GitHub -->
  <a href="https://github.com/BonyKoshy" target="_blank" title="GitHub">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="32" height="32" alt="GitHub Icon"/>
  </a>

  <!-- Instagram -->
  <a href="https://instagram.com/bonn_i.e" target="_blank" title="Instagram">
    <img src="https://img.icons8.com/ios-filled/50/E4405F/instagram-new.png" width="32" height="32" alt="Instagram Icon"/>
  </a>
</div>

