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


class data(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Shows user data")
    async def data(self, ctx, user: discord.User):
        async with ctx.typing():
            data = await support.globalData.getUser(user)
            await ctx.reply(embed=discord.Embed(description=f"""
ID: `{data[0]}`
Name: `{data[1]}`
Balance: `{data[2]}`
Admin: `{data[4]}`
Banned: `{data[3]}`
Ban Reason: `{data[5]}`
Ban Date: `{data[6]}`
Ban Duration: `{data[7]}`
""", colour=support.colours.default))

def setup(bot):
    bot.add_cog(data(bot))
