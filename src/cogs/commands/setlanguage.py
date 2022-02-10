"""
Give Money Command
~~~~~~~~~~~~~~~~~
Gives moni

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import guild_only
import support
from discord.ext.commands import cooldown, BucketType


class setLanguage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.has_permissions(administrator=True)
    @guild_only()
    @commands.command(description=support.getDescription("en.json", "setLanguage"), aliases=["language", "set_language", "lang"])
    async def setLanguage(self, ctx, language):

        if language+'.json' in support.languages:
            await support.globalData.setLanguage(ctx.guild, f"{language}.json")
            lang=support.getLanguageFileG(ctx.guild)
            await ctx.reply(mention_author=False, embed=discord.Embed(description=lang["commands"]["setLanguage"]["returnSuccess"].format(lang=lang["name"]), color=support.colours.default))
        else:
            lang=support.getLanguageFileG(ctx.guild)
            await ctx.reply(mention_author=False, embed=discord.Embed(description=lang["commands"]["setLanguage"]["notFound"].format(lang=language), color=support.colours.default))
def setup(bot):
    bot.add_cog(setLanguage(bot))
