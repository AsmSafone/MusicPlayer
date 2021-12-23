<h1 align= center><b>⭐️ Music Player ⭐️</b></h1>
<h3 align = center> A Telegram Music Bot written in Python using Pyrogram and Py-Tgcalls </h3>

<p align="center">
<a href="https://python.org"><img src="http://forthebadge.com/images/badges/made-with-python.svg" alt="made-with-python"></a>
<br>
    <img src="https://img.shields.io/github/license/AsmSafone/MusicPlayer?style=for-the-badge" alt="LICENSE">
    <img src="https://img.shields.io/github/contributors/AsmSafone/MusicPlayer?style=for-the-badge" alt="Contributors">
    <img src="https://img.shields.io/github/repo-size/AsmSafone/MusicPlayer?style=for-the-badge" alt="Repository Size"> <br>
    <img src="https://img.shields.io/github/forks/AsmSafone/MusicPlayer?style=for-the-badge" alt="Forks">
    <img src="https://img.shields.io/github/stars/AsmSafone/MusicPlayer?style=for-the-badge" alt="Stars">
    <img src="https://img.shields.io/github/watchers/AsmSafone/MusicPlayer?style=for-the-badge" alt="Watchers">
    <img src="https://img.shields.io/github/commit-activity/w/AsmSafone/MusicPlayer?style=for-the-badge" alt="Commit Activity">
    <img src="https://img.shields.io/github/issues/AsmSafone/MusicPlayer?style=for-the-badge" alt="Issues">
</p>

## ✨ <a name="features"></a>Features

### ⚡️ Fast & Light

Starts streaming your inputs while downloading and converting them. Also, it
doesn't make produce files.

### 👮🏻‍♀️ Safe and handy

Restricts control and sensitive commands to admins.

### 🗑 Clean and spam free

Deletes old playing trash to keep your chats clean.

### 😎 Has cool controls

Lets you switch stream mode, loop, pause, resume, mute, unmute anytime.

### 🖼 Has cool thumbnails

Response your commands with cool thumbnails on the chat.

### 😉 Streams whatever you like

You can stream audio or video files, YouTube videos with any duration,
YouTube lives, YouTube playlists and even custom live streams like radios or m3u8 links or files in
the place it is hosted!

### 📊 Streams in multiple places

Allows you to stream different things in multiple chats simultaneously. Each
chat will have its own song queue.

### 🗣 Speaks different languages

Music Player is multilingual and speaks [various languages](#languages),
thanks to the translators.

## 🚀 <a name="deploy"></a>Deploy

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AsmSafone/MusicPlayer)

## ☁️ <a name="self_host"></a>Self Host

```bash
$ git clone https://github.com/AsmSafone/MusicPlayer
$ cd MusicPlayer
$ cp sample.env .env
< edit .env with your own values >
$ sudo docker build . -t musicplayer
$ sudo docker run musicplayer
```

## ⚒ <a name="configs"></a>Configs

- `API_ID`: Telegram app id.
- `API_HASH`: Telegram app hash.
- `SESSION`: Pyrogram string session. You can generate from [here](https://replit.com/@AsmSafone/genStr).
- `SUDOERS`: ID of sudo users (separate multiple ids with space).
- `PREFIX`: Commad prefixes (separate multiple prefix with space). Eg: `! /`
- `LANGUAGE`: An [available](#languages) bot language (can change it anytime). Default: `en`.

## 📄 <a name="commands"></a>Commands

```text

• <prefix>ping
Usage: Check if alive or not

• <prefix>start | <prefix>help
Usage: Show the help for commands

• <prefix>mode | <prefix>switch
Usage: Switch the stream mode (audio/video)

• <prefix>p | <prefix>play [song name | youtube link]
Usage: Play a song in vc, if already playing add to queue

• <prefix>radio | <prefix>stream [radio url | stream link]
Usage: Play a live stream in vc, if already playing add to queue

• <prefix>pl | <prefix>playlist [youtube playlist link]
Usage: Play the whole youtube playlist at once

• <prefix>skip | <prefix>next
Usage: Skip to the next song

• <prefix>m | <prefix>mute
Usage: Mute the current stream

• <prefix>um | <prefix>unmute
Usage: Unmute the muted stream

• <prefix>ps | <prefix>pause
Usage: Pause the current stream

• <prefix>rs | <prefix>resume
Usage: Resume the paused stream

• <prefix>list | <prefix>queue
Usage: Show the songs in the queue

• <prefix>mix | <prefix>shuffle
Usage: Shuflle the queued playlist

• <prefix>loop | <prefix>repeat
Usage: Enable or disable the loop mode

• <prefix>lang | language [language code]
Usage: Set the bot language in a group

• <prefix>ip | <prefix>import
Usage: Import queue from exported file

• <prefix>ep | <prefix>export
Usage: Export the queue for import in future

• <prefix>stop | <prefix>leave
Usage: Leave from vc and clear the queue
```

## 🗣 <a name="languages"></a>Languages

```text
en    English
```

## 💜 <a name="contribute"></a>Contribute

New languages, bug fixes and improvements following
[our contribution guidelines](./CONTRIBUTING.md) are warmly welcomed!

## 🛫 <a name="supports"></a>Supports

For any kind of help join [our support group](https://t.me/AsmSupport).

## ✨ <a name="credits"></a>Credits

- [Me](https://github.com/AsmSafone) for [Noting](https://github.com/AsmSafone/MusicPlayer) 😬
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram) ❤️
- [Laky-64](https://github.com/Laky-64) for [Py-TgCalls](https://github.com/pytgcalls/pytgcalls) ❤️
- And Thanks To All [Contributors](https://github.com/AsmSafone/MusicPlayer/graphs/contributors)! ❤️

## 📃 <a name="license"></a>License

Music Player is licenced under the GNU Affero General Public License v3.0.
Read more [here](./LICENSE).
