from redbot.core import commands
import requests

class CrocdbSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="crocdbsearch", help="Search for ROMs using the CrocDB API. Usage: [p]crocdbsearch <query> [platform] [region]")
    async def crocdbsearch(
        self,
        ctx: commands.Context,
        query: str,
        platform: str = "ps2",
        region: str = "us"
    ):
        

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
