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
from cogs import checks

class set_money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @is_owner()
    #@checks.admin()
    @commands.command(description="commands.set_money.description", aliases=["set"])
    async def set_money(self, ctx, user, value: int): 
        try:
            user = await commands.UserConverter().convert(ctx, user)
            await support.globalData.setBalance(user, value)
            await ctx.send(embed=discord.Embed(description=f"Updated {user.mention} balance to `{await support.globalData.getBalance(user)}`$", colour=support.colours.default))
        except:
            if user.lower()=="everyone":
                await support.globalData.setEveryoneBalance(value)
                await ctx.send(embed=discord.Embed(description=f"Updated Everyone's balance to `{value}`$", colour=support.colours.default))
            else:
                raise commands.UserNotFound(user)

def setup(bot):
    bot.add_cog(set_money(bot))
