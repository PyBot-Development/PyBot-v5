"""
PP Command
~~~~~~~~~~~~~~~~~
Calculates PP size

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
import random
from datetime import datetime
from cogs import checks

class pp(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["dick", "penis", "cock"], description=support.getDescription("en.json", "pp"))
    async def pp(self, ctx, *, user: discord.User = None):
        lang = support.getLanguageFileG(ctx.guild)
        
        if user is None:
            user = ctx.message.author
        ids = [609551301730369547, 818236132578820126, 484170415720235009,
               824324885379416106, 760602301790158868, 846298981797724161,
               424598691542990858, 459554887316013067]
        if user.id in ids:
            ppsize = "∞"
            ppsize_inch = "∞"
            colour_hex = '%02x%02x%02x' % (int(231), int(145), int(255))
        else:
            ppsize = random.uniform(0.00, 200.00)
            ppsize_inch = ppsize/2.54
            colour_hex = '%02x%02x%02x' % (
                int((ppsize/2)*2.31), int((ppsize/2)*1.45), int((ppsize/2)*2.55))

        colour = int(colour_hex, 16)
        try:
            embed = discord.Embed(
                description=lang["commands"]["pp"]["returnSuccess"].format(user=user, ppsize=f"{ppsize:.2f}", inchsize=f"{ppsize_inch:.2f}"), color=colour)
        except:
            embed = discord.Embed(
                description=lang["commands"]["pp"]["returnSuccess"].format(user=user, ppsize=f"{ppsize}", inchsize=f"{ppsize_inch}"), color=colour)
        await ctx.reply(mention_author=False, embed=embed)


def setup(bot):
    bot.add_cog(pp(bot))
