"""
On Ready
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs code when bot is ready

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import support
from datetime import datetime   
import discord
from run import __version__
class on_ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        support.log(datetime.utcnow(), "INFO", "Startup",
                    f"{self.client.user} is online!")
        await self.client.change_presence(activity=discord.Game(name=f"on {len(self.client.guilds)} Servers, Version: {__version__}"))
def setup(client):
    client.add_cog(on_ready(client))
