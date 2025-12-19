import asyncio
from taskiq import TaskiqEvents
from taskiq_redis import ListQueueBroker
from deep_translator import GoogleTranslator

# Redis Broker for TaskIQ
broker = ListQueueBroker(
    url="redis://localhost:6379"
)

@broker.task
def translate_message_task(text: str, target_lang: str) -> str:
    """
    Runs in a worker process. 
    Performs the blocking network call to Google Translate.
    """
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation failed: {e}")
        return text