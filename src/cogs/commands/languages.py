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
import json

class languages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.languages.description")
    async def languages(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        languages = []

        for i in support.languages:
            with open(f"{support.path}/data/languages/{i}") as file:
                language = json.load(file)
                languages.append(f"`{i[:-5]}` - {language['name']}")
        
        await ctx.send(embed=discord.Embed(title=lang["commands"]["languages"]["returnSuccess"], description=''.join(f"{i}\n" for i in languages),color=support.colours.default))
        
def setup(bot):
    bot.add_cog(languages(bot))
