import nextcord
from redbot.core import commands
import aiohttp

class Scoop(commands.Cog):
    """Get a random retro game from CrocDB."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crocdb(self, ctx):
        """Get a random game scoop from CrocDB.net."""
        api_url = "https://api.crocdb.net/entry/random"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    if response.status != 200:
                        await ctx.send("❌ Could not fetch data from CrocDB.")
                        return

                    data = await response.json()
                    entry = data.get("entry", {})
                    title = entry.get("title", "Unknown Title")
                    platform = entry.get("platform", "Unknown Platform")
                    regions = entry.get("regions", [])
                    slug = entry.get("slug", "")
                    links = entry.get("links", [])

                    region = regions[0] if regions else "N/A"
                    link = links[0] if links else {}
                    format_ = link.get("format", "Unknown Format")
                    size = link.get("size_str", "Unknown Size")
                    host = link.get("host", "Unknown Host")
                    download_url = link.get("url", "No link")

                    info_url = f"https://crocdb.net/entry/{slug}"

                    embed = nextcord.Embed(
                        title=title,
                        url=info_url,
                        description=f"🕹️ **{title}** on **{platform.upper()}**",
                        color=nextcord.Color.red()
                    )
                    embed.add_field(name="Region", value=region.upper(), inline=True)
                    embed.add_field(name="Format", value=format_, inline=True)
                    embed.add_field(name="Size", value=size, inline=True)
                    embed.add_field(name="Download", value=f"[{host}]({download_url})", inline=False)
                    embed.set_footer(text="Random game from CrocDB.net")

                    await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"⚠️ Error: {str(e)}")
