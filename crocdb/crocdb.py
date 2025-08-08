import discord
from redbot.core import commands
import aiohttp
import requests

class Crocdb(commands.Cog):
    """Get a random retro game from CrocDB."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crocdb(self, ctx, query: str = None, platform: str = "ps2", region: str = "us"):
        """Get a random or search for a game from CrocDB.net."""
        if query:
            
            url = "https://api.crocdb.net/search"
            headers = {"Content-Type": "application/json"}
            payload = {
                "search_key": query,
                "platforms": [platform],
                "regions": [region],
                "max_results": 5,
                "page": 1
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("data", {}).get("results", [])

                    if not results:
                        await ctx.send("No results found.")
                        return

                    # Build a response message
                    msg_lines = []
                    for entry in results:
                        title = entry.get("title", "Unknown Title")
                        plat = entry.get("platform", "Unknown Platform")
                        rom_id = entry.get("rom_id", "N/A")
                        link = entry.get("links", [{}])[0].get("url", "No URL")
                        msg_lines.append(f"**{title}** (`{plat}`) - [Link]({link}) - ROM ID: `{rom_id}`")

                    message = "\n".join(msg_lines)
                    await ctx.send(message[:2000])  # Discord max msg length
                else:
                    await ctx.send(f"API error: {response.status_code}")
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
        
            api_url = "https://api.crocdb.net/entry/random"

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(api_url) as response:
                        if response.status != 200:
                            await ctx.send("❌ Could not fetch data from CrocDB.")
                            return

                        data = await response.json()

                        entry = data.get("data", {}).get("entry", {})
                        title = entry.get("title", "Unknown Title")
                        platform = entry.get("platform", "Unknown Platform")
                        regions = entry.get("regions", [])
                        slug = entry.get("slug", "")
                        links = entry.get("links", [])
                        boxart = entry.get("boxart_url", "")
                        region = regions[0] if regions else "N/A"
                        link = links[0] if links else {}
                        format_ = link.get("format", "Unknown Format")
                        size = link.get("size_str", "Unknown Size")
                        host = link.get("host", "Unknown Host")
                        download_url = link.get("url", "No link")

                        info_url = f"https://crocdb.net/rom/{slug}"

                        embed = discord.Embed(
                            title=title,
                            url=info_url,
                            description=f"🕹️ **{title}** on **{platform.upper()}**",
                            color=discord.Color.red()
                        )
                        embed.set_thumbnail(url=boxart)
                        embed.add_field(name="Region", value=region.upper(), inline=True)
                        embed.add_field(name="Format", value=format_, inline=True)
                        embed.add_field(name="Size", value=size, inline=True)
                        embed.add_field(name="Download", value=f"[{host}]({download_url})", inline=False)
                        embed.set_footer(text="Random game from CrocDB.net")

                        await ctx.send(embed=embed)

                except Exception as e:
                    await ctx.send(f"⚠️ Error: {str(e)}")
