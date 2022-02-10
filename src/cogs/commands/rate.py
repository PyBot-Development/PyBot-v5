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
from discord.commands import Option


async def convertToHex(self, num: int, rgb: list, invert: bool = False, textAddition: str = "") -> tuple:
    if invert:
        return ('%02x%02x%02x' % (int(rgb[0]-num*(rgb[0]/100)), int(rgb[1]-num*(rgb[1]/100)), int(rgb[2]-num*(rgb[2]/100))),
                (textAddition if num >= 50 else ""))
    else:
        return ('%02x%02x%02x' % (int(num*(rgb[0]/100)), int(num*(rgb[1]/100)), int(num*(rgb[2]/100))),
                (textAddition if num >= 50 else ""))


class rate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['r', 'meter'], description=support.getDescription("en.json", "rate"))
    async def rate(self, ctx, user, *, rest=None):
        lang = support.getLanguageFileG(ctx.guild)
        async with ctx.typing():

            randomNumber = int(random.randint(0, 100))

            words = {
                "gay": await self.convertToHex(num=randomNumber, rgb=[255, 105, 180], textAddition="🏳️‍🌈"),
                "black": await self.convertToHex(num=randomNumber, 	rgb=[232, 190, 172], invert=True),
                "furry": await self.convertToHex(num=randomNumber, rgb=[191, 111, 252], textAddition="<:furryowo:927510365133221929>"),
                "cum": await self.convertToHex(num=randomNumber, rgb=[255, 255, 255])
            }

            try:
                user = await commands.UserConverter().convert(ctx, user)
                ColourHex, addition = words.get(rest.lower(), await self.convertToHex(num=randomNumber, rgb=[155, 255, 133]))
                msg = lang["commands"]["rate"]["returnSuccess"].format(
                    picked_random=randomNumber, rate_thing=f"{(rest if rest != None else '')}{(addition if addition != None else '')}", user=user)
            except commands.errors.UserNotFound:
                ColourHex, addition = words.get(user.lower(), await self.convertToHex(num=randomNumber, rgb=[155, 255, 133]))
                msg = lang["commands"]["rate"]["returnSuccess"].format(
                    picked_random=randomNumber, rate_thing=f"{user} {(rest if rest != None else '')}{(addition if addition != None else '')}", user=ctx.message.author)
            colour = int(ColourHex, 16)
            await ctx.reply(mention_author=False, embed=discord.Embed(description=msg, color=colour))

class rate_slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @commands.slash_command(description=support.getDescription("en.json", "rate"))
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
                "furry": await self.convertToHex(num=randomNumber, rgb=[191, 111, 252], textAddition="<:furryowo:927510365133221929>"),
                "cum": await self.convertToHex(num=randomNumber, rgb=[255, 255, 255])
            }

            user = ctx.author if user is None else user

            ColourHex, addition = words.get(rest.lower(), await self.convertToHex(num=randomNumber, rgb=[155, 255, 133]))
            msg = lang["commands"]["rate"]["returnSuccess"].format(
                picked_random=randomNumber, rate_thing=f"{(rest if rest != None else '')}{(addition if addition != None else '')}", user=user)

            colour = int(ColourHex, 16)
            await ctx.respond(embed=discord.Embed(description=msg, color=colour))


def setup(bot):
    bot.add_cog(rate(bot))
    bot.add_cog(rate_slash(bot))
