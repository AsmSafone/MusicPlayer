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

import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self) -> None:
        self.API_ID: str = os.environ.get("27015202", None)
        self.API_HASH: str = os.environ.get("b817ca2d21c5471522ec93b819301d56", None)
        self.SESSION: str = os.environ.get("BQGcOCIAiYG0zbq7iIKoUCvarFjUwL7iU4IoitKLMwXTcHbXQMg6gkoyfEGszEeX5LzO6VyaAxjNkU7numNNVmUMel-Z0HllWPWMowMu2kFYMSNhL6T_nOHd4o7BPqHv9byZbZHXs8MHip-akQgfIZcF3-L2ln5vdCCaTuPbhXpqRjjy2EKrL_k2a3kZf50slrnupV_N0scjCLpzr35cOOG_GTqgVDJIQc9QbQnjT-raFuDeg51F-oHPtkuh7oHj-5cZtyUGoZvEnztcwA75-d3KMnCweprIBP4YR0JSCCTVRaLkT5r0jKge4OBISbZdfY-UMTKWg9CHHWbunZt9F7wljBs8iwAAAAGYTkO_AA", None)
        self.BOT_TOKEN: str = os.environ.get("7821128321:AAHUy0jo5JFoRTmYNNf5xBwLxrqxTQ_1oac", None)
        self.SUDOERS: list = [
            int(id) for id in os.environ.get("SUDOERS", "5789538424").split() if id.isnumeric()
        ]
        if not self.SESSION or not self.API_ID or not self.API_HASH:
            print("ERROR: SESSION, API_ID and API_HASH is required!")
            quit(0)
        self.SPOTIFY: bool = False
        self.QUALITY: str = os.environ.get("QUALITY", "high").lower()
        self.PREFIXES: list = os.environ.get("PREFIX", "!").split()
        self.LANGUAGE: str = os.environ.get("LANGUAGE", "en").lower()
        self.STREAM_MODE: str = (
            "audio"
            if (os.environ.get("STREAM_MODE", "audio").lower() == "audio")
            else "video"
        )
        self.ADMINS_ONLY: bool = os.environ.get("ADMINS_ONLY", False)
        self.SPOTIFY_CLIENT_ID: str = os.environ.get("SPOTIFY_CLIENT_ID", None)
        self.SPOTIFY_CLIENT_SECRET: str = os.environ.get("SPOTIFY_CLIENT_SECRET", None)


config = Config()
