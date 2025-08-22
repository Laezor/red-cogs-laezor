from .randmovie import RandomMovie

async def setup(bot):
    await bot.add_cog(RandomMovie(bot))