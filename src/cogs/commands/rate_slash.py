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

    async def convertToHex(self, num: int, rgb: list, invert: bool = False, textAddition: str = "") -> tuple:
        if invert:
            return ('%02x%02x%02x' % (int(rgb[0]-num*(rgb[0]/100)), int(rgb[1]-num*(rgb[1]/100)), int(rgb[2]-num*(rgb[2]/100))),
                (textAddition if num >= 50 else ""))
        else:
            return ('%02x%02x%02x' % (int(num*(rgb[0]/100)), int(num*(rgb[1]/100)), int(num*(rgb[2]/100))),
                (textAddition if num >= 50 else ""))

    @checks.default()
    @client.slash_command(description="commands.rate.description")
    async def rate(self, ctx,
                   rest: Option(str, "Rate What?"),
                   user: Option(str, "User or Thing to rate",
                                required=False) = None,
                   ):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            randomNumber = int(random.randint(0, 100))
            words = {
                "gay": await self.convertToHex(num=randomNumber, rgb=[255, 105, 180], textAddition="🏳️‍🌈"),
                "black": await self.convertToHex(num=randomNumber, 	rgb=[232, 190, 172], invert=True),
                "furry": await self.convertToHex(num=randomNumber, rgb=[191, 111, 252], textAddition="<a:uwu:870669804233707580>"),
                "cum": await self.convertToHex(num=randomNumber, rgb=[255, 255, 255])
            }

            user = ctx.author if user is None else user

            ColourHex, addition = words.get(rest.lower(), await self.convertToHex(num=randomNumber, rgb=[155, 255, 133]))
            msg = lang["commands"]["rate"]["returnSuccess"].format(
                picked_random=randomNumber, rate_thing=f"{(rest if rest != None else '')}{(addition if addition != None else '')}", user=user)

            colour = int(ColourHex, 16)
            await ctx.respond(mention_author=False, embed=discord.Embed(description=msg, color=colour))


def setup(bot):
    bot.add_cog(rate_slash(bot))
