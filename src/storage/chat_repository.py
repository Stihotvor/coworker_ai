import json
import os
from typing import Type

import redis


# TODO: Add support to update the chat history record by record with the redis set
class ChatRepository:
    """
    Redis based chat repository. It stores the chat history for each user session. Individual chats are stored
    in separate keys in the Redis database. The key is the user session id and the value is the chat history.
    Data schema:
        {
            "user_session_id_1": [
                ["Hello, what is FRK", "FRK is the abbreviation for the First Responder Kit."],
                ["Where can I find the FRK documentation?", "You can find the FRK documentation at..."]
            ],
            "user_session_id_2": [
                ["Hello, what is FRK", "FRK is the abbreviation for the First Responder Kit."],
                ["Where can I find the FRK documentation?", "You can find the FRK documentation at..."]
            ]
        }

    """
    def __init__(self, cache_client_cls: Type["redis.Redis"] = redis.Redis):
        self._client = self.get_cache_client(cache_cls=cache_client_cls)

    def get_cache_client(self, cache_cls: Type["redis.Redis"]) -> "redis.Redis":
        connection_kwargs = {
            "host": os.getenv("REDIS_HOST"),
            "port": int(os.getenv("REDIS_PORT"))
        }
        return cache_cls(**connection_kwargs)

    def get_chat_history(self, user_session_id: str = "single_user") -> list[list[str]]:
        """Fetch the chat history for the given user session id."""
        result = self._client.get(user_session_id)
        if result:
            return json.loads(result)
        return []

    def update_chat_history(self, chat_history: list[list[str]], user_session_id: str = "single_user"):
        """Update the chat history for the given user session id."""
        chat_history = json.dumps(chat_history)
        self._client.set(user_session_id, chat_history)

    def reset_chat_history(self, user_session_id: str = "single_user"):
        """Reset the chat history for the given user session id."""
        self._client.delete(user_session_id)
