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
from discord.commands import Option
from colour import Color

class embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description=support.getDescription("en.json", "embed"))
    async def embed(self, ctx, description=None, color=None, title=None,):
        r, g, b = Color(color).get_rgb()
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        _colour = discord.Colour.from_rgb(r, g, b)
        await ctx.send(embed=discord.Embed(title=title, description=description, color=_colour))

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.slash_command(description=support.getDescription("en.json", "embed"), name="embed")
    async def embed_slash(self, ctx,
                   title: Option(str, "Embed Title", required=False) = "",
                   description: Option(str, "Embed Description", required=False) = "",
                   colour: Option(str, "Embed Colour (Hex)", required=False) = "#000000"
                   ):
        r, g, b = Color(colour).get_rgb()
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        _colour = discord.Colour.from_rgb(r, g, b)
        print(_colour)
        await ctx.send(embed=discord.Embed(title=title, description=description, color=_colour))
        await ctx.response.send_message("Embed Was Created", ephemeral=True)

def setup(bot):
    bot.add_cog(embed(bot))
