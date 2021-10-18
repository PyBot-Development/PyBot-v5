"""
Doom Slayer Command
~~~~~~~~~~~~~~~~~
Sussy Baka

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import os


class doom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Makes Doom slayer", aliases=["doom_slayer"])
    async def doom(self, ctx, user: nextcord.User=None):
        async with ctx.typing():
            if user is None:
                user = ctx.message.author

            img = await support.processing.overlay_position(user.display_avatar, f"{support.path}/data/resources/templates/doom_slayer.png", (90, 35), (50, 50), ctx.message.author.id, (236, 423))
            file = nextcord.File(img)
            await ctx.send(embed=nextcord.Embed(description=f"{user.display_name} The Doom slayer.", color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(doom(bot))
