from .crocdb import Crocdb

async def setup(bot):
    await bot.add_cog(Crocdb(bot))
