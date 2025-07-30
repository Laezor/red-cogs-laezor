from redbot.core import commands
import aiohttp
import re
import random
import asyncio

NUM_GAMES = 12

class RandomSteamCog(commands.Cog):
    """Get a random Steam game with a shuffling animation!"""
    def __init__(self, bot):
        self.bot = bot

    async def get_random_appid(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://store.steampowered.com/explore/random/") as r:
                    text = await r.text()
            match = re.search(r"app/(\d+)", text)
            return match.group(1) if match else None
        except Exception as e:
            return None

    async def get_app_details(self, appid):
        try:
            url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.json()
            if not data[appid]["success"]:
                return None
            return data[appid]["data"]
        except Exception as e:
            return None

    def is_game_valid(self, app):
        try:
            if app.get("type") != "game":
                return False
            if app.get("release_date", {}).get("coming_soon"):
                return False
            if app.get("ratings", {}).get("steam_germany", {}).get("rating") == "BANNED":
                return False
            germany_desc = app.get("ratings", {}).get("steam_germany", {}).get("descriptors", [])
            dejus_desc = app.get("ratings", {}).get("dejus", {}).get("descriptors", [])
            banned_keywords = ["Sexuelle", "Schimpfwörte"]
            banned_dejus = ["Nudez"]
            if any(word in germany_desc for word in banned_keywords):
                return False
            if any(word in dejus_desc for word in banned_dejus):
                return False
            return True
        except:
            return False

    def safe_join(self, items):
        if not items:
            return ""
        return ", ".join(item.get("description", "") if isinstance(item, dict) else item for item in items)

    @commands.command()
    async def randomsteam(self, ctx):
        """Get a random Steam game with a shuffling animation!"""
        await ctx.send("Selecting a game, please wait!\n")
        game_list = []
        seen_ids = set()
        # Fetch games
        while len(game_list) < NUM_GAMES:
            appid = await self.get_random_appid()
            if not appid or appid in seen_ids:
                continue
            app = await self.get_app_details(appid)
            if app and self.is_game_valid(app):
                seen_ids.add(appid)
                app["steam_appid"] = appid
                game_list.append(app)
        # Shuffling animation
        msg = await ctx.send("\nShuffling Game List!")
        for i in range(6):
            random.shuffle(game_list)
            await msg.edit(content=f"Shuffling{' .' * (i % 4)}")
            await asyncio.sleep(0.5)
        # Pick a game
        selected_game = random.choice(game_list)
        info = {
            "Game Name": selected_game.get("name"),
            "Developer(s)": ", ".join(selected_game.get("developers", [])),
            "Publisher(s)": ", ".join(selected_game.get("publishers", [])),
            "Description": selected_game.get("short_description"),
            "Features": self.safe_join(selected_game.get("categories", [])),
            "Genres": self.safe_join(selected_game.get("genres", [])),
            "Is Free": selected_game.get("is_free"),
            "Required Age": selected_game.get("required_age"),
            "Release Date": selected_game.get("release_date", {}).get("date"),
            "Total Recommendations": selected_game.get("recommendations", {}).get("total"),
            "More Details": f"https://store.steampowered.com/app/{selected_game.get('steam_appid')}"
        }
        # Format info for Discord
        embed_lines = [f"**{k}:** {v}" for k, v in info.items() if v]
        await ctx.send("\n**🎲 Chosen Game Below!**\n" + "\n".join(embed_lines))


