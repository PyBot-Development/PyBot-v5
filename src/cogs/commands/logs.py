from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType

class logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["log"], description="Sends bot logs")
    async def logs(self, ctx):
        await ctx.send(file=nextcord.File(f"{support.path}/logs/{support.startup_date}.log"))
        

def setup(bot):
    bot.add_cog(logs(bot))