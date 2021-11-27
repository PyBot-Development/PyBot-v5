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
from datetime import datetime

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.admin()
    @commands.command(description="commands.ban.description")
    async def ban(self, ctx, user: discord.User, *, reason):
        lang = support.getLanguageFileG(ctx.guild)
        async with ctx.typing():
            await support.globalData.banUser(user, reason, datetime.utcnow(), ctx.message.author)
            await ctx.reply(embed=discord.Embed(description=lang["commands"]["ban"]["returnSuccess"].format(user=user.mention, reason=reason), colour=support.colours.default))

def setup(bot):
    bot.add_cog(ban(bot))
