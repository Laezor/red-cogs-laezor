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

    @commands.hybrid_command(name="protondbsearch", description="Search for a game on ProtonDB")
    @app_commands.describe(game="Start typing to search protondb")
    @app_commands.autocomplete(game=steam_autocomplete)
    async def protondbsearch(self, ctx: commands.Context, game: str):
        """Slash + text command to search for a game on ProtonDB."""

        # Fetch game title from Steam API
        steam_title = None
        steam_url = f"https://store.steampowered.com/api/appdetails?appids={game}&l=english"
        async with aiohttp.ClientSession() as session:
            async with session.get(steam_url, timeout=5) as resp:
                if resp.status == 200:
                    steam_data = await resp.json()
                    app_data = steam_data.get(game, {}).get("data", {})
                    steam_title = app_data.get("name")

        url =  f"https://jazzy-starlight-aeea19.netlify.app/api/v1/reports/summaries/{game}.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status != 200:
                    return await ctx.send("Failed to fetch data from ProtonDB.")
                data = await resp.json()
        
        tier = data.get("tier", "N/A")
        trending_tier = data.get("trendingTier", "N/A")
        confidence = str(data.get("confidence", "N/A")).capitalize()
        score = str(data.get("score", "N/A"))
        total = str(data.get("total", "N/A"))
        best_reported_tier = data.get('bestReportedTier', 'N/A')
        
        tier_descriptions = {
            "platinum": "Game works out of the box",
            "gold": "Runs perfectly after tweaks",
            "silver": "Runs with minor issues, generally playable",
            "bronze": "Runs but often crashes or some other issue",
            "borked": "Doesn't run"
        }
        description = tier_descriptions.get(tier.lower(), "No description available.")
        
        message = (
            f"**ProtonDB Report**\n"
            f"Game: {steam_title or 'Unknown Title'} (AppID: {game})\n"
            f"Best Reported Tier: {best_reported_tier.title()}\n"
            f"Tier: {tier.title()}\n"
            f"Trending Tier: {trending_tier.title()}\n"
            f"Confidence: {confidence}\n"
            f"Score: {score}\n"
            f"Total Reports: {total}\n"
            f"Tier Description: {description}"
        )
        await ctx.send(message)
        