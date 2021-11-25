"""
Lyrics Command
~~~~~~~~~~~~~~~~~
Sends song lyrics

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks
import lyricsgenius
import os

genius = lyricsgenius.Genius("yGRPyGYBY3sCM_baVIGA4pBPLAg-_5EDRnOW5MqYMAjjq7rwFew40MnPQEmyy7cA", verbose=False)


class showLyrics(discord.ui.View):
    def __init__(self, song):
        super().__init__(timeout=20)
        self.message = None
        self.song = song
    async def on_timeout(self) -> None:
        self.show.disabled = True
        await self.message.edit(view=self)
        return await super().on_timeout()

    @discord.ui.button(label="Show", style=discord.ButtonStyle.grey)
    async def show(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message(embed=discord.Embed(title=f"{self.song.title} - {self.song.artist} Lyrics", description=f"{self.song.lyrics}", color=support.colours.default), ephemeral=True)


class lyrics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends song lyrics")
    async def lyrics(self, ctx, *, name):
        song = genius.search_song(name)
        buttons = showLyrics(song)
        #with open(f"{support.path}/data/temp/lyrics.txt", "w+") as file:
        #    file.write(song.lyrics)
        #await ctx.response.send_message(embed=discord.Embed(description=song.lyrics, color=support.colours.default), ephemeral=True)
        message = await ctx.send(embed=discord.Embed(
            description=f"Click button to show `{song.title} - {song.artist}` lyrics", color=support.colours.default), view=buttons)
        buttons.message = message
        #await ctx.send(file=discord.File(f"{support.path}/data/temp/lyrics.txt") embed=discord.Embed())
        #os.remove(f"{support.path}/data/temp/lyrics.txt")


def setup(bot):
    bot.add_cog(lyrics(bot))
