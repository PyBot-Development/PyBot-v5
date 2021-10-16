"""
YT Command
~~~~~~~~~~~~~~~~~
Searches youtube

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import urllib
import re


class yt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["youtube", "video"], description="Searches YouTube")
    async def yt(self, ctx, *, search):
        async with ctx.typing():
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen(
                'http://www.youtube.com/results?' + query_string)
            search_results = re.findall(
                r'/watch\?v=(.{11})', htm_content.read().decode())
            await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


def setup(bot):
    bot.add_cog(yt(bot))
