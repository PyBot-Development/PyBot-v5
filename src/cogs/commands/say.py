"""
Say Command
~~~~~~~~~~~~~~~~~
Says something using bot

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
from cogs import checks

class say(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["tell", "sudo"], description="commands.say.description")
    async def say(self, ctx, *, arg):
        await ctx.send(f"​{arg}".replace("@", "@ "))


def setup(bot):
    bot.add_cog(say(bot))
