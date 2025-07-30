from .wallhaven import WallhavenCog

async def setup(bot):
    await bot.add_cog(WallhavenCog(bot))