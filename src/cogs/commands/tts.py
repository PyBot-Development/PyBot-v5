"""
TTS Command
~~~~~~~~~~~~~~~~~
Text To Speech

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
import os
from cogs import checks

class tts(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.tts.description")
    async def tts(self, ctx, *, text):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            max = 1000
            if len(str(text)) > max:
                await ctx.send(embed=discord.Embed(description=lang["commands"]["tts"]["maxLenght"].format(max=max), color=support.colours.default))
                return
            text = text.split("-l")
            text.append("en")
            file = await support.processing.tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))
            await ctx.send(file=discord.File(file), content=lang["commands"]["tts"]["returnSuccess"])
            os.remove(file)


def setup(bot):
    bot.add_cog(tts(bot))
