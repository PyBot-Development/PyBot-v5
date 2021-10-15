from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support

class say(commands.Cog):
    def __init__(self, client):
        self.client = client
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["tell", "sudo"])
    async def say(self, ctx, *, arg):
        await ctx.send(f"​{arg}".replace("@everyone", "@​everyone").replace("@here", "@​here"))

def setup(bot):
    bot.add_cog(say(bot))