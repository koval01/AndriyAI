import aioredis
import json
from aiogram.types import Message
from config import REDIS_URL
from typing import List
import logging as log


class History:

    def __init__(self, message: Message, ai_response: str = None) -> None:
        self.max_len_list = 350
        self.message = message
        self.ai_response = ai_response
        self.r = aioredis.from_url(
            REDIS_URL, encoding="utf-8",
            decode_responses=True, max_connections=20)

    @property
    async def get_history(self) -> List[dict]:
        try:
            value = await self.r.hget("chat", self.message.from_user.id)
            await self.r.close()
            return json.loads(value)
        except Exception as e:
            log.info("Error get data from Redis. Details: %s" % e)
            return []

    async def write_history(self, history: list) -> bool:
        try:
            await self.r.hset(
                "chat", self.message.from_user.id,
                json.dumps(history))
            await self.r.close()
            return True
        except Exception as e:
            log.warning("Error write history. Details: %s" % e)
            return False

    def _cut_long_list(self, list_: list) -> list:
        return list_[-self.max_len_list:] \
            if list_[-1]["sender"] == "bot" \
            else list_[-self.max_len_list-1:]

    @property
    async def add_message(self) -> bool:
        try:
            history = await self.get_history
            history.append({"sender": "user", "text": self.message.text})
            history.append({"sender": "bot", "text": self.ai_response})
            history = self._cut_long_list(history)
            await self.write_history(history)
            return True
        except Exception as e:
            log.error("Error write message to history. Details: %s" % e)
            return False
