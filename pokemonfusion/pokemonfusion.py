import discord
from redbot.core import commands
import requests
import random

class PokemonFusion(commands.Cog):
    """Pokemon Fusion"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemonfusion(self, ctx):
        """Pokemon Fusion"""
        pkmn1 = random.randint(1, 420)
        pkmn2 = random.randint(1, 420)
        url1 = f"https://fusioncalc.com/wp-content/themes/twentytwentyone/pokemon/autogen-fusion-sprites-master/Battlers/{pkmn1}/{pkmn1}.{pkmn2}.png"
        url2 = f"https://fusioncalc.com/wp-content/themes/twentytwentyone/pokemon/autogen-fusion-sprites-master/Battlers/{pkmn2}/{pkmn2}.{pkmn1}.png"
        await ctx.send(url1)
        await ctx.send(url2)
