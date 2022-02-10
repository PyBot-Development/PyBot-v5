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
import support
from cogs import checks
from discord.commands import Option

class say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["tell", "sudo"], description=support.getDescription("en.json", "say"))
    async def say(self, ctx, *, arg):
        await ctx.send(f"\u200b{arg}".replace("@", "@\u200b"))

class say_slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @commands.slash_command(description=support.getDescription("en.json", "say"))
    async def say(
        self,
        ctx,
        arg: Option(str, "What do you want me to say?"),
    ):
        await ctx.send(f"\u200b{arg}".replace("@", "@\u200b"))
        await ctx.response.send_message("Message was sent.", ephemeral=True)

def setup(bot):
    bot.add_cog(say(bot))
    bot.add_cog(say_slash(bot))
