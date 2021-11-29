"""
Give Money Command
~~~~~~~~~~~~~~~~~
Gives moni

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType


class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.command(description="commands.prefix.description")
    async def prefix(self, ctx, prefix):
        lang=support.getLanguageFileG(ctx.guild)
        prefix=prefix[0:6]
        prefix=support.globalData.setPrefix(ctx.guild, prefix)
        await ctx.send(embed=discord.Embed(description=lang["commands"]["prefix"]["returnSuccess"].format(prefix=prefix), color=support.colours.default))
def setup(bot):
    bot.add_cog(prefix(bot))
