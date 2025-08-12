from langchain_community.chat_message_histories import PostgresChatMessageHistory
from app.core.config import settings

def get_memory(session_id: str):
    return PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=settings.DB_CONNECTION_STRING,
        table_name="message_database_2"
    )
