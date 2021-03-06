"""
IQ Command
~~~~~~~~~~~~~~~~~
Calculates IQ

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from numpy import random
from cogs import checks

class iq(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_number(self):
        if random.random() <= 0.65:
            return random.uniform(80.00, 120.00)
        else:
            return random.uniform(0.00, 420.00)

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description=support.getDescription("en.json", "iq"))
    async def iq(self, ctx, *, user: discord.User = None):
        lang = support.getLanguageFileG(ctx.guild)
        iq_size = self.get_number()
        if user is None:
            user = ctx.message.author
        if user.id in [846298981797724161, 818236132578820126]:
            iq_size = 420.00
        colour_hex = '%02x%02x%02x' % (
            int((iq_size/4.2)*2.55), int((iq_size/4.2)*2.51), int((iq_size/4.2)*1.91))
        colour = int(colour_hex, 16)
        embed = discord.Embed(
            description=lang["commands"]["iq"]["returnSuccess"].format(
                user=user.mention,
                iq=f"{iq_size:.2f}"
            ), color=colour)
        await ctx.reply(mention_author=False, embed=embed)


def setup(bot):
    bot.add_cog(iq(bot))
