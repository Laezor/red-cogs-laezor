from .latestrom import LatestRom

async def setup(bot):
    await bot.add_cog(LatestRom(bot))