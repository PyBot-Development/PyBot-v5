"""
Kill Command
~~~~~~~~~~~~~~~~~
Sussy Baka Impostor Amogus

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import os


class kill(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Kills Someone", aliases=["murder", "blood"])
    async def kill(self, ctx, user: nextcord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author
            img = await support.processing.overlay(user.display_avatar, f"{support.path}/data/resources/templates/blood_template.png", ctx.message.author.id)
            file = nextcord.File(img)
            await ctx.send(embed=nextcord.Embed(description="🔪", color=support.colours.red).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(kill(bot))
