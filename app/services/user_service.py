from app.db import get_db_connection
from typing import Tuple

def update_user_language(username: str, language: str) -> Tuple[bool, str]:
    """Updates the user's preferred language."""
    if language not in ["en", "es", "fr", "de", "hi", "zh", "ja", "ko", "ar", "ru"]:
        return False, "Invalid language"

    conn = get_db_connection()
    try:
        conn.execute("UPDATE users SET language = ? WHERE username = ?", 
                    (language, username))
        conn.commit()
        conn.close()
        return True, "Language updated successfully"
    except Exception as e:
        conn.close()
        return False, str(e)
