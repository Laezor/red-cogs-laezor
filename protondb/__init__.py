from protondb.protodbsearch import ProtonDBSearch


async def setup(bot):
    await bot.add_cog(ProtonDBSearch(bot))