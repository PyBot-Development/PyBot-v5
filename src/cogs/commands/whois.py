"""
WHOIS Command
~~~~~~~~~~~~~~~~~
Shows user info

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class whois(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @commands.guild_only()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description=support.getDescription("en.json", "whois"))
    async def whois(self, ctx, *, user: discord.Member = None):
        lang = support.getLanguageFileG(ctx.guild)
        if user is None:
            user = ctx.message.author
        roles = "None"
        if len(user.roles) > 1:
            roles = "".join(f"{i.mention} " for i in user.roles[1:])
        fetched = await self.client.fetch_user(user.id)
        embed = discord.Embed(title=f"{user}",
                               description=lang["commands"]["whois"]["returnSuccess"].format(mention=user.mention, id=user.id, created_at=user.created_at, status=user.status, bot=user.bot, joined_at=user.joined_at, nick=user.nick, premium_since=user.premium_since, roles=roles), color=user.color)
        embed.set_thumbnail(url=user.display_avatar)

        if fetched.banner != None:
            embed.set_image(url=fetched.banner)
        await ctx.reply(mention_author=False, embed=embed)


def setup(bot):
    bot.add_cog(whois(bot))
