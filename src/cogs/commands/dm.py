from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType

class dm(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="DMs user")
    async def dm(self, ctx, user, *,message):
        user = await commands.UserConverter().convert(ctx, user)
        channel = await user.create_dm()
        await channel.send(message)
        await ctx.send(embed=nextcord.Embed(description=f"DMed {user.mention()}: `{message}`.", color=support.colours.default), delete_after=10)

def setup(bot):
    bot.add_cog(dm(bot))