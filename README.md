# Sickwell Music Bot v4.7.5
[![Discord](https://img.shields.io/discord/1470582581526528183?color=5865F2&label=Discord&logo=discord&logoColor=white)](https://discord.gg/GPWX58cbEX)
[![Top.gg](https://img.shields.io/badge/Top.gg-Verified-00ff88?logo=discord)](https://top.gg/bot/YOUR_BOT_ID)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

&gt; Advanced Discord music bot with smart discovery, rarity filters, achievement system, and autopilot mode.  
&gt; Not just a music player — it's a music discovery game.

[🔗 Terms of Service](https://sickwell322.github.io/Sickwell_music/tos.html) | [🔒 Privacy Policy](https://sickwell322.github.io/Sickwell_music/privacy.html) | [💬 Support Server](https://discord.gg/GPWX58cbEX)

---

## 🎵 Key Features

### 🎮 Smart Random Discovery
- **7 Rarity Filters**: Micro (1K-50K) → Small → Medium → Large → Mega (100M+) → Deep (underground) → Any
- **Anti-Spam Filter**: Automatically blocks karaoke, instrumental, slowed+reverb versions
- **Tag Combinator**: Mixes base queries with year/style/mood modifiers for unique discoveries

### 🏆 Social & Stats System (v4.7)
- **30 Achievements**: From "First Steps" to "Audiophile" (500h listening time)
- **Personal Stats**: `/stats` shows tracks played, listening time, top 5 genres, achievement progress
- **Leaderboards**: Server `/top` and Global `/globaltop` rankings
- **Hybrid Commands**: Works with both `!command` and `/slash` formats

### 🤖 Autopilot Mode (v4.7.5)
- Auto-detects empty queue and adds 2-5 similar tracks after 30s delay
- Analyzes last 3 tracks from history to match genre/style
- Admin toggle: `/autopilot [on/off/status]`

### 🌍 Multilingual
- Auto-detects server language (Russian/English)
- Manual toggle: `/language [ru/en]`
- Full localization for commands, responses, and achievements

---

## 📋 Commands

### Music Playback
| Command | Description | Permissions |
|---------|-------------|-------------|
| `/start` or `!start` | Connect bot to voice channel | Everyone |
| `/play &lt;query&gt;` | Search and play from YouTube | Everyone |
| `/search &lt;query&gt;` | Show 5 results to choose from | Everyone |
| `/skip` / `/previous` | Skip track or go back | Everyone |
| `/pause` / `/resume` | Playback control | Everyone |
| `/stop` | Stop and disconnect | Everyone |

### Smart Random
| Command | Description |
|---------|-------------|
| `/random [rarity]` | Add random track (micro/small/medium/large/mega/deep/any) |
| `/addrandom &lt;count&gt; [rarity]` | Add multiple random tracks (1-10) |

### Queue Management
| Command | Description |
|---------|-------------|
| `/queue` | Show queue with live progress bar |
| `/shuffle` | Shuffle current queue |
| `/remove &lt;position&gt;` | Remove specific track |
| `/loop [off/one/all]` | Set loop mode |

### Stats & Social
| Command | Description |
|---------|-------------|
| `/stats` | Your personal statistics and achievements |
| `/top` | Server leaderboard (tracks & time) |
| `/globaltop` | Global most played tracks across all servers |

### Admin Settings
| Command | Description | Permissions |
|---------|-------------|-------------|
| `/autopilot [on/off/status]` | Toggle autopilot mode | Administrator |
| `/language [ru/en]` | Set bot language | Administrator |

---

## 🔒 Data Collection & Privacy

**For Top.gg Reviewers & Users:**

### What We Collect
- **Discord User ID**: To bind stats and achievements to your account (stored as hash)
- **Discord Server ID**: To manage queue and settings per server
- **Listening Statistics**: Track count, listening time (minutes), genre tags (for achievements)
- **Voice Channel IDs**: Temporary session data (cleared on disconnect)

### What We DO NOT Collect
- Email addresses, phone numbers, or personal messages
- IP addresses or geolocation
- YouTube search history (queries are ephemeral)
- Voice chat audio content

### Data Storage
- **SQLite Database**: Local file-based storage (not cloud)
- **Location**: Stored on bot host server (currently PC, migrating to Raspberry Pi)
- **Retention**: User stats persist until explicit deletion request; Server data cleared on bot removal
- **Access**: Only bot owner (@jsickwell) has file access

### User Rights (GDPR/CCPA compliant)
- Right to deletion: Request full stats wipe via `@jsickwell` on Discord
- Right to access: View your data via `/stats` command
- Opt-out: Don't use stat-related commands (core music works without tracking)

**Full Policy**: [Privacy Policy](https://sickwell322.github.io/Sickwell_music/privacy.html)

---

## 🛠️ Tech Stack
- **Library**: [discord.py](https://github.com/Rapptz/discord.py) (v2.3+)
- **Audio**: yt-dlp + FFmpeg
- **Database**: SQLite3 (local)
- **Hosting**: Currently Windows PC (migrating to Raspberry Pi 5)
- **Donations**: DonationAlerts API integration

---

## 🚀 Self-Hosting

```bash
git clone https://github.com/sickwell322/Sickwell_music.git
cd Sickwell_music
pip install -r requirements.txt

# Create .env file:
echo "DISCORD_TOKEN=your_token_here" &gt; .env
echo "DONATIONALERTS_TOKEN=your_token" &gt;&gt; .env  # Optional

python Music_bot.py

Requirements: Python 3.10+, FFmpeg installed, 2GB+ RAM
📞 Support & Links
Discord Server: discord.gg/GPWX58cbEX
Developer: @jsickwell (Telegram)
Website: sickwell322.github.io/Sickwell_music
Donate: DonationAlerts (Server Fund for Raspberry Pi)
Version: v4.7.5 (Autopilot Update) | Last Updated: 26.02.2026
Made with 💚 by ЦНИ (Center of Unrealized Ideas)
