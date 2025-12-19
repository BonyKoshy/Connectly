import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string-2026'
    DB_PATH = os.path.join(os.getcwd(), 'chat.db') 
    REDIS_URL = os.environ.get('REDIS_URL') or "redis://localhost:6379"

config = {
    'default': Config
}