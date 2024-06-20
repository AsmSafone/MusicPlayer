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
from pyrogram import enums
from pyrogram.types import Message


async def is_sudo(message: Message):
    if message.from_user and message.from_user.id in config.SUDOERS:
        return True
    else:
        return False


async def is_admin(message: Message):
    if message.from_user:
        user = await message.chat.get_member(message.from_user.id)
        if user.status in [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        ]:
            return True
        elif message.from_user.id in config.SUDOERS:
            return True
    elif message.sender_chat:
        if message.sender_chat.id == message.chat.id:
            return True
    else:
        return False
