"""
Logs Command
~~~~~~~~~~~~~~~~~
Sends logs

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["log"], description="Sends bot logs")
    async def logs(self, ctx):
        await ctx.send(file=discord.File(f"{support.path}/logs/{support.startup_date}.log"))


def setup(bot):
    bot.add_cog(logs(bot))
