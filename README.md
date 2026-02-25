# Sickwell Music Bot v4.7

**Not just a music bot. It's a music discovery game.**

Discord bot with smart random track discovery, rarity filters, and achievement system.

## 🎲 Unique Features

- **Rarity-Based Random** — 7 filters: Micro (1K-50K) to Mega (100M+ views)
- **30 Achievements** — Collect rewards for listening time, rare finds, genres
- **Live Stats** — Personal `/stats`, server `/top`, global `/globaltop`
- **Anti-Karaoke Filter** — No more "slowed + reverb" spam
- **Hybrid Commands** — Use `!` or `/` prefixes

## 🚀 Quick Start

1. Invite bot to your server
2. Join voice channel
3. Type `/start` or `!start`
4. Use `/play &lt;song&gt;` or `/random [rarity]`

## 🛠️ Self-Hosting

```bash
git clone https://github.com/sickwell322/Sickwell_music.git
cd Sickwell_music
pip install -r requirements.txt
# Create .env file with your DISCORD_TOKEN
python Music_bot.py
