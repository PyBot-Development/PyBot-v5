"""
Embed Command
~~~~~~~~~~~~~~~~~
Sends Embeded message

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks
from run import client
from discord.commands import Option

class embed_slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @client.slash_command(description="commands.embed.description", name="embed")
    async def embed_slash(self, ctx,
                   title: Option(str, "Embed Title", required=False) = "",
                   description: Option(str, "Embed Description", required=False) = "",
                   colour: Option(str, "Embed Colour (Hex)", required=False) = "#000000"
                   ):
        colour = int(colour.replace("#", ""), 16)
        await ctx.send(embed=discord.Embed(title=title, description=description, color=colour))
        await ctx.response.send_message("Embed Was Created", ephemeral=True)

def setup(bot):
    bot.add_cog(embed_slash(bot))
