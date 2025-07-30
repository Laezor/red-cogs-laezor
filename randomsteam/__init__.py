from .randomsteam import RandomSteamCog

async def setup(bot):
    await bot.add_cog(RandomSteamCog(bot))