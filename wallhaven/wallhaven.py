from redbot.core import commands
import aiohttp

api_url = "https://wallhaven.cc/api/v1/search?sorting=random"

class WallhavenCog(commands.Cog):
    """Wallhaven image search"""
    def __init__(self, bot):
        self.bot = bot

    async def get_random_wallhaven_image(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()
            
                return data["data"][0]["path"]

    @commands.command()
    async def wallhaven(self, ctx):
        await ctx.send(await self.get_random_wallhaven_image())










