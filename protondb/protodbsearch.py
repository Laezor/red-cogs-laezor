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

        url =  f"https://jazzy-starlight-aeea19.netlify.app/api/v1/reports/summaries/{game}.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status != 200:
                    return await ctx.send("Failed to fetch data from ProtonDB.")
                data = await resp.json()
        embed = discord.Embed(
            title="ProtonDB Report",
            description=f"**Best Reported Tier:** {data.get('bestReportedTier', 'N/A').title()}",
            color=discord.Color.green() if data.get("tier", "").lower() == "platinum" else discord.Color.blurple()
        )
        embed.add_field(name="Tier", value=data.get("tier", "N/A").title(), inline=True)
        embed.add_field(name="Trending Tier", value=data.get("trendingTier", "N/A").title(), inline=True)
        embed.add_field(name="Confidence", value=str(data.get("confidence", "N/A")).capitalize(), inline=True)
        embed.add_field(name="Score", value=str(data.get("score", "N/A")), inline=True)
        embed.add_field(name="Total Reports", value=str(data.get("total", "N/A")), inline=True)
        
        # Add tier description
        tier = data.get("tier", "").lower()
        tier_descriptions = {
            "platinum": "Game works out of the box",
            "gold": "Runs perfectly after tweaks",
            "silver": "Runs with minor issues, generally playable",
            "bronze": "Runs but often crashes or some other issue",
            "borked": "Doesn't run"
        }
        description = tier_descriptions.get(tier, "No description available.")
        embed.add_field(name="Tier Description", value=description, inline=False)
        await ctx.send(embed=embed)
        