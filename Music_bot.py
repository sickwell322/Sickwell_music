import discord
from discord.ext import commands
from discord.ui import View, Button, Select
import yt_dlp as youtube_dl
import asyncio
import os
import random as rand
import time
import json
import aiohttp
from collections import OrderedDict
from dotenv import load_dotenv

load_dotenv()

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_SEARCH_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'socket_timeout': 10,
}

YDL_EXTRACT_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 10,
}

BASE_QUERIES = [
    # === PHONK & DRIFT (расширенный) ===
    "phonk", "drift phonk", "slowed phonk", "brazilian phonk", "aggresive phonk",
    "memphis phonk", "cowbell phonk", "house phonk", "dark phonk", "phonk house",
    "funk brasil", "funk mandelao", "phonk remix", "drift music", "car music",
    "street racing music", "tokyo drift", "eurobeat", "initial d", "gasolina",
    
    # === RUSSIAN RAP (новая школа + старая) ===
    "russian rap", "rus rap", "ru rap", "russian drill", "russian trap",
    "kyivstoner", "korzh", "skriptonit", "morgenshtern", "big baby tape", 
    "oxxxymiron", "face", "pharaoh", "boulevard depo", "lsp", "markul",
    "t-fest", "skryptonite", "niman", "zomb", "dequine", "loqiemean",
    "thomas mraz", "saluki", "kizaru", "mayot", "seemee", "og buda",
    "alblak 52", "3731", "soda luv", "aikko", "oggy", "gravework",
    "atl", "kasta", "centr", "rem digga", "basta", "kreed", "timati",
    "dora", "alyona alyona", "instasamka", "slava marlow", "eldzhey",
    "flesh", "lil krystalll", "platina", "fogel", "gena glock",
    
    # === RUSSIAN ROCK / ALTERNATIVE ===
    "russian rock", "russian indie", "russian pop", "русская музыка",
    "kino", "dDT", "akvarium", "splin", "nautilus pompilius", "aria",
    "bi-2", "zemfira", "mumiy troll", "louna", "slot", "tracktor bowling",
    "nervy", "anacondaz", "noize mc", "krovostok", "gruppa krovi",
    "shortparis", "pompeya", "sBPCh", "ic3peak", "gleb",
    
    # === INTERNATIONAL HIP-HOP (современный) ===
    "trap", "drill", "rage", "plugg", "cloud rap", "emo rap", "soundcloud rap",
    "playboi carti", "travis scott", "kanye west", "drake", "future", "young thug",
    "gunna", "lil baby", "lil uzi vert", "juice wrld", "xxxtentacion", "ski mask",
    "trippie redd", "lil peep", "ghostemane", "$uicideboy$", "bones", "xavier wulf",
    "asap rocky", "asap mob", "tyler the creator", "frank ocean", "brockhampton",
    "ken carson", "destroy lonely", "yeat", "sep", "kankan", "summrs",
    "autumn!", "soFaygo", "lucki", "unotheactivist", "thouxanbanfauni",
    "city morgue", "zillakami", "sosmula", "night lovell", "pouya",
    "freddie dredd", "hemlock ernst", "jpegmafia", "danny brown",
    
    # === INTERNATIONAL HIP-HOP (классика/золотая эра) ===
    "eminem", "50 cent", "snoop dogg", "dr dre", "ice cube", "nwa",
    "tupac", "biggie", "nas", "jay z", "kendrick lamar", "j cole",
    "logic", "joyner lucas", "tech n9ne", "hopsin", "mac miller",
    "childish gambino", "outkast", "andre 3000", "tyler creator igor",
    
    # === POP / ALT / INDIE (international) ===
    "the weeknd", "imagine dragons", "linkin park", "queen", "arctic monkeys",
    "radiohead", "nirvana", "metallica", "green day", "blink 182",
    "dua lipa", "billie eilish", "post malone", "doja cat", "lil nas x",
    "harry styles", "olivia rodrigo", "taylor swift", "ariana grande",
    "justin bieber", "ed sheeran", "maroon 5", "coldplay", "bastille",
    "glass animals", "tame impala", "mac demarco", "clairo", "girl in red",
    "cage the elephant", "foals", "two door cinema club", "the neighbourhood",
    "cigarettes after sex", "mxmtoon", "beabadoobee", "mitski", "boygenius",
    
    # === ELECTRONIC / EDM / BASS ===
    "electronic dance music", "dubstep", "riddim", "trap edm", "future bass",
    "house music", "tech house", "deep house", "progressive house", "bass house",
    "garage", "uk garage", "dnb", "drum and bass", "neurofunk", "liquid dnb",
    "aphex twin", "deadmau5", "skrillex", "zedd", "martin garrix", "david guetta",
    "calvin harris", "diplo", "major lazer", "flume", "san holo", "illenium",
    "porter robinson", "madeon", "daft punk", "justice", "kavinsky",
    "synthwave", "retrowave", "dark synth", "vaporwave", "lofi hip hop",
    
    # === HYPERPOP / DIGICORE / EXPERIMENTAL ===
    "hyperpop", "digicore", "glitchcore", "100 gecs", "sophie", "ag cook",
    "bladee", "ecco2k", "thaiboy digital", "drain gang", "gtbsbe",
    "osquinn", "ericdoa", "glaive", "aldn", "midwxst", "kmoe",
    "blackwinterwells", "daine", "charli xcx", "sophie msmsmsm",
    "food house", "fraxiom", " underscores", "recovery girl",
    
    # === TYPE BEATS (популярные продюсеры) ===
    "southside type beat", "metro boomin type beat", "pi'erre bourne type beat",
    "murda beatz type beat", "nick mira type beat", "internet money type beat",
    "wheezy type beat", "tay keith type beat", "808 mafia type beat",
    "cookin soul beats", "alky beats", "lxfi beats", "fantom beats",
    
    # === GAMING / AESTHETIC ===
    "gaming music", "csgo music", "dota 2 music", "valorant music",
    "sigma music", "gigachad music", "sad music", "night drive music",
    "midnight drive", "rainy mood", "lofi study", "chill beats",
    "aesthetic music", "vibes", "mood", "late night vibes",
    
    # === MEME / NICHE (но с аудиторией) ===
    "cursed audio", "bass boosted earrape", "distorted", "loud nigra",
    "ambatukam", "bro did you really just talk during independent reading",
    "goofy ahh sounds", "bruh sound effect", "vine boom", "anime opening",
    "amv music", "nightcore", "daycore", "slowed reverb", "sped up",
    
    # === JAZZ / SOUL / FUNK (для разнообразия) ===
    "jazz relax", "lofi jazz", "chillhop", "funk music", "soul music",
    "rnb", "r&b", "frank sinatra", "michael jackson", "prince",
    "kool and the gang", "earth wind fire", "jamiroquai",
]

# Модификаторы можно расширить для большего разнообразия комбинаций
YEAR_MODIFIERS = ["2024", "2023", "2022", "2021", "2020", "2019", "classic", "new", "latest", "old", "vintage", ""]
STYLE_MODIFIERS = ["remix", "slowed", "reverb", "bass boosted", "nightcore", 
                   "8d audio", "speed up", "type beat", "instrumental", 
                   "acoustic version", "live version", "cover", "edit", 
                   "mix", "playlist", "compilation", "full album", ""]
MOOD_MODIFIERS = ["sad", "happy", "dark", "aggressive", "chill", "relax", 
                  "gaming", "workout", "midnight", "sunset", "rainy", 
                  "focus", "party", "aesthetic", "vibes", ""]

class FundManager:
    def __init__(self):
        self.file_path = "fund.json"
        self.data = self.load()
        if not self.data:
            self.data = {
                "current": 0.0,
                "goal": 20000,
                "currency": "₽",
                "goal_name": "Raspberry Pi 4 (своя железка!)",
                "donors": [],
                "last_update": None
            }
            self.save()
    
    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def update_amount(self, amount, donors_list=None):
        self.data["current"] = float(amount)
        if donors_list:
            self.data["donors"] = donors_list[:10]
        self.data["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save()
    
    def get_progress_bar(self, length=10):
        progress = min(self.data["current"] / self.data["goal"], 1.0)
        filled = int(length * progress)
        empty = length - filled
        if progress >= 1.0:
            return "🟨" * length + " ✨ Цель достигнута!"
        else:
            return "🟩" * filled + "🟨" * (1 if filled < length else 0) + "⬜" * (empty - (1 if filled < length else 0))
    
    def get_remaining(self):
        return max(self.data["goal"] - self.data["current"], 0)
    
    def get_percent(self):
        return min(int((self.data["current"] / self.data["goal"]) * 100), 100)


class DonationAlertsAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://www.donationalerts.com/api/v1"
    
    async def get_donations(self, session, limit=100):
        url = f"{self.base_url}/alerts/donations"
        params = {"page_size": limit, "currency": "RUB"}
        
        try:
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("data", [])
                else:
                    print(f"DA API Error: {resp.status}")
                    return []
        except Exception as e:
            print(f"Error fetching donations: {e}")
            return []
    
    async def update_fund_from_api(self, fund_manager):
        if not self.token:
            return None, "Токен не настроен"
        
        async with aiohttp.ClientSession() as session:
            donations = await self.get_donations(session)
            if donations is None:
                return None, "Ошибка подключения к DonationAlerts"
            
            total = 0.0
            donors = []
            
            for donation in donations:
                amount = float(donation.get("amount", 0))
                currency = donation.get("currency", "RUB")
                if currency == "RUB":
                    total += amount
                
                username = donation.get("username", "Аноним")
                message = donation.get("message", "")
                
                donor_info = {
                    "name": username[:20],
                    "amount": amount,
                    "message": message[:30] if message else "",
                    "date": donation.get("created_at", "")
                }
                
                donors = [d for d in donors if d["name"] != donor_info["name"]]
                donors.insert(0, donor_info)
            
            fund_manager.update_amount(total, donors)
            return total, None


class FundView(View):
    def __init__(self, bot_instance, is_admin=False):
        super().__init__(timeout=120)
        self.bot = bot_instance
        self.is_admin = is_admin
        
        donate_btn = Button(
            label="💚 Помочь проекту", 
            style=discord.ButtonStyle.link,
            url="https://www.donationalerts.com/r/jsickwell"
        )
        self.add_item(donate_btn)
    
    @discord.ui.button(label="🔄 Обновить статус", style=discord.ButtonStyle.secondary, row=1)
    async def refresh_btn(self, interaction: discord.Interaction, button: Button):
        if not self.is_admin:
            await interaction.response.send_message("❌ Только администратор может обновлять статус фонда!", ephemeral=True)
            return
        
        await interaction.response.defer(thinking=True, ephemeral=True)
        amount, error = await self.bot.da_api.update_fund_from_api(self.bot.fund)
        
        if error:
            await interaction.followup.send(f"❌ Ошибка: {error}", ephemeral=True)
        else:
            embed = self.create_fund_embed()
            await interaction.message.edit(embed=embed)
            await interaction.followup.send(f"✅ Обновлено! Собрано: {amount:,.0f}₽", ephemeral=True)
    
    @discord.ui.button(label="📊 Подробности", style=discord.ButtonStyle.secondary, row=1)
    async def details_btn(self, interaction: discord.Interaction, button: Button):
        fund = self.bot.fund.data
        
        embed = discord.Embed(
            title="📊 Статистика фонда",
            color=discord.Color.gold() if fund["current"] >= fund["goal"] else discord.Color.blue()
        )
        
        embed.add_field(name="Цель", value=fund["goal_name"], inline=False)
        embed.add_field(name="Собрано", value=f"{fund['current']:,.0f} {fund['currency']}", inline=True)
        embed.add_field(name="Цель", value=f"{fund['goal']:,.0f} {fund['currency']}", inline=True)
        embed.add_field(name="Осталось", value=f"{self.bot.fund.get_remaining():,.0f} {fund['currency']}", inline=True)
        
        if fund["last_update"]:
            embed.add_field(name="Обновлено", value=fund["last_update"], inline=False)
        
        if fund["donors"]:
            donors_text = ""
            for i, donor in enumerate(fund["donors"][:5], 1):
                msg = f" \"{donor['message']}\"" if donor["message"] else ""
                donors_text += f"{i}. **{donor['name']}** — {donor['amount']:,.0f}₽{msg}\n"
            embed.add_field(name="💚 Топ донатеры", value=donors_text, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    def create_fund_embed(self):
        fund = self.bot.fund.data
        progress_bar = self.bot.fund.get_progress_bar(10)
        percent = self.bot.fund.get_percent()
        
        color = discord.Color.green() if percent < 50 else (discord.Color.gold() if percent < 100 else discord.Color.purple())
        
        embed = discord.Embed(
            title="🎯 Server Fund",
            description=f"**{fund['goal_name']}**\n\n{progress_bar}\n\n**{fund['current']:,.0f}₽** / **{fund['goal']:,.0f}₽** ({percent}%)",
            color=color,
            url="https://www.donationalerts.com/r/jsickwell"
        )
        
        remaining = self.bot.fund.get_remaining()
        if remaining > 0:
            embed.add_field(name="💰 Осталось собрать", value=f"{remaining:,.0f}₽", inline=True)
        else:
            embed.add_field(name="🎉 Статус", value="Цель достигнута! Заказываем железку...", inline=True)
        
        if fund["donors"]:
            recent = ""
            for donor in fund["donors"][:3]:
                msg = f" *({donor['message']})*" if donor["message"] else ""
                recent += f"• **{donor['name']}** — {donor['amount']:,.0f}₽{msg}\n"
            embed.add_field(name="💚 Последние донаты", value=recent, inline=False)
        
        embed.set_footer(text="Обновляется вручную • Нажми 🔄 чтобы проверить новые донаты")
        return embed


class QueueView(View):
    def __init__(self, bot_instance, ctx):
        super().__init__(timeout=120)
        self.bot = bot_instance
        self.ctx = ctx
        self.update_select_options()
        
    def update_select_options(self):
        queue_list = self.bot.get_queue(self.ctx.guild.id)
        
        for child in self.children[:]:
            if isinstance(child, Select) and child.custom_id == "queue_select":
                self.remove_item(child)
        
        if len(queue_list) > 0:
            options = []
            for i, song in enumerate(queue_list[:10], 1):
                label = f"{i}. {song['title'][:30]}..." if len(song['title']) > 30 else f"{i}. {song['title']}"
                duration = song['duration']
                options.append(
                    discord.SelectOption(
                        label=label,
                        value=str(i-1),
                        description=f"⏱️ {duration} | 💿 Выбрать этот трек",
                        emoji=f"{i}️⃣" if i <= 9 else "🔟"
                    )
                )
            
            select = Select(
                placeholder="▶️ Выбрать трек для воспроизведения...",
                min_values=1,
                max_values=1,
                options=options,
                custom_id="queue_select",
                row=2
            )
            select.callback = self.select_callback
            self.add_item(select)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not self.ctx.voice_client:
            await interaction.response.send_message("❌ Бот не в голосовом канале", ephemeral=True)
            return False
        if not interaction.user.voice or interaction.user.voice.channel != self.ctx.voice_client.channel:
            await interaction.response.send_message("❌ Ты не в голосовом канале с ботом", ephemeral=True)
            return False
        return True

    async def select_callback(self, interaction: discord.Interaction):
        queue_list = self.bot.get_queue(self.ctx.guild.id)
        
        if not queue_list:
            await interaction.response.send_message("📭 Очередь пуста!", ephemeral=True)
            return
        
        selected_index = int(interaction.data['values'][0])
        selected_song = queue_list[selected_index]
        queue_list.pop(selected_index)
        
        current = self.bot.current.get(self.ctx.guild.id)
        if current and self.ctx.voice_client and (self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused()):
            history = self.bot.get_history(self.ctx.guild.id)
            history.append(current)
            if len(history) > 20:
                history.pop(0)
        
        queue_list.insert(0, selected_song)
        
        if self.ctx.voice_client:
            self.ctx.voice_client.stop()
        
        await interaction.response.send_message(f"▶️ Воспроизвожу: **{selected_song['title'][:40]}...**", ephemeral=True)
        await self.update_queue_message(interaction)

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.secondary)
    async def prev_btn(self, interaction: discord.Interaction, button: Button):
        await self.do_previous(interaction)
        
    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.secondary)
    async def pause_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_playing():
            self.ctx.voice_client.pause()
            await interaction.response.send_message("⏸️ Пауза", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def resume_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_paused():
            self.ctx.voice_client.resume()
            await interaction.response.send_message("▶️ Продолжаю", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Нет паузы", ephemeral=True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary)
    async def skip_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and (self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused()):
            self.ctx.voice_client.stop()
            await interaction.response.send_message("⏭️ Пропущено", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger)
    async def delete_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and (self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused()):
            self.ctx.voice_client.stop()
            await interaction.response.send_message("🗑️ Трек удален", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="🎲", style=discord.ButtonStyle.primary, row=1)
    async def add_random(self, interaction: discord.Interaction, button: Button):
        count = rand.randint(3, 8)
        rarity = rand.choice(["any", "medium", "deep"])
        rarity_text = {"any": "любые", "medium": "средней популярности", "deep": "глубинные (>1к <500к)"}
        
        await interaction.response.send_message(f"🎲 Ищу {rarity_text[rarity]} треки ({count} шт)...", ephemeral=True)
        added = await self.bot.add_random_tracks(self.ctx, count=count, rarity=rarity)
        await interaction.followup.send(f"✅ Добавлено {added} треков!", ephemeral=True)
        await self.update_queue_message(interaction)

    @discord.ui.button(label="🔀", style=discord.ButtonStyle.secondary, row=1)
    async def shuffle_btn(self, interaction: discord.Interaction, button: Button):
        queue = self.bot.get_queue(self.ctx.guild.id)
        if len(queue) < 2:
            await interaction.response.send_message("❌ Недостаточно треков", ephemeral=True)
            return
        rand.shuffle(queue)
        await interaction.response.send_message(f"🔀 Очередь перемешана!", ephemeral=True)
        self.update_select_options()
        await self.update_queue_message(interaction)

    @discord.ui.button(label="🔁", style=discord.ButtonStyle.secondary, row=1)
    async def loop_btn(self, interaction: discord.Interaction, button: Button):
        current_mode = self.bot.loop_modes.get(self.ctx.guild.id, 'off')
        modes = {'off': 'one', 'one': 'all', 'all': 'off'}
        new_mode = modes[current_mode]
        self.bot.loop_modes[self.ctx.guild.id] = new_mode
        emojis = {'off': '❌', 'one': '🔂', 'all': '🔁'}
        await interaction.response.send_message(f"{emojis[new_mode]} Режим повтора: {new_mode}", ephemeral=True)

    @discord.ui.button(label="🚪", style=discord.ButtonStyle.danger, row=1)
    async def leave_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client:
            self.bot.queues[self.ctx.guild.id] = []
            self.bot.current[self.ctx.guild.id] = None
            self.bot.history[self.ctx.guild.id] = []
            self.ctx.voice_client.stop()
            await self.ctx.voice_client.disconnect()
            await interaction.response.send_message("🚪 Бот отключен", ephemeral=True)
            self.stop()
        else:
            await interaction.response.send_message("❌ Я не в канале", ephemeral=True)

    async def do_previous(self, interaction):
        history = self.bot.history.get(self.ctx.guild.id, [])
        if not history:
            await interaction.response.send_message("❌ Нет предыдущих треков", ephemeral=True)
            return
        
        prev_song = history.pop()
        queue = self.bot.get_queue(self.ctx.guild.id)
        
        current = self.bot.current.get(self.ctx.guild.id)
        if current and self.ctx.voice_client.is_playing():
            queue.insert(0, current)
        
        queue.insert(0, prev_song)
        self.ctx.voice_client.stop()
        await interaction.response.send_message("⏮️ Возвращаю предыдущий трек", ephemeral=True)

    async def update_queue_message(self, interaction):
        """Обновляет сообщение очереди с обработкой удаленных сообщений"""
        try:
            queue_list = self.bot.get_queue(self.ctx.guild.id)
            current = self.bot.current.get(self.ctx.guild.id)
            
            embed = discord.Embed(title="📜 Текущая очередь", color=discord.Color.purple())
            
            if current:
                start_time = self.bot.start_times.get(self.ctx.guild.id, time.time())
                elapsed = int(time.time() - start_time)
                total = current.get('duration_seconds', 0)
                progress_bar = self.bot.create_progress_bar(elapsed, total)
                time_str = self.bot.format_duration(elapsed)
                total_str = current['duration']

                embed.add_field(
                    name="▶️ Сейчас",
                    value=f"[{current['title'][:40]}...]({current['webpage_url']})\n`{progress_bar}`\n`{time_str} / {total_str}`",
                    inline=False
                )

            if queue_list:
                text = ""
                for i, song in enumerate(queue_list[:10], 1):
                    text += f"`{i}.` {song['title'][:30]}... | `{song['duration']}`\n"
                if len(queue_list) > 10:
                    text += f"\n*...и еще {len(queue_list)-10}*"
                embed.add_field(name=f"Далее ({len(queue_list)}):", value=text, inline=False)
            else:
                embed.add_field(name="Далее:", value="📭 Пусто", inline=False)

            history_count = len(self.bot.history.get(self.ctx.guild.id, []))
            embed.set_footer(text=f"⏮️ История: {history_count} треков | Выбери трек из списка ниже ⬇️")

            self.update_select_options()
            
            # Обработка случая, когда сообщение удалено или interaction завершен
            try:
                if interaction.response.is_done():
                    await interaction.message.edit(embed=embed, view=self)
                else:
                    await interaction.response.edit_message(embed=embed, view=self)
            except discord.NotFound:
                # Сообщение было удалено, просто игнорируем
                pass
            except discord.HTTPException as e:
                print(f"HTTP ошибка при редактировании: {e}")
            except Exception as e:
                print(f"Ошибка редактирования сообщения: {e}")
                
        except Exception as e:
            print(f"Ошибка в update_queue_message: {e}")


class MusicControls(View):
    def __init__(self, bot_instance, ctx):
        super().__init__(timeout=None)
        self.bot = bot_instance
        self.ctx = ctx
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not self.ctx.voice_client:
            await interaction.response.send_message("❌ Бот не в голосовом канале", ephemeral=True)
            return False
        if not interaction.user.voice or interaction.user.voice.channel != self.ctx.voice_client.channel:
            await interaction.response.send_message("❌ Ты не в голосовом канале с ботом", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.secondary, custom_id="prev_main")
    async def prev_btn(self, interaction: discord.Interaction, button: Button):
        await self.do_previous(interaction)

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.secondary, custom_id="pause_main")
    async def pause_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_playing():
            self.ctx.voice_client.pause()
            await interaction.response.edit_message(content="⏸️ Пауза")
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary, custom_id="resume_main")
    async def resume_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and self.ctx.voice_client.is_paused():
            self.ctx.voice_client.resume()
            await interaction.response.edit_message(content="▶️ Продолжаю")
        else:
            await interaction.response.send_message("❌ Нет паузы", ephemeral=True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary, custom_id="skip_main")
    async def skip_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and (self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused()):
            self.ctx.voice_client.stop()
            await interaction.response.send_message("⏭️ Пропущено", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger, custom_id="delete_main")
    async def delete_btn(self, interaction: discord.Interaction, button: Button):
        if self.ctx.voice_client and (self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused()):
            self.ctx.voice_client.stop()
            await interaction.response.send_message("🗑️ Трек удален", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Ничего не играет", ephemeral=True)

    @discord.ui.button(label="📜", style=discord.ButtonStyle.secondary, row=1, custom_id="queue_main")
    async def queue_btn(self, interaction: discord.Interaction, button: Button):
        queue_list = self.bot.get_queue(self.ctx.guild.id)
        current = self.bot.current.get(self.ctx.guild.id)
        
        if not current and not queue_list:
            await interaction.response.send_message("📭 Очередь пуста", ephemeral=True)
            return
        
        embed = discord.Embed(title="📜 Текущая очередь", color=discord.Color.purple())
        
        if current:
            start_time = self.bot.start_times.get(self.ctx.guild.id, time.time())
            elapsed = int(time.time() - start_time)
            total = current.get('duration_seconds', 0)
            progress_bar = self.bot.create_progress_bar(elapsed, total)
            time_str = self.bot.format_duration(elapsed)
            total_str = current['duration']
            
            embed.add_field(
                name="▶️ Сейчас",
                value=f"[{current['title'][:40]}...]({current['webpage_url']})\n`{progress_bar}`\n`{time_str} / {total_str}`",
                inline=False
            )
        
        if queue_list:
            text = ""
            for i, song in enumerate(queue_list[:10], 1):
                text += f"`{i}.` {song['title'][:30]}... | `{song['duration']}`\n"
            if len(queue_list) > 10:
                text += f"\n*...и еще {len(queue_list)-10}*"
            embed.add_field(name=f"Далее ({len(queue_list)}):", value=text, inline=False)
        else:
            embed.add_field(name="Далее:", value="📭 Пусто", inline=False)
        
        history_count = len(self.bot.history.get(self.ctx.guild.id, []))
        embed.set_footer(text=f"⏮️ История: {history_count} треков | Выбери трек из списка ниже ⬇️")
        
        view = QueueView(self.bot, self.ctx)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🔁", style=discord.ButtonStyle.secondary, row=1, custom_id="loop_main")
    async def loop_btn(self, interaction: discord.Interaction, button: Button):
        current_mode = self.bot.loop_modes.get(self.ctx.guild.id, 'off')
        modes = {'off': 'one', 'one': 'all', 'all': 'off'}
        new_mode = modes[current_mode]
        self.bot.loop_modes[self.ctx.guild.id] = new_mode
        emojis = {'off': '❌', 'one': '🔂', 'all': '🔁'}
        await interaction.response.send_message(f"{emojis[new_mode]} Режим повтора: {new_mode}", ephemeral=True)

    @discord.ui.button(label="🔀", style=discord.ButtonStyle.secondary, row=1, custom_id="shuffle_main")
    async def shuffle_btn(self, interaction: discord.Interaction, button: Button):
        queue = self.bot.get_queue(self.ctx.guild.id)
        if len(queue) < 2:
            await interaction.response.send_message("❌ Недостаточно треков", ephemeral=True)
            return
        rand.shuffle(queue)
        await interaction.response.send_message(f"🔀 Очередь перемешана! ({len(queue)} треков)", ephemeral=True)

    @discord.ui.button(label="🎲", style=discord.ButtonStyle.primary, row=1, custom_id="add_random")
    async def add_random_btn(self, interaction: discord.Interaction, button: Button):
        count = rand.randint(3, 8)
        rarity = rand.choice(["any", "medium", "deep"])
        
        await interaction.response.send_message("🎲 Ищу случайные треки...", ephemeral=True)
        added = await self.bot.add_random_tracks(self.ctx, count=count, rarity=rarity)
        await interaction.followup.send(f"✅ Добавлено {added} треков в очередь!", ephemeral=True)
    
    @discord.ui.button(label="💰 Фонд", style=discord.ButtonStyle.success, row=1, custom_id="fund_btn")
    async def fund_btn(self, interaction: discord.Interaction, button: Button):
        admin_id = os.getenv('ADMIN_ID')
        is_admin = str(interaction.user.id) == admin_id if admin_id else False
        
        view = FundView(self.bot, is_admin)
        embed = view.create_fund_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def do_previous(self, interaction):
        history = self.bot.history.get(self.ctx.guild.id, [])
        if not history:
            await interaction.response.send_message("❌ Нет предыдущих треков", ephemeral=True)
            return
        
        prev_song = history.pop()
        queue = self.bot.get_queue(self.ctx.guild.id)
        
        current = self.bot.current.get(self.ctx.guild.id)
        if current and self.ctx.voice_client.is_playing():
            queue.insert(0, current)
        
        queue.insert(0, prev_song)
        self.ctx.voice_client.stop()
        await interaction.response.send_message("⏮️ Возвращаю предыдущий трек", ephemeral=True)


class MusicBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            case_insensitive=True
        )
        
        self.queues = {}
        self.current = {}
        self.history = {}
        self.loop_modes = {}
        self.start_times = {}
        self.search_cache = OrderedDict()
        self.MAX_CACHE_SIZE = 50
        self.MAX_DURATION_SECONDS = 420
        
        self.played_tracks = {}
        self.MAX_HISTORY_TRACKS = 20
        
        self.fund = FundManager()
        da_token = os.getenv('DONATIONALERTS_TOKEN')
        self.da_api = DonationAlertsAPI(da_token) if da_token else None

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

    def get_history(self, guild_id):
        if guild_id not in self.history:
            self.history[guild_id] = []
        return self.history[guild_id]

    def get_cached_search(self, query, max_results):
        cache_key = f"{query}_{max_results}"
        if cache_key in self.search_cache:
            self.search_cache.move_to_end(cache_key)
            return self.search_cache[cache_key]
        return None

    def set_cached_search(self, query, max_results, results):
        cache_key = f"{query}_{max_results}"
        self.search_cache[cache_key] = results
        self.search_cache.move_to_end(cache_key)
        if len(self.search_cache) > self.MAX_CACHE_SIZE:
            self.search_cache.popitem(last=False)

    def generate_smart_query(self, guild_id):
        if guild_id not in self.played_tracks:
            self.played_tracks[guild_id] = []
        
        available_base = [q for q in BASE_QUERIES if q not in self.played_tracks[guild_id]]
        if not available_base:
            self.played_tracks[guild_id] = []
            available_base = BASE_QUERIES
        
        base = rand.choice(available_base)
        self.played_tracks[guild_id].append(base)
        if len(self.played_tracks[guild_id]) > self.MAX_HISTORY_TRACKS:
            self.played_tracks[guild_id].pop(0)
        
        modifiers = []
        
        if rand.random() < 0.7:
            year = rand.choice(YEAR_MODIFIERS)
            if year:
                modifiers.append(year)
        
        if rand.random() < 0.5:
            style = rand.choice(STYLE_MODIFIERS)
            if style:
                modifiers.append(style)
        
        if rand.random() < 0.3:
            mood = rand.choice(MOOD_MODIFIERS)
            if mood:
                modifiers.append(mood)
        
        if modifiers:
            query = f"{base} {' '.join(modifiers)}"
        else:
            query = base
        
        return query.strip()

    async def search_youtube(self, query, max_results=5):
        """Быстрый поиск с extract_flat (только метаданные)"""
        cached = self.get_cached_search(query, max_results)
        if cached:
            return cached

        def search():
            with youtube_dl.YoutubeDL(YDL_SEARCH_OPTIONS) as ydl:
                try:
                    if 'youtube.com' in query or 'youtu.be' in query:
                        info = ydl.extract_info(query, download=False)
                        return [info] if 'entries' not in info else info['entries']
                    else:
                        info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
                        entries = info.get('entries', [])
                        return [e for e in entries if e is not None]
                except Exception as e:
                    print(f"Ошибка поиска: {e}")
                    return None
        
        try:
            loop = asyncio.get_event_loop()
            results = await asyncio.wait_for(
                loop.run_in_executor(None, search),
                timeout=15.0
            )
            if results:
                self.set_cached_search(query, max_results, results)
            return results
        except asyncio.TimeoutError:
            print(f"Таймаут поиска: {query}")
            return None
        except Exception as e:
            print(f"Ошибка: {e}")
            return None

    async def extract_video_info(self, video_id_or_url):
        """Полное извлечение для конкретного видео (получение прямой ссылки)"""
        def extract():
            with youtube_dl.YoutubeDL(YDL_EXTRACT_OPTIONS) as ydl:
                try:
                    if len(video_id_or_url) == 11 and ' ' not in video_id_or_url:
                        url = f"https://www.youtube.com/watch?v={video_id_or_url}"
                    else:
                        url = video_id_or_url
                    
                    info = ydl.extract_info(url, download=False)
                    return info
                except Exception as e:
                    error_msg = str(e)
                    if "not available" in error_msg or "age-restricted" in error_msg:
                        return {"error": "unavailable", "message": error_msg}
                    print(f"Ошибка извлечения видео: {e}")
                    return None
        
        try:
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, extract),
                timeout=10.0
            )
            return result
        except asyncio.TimeoutError:
            return {"error": "timeout"}
        except Exception as e:
            print(f"Ошибка извлечения: {e}")
            return None

    async def add_random_tracks(self, ctx, count=5, rarity="any"):
        """Исправленная версия: один запрос = один трек"""
        added = 0
        attempts = 0
        max_attempts = count * 4
        
        added_video_ids = set()
        
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            return 0
        
        # Генерируем отдельный запрос для КАЖДОГО трека
        while added < count and attempts < max_attempts:
            query = self.generate_smart_query(ctx.guild.id)
            
            # Ищем всего 5 результатов (достаточно для 1 трека)
            results = await self.search_youtube(query, max_results=5)
            
            if not results or len(results) == 0:
                attempts += 1
                await asyncio.sleep(0.3)
                continue
            
            # Перемешиваем и ищем первый подходящий
            rand.shuffle(results)
            found_in_this_query = False
            
            for entry in results:
                if not entry:
                    continue
                
                video_id = entry.get('id') or entry.get('url', '').split('v=')[-1].split('&')[0]
                
                if video_id in added_video_ids:
                    continue
                
                # Быстрая проверка длительности из flat info
                duration = entry.get('duration') or 0
                if duration > self.MAX_DURATION_SECONDS:
                    continue
                
                # Проверка просмотров
                views = entry.get('view_count', 0) or 0
                if rarity == "deep" and not (1000 <= views <= 500000):
                    continue
                elif rarity == "medium" and not (10000 <= views <= 2000000):
                    continue
                
                # Полное извлечение только для одного трека
                full_info = await self.extract_video_info(video_id)
                
                if not full_info or full_info.get('error'):
                    continue
                
                real_duration = full_info.get('duration', 0)
                if real_duration <= 0 or real_duration > self.MAX_DURATION_SECONDS:
                    continue
                
                # Добавляем трек
                song = {
                    'title': full_info['title'],
                    'url': full_info['url'],
                    'webpage_url': full_info['webpage_url'],
                    'thumbnail': full_info.get('thumbnail'),
                    'duration': self.format_duration(real_duration),
                    'duration_seconds': real_duration,
                    'requester': ctx.author.name,
                    'views': full_info.get('view_count', 0) or 0
                }
                
                added_video_ids.add(video_id)
                self.get_queue(ctx.guild.id).append(song)
                added += 1
                found_in_this_query = True
                
                # Запускаем первый трек
                if not ctx.voice_client.is_playing() and not self.current.get(ctx.guild.id):
                    try:
                        await self.play_next(ctx)
                    except Exception as e:
                        print(f"Ошибка воспроизведения: {e}")
                
                break  # <-- КЛЮЧЕВОЕ: берем только 1 трек из поиска и выходим
            
            if not found_in_this_query:
                attempts += 1
            
            # Небольшая пауза между поисками
            if added < count:
                await asyncio.sleep(0.4)
        
        return added

    def format_duration(self, seconds):
        """Исправлено: приведение к int для избежания ошибки форматирования"""
        if not seconds or seconds <= 0:
            return "N/A"
        seconds = int(seconds)  # Приведение к int
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"

    def create_progress_bar(self, current, total, length=15):
        """Исправлено: обработка float значений"""
        if not total or total <= 0:
            return "▬" * length
        current = float(current)
        total = float(total)
        progress = min(current / total, 1.0)
        filled = int(length * progress)
        empty = length - filled
        if empty > 0:
            return "▬" * filled + "🔘" + "▬" * (empty - 1)
        return "▬" * length

    async def play_next(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        history = self.get_history(ctx.guild.id)
        
        if queue:
            song = queue.pop(0)
            current = self.current.get(ctx.guild.id)
            
            if current:
                history.append(current)
                if len(history) > 20:
                    history.pop(0)
            
            if self.loop_modes.get(ctx.guild.id) == 'one':
                queue.insert(0, song.copy())
            elif self.loop_modes.get(ctx.guild.id) == 'all':
                queue.append(song.copy())
            
            self.current[ctx.guild.id] = song
            self.start_times[ctx.guild.id] = time.time()
            
            if not ctx.voice_client:
                return
            
            source = discord.FFmpegPCMAudio(song['url'], **FFMPEG_OPTIONS)
            
            def after_playing(error):
                if error:
                    print(f"Ошибка: {error}")
                asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.loop)
            
            ctx.voice_client.play(source, after=after_playing)
            
            duration = song.get('duration_seconds', 0)
            duration_str = self.format_duration(duration)
            views = song.get('views', 0)
            views_str = f"👁️ {int(views):,}" if views else ""  # Приведение к int
            
            embed = discord.Embed(
                title="▶️ Сейчас играет",
                description=f"[{song['title']}]({song['webpage_url']})",
                color=discord.Color.green()
            )
            
            if song.get('thumbnail'):
                embed.set_thumbnail(url=song['thumbnail'])
            
            progress_bar = self.create_progress_bar(0, duration)
            embed.add_field(name="Прогресс", value=f"`{progress_bar}` 0:00 / {duration_str}", inline=False)
            
            if views_str:
                embed.add_field(name="Просмотры", value=views_str, inline=True)
            
            embed.set_footer(text=f"Запросил: {song['requester']} | 🔁 {self.loop_modes.get(ctx.guild.id, 'off')}")
            
            view = MusicControls(self, ctx)
            msg = await ctx.send(embed=embed, view=view)
            
            if duration > 0:
                asyncio.create_task(self.update_progress_bar(ctx, msg, duration))
        else:
            self.current[ctx.guild.id] = None
            self.start_times[ctx.guild.id] = None
            await ctx.send("✅ Очередь закончилась. Отключаюсь через 30 секунд...")
            await asyncio.sleep(30)
            if ctx.voice_client and not self.current.get(ctx.guild.id):
                await ctx.voice_client.disconnect()

    async def update_progress_bar(self, ctx, message, total_duration):
        """Обновление прогресса с увеличенным интервалом (10 сек)"""
        start_time = self.start_times.get(ctx.guild.id, time.time())
        last_update = -1
        
        await asyncio.sleep(2)
        
        while (ctx.voice_client and 
               (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()) and
               self.current.get(ctx.guild.id)):
            
            current_time = time.time() - start_time
            
            if current_time > total_duration:
                break
            
            current_int = int(current_time)
            
            # Обновляем каждые 10 секунд (было 5) + первые 2 секунды
            if (current_int % 10 == 0 and current_int != last_update) or current_time < 2:
                last_update = current_int
                try:
                    embed = message.embeds[0]
                    progress_bar = self.create_progress_bar(current_time, total_duration)
                    time_str = self.format_duration(current_int)
                    total_str = self.format_duration(total_duration)
                    
                    embed.set_field_at(0, name="Прогресс", 
                                     value=f"`{progress_bar}` {time_str} / {total_str}", 
                                     inline=False)
                    await message.edit(embed=embed)
                except discord.NotFound:
                    # Сообщение удалено
                    break
                except discord.HTTPException:
                    # Rate limit или другая ошибка HTTP
                    break
                except Exception as e:
                    print(f"Ошибка обновления прогресса: {e}")
                    break
            
            await asyncio.sleep(1)

    async def add_to_queue(self, ctx, song_info):
        if not song_info.get('url') or 'googlevideo' not in song_info.get('url', ''):
            full_info = await self.extract_video_info(song_info.get('webpage_url') or song_info.get('id'))
            if full_info and not full_info.get('error'):
                song_info = full_info
            else:
                await ctx.send("❌ Не удалось получить ссылку на видео (возможно, недоступно)")
                return

        song = {
            'title': song_info['title'],
            'url': song_info['url'],
            'webpage_url': song_info['webpage_url'],
            'thumbnail': song_info.get('thumbnail'),
            'duration': self.format_duration(song_info.get('duration', 0)),
            'duration_seconds': song_info.get('duration', 0) if isinstance(song_info.get('duration'), (int, float)) else 0,
            'requester': ctx.author.name,
            'views': song_info.get('view_count', 0) or 0
        }
        
        if ctx.voice_client and ctx.voice_client.is_playing():
            self.get_queue(ctx.guild.id).append(song)
            embed = discord.Embed(
                title="📝 Добавлено в очередь",
                description=f"[{song['title']}]({song['webpage_url']})",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=song['thumbnail'])
            embed.add_field(name="Длительность", value=song['duration'], inline=True)
            embed.add_field(name="Позиция", value=len(self.get_queue(ctx.guild.id)), inline=True)
            if song['views']:
                embed.add_field(name="Просмотры", value=f"👁️ {int(song['views']):,}", inline=True)  # Приведение к int
            await ctx.send(embed=embed)
        else:
            self.get_queue(ctx.guild.id).append(song)
            await self.play_next(ctx)


bot = MusicBot()

@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен! (Исправленная версия)')
    print('⚡ Обработка удаленных сообщений и приведение типов')
    if not os.path.exists("fund.json"):
        print("💰 Фонд инициализирован (fund.json создан)")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    
    voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    
    if before.channel and voice_client and voice_client.channel == before.channel:
        members = [m for m in before.channel.members if not m.bot]
        if len(members) == 0:
            await asyncio.sleep(5)
            members = [m for m in before.channel.members if not m.bot]
            if len(members) == 0 and voice_client.is_connected():
                await voice_client.disconnect()

@bot.command()
async def start(ctx):
    if not ctx.author.voice:
        return await ctx.send("❌ Сначала зайди в голосовой канал!")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        await ctx.send(f"✅ Подключился к **{ctx.author.voice.channel.name}**")
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        return await ctx.send(f"❌ Бот занят в другом канале: **{ctx.voice_client.channel.name}**")
    
    current = bot.current.get(ctx.guild.id)
    queue_list = bot.get_queue(ctx.guild.id)
    
    if current:
        duration = current.get('duration_seconds', 0)
        duration_str = bot.format_duration(duration)
        views = current.get('views', 0)
        
        embed = discord.Embed(
            title="🎵 Панель управления",
            description=f"[{current['title']}]({current['webpage_url']})",
            color=discord.Color.green()
        )
        
        if current.get('thumbnail'):
            embed.set_thumbnail(url=current['thumbnail'])
        
        start_time = bot.start_times.get(ctx.guild.id, time.time())
        elapsed = int(time.time() - start_time)
        progress_bar = bot.create_progress_bar(elapsed, duration)
        time_str = bot.format_duration(elapsed)
        
        embed.add_field(name="Прогресс", value=f"`{progress_bar}` {time_str} / {duration_str}", inline=False)
        if views:
            embed.add_field(name="Просмотры", value=f"👁️ {int(views):,}", inline=True)  # Приведение к int
        embed.add_field(name="В очереди", value=f"{len(queue_list)} треков", inline=True)
        embed.add_field(name="Режим", value=f"🔁 {bot.loop_modes.get(ctx.guild.id, 'off')}", inline=True)
        embed.set_footer(text=f"Запросил: {current['requester']} | 💰 Фонд: {bot.fund.get_percent()}%")
        
        view = MusicControls(bot, ctx)
        await ctx.send(embed=embed, view=view)
    else:
        embed = discord.Embed(
            title="🎵 Панель управления",
            description="Готов играть! Используй кнопки ниже:",
            color=discord.Color.blue()
        )
        embed.add_field(name="В очереди", value=f"{len(queue_list)} треков", inline=True)
        embed.add_field(name="Режим", value=f"🔁 {bot.loop_modes.get(ctx.guild.id, 'off')}", inline=True)
        embed.add_field(name="Фонд", value=f"💰 {bot.fund.get_percent()}% к Raspberry Pi", inline=True)
        embed.set_footer(text="🎲 — случайные треки | 💰 — поддержать проект")
        
        view = MusicControls(bot, ctx)
        await ctx.send(embed=embed, view=view)

@bot.command()
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("❌ Зайди в голосовой канал!")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        return await ctx.send("❌ Бот занят в другом канале!")
    
    async with ctx.typing():
        results = await bot.search_youtube(query, max_results=5)
    
    if not results or len(results) == 0:
        return await ctx.send("❌ Не удалось найти видео!")
    
    first = results[0]
    full_info = await bot.extract_video_info(first.get('id') or first.get('webpage_url'))
    
    if not full_info or full_info.get('error'):
        return await ctx.send("❌ Найдено видео недоступно (возрастное ограничение или удалено)")
    
    await bot.add_to_queue(ctx, full_info)

@bot.command()
async def previous(ctx):
    if not ctx.voice_client:
        return await ctx.send("❌ Ничего не играет")
    
    history = bot.get_history(ctx.guild.id)
    if not history:
        return await ctx.send("❌ Нет предыдущих треков")
    
    prev_song = history.pop()
    queue = bot.get_queue(ctx.guild.id)
    
    current = bot.current.get(ctx.guild.id)
    if current and ctx.voice_client.is_playing():
        queue.insert(0, current)
    
    queue.insert(0, prev_song)
    ctx.voice_client.stop()
    await ctx.send(f"⏮️ Возвращаю: {prev_song['title'][:40]}...")

@bot.command()
async def search(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("❌ Зайди в голосовой канал!")
    
    async with ctx.typing():
        results = await bot.search_youtube(query, max_results=5)
    
    if not results or len(results) == 0:
        return await ctx.send("❌ Ничего не найдено!")
    
    embed = discord.Embed(
        title=f"🔍 Результаты: {query}",
        description="Напиши номер (1-5) или `отмена`",
        color=discord.Color.gold()
    )
    
    for i, video in enumerate(results[:5], 1):
        duration = bot.format_duration(video.get('duration', 0))
        views = video.get('view_count', 0)
        views_str = f"👁️ {int(views):,}" if views else "👁️ скрыто"  # Приведение к int
        embed.add_field(
            name=f"{i}. {video['title'][:45]}",
            value=f"⏱️ {duration} | {views_str}",
            inline=False
        )
    
    await ctx.send(embed=embed)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and \
               (m.content.isdigit() and 1 <= int(m.content) <= 5 or m.content.lower() in ['отмена', 'cancel'])
    
    try:
        response = await bot.wait_for('message', check=check, timeout=30.0)
        
        if response.content.lower() in ['отмена', 'cancel']:
            return await ctx.send("❌ Отменено")
        
        choice = int(response.content) - 1
        selected = results[choice]
        
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            return await ctx.send("❌ Бот занят в другом канале!")
        
        full_info = await bot.extract_video_info(selected.get('id') or selected.get('webpage_url'))
        if not full_info or full_info.get('error'):
            return await ctx.send("❌ Выбранное видео недоступно")
        
        await bot.add_to_queue(ctx, full_info)
        
    except asyncio.TimeoutError:
        await ctx.send("⏰ Время вышло!")

@bot.command()
async def random(ctx, rarity="any"):
    if not ctx.author.voice:
        return await ctx.send("❌ Зайди в голосовой канал!")
    
    if rarity not in ["any", "medium", "deep"]:
        rarity = "any"
    
    query = bot.generate_smart_query(ctx.guild.id)
    await ctx.send(f"🎲 Ищу `{query}` ({rarity})...")
    
    results = await bot.search_youtube(query, max_results=15)
    
    if not results or len(results) == 0:
        return await ctx.send("❌ Ничего не найдено по этому запросу!")
    
    candidates = []
    for video in results:
        if not video:
            continue
        candidates.append(video)
    
    rand.shuffle(candidates)
    
    for candidate in candidates:
        full_info = await bot.extract_video_info(candidate.get('id') or candidate.get('webpage_url'))
        
        if not full_info or full_info.get('error'):
            continue
        
        dur = full_info.get('duration', 0)
        if not isinstance(dur, (int, float)) or dur <= 0 or dur > bot.MAX_DURATION_SECONDS:
            continue
        
        views = full_info.get('view_count', 0) or 0
        
        if rarity == "deep" and not (1000 <= views <= 500000):
            continue
        elif rarity == "medium" and not (10000 <= views <= 2000000):
            continue
        
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            return await ctx.send("❌ Бот занят в другом канале!")
        
        views_str = f"👁️ {int(views):,}" if views else ""  # Приведение к int
        duration_str = bot.format_duration(dur)
        
        await ctx.send(f"🎲 **Найдено:** `{query}` | ⏱️ `{duration_str}` | {views_str}")
        await bot.add_to_queue(ctx, full_info)
        return
    
    await ctx.send("❌ Не удалось найти подходящий трек (все недоступны или не подходят по фильтрам)")

@bot.command()
async def addrandom(ctx, count: int = 5, rarity: str = "any"):
    if not ctx.author.voice:
        return await ctx.send("❌ Зайди в голосовой канал!")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        return await ctx.send("❌ Бот занят в другом канале!")
    
    if count > 15:
        count = 15
    
    if rarity not in ["any", "medium", "deep"]:
        rarity = "any"
    
    rarity_desc = {"any": "любые", "medium": "средней популярности", "deep": "редкие (1к-500к)"}
    
    msg = await ctx.send(f"🎲 Добавляю {count} {rarity_desc[rarity]} треков...")
    added = await bot.add_random_tracks(ctx, count=count, rarity=rarity)
    await msg.edit(content=f"✅ Добавлено {added} треков в очередь!")

@bot.command()
async def fund(ctx):
    admin_id = os.getenv('ADMIN_ID')
    is_admin = str(ctx.author.id) == admin_id if admin_id else False
    
    view = FundView(bot, is_admin)
    embed = view.create_fund_embed()
    await ctx.send(embed=embed, view=view)

@bot.command()
async def loop(ctx, mode: str = None):
    if mode not in ['off', 'one', 'all', None]:
        return await ctx.send("❌ Используй: `off`, `one` (текущий), `all` (очередь)")
    
    if mode is None:
        current = bot.loop_modes.get(ctx.guild.id, 'off')
        await ctx.send(f"🔁 Текущий режим: `{current}`")
        return
    
    bot.loop_modes[ctx.guild.id] = mode
    emojis = {'off': '❌', 'one': '🔂', 'all': '🔁'}
    await ctx.send(f"{emojis[mode]} Режим повтора: `{mode}`")

@bot.command()
async def remove(ctx, index: int):
    queue = bot.get_queue(ctx.guild.id)
    
    if not queue:
        return await ctx.send("📭 Очередь пуста")
    
    if index < 1 or index > len(queue):
        return await ctx.send(f"❌ Укажи номер от 1 до {len(queue)}")
    
    removed = queue.pop(index - 1)
    embed = discord.Embed(
        title="🗑️ Удалено из очереди",
        description=f"[{removed['title'][:50]}...]({removed['webpage_url']})",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def shuffle(ctx):
    queue = bot.get_queue(ctx.guild.id)
    if len(queue) < 2:
        return await ctx.send("❌ Недостаточно треков")
    
    rand.shuffle(queue)
    await ctx.send(f"🔀 Очередь перемешана! ({len(queue)} треков)")

@bot.command()
async def queue(ctx):
    queue_list = bot.get_queue(ctx.guild.id)
    current = bot.current.get(ctx.guild.id)
    
    if not current and not queue_list:
        return await ctx.send("📭 Очередь пуста")
    
    embed = discord.Embed(title="📜 Плейлист", color=discord.Color.purple())
    
    if current:
        start_time = bot.start_times.get(ctx.guild.id, time.time())
        elapsed = int(time.time() - start_time)
        total = current.get('duration_seconds', 0)
        
        progress_bar = bot.create_progress_bar(elapsed, total)
        time_str = bot.format_duration(elapsed)
        total_str = current['duration']
        views = current.get('views', 0)
        views_str = f" | 👁️ {int(views):,}" if views else ""  # Приведение к int
        
        embed.add_field(
            name="▶️ Сейчас играет",
            value=f"[{current['title']}]({current['webpage_url']})\n"
                  f"`{progress_bar}`\n"
                  f"`{time_str} / {total_str}`{views_str}",
            inline=False
        )
        
        loop_mode = bot.loop_modes.get(ctx.guild.id, 'off')
        if loop_mode != 'off':
            embed.add_field(name="🔁 Режим", value=loop_mode, inline=True)
    
    if queue_list:
        text = ""
        for i, song in enumerate(queue_list[:10], 1):
            views = song.get('views', 0)
            views_str = f"👁️ {int(views):,}" if views else ""  # Приведение к int
            text += f"`{i}.` [{song['title'][:35]}...]({song['webpage_url']}) | `{song['duration']}` {views_str}\n"
        if len(queue_list) > 10:
            text += f"\n*...и еще {len(queue_list)-10}*"
        embed.add_field(name=f"В очереди ({len(queue_list)}):", value=text, inline=False)
    else:
        embed.add_field(name="В очереди:", value="📭 Пусто", inline=False)
    
    history_count = len(bot.history.get(ctx.guild.id, []))
    embed.set_footer(text=f"⏮️ История: {history_count} треков | 💰 Фонд: {bot.fund.get_percent()}%")
    
    await ctx.send(embed=embed)

@bot.command()
async def skip(ctx):
    if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
        ctx.voice_client.stop()
        await ctx.send("⏭️ Пропущено")
    else:
        await ctx.send("❌ Ничего не играет")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        bot.queues[ctx.guild.id] = []
        bot.current[ctx.guild.id] = None
        bot.history[ctx.guild.id] = []
        bot.start_times[ctx.guild.id] = None
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Остановлено. Пока!")
    else:
        await ctx.send("❌ Я не в канале")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Отключаюсь")
    else:
        await ctx.send("❌ Я не в канале")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Пауза")
    else:
        await ctx.send("❌ Ничего не играет")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Продолжаю")
    else:
        await ctx.send("❌ Нет паузы")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🎵 Sickwell Music Bot",
        description="Музыкальный бот с умным рандомом (исправленная версия)",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎛️ Основное",
        value="`!start` — Подключиться и открыть панель\n"
              "`!play <запрос>` — Включить трек\n"
              "`!addrandom [N] [any/medium/deep]` — Добавить N случайных треков\n"
              "`!search <запрос>` — Выбрать из 5 вариантов\n"
              "`!random [rarity]` — Один случайный трек",
        inline=False
    )
    
    embed.add_field(
        name="📜 Очередь",
        value="`!queue` — Показать очередь (с просмотрами)\n"
              "`!remove <номер>` — Удалить трек\n"
              "`!shuffle` — Перемешать\n"
              "`!skip` / `!previous` — Навигация",
        inline=False
    )
    
    embed.add_field(
        name="🎲 Умный рандом",
        value="Комбинирует теги + модификаторы (год/стиль/настроение)\n"
              "Фильтры: `any` (любые), `medium` (10к-2млн), `deep` (1к-500к просмотров)",
        inline=False
    )
    
    embed.add_field(
        name="💰 Server Fund",
        value="`!fund` — Показать сбор на Raspberry Pi\n"
              "Цель: 20 000₽ на свою железку\n"
              "Кнопка 💰 в плеере или команда `!fund`",
        inline=False
    )
    
    embed.add_field(
        name="⌨️ Кнопки",
        value="`⏮️⏸️▶️⏭️` — Управление (серые)\n"
              "`🗑️🚪` — Удалить/Выйти (красные)\n"
              "`🎲` — Рандом (желтая)\n"
              "`💰` — Фонд (зеленая)",
        inline=False
    )
    
    embed.set_footer(text="⚡ Быстрый поиск | Умный рандом | Прозрачный фонд")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Укажи аргумент! Например: `!play` или `!random deep`")
    else:
        print(f"Ошибка: {error}")

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("❌ Создай файл .env с DISCORD_TOKEN=твой_токен")
        print("❌ И DONATIONALERTS_TOKEN=твой_токен_да (опционально)")
        input("Нажми Enter...")
    else:
        bot.run(TOKEN)