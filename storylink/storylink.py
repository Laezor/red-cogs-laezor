import discord
from redbot.core import commands
import random

class StoryLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="storylink")
    async def storylink(self, ctx):
        # Get a list of online members (excluding bots)
        online_members = [
            m for m in ctx.guild.members
            if m.status == discord.Status.online and not m.bot
        ]
        
        if len(online_members) < 2:
            return await ctx.send("Not enough online members to create a story!")

        # Pick two random users
        person1, person2 = random.sample(online_members, 2)

        # Expanded random story elements
        settings = [
            "in a haunted arcade",
            "on a distant moon",
            "during a potato festival",
            "inside a giant library",
            "while escaping a dragon",
            "at the bottom of the ocean",
            "inside a volcano’s gift shop",
            "on top of a moving train",
            "in a parallel universe made of cheese",
            "while trapped in a time loop",
            "inside a gigantic video game console",
            "at the edge of the world",
            "while competing in an intergalactic cooking show",
            "in a city made of candy",
            "at a karaoke battle between robots",
            "inside a floating castle",
            "during a thunderstorm made of glitter",
            "while surfing a lava wave",
            "in the middle of a zombie disco",
            "while hiding from invisible squirrels"
        ]

        actions = [
            "stole a spaceship",
            "baked a cursed pie",
            "invented invisible socks",
            "accidentally opened a wormhole",
            "started a pillow fight revolution",
            "taught penguins how to dance",
            "built a robot that only speaks in riddles",
            "convinced a dragon to become a vegan",
            "escaped a labyrinth made of spaghetti",
            "created a perfume that makes you float",
            "hosted a tea party for ghosts",
            "launched a chicken into orbit",
            "solved a 10,000-piece puzzle in the dark",
            "built a rollercoaster for ants",
            "trained a squirrel army",
            "found a map to the Sandwich Dimension",
            "disguised themselves as flamingos",
            "invented a new language made of whistles",
            "tamed a tornado",
            "turned a volcano into a chocolate fountain"
        ]

        random.shuffle(settings)
        random.shuffle(actions)

        story = (
            f"🌟 **Alternate Universe Report** 🌟\n\n"
            f"In another timeline, {person1.mention} and {person2.mention} met {random.choice(settings)} "
            f"and together they {random.choice(actions)}. The world was never the same again."
        )

        await ctx.send(story)


