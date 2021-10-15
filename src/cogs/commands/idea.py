from re import I
from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType
import asyncio

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
    @commands.command()
    async def idea(self, ctx, *, Text):
        await self.get_channel()
        await self.channel.send(content="<@846298981797724161>" ,embed=nextcord.Embed(
            title=ctx.message.author.id,
            description=Text,
            color=support.colours.default
        ).set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url))
        await ctx.send(embed=nextcord.Embed(
            description="Your idea was sent.",
            color=support.colours.default
            ))
    

def setup(bot):
    bot.add_cog(idea(bot))