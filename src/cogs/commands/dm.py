"""
Dm Command
~~~~~~~~~~~~~~~~~
DM's user

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType


class dm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="DMs user")
    async def dm(self, ctx, user, *, message):
        user = await commands.UserConverter().convert(ctx, user)
        channel = await user.create_dm()
        await channel.send(message)
        await ctx.send(embed=discord.Embed(description=f"DMed {user.mention()}: `{message}`.", color=support.colours.default), delete_after=10)


def setup(bot):
    bot.add_cog(dm(bot))
