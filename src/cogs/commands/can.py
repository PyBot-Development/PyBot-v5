"""
Can Generator
~~~~~~~~~~~~~~~~~
Can generator 😳

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import os


class can(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Generates Can")
    async def can(self, ctx, text, bottom_text=""):
        async with ctx.typing():
            img = await support.processing.GENERATE_CAN(ctx.message.author.id, text, bottom_text)
            if not img:
                raise commands.BadArgument(
                    "Text and Bottom Text max lenght is 20.")
            file = nextcord.File(img)
            await ctx.send(embed=nextcord.Embed(description="Can.", color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(can(bot))
