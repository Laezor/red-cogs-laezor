import discord
from redbot.core import commands
import requests

class RandomMovie(commands.Cog):
    """Get a random movie from Reelgood."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randommovie(self, ctx):
        """Fetch a random movie."""
        url = (
            "https://api.reelgood.com/v3.0/content/random"
            "?availability=onAnySource&content_kind=movie&nocache=true&region=us&spin_count=1"
        )
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

        try:
            req = requests.get(url, headers=headers, timeout=10)
            if req.status_code != 200:
                await ctx.send(f"❌ Error: Failed to fetch data. Status code {req.status_code}")
                return

            movie = req.json()
            title = movie.get("title", "Unknown Title")
            overview = movie.get("overview", "No description available.")
            runtime = movie.get("runtime", "Unknown")
            movie_id = movie.get("id")
            release_date = movie.get("release_on", "Unknown")

            embed = discord.Embed(
                title=title,
                description=overview,
                color=discord.Color.blue()
            )
            embed.add_field(name="Runtime", value=f"{runtime} minutes", inline=False)
            embed.add_field(name="Released", value=f"{release_date}", inline=False)
            if movie_id:
                embed.set_image(url=f"https://img.rgstatic.com/content/movie/{movie_id}/poster-342.webp")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Failed to fetch or parse movie data. Error: {e}")



