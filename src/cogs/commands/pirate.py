"""
Pirate Command
~~~~~~~~~~~~~~~~~
Sussy Baka

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import os


class pirate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Makes a Pirate")
    async def pirate(self, ctx, user: nextcord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author

            img = await support.processing.overlay_position(user.display_avatar, f"{support.path}/data/resources/templates/pirate.png", (110, 80), (105, 105), ctx.message.author.id, (320, 374))
            file = nextcord.File(img)
            await ctx.send(embed=nextcord.Embed(description=f"{user.display_name} The Pirate 🏴‍☠️.", color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(pirate(bot))
