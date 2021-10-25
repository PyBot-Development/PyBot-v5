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


class give_money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @is_owner()
    @commands.command(description="Gives Money")
    async def give_money(self, ctx, user: discord.User, value: int):
        current = await support.globalData.getBalance(user)
        current += value
        await support.globalData.setBalance(user, value)
        await ctx.send(await support.globalData.getBalance(user))

def setup(bot):
    bot.add_cog(give_money(bot))
