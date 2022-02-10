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
from cogs import checks
from discord.commands import Option

class check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description=support.getDescription("en.json", "check"))
    async def check(self, ctx, *, combo):
        await ctx.reply(mention_author=False, embed=discord.Embed(description=support.check(combo).result, color=support.colours.default))

class check_slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @commands.slash_command(description=support.getDescription("en.json", "check"))
    async def check(self, ctx, combo: Option(str, "Login and Password to account")):
        await ctx.response.send_message(embed=discord.Embed(description=support.check(combo).result, color=support.colours.default), ephemeral=True)

def setup(bot):
    bot.add_cog(check(bot))
    bot.add_cog(check_slash(bot))