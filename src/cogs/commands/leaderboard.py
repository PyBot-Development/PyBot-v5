"""
Balance command
~~~~~~~~~~~~~~~~~
Shows balance

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import is_owner
import support
from discord.ext.commands import cooldown, BucketType


class leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Shows user money leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        users = await support.globalData.getAllUsers()
        users = sorted(users, key=lambda user: user[2], reverse=True)
        lboard = ''.join(f"\n{users.index(user)+1}. <@{user[0]}>: {user[2]}$" for user in users)
        await ctx.send(embed=discord.Embed(description=f"{lboard}", colour=support.colours.default))


def setup(bot):
    bot.add_cog(leaderboard(bot))
