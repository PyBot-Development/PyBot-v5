from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType

class embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Creates Embed Message")
    async def embed(self, ctx, description=None, color=None, title=None,):
        colour = int(color.replace("#", ""), 16)
        await ctx.send(embed=nextcord.Embed(title=title, description=description, color=colour))

def setup(bot):
    bot.add_cog(embed(bot))