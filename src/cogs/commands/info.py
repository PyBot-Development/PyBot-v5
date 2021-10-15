"""
Info Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives info about bot

:copyright: (c) 2021 Novasky-Guy
:license: GPL-3.0, see LICENSE for more details.
"""

from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType
from datetime import timedelta, datetime
import math
from run import __version__, __title__, __copyright__, __license__

class info(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends Info About Bot")
    async def info(self, ctx):
        author = await self.client.fetch_user(846298981797724161)
        onlineFor = int(datetime.utcnow().timestamp()) - support.startup_timestamp
        await ctx.send(embed=nextcord.Embed(
            title=f"{__title__} Info",
            description=f"""
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

Current Version: {__version__}
V5 Creation Date: <t:1633946400:D>

Author: {author.mention}
Prefix: {support.prefix}
Online For: {timedelta(seconds=math.floor(onlineFor))}

Copyright: {__copyright__}
License: {__license__}

Commands Count: {len(self.client.commands)}
""", colour=support.colours.default))

def setup(bot):
    bot.add_cog(info(bot))