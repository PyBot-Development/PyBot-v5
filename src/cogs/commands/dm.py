"""
Dm Command
~~~~~~~~~~~~~~~~~
DM's user

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class dm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.dm.description")
    async def dm(self, ctx, user, *, message):
        lang = support.getLanguageFileG(ctx.guild)
        user = await commands.UserConverter().convert(ctx, user)
        channel = await user.create_dm()
        await channel.send(message)
        await ctx.send(embed=discord.Embed(description=lang["commands"]["dm"]["returnSuccess"].format(message=message, user=user.mention), color=support.colours.default), delete_after=10)


def setup(bot):
    bot.add_cog(dm(bot))
