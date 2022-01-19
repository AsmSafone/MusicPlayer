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
import json
import shutil
from config import config
from core.song import Song
from pyrogram.types import Message
from pytgcalls.types import Update
from pyrogram import Client, filters
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded
from core.decorators import language, register, only_admins, handle_error
from core import (
    app, ydl, safone, search, is_sudo, is_admin, get_group, get_queue,
    pytgcalls, set_group, set_title, all_groups, clear_queue, skip_stream,
    check_yt_url, extract_args, start_stream, shuffle_queue, delete_messages,
    get_spotify_playlist, get_youtube_playlist)


REPO = """
🤖 **Music Player**
- Repo: [GitHub](https://github.com/AsmSafone/MusicPlayer)
- License: AGPL-3.0-or-later
"""

if config.BOT_TOKEN:
    bot = Client(
        "MusicPlayer",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
    )
    client = bot
else:
    client = app


@client.on_message(
    filters.command("repo", config.PREFIXES) & ~filters.bot & ~filters.edited
)
@handle_error
async def repo(_, message: Message):
    await message.reply_text(REPO, disable_web_page_preview=True)


@client.on_message(
    filters.command("ping", config.PREFIXES) & ~filters.bot & ~filters.edited
)
@handle_error
async def ping(_, message: Message):
    await message.reply_text(f"🤖 **Pong!**\n`{await pytgcalls.ping} ms`")


@client.on_message(
    filters.command("start", config.PREFIXES) & ~filters.bot & ~filters.edited
)
@language
@handle_error
async def start(_, message: Message, lang):
    await message.reply_text(lang["startText"] % message.from_user.mention)


@client.on_message(
    filters.command("help", config.PREFIXES) & ~filters.private & ~filters.edited
)
@language
@handle_error
async def help(_, message: Message, lang):
    await message.reply_text(lang["helpText"].replace("<prefix>", config.PREFIXES[0]))


@client.on_message(
    filters.command(["p", "play"], config.PREFIXES) & ~filters.private & ~filters.edited
)
@register
@language
@handle_error
async def play_stream(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["admins_only"]:
        check = await is_admin(message)
        if not check:
            k = await message.reply_text(lang["notAllowed"])
            return await delete_messages([message, k])
    song = await search(message)
    if song is None:
        k = await message.reply_text(lang["notFound"])
        return await delete_messages([message, k])
    ok, status = await song.parse()
    if not ok:
        raise Exception(status)
    if not group["is_playing"]:
        set_group(chat_id, is_playing=True, now_playing=song)
        await start_stream(song, lang)
        await delete_messages([message])
    else:
        queue = get_queue(chat_id)
        await queue.put(song)
        k = await message.reply_text(
            lang["addedToQueue"] % (song.title, song.source, len(queue)),
            disable_web_page_preview=True,
        )
        await delete_messages([message, k])


@client.on_message(
    filters.command(["radio", "stream"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@handle_error
async def live_stream(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["admins_only"]:
        check = await is_admin(message)
        if not check:
            k = await message.reply_text(lang["notAllowed"])
            return await delete_messages([message, k])
    args = extract_args(message.text)
    if args is None:
        k = await message.reply_text(lang["notFound"])
        return await delete_messages([message, k])
    if " " in args and args.count(" ") == 1 and args[-5:] == "parse":
        song = Song({"source": args.split(" ")[0], "parsed": False}, message)
    else:
        is_yt_url, url = check_yt_url(args)
        if is_yt_url:
            meta = ydl.extract_info(url, download=False)
            formats = meta.get("formats", [meta])
            for f in formats:
                ytstreamlink = f["url"]
            link = ytstreamlink
            song = Song(
                {"title": "YouTube Stream", "source": link, "remote": link}, message
            )
        else:
            song = Song(
                {"title": "Live Stream", "source": args, "remote": args}, message
            )
    ok, status = await song.parse()
    if not ok:
        raise Exception(status)
    if not group["is_playing"]:
        set_group(chat_id, is_playing=True, now_playing=song)
        await start_stream(song, lang)
        await delete_messages([message])
    else:
        queue = get_queue(chat_id)
        await queue.put(song)
        k = await message.reply_text(
            lang["addedToQueue"] % (song.title, song.source, len(queue)),
            disable_web_page_preview=True,
        )
        await delete_messages([message, k])


@client.on_message(
    filters.command(["skip", "next"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def skip_track(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["loop"]:
        await skip_stream(group["now_playing"], lang)
    else:
        queue = get_queue(chat_id)
        if len(queue) > 0:
            next_song = await queue.get()
            if not next_song.parsed:
                ok, status = await next_song.parse()
                if not ok:
                    raise Exception(status)
            set_group(chat_id, now_playing=next_song)
            await skip_stream(next_song, lang)
            await delete_messages([message])
        else:
            set_group(chat_id, is_playing=False, now_playing=None)
            await set_title(message, "")
            try:
                await pytgcalls.leave_group_call(chat_id)
                k = await message.reply_text(lang["queueEmpty"])
            except (NoActiveGroupCall, GroupCallNotFound):
                k = await message.reply_text(lang["notActive"])
            await delete_messages([message, k])


@client.on_message(
    filters.command(["m", "mute"], config.PREFIXES) & ~filters.private & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def mute_vc(_, message: Message, lang):
    chat_id = message.chat.id
    try:
        await pytgcalls.mute_stream(chat_id)
        k = await message.reply_text(lang["muted"])
    except (NoActiveGroupCall, GroupCallNotFound):
        k = await message.reply_text(lang["notActive"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["um", "unmute"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def unmute_vc(_, message: Message, lang):
    chat_id = message.chat.id
    try:
        await pytgcalls.unmute_stream(chat_id)
        k = await message.reply_text(lang["unmuted"])
    except (NoActiveGroupCall, GroupCallNotFound):
        k = await message.reply_text(lang["notActive"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["ps", "pause"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def pause_vc(_, message: Message, lang):
    chat_id = message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        k = await message.reply_text(lang["paused"])
    except (NoActiveGroupCall, GroupCallNotFound):
        k = await message.reply_text(lang["notActive"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["rs", "resume"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def resume_vc(_, message: Message, lang):
    chat_id = message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        k = await message.reply_text(lang["resumed"])
    except (NoActiveGroupCall, GroupCallNotFound):
        k = await message.reply_text(lang["notActive"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["stop", "leave"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def leave_vc(_, message: Message, lang):
    chat_id = message.chat.id
    set_group(chat_id, is_playing=False, now_playing=None)
    await set_title(message, "")
    clear_queue(chat_id)
    try:
        await pytgcalls.leave_group_call(chat_id)
        k = await message.reply_text(lang["leaveVC"])
    except (NoActiveGroupCall, GroupCallNotFound):
        k = await message.reply_text(lang["notActive"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["list", "queue"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@handle_error
async def queue_list(_, message: Message, lang):
    chat_id = message.chat.id
    queue = get_queue(chat_id)
    if len(queue) > 0:
        k = await message.reply_text(str(queue), disable_web_page_preview=True)
    else:
        k = await message.reply_text(lang["queueEmpty"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["mix", "shuffle"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def shuffle_list(_, message: Message, lang):
    chat_id = message.chat.id
    if len(get_queue(chat_id)) > 0:
        shuffled = shuffle_queue(chat_id)
        k = await message.reply_text(str(shuffled), disable_web_page_preview=True)
    else:
        k = await message.reply_text(lang["queueEmpty"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["loop", "repeat"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def loop_stream(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["loop"]:
        set_group(chat_id, loop=False)
        k = await message.reply_text(lang["loopMode"] % "Disabled")
    elif group["loop"] == False:
        set_group(chat_id, loop=True)
        k = await message.reply_text(lang["loopMode"] % "Enabled")
    await delete_messages([message, k])


@client.on_message(
    filters.command(["mode", "switch"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def switch_mode(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["stream_mode"] == "audio":
        set_group(chat_id, stream_mode="video")
        k = await message.reply_text(lang["videoMode"])
    else:
        set_group(chat_id, stream_mode="audio")
        k = await message.reply_text(lang["audioMode"])
    await delete_messages([message, k])


@client.on_message(
    filters.command(["admins", "adminsonly"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def admins_only(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["admins_only"]:
        set_group(chat_id, admins_only=False)
        k = await message.reply_text(lang["adminsOnly"] % "Disabled")
    else:
        set_group(chat_id, admins_only=True)
        k = await message.reply_text(lang["adminsOnly"] % "Enabled")
    await delete_messages([message, k])


@client.on_message(
    filters.command(["lang", "language"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def set_lang(_, message: Message, lang):
    chat_id = message.chat.id
    lng = extract_args(message.text)
    if lng != "":
        langs = [
            file.replace(".json", "")
            for file in os.listdir(f"{os.getcwd()}/lang/")
            if file.endswith(".json")
        ]
        if lng == "list":
            k = await message.reply_text("\n".join(langs))
        elif lng in langs:
            set_group(chat_id, lang=lng)
            k = await message.reply_text(lang["langSet"] % lng)
        else:
            k = await message.reply_text(lang["notFound"])
        await delete_messages([message, k])


@client.on_message(
    filters.command(["ep", "export"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def export_queue(_, message: Message, lang):
    chat_id = message.chat.id
    queue = get_queue(chat_id)
    if len(queue) > 0:
        data = json.dumps([song.to_dict() for song in queue], indent=2)
        filename = f"{message.chat.username or message.chat.id}.json"
        with open(filename, "w") as file:
            file.write(data)
        await message.reply_document(
            filename, caption=lang["queueExported"] % len(queue)
        )
        os.remove(filename)
        await delete_messages([message])
    else:
        k = await message.reply_text(lang["queueEmpty"])
        await delete_messages([message, k])


@client.on_message(
    filters.command(["ip", "import"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@only_admins
@handle_error
async def import_queue(_, message: Message, lang):
    if not message.reply_to_message or not message.reply_to_message.document:
        k = await message.reply_text(lang["replyToAFile"])
        return await delete_messages([message, k])
    chat_id = message.chat.id
    filename = await message.reply_to_message.download()
    data_str = None
    with open(filename, "r") as file:
        data_str = file.read()
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        k = await message.reply_text(lang["invalidFile"])
        return await delete_messages([message, k])
    try:
        temp_queue = []
        for song_dict in data:
            song = Song(song_dict["source"], message)
            song.title = song_dict["title"]
            temp_queue.append(song)
    except BaseException:
        k = await message.reply_text(lang["invalidFile"])
        return await delete_messages([message, k])
    group = get_group(chat_id)
    queue = get_queue(chat_id)
    if group["is_playing"]:
        for _song in temp_queue:
            await queue.put(_song)
    else:
        song = temp_queue[0]
        set_group(chat_id, is_playing=True, now_playing=song)
        ok, status = await song.parse()
        if not ok:
            raise Exception(status)
        await start_stream(song, lang)
        for _song in temp_queue[1:]:
            await queue.put(_song)
    k = await message.reply_text(lang["queueImported"] % len(temp_queue))
    await delete_messages([message, k])


@client.on_message(
    filters.command(["pl", "playlist"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@register
@language
@handle_error
async def import_playlist(_, message: Message, lang):
    chat_id = message.chat.id
    group = get_group(chat_id)
    if group["admins_only"]:
        check = await is_admin(message)
        if not check:
            k = await message.reply_text(lang["notAllowed"])
            return await delete_messages([message, k])
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = extract_args(message.text)
    if text == "":
        k = await message.reply_text(lang["notFound"])
        return await delete_messages([message, k])
    if "youtube.com/playlist?list=" in text:
        try:
            temp_queue = get_youtube_playlist(text, message)
        except BaseException:
            k = await message.reply_text(lang["notFound"])
            return await delete_messages([message, k])
    elif "open.spotify.com/playlist/" in text:
        if not config.SPOTIFY:
            k = await message.reply_text(lang["spotifyNotEnabled"])
            return await delete_messages([message, k])
        try:
            temp_queue = get_spotify_playlist(text, message)
        except BaseException:
            k = await message.reply_text(lang["notFound"])
            return await delete_messages([message, k])
    else:
        k = await message.reply_text(lang["invalidFile"])
        return await delete_messages([message, k])
    queue = get_queue(chat_id)
    if not group["is_playing"]:
        song = await temp_queue.__anext__()
        set_group(chat_id, is_playing=True, now_playing=song)
        ok, status = await song.parse()
        if not ok:
            raise Exception(status)
        await start_stream(song, lang)
        async for _song in temp_queue:
            await queue.put(_song)
        queue.get_nowait()
    else:
        async for _song in temp_queue:
            await queue.put(_song)
    k = await message.reply_text(lang["queueImported"] % len(group["queue"]))
    await delete_messages([message, k])


@client.on_message(
    filters.command(["update", "restart"], config.PREFIXES)
    & ~filters.private
    & ~filters.edited
)
@language
@handle_error
async def update_restart(_, message: Message, lang):
    check = await is_sudo(message)
    if not check:
        k = await message.reply_text(lang["notAllowed"])
        return await delete_messages([message, k])
    chats = all_groups()
    stats = await message.reply_text(lang["update"])
    for chat in chats:
        try:
            await pytgcalls.leave_group_call(chat)
        except (NoActiveGroupCall, GroupCallNotFound):
            pass
    await stats.edit_text(lang["restart"])
    shutil.rmtree("downloads", ignore_errors=True)
    os.system(f"kill -9 {os.getpid()} && bash startup.sh")


@pytgcalls.on_stream_end()
@language
@handle_error
async def stream_end(_, update: Update, lang):
    if isinstance(update, StreamAudioEnded) or isinstance(update, StreamVideoEnded):
        chat_id = update.chat_id
        group = get_group(chat_id)
        if group["loop"]:
            await skip_stream(group["now_playing"], lang)
        else:
            queue = get_queue(chat_id)
            if len(queue) > 0:
                next_song = await queue.get()
                if not next_song.parsed:
                    ok, status = await next_song.parse()
                    if not ok:
                        raise Exception(status)
                set_group(chat_id, now_playing=next_song)
                await skip_stream(next_song, lang)
            else:
                if safone.get(chat_id) is not None:
                    try:
                        await safone[chat_id].delete()
                    except BaseException:
                        pass
                await set_title(chat_id, "", client=app)
                set_group(chat_id, is_playing=False, now_playing=None)
                await pytgcalls.leave_group_call(chat_id)


@pytgcalls.on_closed_voice_chat()
@handle_error
async def closed_vc(_, chat_id: int):
    if chat_id not in all_groups():
        if safone.get(chat_id) is not None:
            try:
                await safone[chat_id].delete()
            except BaseException:
                pass
        await set_title(chat_id, "", client=app)
        set_group(chat_id, now_playing=None, is_playing=False)
        clear_queue(chat_id)


@pytgcalls.on_kicked()
@handle_error
async def kicked_vc(_, chat_id: int):
    if chat_id not in all_groups():
        if safone.get(chat_id) is not None:
            try:
                await safone[chat_id].delete()
            except BaseException:
                pass
        await set_title(chat_id, "", client=app)
        set_group(chat_id, now_playing=None, is_playing=False)
        clear_queue(chat_id)


@pytgcalls.on_left()
@handle_error
async def left_vc(_, chat_id: int):
    if chat_id not in all_groups():
        if safone.get(chat_id) is not None:
            try:
                await safone[chat_id].delete()
            except BaseException:
                pass
        await set_title(chat_id, "", client=app)
        set_group(chat_id, now_playing=None, is_playing=False)
        clear_queue(chat_id)


client.start()
pytgcalls.run()
