from collections import OrderedDict
from threading import RLock
from time import monotonic
from typing import Literal, TypedDict


class ConversationMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class ChatHistoryStore:
    """Small process-local store for recent turns in each conversation."""

    def __init__(
        self,
        max_conversations: int = 500,
        max_turns: int = 8,
        ttl_seconds: int = 24 * 60 * 60,
        max_message_chars: int = 4000,
    ) -> None:
        self.max_conversations = max_conversations
        self.max_turns = max_turns
        self.ttl_seconds = ttl_seconds
        self.max_message_chars = max_message_chars
        self._items: OrderedDict[str, tuple[float, list[ConversationMessage]]] = OrderedDict()
        self._lock = RLock()

    def get_history(self, conversation_id: str) -> list[ConversationMessage]:
        with self._lock:
            now = monotonic()
            self._purge_expired(now)
            item = self._items.get(conversation_id)
            if item is None:
                return []

            self._items[conversation_id] = (now, item[1])
            self._items.move_to_end(conversation_id)
            return [dict(message) for message in item[1]]

    def append_turn(self, conversation_id: str, question: str, answer: str) -> None:
        with self._lock:
            now = monotonic()
            self._purge_expired(now)
            item = self._items.get(conversation_id)
            messages = list(item[1]) if item else []
            messages.extend([
                {"role": "user", "content": question[:self.max_message_chars]},
                {"role": "assistant", "content": answer[:self.max_message_chars]},
            ])
            messages = messages[-(self.max_turns * 2):]
            self._items[conversation_id] = (now, messages)
            self._items.move_to_end(conversation_id)

            while len(self._items) > self.max_conversations:
                self._items.popitem(last=False)

    def _purge_expired(self, now: float) -> None:
        expired = [
            conversation_id
            for conversation_id, (updated_at, _) in self._items.items()
            if now - updated_at > self.ttl_seconds
        ]
        for conversation_id in expired:
            self._items.pop(conversation_id, None)
