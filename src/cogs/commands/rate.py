"""
Rate Command
~~~~~~~~~~~~~~~~~
Rates Things

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
import random
from cogs import checks

class rate(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['r', 'meter'], description="commands.rate.description")
    async def rate(self, ctx, user, *, rest_of_the_text=""):
        lang = support.getLanguageFileG(ctx.guild)
        async with ctx.typing():
            picked_random = random.randint(0, 100)
            thestuff = {
                "gay":   '%02x%02x%02x' % (int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55)), int(picked_random*random.uniform(0, 2.55))),
                "black": '%02x%02x%02x' % (int(253-(picked_random*2.53)),              int(231-(picked_random*2.31)),              int(214-(picked_random*2.14))),
                "furry": '%02x%02x%02x' % (int(picked_random*1.67),                    int(picked_random*1.99),                    int(picked_random*2.3)),
                "cum":   '%02x%02x%02x' % (int(picked_random*2.55),                    int(picked_random*2.55),                    int(picked_random*2.55)),
            }
            if(picked_random > 50 and user.lower() == "gay" or picked_random > 50 and rest_of_the_text.lower() == "gay"):
                rest_of_the_text = rest_of_the_text+"🏳️‍🌈"
            elif(picked_random > 50 and user.lower() == "furry" or picked_random > 50 and rest_of_the_text.lower() == "furry"):
                rest_of_the_text = f"{rest_of_the_text}<a:uwu:870669804233707580>"
            try:
                user = await commands.UserConverter().convert(ctx, user)
                msg = lang["commands"]["rate"]["returnSuccess2"].format(picked_random=picked_random, rate_thing=rest_of_the_text, user=user)
                colour_hex = thestuff.get(rest_of_the_text.lower(), '%02x%02x%02x' % (
                    int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33)))
            except:
                if user.startswith("@$"):
                    colour_hex = thestuff.get(rest_of_the_text.lower(), '%02x%02x%02x' % (
                        int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33)))
                    msg = lang["commands"]["rate"]["returnSuccess2"].format(picked_random=picked_random, rate_thing=rest_of_the_text, user=user[2:])
                else:
                    colour_hex = thestuff.get(user.lower(), '%02x%02x%02x' % (
                        int(picked_random*1.55), int(picked_random*2.55), int(picked_random*1.33)))
                    msg = lang["commands"]["rate"]["returnSuccess1"].format(picked_random=picked_random, rate_thing=f"{user}{rest_of_the_text}")
                    
            colour = int(colour_hex, 16)
            embed = discord.Embed(title=msg, color=colour)
            await ctx.reply(mention_author=False, embed=embed)


def setup(bot):
    bot.add_cog(rate(bot))
