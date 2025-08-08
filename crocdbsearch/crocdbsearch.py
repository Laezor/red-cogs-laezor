import discord
from redbot.core import commands, app_commands
import requests

class CrocdbSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crocdbsearch", description="Search for ROMs using the CrocDB API.")
    @app_commands.describe(
        query="Game title to search for",
        platform="Platform IDs (e.g., snes, ps2)",
        region="Region IDs (e.g., us, eu)"
    )
    async def crocdbsearch(
        self,
        interaction: discord.Interaction,
        query: str,
        platform: str = "ps2",
        region: str = "us"
    ):
        await interaction.response.defer(ephemeral=True)  # Prevents timeouts on slow requests

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
                    await interaction.followup.send("No results found.", ephemeral=True)
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
                await interaction.followup.send(message[:2000], ephemeral=True)  # Discord max msg length
            else:
                await interaction.followup.send(f"API error: {response.status_code}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
