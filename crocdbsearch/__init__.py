from .crocdbsearch import CrocdbSearch

async def setup(bot):
    await bot.add_cog(CrocdbSearch(bot))
