"""
Cum UwU
~~~~~~~~~~~~~~~~~
CUUM 😳

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import os


class cum(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sussy Baka")
    async def cum(self, ctx, user: nextcord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author
            img = await support.processing.overlay(user.display_avatar, f"{support.path}/data/resources/templates/cum_template.png", ctx.message.author.id)
            file = nextcord.File(img)
            await ctx.send(embed=nextcord.Embed(description="Cummies Uwu.", color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(cum(bot))