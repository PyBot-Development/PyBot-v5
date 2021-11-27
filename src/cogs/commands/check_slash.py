"""
Check Slash Command
~~~~~~~~~~~~~~~~~
Checks minecraft account

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
from discord.commands import Option
import support
from run import client
from cogs import checks

class check_slash(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @checks.default()
    @client.slash_command(description="commands.check.description")
    async def check(self, ctx, combo: Option(str, "Login and Password to account")):
        await ctx.response.send_message(embed=discord.Embed(description=support.check(combo).result, color=support.colours.default), ephemeral=True)


def setup(bot):
    bot.add_cog(check_slash(bot))
