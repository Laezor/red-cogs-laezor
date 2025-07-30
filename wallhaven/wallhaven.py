from redbot.core import commands
import aiohttp
import discord

class WallhavenCategoryView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30)
        self.bot = bot
        self.value = None

        self.add_item(WallhavenCategorySelect(self))

class WallhavenCategorySelect(discord.ui.Select):
    def __init__(self, view: WallhavenCategoryView):
        options = [
            discord.SelectOption(label="General", value="100", description="General wallpapers"),
            discord.SelectOption(label="Anime", value="101", description="Anime wallpapers"),
            discord.SelectOption(label="People", value="111", description="People wallpapers"),
        ]

        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self.view = view

    async def callback(self, interaction: discord.Interaction):
        category_value = self.values[0]
        await interaction.response.defer()

        url = f"https://wallhaven.cc/api/v1/search?sorting=random&categories={category_value}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                image_url = data["data"][0]["path"]

        await interaction.followup.send(image_url)
        self.view.stop()


class WallhavenCog(commands.Cog):
    """Wallhaven image search with category selection"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallhaven(self, ctx):
        """Search for a random Wallhaven image by category"""
        view = WallhavenCategoryView(self.bot)
        await ctx.send("Choose a wallpaper category:", view=view)
