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

things = [
    "Your mom gave you `{ammount}`$",
    "You work very hard and you get `{ammount}`$",
    "You sold your virginity and got `{ammount}`$",
    "You fucked your mom `{ammount}`$",
    "You got your unemployment benefit +`{ammount}`$",
    "Stonks `{ammount}`$",
    "Your mom's girlfriend gave you `{ammount}`$",
    "Virginity reward `{ammount}`$",
    "You sold you cock and balls for `{ammount}`$",
    "Hot milfs in your area gave you `{ammount}`$",
    "You're 10M user visiting this site! Congratulations on your `{ammount}`$!",
    "You Never gave up, Never let down, Never ran around and desert you, Never made you cry, Never said goodbye, Never told a lie and hurt you! `{ammount}`$",
    "PAPIEŻ 2137 JEBAĆ BYDGOSZCZ!! UWUWUWU `{ammount}`$ <:papaj:902218558849839114><:papaj:902218558849839114><:papaj:902218558849839114><:papaj:902218558849839114>",
    "Umm.. You got `{ammount}`$ for.. ✈️🗼🗼 HOW IS THAT LEGAL?! WTF",
    "You came and found `{ammount}`$"
]

class work(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, 3600, BucketType.user)
    @commands.command(description="Gives you moni uwu")
    async def work(self, ctx):
        money = random.randint(2000, 20000)
    
        await support.globalData.addBalance(ctx.message.author, money)
        await ctx.send(embed=discord.Embed(
            description=random.choice(things).format(ammount=money),
            colour=support.colours.default))

def setup(bot):
    bot.add_cog(work(bot))
