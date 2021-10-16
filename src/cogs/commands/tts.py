"""
TTS Command
~~~~~~~~~~~~~~~~~
Text To Speech

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType
import os


class tts(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Text to speech")
    async def tts(self, ctx, *, text):
        async with ctx.typing():
            max = 1000
            if len(str(text)) > max:
                await ctx.send(embed=nextcord.Embed(description=f"Max Characters is {max}", color=support.colours.default))
                return
            text = text.split("-l")
            text.append("en")
            file = await support.processing.tts(f"{text[0]}", f"{text[1]}".replace(" ", ""))
            await ctx.send(file=nextcord.File(file), content="Text To Speech")
            os.remove(file)


def setup(bot):
    bot.add_cog(tts(bot))
