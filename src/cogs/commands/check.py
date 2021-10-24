from re import L
"""
Check Command
~~~~~~~~~~~~~~~~~
Checks minecraft account

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""


from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType

class check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Checks minecraft alt")
    async def check(self, ctx, *, combo):
        await ctx.send(embed=discord.Embed(description=support.check(combo).result, color=support.colours.default))

def setup(bot):
    bot.add_cog(check(bot))