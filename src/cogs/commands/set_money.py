"""
Give Money Command
~~~~~~~~~~~~~~~~~
Gives moni

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import is_owner
import support
from discord.ext.commands import cooldown, BucketType


class set_money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @is_owner()
    @commands.command(description="Sets Money", aliases=["set"])
    async def set_money(self, ctx, user: discord.User, value: int):
        await support.globalData.setBalance(user, value)
        await ctx.send(embed=discord.Embed(description=f"Updated {user.mention} balance to `{await support.globalData.getBalance(user)}`$", colour=support.colours.default))

def setup(bot):
    bot.add_cog(set_money(bot))
