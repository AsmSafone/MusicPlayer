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

import random
import asyncio


class Queue(asyncio.Queue):
    def __init__(self) -> None:
        super().__init__()

    def clear(self) -> None:
        self._queue.clear()
        self._init(0)

    def shuffle(self) -> "Queue":
        copy = list(self._queue.copy())
        copy.sort(key=lambda _: random.randint(0, 999999999))
        self.clear()
        self._queue.extend(copy)
        return self

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self):
            raise StopIteration

        item = self._queue[self.__index]
        self.__index += 1
        return item

    def __len__(self):
        return len(self._queue)

    def __getitem__(self, index):
        return self._queue[index]

    def __str__(self):
        queue = list(self._queue)
        string = ""
        for x, item in enumerate(queue):
            if x < 10:
                string += f"**{x+1}. [{item.title}]({item.source})** \n- Requested By: {item.requested_by.mention if item.requested_by else item.request_msg.sender_chat.title}\n"
            else:
                string += f"`\n...{len(queue)-10}`"
                return string
        return string
