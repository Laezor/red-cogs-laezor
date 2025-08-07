from .crocdb import Scoop

async def setup(bot):
    await bot.add_cog(Scoop(bot))
