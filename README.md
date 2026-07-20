# 🎵 SteelSeriesDisplay

> Now-playing music display for the OLED screen of your SteelSeries keyboard —
> title, artist, album art and a live progress bar via the GameSense API.

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat)](https://learn.microsoft.com/windows/)
[![SteelSeries](https://img.shields.io/badge/API-GameSense-FF5200?style=flat&logo=steelseries&logoColor=white)](https://github.com/SteelSeries/gamesense-sdk)
[![Pillow](https://img.shields.io/badge/imaging-Pillow-yellow?style=flat)](https://python-pillow.org/)

Works with any player or browser that reports playback to Windows
(Spotify, Yandex Music, YouTube, VLC, ...) — the app reads the system media
session, so no per-player integration is needed.

## ✨ Features

- 🎵 **Current track info** — title and artist of whatever is playing,
  straight from the Windows media session (`winsdk`).
- 🖼 **Album art** — the thumbnail is resized to 40×40, converted to a 1-bit
  bitmap and drawn next to the text (`with_icon` view; there is also a
  text-only `icon_less` view).
- ⏱ **Live progress bar** — elapsed / total time with a smoothly
  interpolated position between player updates.
- 📜 **Marquee scrolling** — long titles scroll with a configurable speed;
  built-in bitmap fonts cover **Latin, Cyrillic, digits and punctuation**.
- 🎬 **Song-change transitions** — `circle`, `slide_x`, `slide_y` or `random`
  animation when a new track starts.
- ⏯ **Pause/resume splash** — optional short "paused"/"resumed" screen
  (`events_duration` > 0).
- ⚙️ **Zero-setup config** — `config.json` is generated with defaults on
  first run; edit and restart.

## 🛠 Tech stack

- Python 3.11+ (asyncio)
- [winsdk](https://pypi.org/project/winsdk/) — Windows `GlobalSystemMediaTransportControlsSession` (now-playing info + thumbnail)
- [aiohttp](https://docs.aiohttp.org/) — SteelSeries GameSense HTTP API
- [Pillow](https://python-pillow.org/) — album-art resizing and bitmap conversion
- [pydantic](https://docs.pydantic.dev/) — typed config
- Custom 1-bit framebuffer renderer (`src/gtk/`) — bitmap fonts, shapes, transitions

## 📋 Requirements

- Windows 10/11
- [SteelSeries GG](https://steelseries.com/gg) (SteelSeries Engine 3) running —
  the app discovers the local GameSense endpoint via
  `%programdata%\SteelSeries\SteelSeries Engine 3\coreProps.json`
- A SteelSeries device with an OLED screen (default resolution 128×40,
  e.g. Apex 7 / Apex Pro; other sizes can be set in the config)

## 🚀 Installation & usage

```bash
git clone https://github.com/kewldan/SteelSeriesDisplay.git
cd SteelSeriesDisplay
pip install -r requirements.txt
python src/main.py
```

Play some music — the screen switches to the track view ("No music" is shown
when nothing is playing). The app registers in SteelSeries GG as
**Music display** (Engine Apps), where you can manage its screen priority.

## ⚙️ Configuration (`config.json`)

Created automatically in the working directory on first run:

| Key | Default | Meaning |
|---|---|---|
| `width` / `height` | `128` / `40` | OLED resolution in pixels |
| `view` | `with_icon` | `with_icon` (album art + text) or `icon_less` (text only) |
| `transition` | `circle` | song-change animation: `circle`, `slide_x`, `slide_y`, `random`, `disabled` |
| `transition_duration` | `3.0` | animation length, seconds |
| `refresh_rate` | `10` | screen redraws per second |
| `music_refresh_rate` | `20` | media-session polls per second |
| `events_duration` | `0.0` | how long to show the "paused"/"resumed" splash (0 = off) |
| `text_speed` | `6.0` | marquee scrolling speed |
| `carousel_stop_time` | `3.0` | pause of the scrolling text, seconds |

## 🙏 Credits

Thanks for the GameSense API to the [author](https://github.com/wolfinabox)
of [Steelseries-OLED-Display-Mirror](https://github.com/wolfinabox/Steelseries-OLED-Display-Mirror).

## 📫 Contact

- kewldanil1@gmail.com
- @kewldan (Telegram, VK, Discord)
