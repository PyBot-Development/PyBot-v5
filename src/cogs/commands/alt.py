"""
Alt Command
~~~~~~~~~~~~~~~~~
Gives random minecraft alt

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class alt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, 1800, BucketType.user)
    @commands.command(description="commands.alt.description")
    async def alt(self, ctx):
        async with ctx.typing():
            alt = await support.getAlt()
            channel = await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(description=f"||{alt}||", color=support.colours.default))


def setup(bot):
    bot.add_cog(alt(bot))
