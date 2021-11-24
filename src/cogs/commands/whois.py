"""
WHOIS Command
~~~~~~~~~~~~~~~~~
Shows user info

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks

class whois(commands.Cog):
    def __init__(self, client):
        self.client = client
    @checks.default()
    @commands.guild_only()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Shows user info")
    async def whois(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        roles = "None"
        if len(user.roles) > 1:
            roles = "".join(f"{i.mention} " for i in user.roles[1:])
        fetched = await self.client.fetch_user(user.id)
        embed = discord.Embed(title=f"{user}",
                               description=f"""
User: {user.mention}
ID: `{user.id}`
Created at: `{user.created_at}`
Status: `{user.status}`
Bot: `{user.bot}`

Joined at: `{user.joined_at}`
Nick: `{user.nick}`
Boosting since: `{user.premium_since}`

Roles:
{roles}
""", color=user.color)
        embed.set_thumbnail(url=user.display_avatar)

        if fetched.banner != None:
            embed.set_image(url=fetched.banner)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(whois(bot))
