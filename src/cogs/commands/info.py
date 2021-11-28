"""
Info Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives info about bot

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from datetime import timedelta, datetime
import math
from run import __version__, __title__, __copyright__, __license__
from cogs import checks

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.info.description")
    async def info(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        author = await self.client.fetch_user(846298981797724161)
        onlineFor = int(datetime.utcnow().timestamp()) - \
            support.startup_timestamp
        await ctx.send(embed=discord.Embed(
            title=f'{__title__} {lang["info"]}',
            description=f'[{lang["discord"]}](https://discord.gg/dfKMTx9Eea)\n\n' + lang["commands"]["info"]["returnSuccess"].format(
                version=__version__,
                author=author.mention,
                prefix=support.prefix,
                onlineFor=timedelta(seconds=math.floor(onlineFor)),
                servers=len(self.client.guilds),
                license=__license__,
                copyright=__copyright__,
                commandsCount=len(self.client.commands)
            ), colour=support.colours.default))


def setup(bot):
    bot.add_cog(info(bot))
