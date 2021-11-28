"""
Give Money Command
~~~~~~~~~~~~~~~~~
Gives moni

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType


class setLanguage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.command(description="commands.setLanguage.description", aliases=["language", "set_language", "lang"])
    async def setLanguage(self, ctx, language):

        if language+'.json' in support.languages:
            await support.globalData.setLanguage(ctx.guild, f"{language}.json")
            lang=support.getLanguageFileG(ctx.guild)
            await ctx.send(embed=discord.Embed(description=lang["commands"]["setLanguage"]["returnSuccess"].format(lang=lang["name"]), color=support.colours.default))
        else:
            lang=support.getLanguageFileG(ctx.guild)
            await ctx.send(embed=discord.Embed(description=lang["commands"]["setLanguage"]["notFound"].format(lang=language), color=support.colours.default))
def setup(bot):
    bot.add_cog(setLanguage(bot))
