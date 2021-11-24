"""
Kill Command
~~~~~~~~~~~~~~~~~
Sussy Baka Impostor Amogus

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
import os
from cogs import checks

class kill(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Kills Someone", aliases=["murder", "blood"])
    async def kill(self, ctx, user: discord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author
            img = await support.processing.overlay(user.display_avatar, f"{support.path}/data/resources/templates/blood_template.png", ctx.message.author.id)
            file = discord.File(img)
            await ctx.send(embed=discord.Embed(description="🔪", color=support.colours.red).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(kill(bot))
