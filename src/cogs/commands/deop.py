"""
Ban command
~~~~~~~~~~~~~~~~~
Bans fucking retard

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks


class deop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.deop.description")
    async def deop(self, ctx, user: discord.User):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            await support.globalData.deopUser(user)
            await ctx.reply(embed=discord.Embed(description=lang["commands"]["deop"]["returnSuccess"].format(user=user.mention), colour=support.colours.default))

def setup(bot):
    bot.add_cog(deop(bot))
