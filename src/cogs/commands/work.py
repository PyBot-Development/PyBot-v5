"""
Work command
~~~~~~~~~~~~~~~~~
You get moni

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import is_owner
import support
from discord.ext.commands import cooldown, BucketType
import random
from cogs import checks



class work(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, 3600, BucketType.user)
    @commands.command(description="commands.work.description")
    async def work(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        money = random.randint(2000, 20000)
        texts = support.getLanguageFile(support.getLanguage(ctx.guild))
        texts = texts["commands"]["work"]["messages"]
        await support.globalData.addBalance(ctx.message.author, money)
        await ctx.send(embed=discord.Embed(
            description=random.choice(texts).format(ammount=money, bitcoin=support.convertToBitcoin(money, "USD")),
            colour=support.colours.default))

def setup(bot):
    bot.add_cog(work(bot))
