"""
Say Command
~~~~~~~~~~~~~~~~~
Says something using bot

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

class hello(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @checks.default()
    @client.slash_command(description="commands.say.description")
    async def say(
        self,
        ctx,
        arg: Option(str, "What do you want me to say?"),
    ):
        await ctx.send(f"​{arg}".replace("@", "@ "))
        

def setup(bot):
    bot.add_cog(hello(bot))
