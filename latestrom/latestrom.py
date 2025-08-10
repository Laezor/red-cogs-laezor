import discord
import feedparser
from redbot.core import commands

class LatestRom(commands.Cog):
    """Fetch latest ROM hacks from ROMhacking.net RSS feed."""

    def __init__(self, bot):
        self.bot = bot
        self.feed_url = "https://www.romhacking.net/romhackingdotnet.rss"

    @commands.command()
    async def latestrom(self, ctx, count: int = 5):
        """Show the latest ROM hacks from ROMhacking.net (default: 5 results)."""
        try:
            feed = feedparser.parse(self.feed_url)

            if not feed.entries:
                await ctx.send("Couldn't fetch any new ROM hacks from the RSS feed.")
                return

            count = max(1, min(count, 10))  # Limit between 1 and 10
            embed = discord.Embed(
                title="Latest ROM Hacks (ROMhacking.net)",
                color=discord.Color.blue()
            )

            for entry in feed.entries[:count]:
                title = entry.get("title", "No title")
                link = entry.get("link", "")
                published = entry.get("published", "Unknown date")
                embed.add_field(
                    name=title,
                    value=f"{published}\n{link}",
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error fetching RSS feed: {e}")