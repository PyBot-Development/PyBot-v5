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

class op(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.admin()
    @commands.command(description="Ops user")
    async def op(self, ctx, user: discord.User):
        async with ctx.typing():
            await support.globalData.opUser(user)
            await ctx.reply(embed=discord.Embed(description=f"🔨 Opped {user.mention}.", colour=support.colours.default))

def setup(bot):
    bot.add_cog(op(bot))
