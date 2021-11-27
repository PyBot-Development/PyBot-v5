"""
Embed Command
~~~~~~~~~~~~~~~~~
Sends Embeded message

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.embed.description")
    async def embed(self, ctx, description=None, color=None, title=None,):
        colour = int(color.replace("#", ""), 16)
        await ctx.send(embed=discord.Embed(title=title, description=description, color=colour))


def setup(bot):
    bot.add_cog(embed(bot))
