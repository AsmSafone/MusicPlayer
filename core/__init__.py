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

from core.funcs import (
    app,
    ydl,
    search,
    safone,
    pytgcalls,
    extract_args,
    check_yt_url,
    skip_stream,
    start_stream,
    generate_cover,
    delete_messages,
    get_youtube_playlist,
)
from core.groups import (
    all_groups,
    set_default,
    get_group,
    set_group,
    set_title,
    get_queue,
    clear_queue,
    shuffle_queue,
)
from core.song import Song
