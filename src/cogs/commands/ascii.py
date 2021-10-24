"""
Ascii Command
~~~~~~~~~~~~~~~~~
Makes ascii art from text

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
import pyfiglet


class ascii(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends ASCII from Text")
    async def ascii(self, ctx, *, arg):
        arg = arg.split("--font ")
        arg.append("big")
        result = pyfiglet.figlet_format(arg[0], font=arg[1])
        await ctx.send(f"```{result}```")


def setup(bot):
    bot.add_cog(ascii(bot))
