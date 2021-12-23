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

import os
import re
import random
import asyncio
import aiohttp
import aiofiles
from config import config
from core.song import Song
from pytube import Playlist
from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import PyTgCalls, StreamType
from PIL import Image, ImageDraw, ImageFont
from core.groups import get_group, set_title
from youtubesearchpython import VideosSearch
from typing import Optional, Tuple, AsyncIterator
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo


safone = {}
app = Client(config.SESSION, api_id=config.API_ID, api_hash=config.API_HASH)
pytgcalls = PyTgCalls(app)


themes = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
]


def search(message: Message) -> Optional[Song]:
    query = ""
    if message.reply_to_message:
        if message.reply_to_message.audio:
            query = message.reply_to_message.audio.title
        else:
            query = message.reply_to_message.text
    else:
        query = extract_args(message.text)
    if query == "":
        return None
    is_yt_url, url = check_yt_url(query)
    if is_yt_url:
        return Song(url, message)
    group = get_group(message.chat.id)
    vs = VideosSearch(
        query, limit=1, language=group["lang"], region=group["lang"]
    ).result()
    if len(vs["result"]) > 0 and vs["result"][0]["type"] == "video":
        video = vs["result"][0]
        return Song(video["link"], message)
    return None


def check_yt_url(text: str) -> Tuple[bool, Optional[str]]:
    pattern = re.compile(
        "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)([a-zA-Z0-9-_]+)?$"
    )
    matches = re.findall(pattern, text)
    if len(matches) <= 0:
        return False, None

    match = "".join(list(matches[0]))
    return True, match


def extract_args(text: str) -> str:
    if " " not in text:
        return ""
    else:
        return text.split(" ", 1)[1]


async def delete_messages(messages):
    await asyncio.sleep(config.TIMEOUT)
    for msg in messages:
        if msg.chat.type == "supergroup":
            try:
                await msg.delete()
            except:
                pass


async def skip_stream(song: Song, lang):
    chat_id = song.request_msg.chat.id
    if safone.get(chat_id) is not None:
        try:
            await safone[chat_id].delete()
        except:
            pass
    group = get_group(chat_id)
    infomsg = await song.request_msg.reply_text(lang["downloading"])
    if group["is_video"]:
        await pytgcalls.change_stream(
            chat_id,
            AudioVideoPiped(
                song.remote_url, HighQualityAudio(), HighQualityVideo(), song.headers
            ),
        )
    else:
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(song.remote_url, HighQualityAudio(), song.headers),
        )
    await set_title(chat_id, song.title, client=app)
    thumb = await generate_cover(
        song.title,
        song.request_msg.chat.title,
        song.request_msg.chat.id,
        song.thumb,
    )
    safone[chat_id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"]
        % (
            song.title,
            song.yt_url,
            song.duration,
            song.request_msg.chat.id,
            song.requested_by.mention
            if song.requested_by
            else song.request_msg.sender_chat.title,
        ),
    )
    await infomsg.delete()
    os.remove(thumb)


async def start_stream(song: Song, lang):
    chat_id = song.request_msg.chat.id
    if safone.get(chat_id) is not None:
        try:
            await safone[chat_id].delete()
        except:
            pass
    group = get_group(chat_id)
    infomsg = await song.request_msg.reply_text(lang["downloading"])
    if group["is_video"]:
        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(
                song.remote_url, HighQualityAudio(), HighQualityVideo(), song.headers
            ),
            stream_type=StreamType().pulse_stream,
        )
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(song.remote_url, HighQualityAudio(), song.headers),
            stream_type=StreamType().pulse_stream,
        )
    await set_title(chat_id, song.title, client=app)
    thumb = await generate_cover(
        song.title,
        song.request_msg.chat.title,
        song.request_msg.chat.id,
        song.thumb,
    )
    safone[chat_id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"]
        % (
            song.title,
            song.yt_url,
            song.duration,
            song.request_msg.chat.id,
            song.requested_by.mention
            if song.requested_by
            else song.request_msg.sender_chat.title,
        ),
    )
    await infomsg.delete()
    os.remove(thumb)


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(title, ctitle, chatid, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb_{chatid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    theme = random.choice(themes)
    image1 = Image.open(f"cache/thumb_{chatid}.png")
    image2 = Image.open(f"theme/{theme}.PNG")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save(f"cache/temp_{chatid}.png")
    img = Image.open(f"cache/temp_{chatid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("theme/font.ttf", 85)
    font2 = ImageFont.truetype("theme/font.ttf", 60)
    draw.text(
        (20, 45),
        f"Playing on: {ctitle[:14]}...",
        fill="white",
        stroke_width=1,
        stroke_fill="white",
        font=font2,
    )
    draw.text(
        (25, 595),
        f"{title[:27]}...",
        fill="white",
        stroke_width=2,
        stroke_fill="white",
        font=font,
    )
    img.save(f"cache/final_{chatid}.png")
    os.remove(f"cache/temp_{chatid}.png")
    os.remove(f"cache/thumb_{chatid}.png")
    return f"cache/final_{chatid}.png"


async def get_youtube_playlist(pl_url: str, message: Message) -> AsyncIterator[Song]:
    pl = Playlist(pl_url)
    for i in range(len(list(pl))):
        song = Song(pl[i], message)
        song.title = pl.videos[i].title
        yield song
