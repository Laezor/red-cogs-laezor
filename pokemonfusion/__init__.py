from .pokemonfusion import PokemonFusion

async def setup(bot):
    await bot.add_cog(PokemonFusion(bot))