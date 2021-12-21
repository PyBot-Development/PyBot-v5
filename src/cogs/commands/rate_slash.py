"""
Check Slash Command
~~~~~~~~~~~~~~~~~
Checks minecraft account

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
from discord.commands import Option
import support
from run import client
import random
from cogs import checks

class rate_slash(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @client.slash_command(description="commands.rate.description")
    async def rate(self, ctx,
                   rate_thing: Option(str, "Rate What?"),
                   user: Option(str, "User or Thing to rate",
                                required=False) = "",
                   ):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            picked_random = random.randint(0, 100)
            thestuff = {
                "gay" and "gej":   '%02x%02x%02x' % (int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55))),
                "black" and "czarny": '%02x%02x%02x' % (int(253-(picked_random*2.53)),              int(231-(picked_random*2.31)),              int(214-(picked_random*2.14))),
                "furry": '%02x%02x%02x' % (int(picked_random*1.67),                    int(picked_random*1.99),                    int(picked_random*2.3)),
                "cum":   '%02x%02x%02x' % (int(picked_random*2.55),                    int(picked_random*2.55),                    int(picked_random*2.55)),
            }

            try:
                user = await commands.UserConverter().convert(ctx, user)
            except:
                pass

            if(picked_random > 50 and user.lower() == "gay" or picked_random > 50 and rate_thing.lower() == "gay"):
                rate_thing = rate_thing+" 🏳️‍🌈"

            if user == "":
                colour_hex = thestuff.get(rate_thing.lower(), '%02x%02x%02x' % (
                    int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33)))
                msg = lang["commands"]["rate"]["returnSuccess1"].format(picked_random=picked_random, rate_thing=rate_thing)
                
            else:
                colour_hex = thestuff.get(user.lower(), '%02x%02x%02x' % (
                    int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33)))
                msg = lang["commands"]["rate"]["returnSuccess2"].format(picked_random=picked_random, rate_thing=rate_thing, user=user)

            colour = int(colour_hex, 16)
            embed = discord.Embed(title=msg, color=colour)
            await ctx.respond(mention_author=False, embed=embed)


def setup(bot):
    bot.add_cog(rate_slash(bot))
