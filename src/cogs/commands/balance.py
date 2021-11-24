"""
Balance command
~~~~~~~~~~~~~~~~~
Shows balance

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import is_owner
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class balance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @commands.command(description="Shows user money", aliases=["bal"])
    async def balance(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.message.author
        current = await support.globalData.getBalance(user)
        await ctx.send(embed=discord.Embed(description=f"{user.mention} balance is `{current}`$", colour=support.colours.default))


def setup(bot):
    bot.add_cog(balance(bot))
