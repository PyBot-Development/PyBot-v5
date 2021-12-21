"""
Idea Command
~~~~~~~~~~~~~~~~~
Allows users to send ideas for bot

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks


class idea(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_channel(self):
        try:
            self.channel.id
        except:
            guild = self.client.get_guild(885976189049651200)
            for i in guild.text_channels:
                if i.id == 885986347234508840:
                    self.channel = i

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.idea.description")
    async def idea(self, ctx, *, Text):
        lang = support.getLanguageFileG(ctx.guild)
        await self.get_channel()
        await self.channel.send(content="<@846298981797724161>", embed=discord.Embed(
            title=ctx.message.author.id,
            description=Text,
            color=support.colours.default
        ).set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar))
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["idea"]["returnSuccess"],
            color=support.colours.default
        ))


def setup(bot):
    bot.add_cog(idea(bot))
