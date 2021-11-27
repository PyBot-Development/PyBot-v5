"""
Nick Command
~~~~~~~~~~~~~~~~~
Changes Nickname

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class command(commands.Cog, name="nick"):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command(description="commands.nick.description")
    async def nick(self, ctx, *, nick=None):
        lang = support.getLanguageFileG(ctx.guild)
        await ctx.message.guild.me.edit(nick=nick)
        await ctx.send(embed=discord.Embed(description=lang["commands"]["lang"]["returnSuccess"].format(nick=nick), color=support.colours.default), delete_after=10)


def setup(bot):
    bot.add_cog(command(bot))
