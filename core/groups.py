"""
Music Player, Telegram Voice Chat Bot
Copyright (c) 2021-present Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from config import config
from core.queue import Queue
from pyrogram.types import Message
from typing import Any, Dict, Union
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle


GROUPS: Dict[int, Dict[str, Any]] = {}


def all_groups():
    return GROUPS.keys()


def set_default(chat_id: int) -> None:
    global GROUPS
    GROUPS[chat_id] = {}
    GROUPS[chat_id]["is_playing"] = False
    GROUPS[chat_id]["now_playing"] = None
    GROUPS[chat_id]["stream_mode"] = config.STREAM_MODE
    GROUPS[chat_id]["admins_only"] = config.ADMINS_ONLY
    GROUPS[chat_id]["loop"] = False
    GROUPS[chat_id]["lang"] = config.LANGUAGE
    GROUPS[chat_id]["queue"] = Queue()


def get_group(chat_id) -> Dict[str, Any]:
    if chat_id not in all_groups():
        set_default(chat_id)
    return GROUPS[chat_id]


def set_group(chat_id: int, **kwargs) -> None:
    global GROUPS
    for key, value in kwargs.items():
        GROUPS[chat_id][key] = value


async def set_title(message_or_chat_id: Union[Message, int], title: str, **kw):
    if isinstance(message_or_chat_id, Message):
        client = message_or_chat_id._client
        chat_id = message_or_chat_id.chat.id
    elif isinstance(message_or_chat_id, int):
        client = kw.get("client")
        chat_id = message_or_chat_id
    try:
        peer = await client.resolve_peer(chat_id)
        chat = await client.send(GetFullChannel(channel=peer))
        await client.send(EditGroupCallTitle(call=chat.full_chat.call, title=title))
    except BaseException:
        pass


def get_queue(chat_id: int) -> Queue:
    return GROUPS[chat_id]["queue"]


def clear_queue(chat_id: int) -> None:
    global GROUPS
    GROUPS[chat_id]["queue"].clear()


def shuffle_queue(chat_id: int) -> Queue:
    global GROUPS
    return GROUPS[chat_id]["queue"].shuffle()
