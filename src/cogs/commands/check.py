from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType
class command(commands.Cog, name="check"):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def check(self, ctx, *, combo):
        await ctx.send(embed=nextcord.Embed(description=support.check(combo).result, color=support.colours.default))

def setup(bot):
    bot.add_cog(command(bot))