"""
Music Player, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

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

import json
import asyncio
from shlex import quote
from subprocess import PIPE
from datetime import timedelta
from aiohttp import ClientSession
from pyrogram.types import User, Message
from typing import Dict, Tuple, Optional, Union


class Song:
    def __init__(self, link: Union[str, dict], request_msg: Message) -> None:
        if isinstance(link, str):
            self.title: str = None
            self.duration: str = None
            self.thumb: str = None
            self.remote_url: str = None
            self.yt_url: str = link
            self.headers: dict = None
            self.request_msg: Message = request_msg
            self.requested_by: User = request_msg.from_user
            self.parsed: bool = False
            self._retries: int = 0
        elif isinstance(link, dict):
            self.title: str = "STREAM 24/7 | LIVE"
            self.duration: str = None
            self.thumb: str = "https://telegra.ph/file/820cac7cb7b1a025542e2.jpg"
            self.remote_url: str = link["url"]
            self.yt_url: str = link["url"]
            self.headers: dict = None
            self.request_msg: Message = request_msg
            self.requested_by: User = request_msg.from_user
            self.parsed: bool = True
            self._retries: int = 0

    async def parse(self) -> Tuple[bool, str]:
        if self._retries >= 5:
            return (False, "MAX_RETRY_LIMIT_REACHED")
        if self.parsed:
            return (True, "ALREADY_PARSED")
        process = await asyncio.create_subprocess_shell(
            f"yt-dlp --print-json --skip-download -f best {quote(self.yt_url)}",
            stdout=PIPE,
            stderr=PIPE,
        )
        out, _ = await process.communicate()
        try:
            video = json.loads(out.decode())
        except json.JSONDecodeError:
            self._retries += 1
            return await self.parse()
        check_audio = await self.check_remote_url(video["url"], video["http_headers"])
        check_image = await self.check_remote_url(
            video["thumbnail"], video["http_headers"]
        )
        if check_audio and check_image:
            if video["is_live"]:
                return (False, "LIVE_STREAM_ERROR")
            self.title = self._escape(video["title"])
            self.duration = str(timedelta(seconds=video["duration"]))
            self.thumb = video["thumbnail"]
            self.remote_url = video["url"]
            self.headers = video["http_headers"]
            self.parsed = True
            return (True, "PARSED")
        else:
            self._retries += 1
            return await self.parse()

    @staticmethod
    async def check_remote_url(
        path: str, headers: Optional[Dict[str, str]] = None
    ) -> bool:
        try:
            session = ClientSession()
            response = await session.get(path, timeout=5, headers=headers)
            response.close()
            await session.close()
            if response.status == 200:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def _escape(_title: str) -> str:
        title = _title
        f = ["**", "__", "`", "~~", "--"]
        for i in f:
            title = title.replace(i, f"\{i}")
        return title

    def to_dict(self) -> Dict[str, str]:
        return {"title": self.title, "yt_url": self.yt_url}
