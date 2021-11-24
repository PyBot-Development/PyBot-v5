"""
Pirate Command
~~~~~~~~~~~~~~~~~
Sussy Baka

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
import os
from cogs import checks

class pirate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Makes a Pirate")
    async def pirate(self, ctx, user: discord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author

            img = await support.processing.overlay_position(user.display_avatar, f"{support.path}/data/resources/templates/pirate.png", (110, 80), (105, 105), ctx.message.author.id, (320, 374))
            file = discord.File(img)
            await ctx.send(embed=discord.Embed(description=f"{user.display_name} The Pirate 🏴‍☠️.", color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(pirate(bot))
