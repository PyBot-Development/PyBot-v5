from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType


class alt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, 300, BucketType.user)
    @commands.command(description="Gives you random minecraft alt")
    async def alt(self, ctx):
        async with ctx.typing():
            alt = await support.getAlt()
            channel = await ctx.message.author.create_dm()
            await channel.send(embed=nextcord.Embed(description=f"||{alt}||", color=support.colours.default))
            
def setup(bot):
    bot.add_cog(alt(bot))