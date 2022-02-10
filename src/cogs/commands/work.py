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
    @commands.command(description=support.getDescription("en.json", "work"))
    async def work(self, ctx):
        support.getLanguageFileG(ctx.guild)
        money = random.randint(2000, 20000)
        texts = support.getLanguageFile(support.getLanguage(ctx.guild))
        texts = texts["commands"]["work"]["messages"]
        bonus = (money * (await support.globalData.getSocialCredit(ctx.message.author)/1000)) - money
        await support.globalData.addBalance(ctx.message.author, money+(bonus if await support.globalData.getSocialCredit(ctx.message.author) >= 1000 else 0))

        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=random.choice(texts)
            .format(ammount=money, bitcoin=support.convertToBitcoin(money, "USD")),
            colour=support.colours.default)
            .set_footer(text=(f"{bonus}$. Social Credit Bonus | {money+bonus}$ in total." if await support.globalData.getSocialCredit(ctx.message.author) >= 1000 else '')))

def setup(bot):
    bot.add_cog(work(bot))
