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

class pay(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.pay.description")
    async def pay(self, ctx, user: discord.User, value: int):
        lang = support.getLanguageFileG(ctx.guild)
        if await support.globalData.getBalance(ctx.message.author) < value:
            await ctx.send(embed=discord.Embed(lang["commands"]["pay"]["notEnoughMoney"], colour=support.colours.red))
            return
        await support.globalData.removebalance(ctx.message.author, value)
        await support.globalData.addBalance(user, value)
        await ctx.send(embed=discord.Embed(description=lang["commands"]["pay"]["returnSuccess"].format(
            user=user.mention,
            vaule=value,
            yourbalance=await support.globalData.getBalance(ctx.message.author),
            theirbalance=await support.globalData.getBalance(user)
        ), colour=support.colours.default))

def setup(bot):
    bot.add_cog(pay(bot))
