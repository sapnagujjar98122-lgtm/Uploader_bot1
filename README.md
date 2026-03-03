# 🎌 KenshinAnime Bot

A powerful Telegram bot for anime content management with auto-upload, custom captions, multi-channel support, and more.

---

## ⚡ Features

- `/upload <name>` — Full guided upload flow (search → audio → season → episode → quality → video)
- Custom captions with variables
- Thumbnail support (custom or AniList poster)
- Multiple target channels
- Storage group (files stored first, then forwarded)
- Auto-delete local files after 10s
- Upload queue with progress bar
- Custom sticker after each episode
- Auto-track anime for new episode notifications
- Admin management (multiple admins)
- Broadcast to all users
- Full upload stats

---

## 🚀 Setup

### 1. Get Telegram Credentials
- Go to https://my.telegram.org → API Development Tools
- Get `API_ID` and `API_HASH`
- Create a bot via @BotFather → get `BOT_TOKEN`

### 2. Get MongoDB URI
- Go to https://www.mongodb.com/cloud/atlas
- Create free cluster → get connection string

### 3. Configure .env
```bash
cp .env.example .env
# Fill in all values
```

### 4. Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Push to GitHub
2. Connect repo to Railway
3. Add environment variables from `.env`
4. Deploy!

### 5. Local Development
```bash
pip install -r requirements.txt
python main.py
```

---

## 📋 Commands

| Command | Description |
|---|---|
| `/upload <name>` | Start upload flow |
| `/queue` | View upload queue |
| `/add_channel` | Add target channel |
| `/list_channels` | List all channels |
| `/remove_channel` | Remove a channel |
| `/set_storage <id>` | Set storage group |
| `/set_caption` | Set caption template |
| `/show_caption` | View current caption |
| `/reset_caption` | Reset to default |
| `/set_thumbnail` | Set default thumbnail |
| `/set_sticker` | Set episode sticker |
| `/set_prefix <text>` | Set file rename prefix |
| `/add_admin <id>` | Add admin |
| `/remove_admin <id>` | Remove admin |
| `/admins` | List admins |
| `/users` | User stats |
| `/stats` | Upload statistics |
| `/broadcast` | Broadcast to all users |
| `/track <name>` | Auto-track anime |
| `/tracklist` | List tracked anime |
| `/delete_after <sec>` | Set file delete delay |
| `/help` | Show help |

---

## 🎨 Caption Variables

```
{anime_name}   →  Solo Leveling
{season}       →  Season 01
{episode}      →  Episode 05
{audio}        →  Hindi Dub
{quality}      →  1080p
```

**Default Caption:**
```
📺 ᴀɴɪᴍᴇ : {anime_name}
━━━━━━━━━━━━━━━━━━━⭒
❖ Sᴇᴀsᴏɴ: {season}
❖ ᴇᴘɪꜱᴏᴅᴇ: {episode}
❖ ᴀᴜᴅɪᴏ: {audio}| #Official
❖ Qᴜᴀʟɪᴛʏ: {quality}
━━━━━━━━━━━━━━━━━━━⭒
POWERED BY: [@KENSHIN_ANIME & @MANWHA_VERSE]
```

---

## 📁 Project Structure

```
KenshinBot/
├── main.py              # Entry point
├── config.py            # Configuration
├── database.py          # MongoDB operations
├── queue_manager.py     # Upload queue worker
├── handlers/
│   ├── start.py         # /start, /help
│   ├── admin.py         # Admin commands
│   ├── upload.py        # Upload flow
│   ├── channels.py      # Channel management
│   └── broadcast.py     # Broadcast
├── utils/
│   ├── scraper.py       # AniList API
│   ├── caption.py       # Caption builder
│   ├── downloader.py    # File download utils
│   └── auto_check.py    # New episode checker
├── requirements.txt
├── Procfile
├── railway.json
└── .env.example
```

---

## 🔄 Upload Flow

```
/upload solo leveling
    ↓
🔍 Search AniList API
    ↓
Select Anime (inline keyboard)
    ↓
Select Audio [Hindi/English/Japanese/Multi...]
    ↓
Select Season [S1/S2/S3...]
    ↓
Select Episode [1-50 buttons or type]
    ↓
Select Quality [480p/720p/1080p/4K/8K]
    ↓
Send Video File
    ↓
📥 Download video
    ↓
✏️ Rename → @KENSHIN_ANIME - Title S01E05 [Hindi Dub] [1080p].mp4
    ↓
📤 Upload to Storage Group
    ↓
📢 Forward to all Target Channels (with caption + thumbnail)
    ↓
🎯 Send Sticker (if set)
    ↓
🗑️ Delete local file (after 10s)
    ↓
✅ Done!
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `API_ID` | ✅ | Telegram API ID |
| `API_HASH` | ✅ | Telegram API Hash |
| `BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `ADMIN_IDS` | ✅ | Comma-separated admin user IDs |
| `MONGO_URI` | ✅ | MongoDB connection string |
| `STORAGE_GROUP_ID` | ✅ | Private group ID for file storage |
| `DELETE_AFTER` | ❌ | Seconds before local file delete (default: 10) |
| `AUTO_CHECK_INTERVAL` | ❌ | Minutes between auto-checks (default: 60) |
| `FILE_PREFIX` | ❌ | File rename prefix (default: @KENSHIN_ANIME) |

---

*Personal project — all responsibility with the user.*
