from aiogram.types import Message

from apis.openai_module import AiResponse
from apis.porfirevich_api import Porfirevich
from apis.redis_history import History
from apis.translate import Translate


class Response:

    def __init__(self, message: Message) -> None:
        self.message = message

    @staticmethod
    def build_prompt(list_: list, porfirevich: bool) -> str:
        return "".join([
            f'{"%s: " % ["You", "Ты"][int(porfirevich)] if m["sender"] == "user" else "%s: " % ["Friend", "Друг"][int(porfirevich)]}{m["text"]}\n '
            for m in list_
        ])

    @property
    def check_message(self) -> bool:
        if len(self.message.text) < 120:
            return False

    @staticmethod
    def _get_resp(org_text: str, prompt: str, porfirevich: bool) -> str:
        return str(Porfirevich(text=org_text, prompt=prompt)) if porfirevich \
            else str(AiResponse(text=org_text, prompt=prompt))

    async def _build_resp(self, porfirevich: bool) -> bool:
        await self.message.answer_chat_action("typing")
        lang_mode = "ru" if porfirevich else "en"
        org_text = str(Translate("uk", lang_mode, self.message.text.strip()))
        history = await History(self.message).get_history
        resp = self._get_resp(
            org_text, prompt=self.build_prompt(
                history, porfirevich=porfirevich),
            porfirevich=porfirevich)
        resp_tr = str(Translate(
            lang_mode, "uk", resp))
        self.message.text = org_text
        write_result = await History(self.message, resp).add_message
        if write_result:
            await self.message.reply(resp_tr)
            return True
        return False

    async def exec(self, porfirevich: bool = False) -> bool:
        resp = await self._build_resp(porfirevich=porfirevich)
        return resp
