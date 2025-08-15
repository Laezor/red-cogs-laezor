import aiohttp
from redbot.core import commands, app_commands
from discord import Interaction

class ProtonDBSearch(commands.Cog):
    """Search for games on the ProtonDB."""

    def __init__(self, bot):
        self.bot = bot

    async def steam_autocomplete(self, interaction: Interaction, current: str):
        """Fetch autocomplete suggestions from Steam's storesearch API."""
        if not current:
            return []

        url = "https://store.steampowered.com/api/storesearch/"
        params = {
            "term": current,
            "l": "english",
            "cc": "NL"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=5) as resp:
                    if resp.status != 200:
                        return []
                    data = await resp.json()
        except Exception:
            return []

        suggestions = []
        for item in data.get("items", [])[:25]:  # Discord max is 25
            title = item.get("name")
            appid = item.get("id")
            if title and appid:
                suggestions.append(app_commands.Choice(name=title, value=str(appid)))

        return suggestions

    @commands.hybrid_command(name="steamsearch", description="Search for a game on Steam")
    @app_commands.describe(game="Start typing to search Steam")
    @app_commands.autocomplete(game=steam_autocomplete)
    async def steamsearch(self, ctx: commands.Context, game: str):
        """Slash + text command to search for a game on Steam."""
        await ctx.send(f"You selected App ID: {game}")