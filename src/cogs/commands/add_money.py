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

class add_money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @is_owner()
    @commands.command(description=support.getDescription("en.json", "give"), aliases=["add"])
    async def add_money(self, ctx, user, value: int):
        try:
            user = await commands.UserConverter().convert(ctx, user)
            await support.globalData.addBalance(user, value)
            await ctx.reply(mention_author=False, embed=discord.Embed(description=f"Added `{value}`$ to {user.mention} balance. Now their balance is `{await support.globalData.getBalance(user)}`$", colour=support.colours.default))
        except:
            if user.lower()=="everyone":
                await support.globalData.addEveryoneBalance(value)
                await ctx.reply(mention_author=False, embed=discord.Embed(description=f"Added `{value}`$ to Everyone's balance.", colour=support.colours.default))
            else:
                raise commands.UserNotFound(user)

def setup(bot):
    bot.add_cog(add_money(bot))
