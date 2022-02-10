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
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["log"], description=support.getDescription("en.json", "logs"))
    async def logs(self, ctx):
        await ctx.reply(mention_author=False, file=discord.File(f"{support.path}/logs/{support.startup_date}.log"))


def setup(bot):
    bot.add_cog(logs(bot))
