from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="nick"):
    def __init__(self, client):
        self.client = client
    
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def nick(self, ctx, *, nick=None):
        await ctx.message.guild.me.edit(nick=nick)
        await ctx.send(embed=nextcord.Embed(description=f"Changed nick to `{nick}`", color=support.colours.default), delete_after=10)

def setup(bot):
    bot.add_cog(command(bot))