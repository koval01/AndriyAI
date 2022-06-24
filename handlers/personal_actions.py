from aiogram import types
from aiogram.types import ContentType, ChatType
from apis.redis_history import History
from other.throttling import rate_limit
from other.messages import messages as msg_dict
from other.response import Response
from dispatcher import dp


@dp.message_handler(commands=['start', 'help', 'info'])
@rate_limit(1, 'start_command')
async def send_welcome(msg: types.Message):
    await msg.reply(msg_dict["start_message"])


@dp.message_handler(commands=['clear'])
@rate_limit(1, 'clear_history')
async def clear_history(msg: types.Message):
    result = await History(msg).write_history([])
    await msg.reply(
        msg_dict["clear_history"] % msg_dict["c_success"]
        if result else
        msg_dict["clear_history"] % msg_dict["c_fail"])


@dp.message_handler(
    content_types=ContentType.TEXT,
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
    is_reply=True)
@dp.message_handler(
    content_types=ContentType.TEXT,
    chat_type=[ChatType.PRIVATE])
@rate_limit(2.5, 'text_from_user')
async def text_messages(msg: types.Message):
    await Response(msg).exec(porfirevich=True)


@dp.message_handler(
    chat_type=[ChatType.PRIVATE],
    content_types=ContentType.ANY)
@rate_limit(0.6, 'any_messages')
async def any_messages(msg: types.Message):
    await msg.reply(msg_dict["unknown_response"])
