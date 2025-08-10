from .latesthack import LatestHack

async def setup(bot):
    await bot.add_cog(LatestHack(bot))