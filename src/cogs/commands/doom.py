"""
Doom Slayer Command
~~~~~~~~~~~~~~~~~
Sussy Baka

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
import os
from cogs import checks

class doom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.doom.description", aliases=["doom_slayer"])
    async def doom(self, ctx, user: discord.User=None):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            if user is None:
                user = ctx.message.author

            img = await support.processing.overlay_position(user.display_avatar, f"{support.path}/data/resources/templates/doom_slayer.png", (90, 35), (50, 50), ctx.message.author.id, (236, 423))
            file = discord.File(img)
            await ctx.reply(mention_author=False, embed=discord.Embed(description=lang["commands"]["doom"]["returnSuccess"].format(user=user.display_name), color=support.colours.default).set_image(url=f"attachment://{ctx.message.author.id}.png"), file=file)
            os.remove(img)


def setup(bot):
    bot.add_cog(doom(bot))
