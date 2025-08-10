import discord
from redbot.core import commands
import requests

class Weather(commands.Cog):
    """Fetch weather from wttr.in"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, location: str = None):
        """
        Get weather from wttr.in.
        Example: [p]weather Athens
        """
        url = f"https://wttr.in/{location or ''}?format=4&m"
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_text = response.text.strip()
        except requests.RequestException as e:
            await ctx.send(f"⚠️ Error fetching weather: {e}")
            return

        await ctx.send(f"```{weather_text}```")