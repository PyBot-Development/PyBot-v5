"""
Alt Command
~~~~~~~~~~~~~~~~~
Gives random minecraft alt

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
from cogs import checks
from discord.ext.commands.core import is_owner
import run
import support
import discord

class botSettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @is_owner()
    @commands.group(description="commands.alt.description", name="bot")
    async def botSettings(self, ctx, **options):
        if ctx.invoked_subcommand is None:
            await ctx.reply(mention_author=False, embed=discord.Embed(description="😠 Pass valid subcommand you fucking donut", color=support.colours.red), delete_after=10)
            return

    @is_owner()
    @botSettings.group(name="reload")
    async def reloadCog(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(mention_author=False, embed=discord.Embed(description="😠 Pass valid subcommand you fucking donut", color=support.colours.red), delete_after=10)
            return
    @reloadCog.group(name="all")
    async def reloadAll(self, ctx):
        for i in run.client.cogs:
            run.client.reload_extension(i)
        await ctx.reply(mention_author=False, content=f"Reloaded all extensions")
    @reloadCog.group(name="command")
    async def reloadCommand(self, ctx, cogName):
        self.client.remove_cog(f'{cogName}')
        run.loadCog(f'commands.{cogName}', False)
        await ctx.reply(mention_author=False, content=f"Reloaded {cogName}")

def setup(bot):
    #bot.add_cog(botSettings(bot))
    pass