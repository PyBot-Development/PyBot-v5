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

    @commands.command(description="commands.data.description")
    async def data(self, ctx, user: discord.User):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            data = await support.globalData.getUser(user)
            await ctx.reply(embed=discord.Embed(description=lang["commands"]["data"]["returnSuccess"].format(
                id=data[0],
                name=data[1],
                balance=data[2],
                admin=data[4],
                banned=data[3],
                reason=data[5],
                date=data[6],
                duration=data[7]
            ), colour=support.colours.default))

def setup(bot):
    bot.add_cog(data(bot))
