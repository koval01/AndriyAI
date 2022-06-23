from apis.openai_module import AiResponse
from apis.translate import Translate
from apis.redis_history import History
from aiogram.types import Message


class Response:

    def __init__(self, message: Message) -> None:
        self.message = message

    @staticmethod
    def build_prompt(list_: list) -> str:
        return "".join([
            f'{"You: " if m["sender"] == "user" else "Friend: "}{m["text"]}\n'
            for m in list_
        ])

    @property
    def check_message(self) -> bool:
        if len(self.message.text) < 120:
            return False

    @property
    async def _build_resp(self) -> bool:
        await self.message.answer_chat_action("typing")
        eng_text = str(Translate("uk", "en", self.message.text.strip()))
        history = await History(self.message).get_history
        resp = str(AiResponse(
                eng_text, prompt=self.build_prompt(history)
            ))
        resp_tr = str(Translate(
            "en", "uk", resp))
        self.message.text = eng_text
        write_result = await History(self.message, resp).add_message
        if write_result:
            await self.message.reply(resp_tr)
            return True
        return False

    @property
    async def exec(self) -> bool:
        resp = await self._build_resp
        return resp
