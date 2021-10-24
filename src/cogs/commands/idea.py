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

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends bot idea giv ideas plz")
    async def idea(self, ctx, *, Text):
        await self.get_channel()
        await self.channel.send(content="<@846298981797724161>", embed=discord.Embed(
            title=ctx.message.author.id,
            description=Text,
            color=support.colours.default
        ).set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar))
        await ctx.send(embed=discord.Embed(
            description="Your idea was sent.",
            color=support.colours.default
        ))


def setup(bot):
    bot.add_cog(idea(bot))
