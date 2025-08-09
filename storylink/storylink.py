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
            "while hiding from invisible squirrels",
            "inside a giant teacup",
            "during an alien karaoke night",
            "in a cave filled with glowing mushrooms",
            "while being chased by a sentient sandwich",
            "inside a library that eats books",
            "at the bottom of a rainbow",
            "while time-traveling with a toaster",
            "in a galaxy shaped like a donut",
            "during a talking cat conference",
            "inside a pocket dimension in someone’s sock",
            "while avoiding a stampede of jellyfish",
            "on a rollercoaster through space",
            "during a meteor shower made of marshmallows",
            "inside a chocolate pyramid",
            "while solving crimes with a penguin detective",
            "in a cloud city powered by kites",
            "while riding a flying sofa",
            "inside a sentient vending machine",
            "during a dance battle with skeletons",
            "while trapped in a maze of mirrors"
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
            "turned a volcano into a chocolate fountain",
            "played chess with an octopus",
            "discovered a new color and named it after themselves",
            "accidentally shrank the moon",
            "turned the sun into a disco ball",
            "built a submarine out of bread",
            "gave a motivational speech to snails",
            "taught a cactus to sing opera",
            "trapped lightning in a teacup",
            "programmed clouds to rain glitter",
            "played hide-and-seek with aliens",
            "built a city out of jelly",
            "invented self-writing books",
            "trained a swarm of bees to paint portraits",
            "turned mountains into giant slides",
            "played rock-paper-scissors with fate",
            "built a time machine out of spoons",
            "taught robots how to bake cookies",
            "made a trampoline park for kangaroos",
            "created a black hole in a jar",
            "hosted the first zero-gravity comedy show"
        ]

        random.shuffle(settings)
        random.shuffle(actions)

        story = (
            f"🌟 **Alternate Universe Report** 🌟\n\n"
            f"In another timeline, {person1} and {person2} met {random.choice(settings)} "
            f"and together they {random.choice(actions)}. The world was never the same again."
        )

        await ctx.send(story)


