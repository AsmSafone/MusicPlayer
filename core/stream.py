import os
from typing import Union
from config import config
from core.song import Song
from pyrogram import Client
from core.funcs import generate_cover
from pytgcalls import PyTgCalls, StreamType
from core.groups import get_group, set_title
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall
from pytgcalls.types.input_stream.quality import (
    LowQualityAudio, LowQualityVideo, HighQualityAudio, HighQualityVideo,
    MediumQualityAudio, MediumQualityVideo)


safone = {}
app = Client(config.SESSION, api_id=config.API_ID, api_hash=config.API_HASH)
pytgcalls = PyTgCalls(app)


async def skip_stream(song: Song, lang):
    chat = song.request_msg.chat
    if safone.get(chat.id) is not None:
        try:
            await safone[chat.id].delete()
        except BaseException:
            pass
    infomsg = await song.request_msg.reply_text(lang["downloading"])
    await pytgcalls.change_stream(
        chat.id,
        get_quality(song),
    )
    await set_title(chat.id, song.title, client=app)
    thumb = await generate_cover(
        song.title,
        chat.title,
        chat.id,
        song.thumb,
    )
    safone[chat.id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"]
        % (
            song.title,
            song.source,
            song.duration,
            song.request_msg.chat.id,
            song.requested_by.mention
            if song.requested_by
            else song.request_msg.sender_chat.title,
        ),
        quote=False,
    )
    await infomsg.delete()
    if os.path.exists(thumb):
        os.remove(thumb)


async def start_stream(song: Song, lang):
    chat = song.request_msg.chat
    if safone.get(chat.id) is not None:
        try:
            await safone[chat.id].delete()
        except BaseException:
            pass
    infomsg = await song.request_msg.reply_text(lang["downloading"])
    try:
        await pytgcalls.join_group_call(
            chat.id,
            get_quality(song),
            stream_type=StreamType().pulse_stream,
        )
    except (NoActiveGroupCall, GroupCallNotFound):
        peer = await app.resolve_peer(chat.id)
        await app.send(
            CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=app.rnd_id() // 9000000000,
            )
        )
        return await start_stream(song, lang)
    await set_title(chat.id, song.title, client=app)
    thumb = await generate_cover(
        song.title,
        chat.title,
        chat.id,
        song.thumb,
    )
    safone[chat.id] = await song.request_msg.reply_photo(
        photo=thumb,
        caption=lang["playing"]
        % (
            song.title,
            song.source,
            song.duration,
            song.request_msg.chat.id,
            song.requested_by.mention
            if song.requested_by
            else song.request_msg.sender_chat.title,
        ),
        quote=False,
    )
    await infomsg.delete()
    if os.path.exists(thumb):
        os.remove(thumb)


def get_quality(song: Song) -> Union[AudioPiped, AudioVideoPiped]:
    group = get_group(song.request_msg.chat.id)
    if group["stream_mode"] == "video":
        if config.QUALITY.lower() == "high":
            return AudioVideoPiped(
                song.remote, HighQualityAudio(), HighQualityVideo(), song.headers
            )
        elif config.QUALITY.lower() == "medium":
            return AudioVideoPiped(
                song.remote,
                MediumQualityAudio(),
                MediumQualityVideo(),
                song.headers,
            )
        elif config.QUALITY.lower() == "low":
            return AudioVideoPiped(
                song.remote, LowQualityAudio(), LowQualityVideo(), song.headers
            )
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return AudioVideoPiped(
                song.remote, HighQualityAudio(), HighQualityVideo(), song.headers
            )
    else:
        if config.QUALITY.lower() == "high":
            return AudioPiped(song.remote, HighQualityAudio(), song.headers)
        elif config.QUALITY.lower() == "medium":
            return AudioPiped(song.remote, MediumQualityAudio(), song.headers)
        elif config.QUALITY.lower() == "low":
            return AudioPiped(song.remote, LowQualityAudio(), song.headers)
        else:
            print("WARNING: Invalid Quality Specified. Defaulting to High!")
            return AudioPiped(song.remote, HighQualityAudio(), song.headers)
