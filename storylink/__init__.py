from .storylink import StoryLink

async def setup(bot):
    await bot.add_cog(StoryLink(bot))