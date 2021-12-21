"""
Loop Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a template for loops

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.
"""

from discord.ext import commands, tasks
import discord
from run import __version__
from support import config

class rpc_update(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rpc_update.start()

    @tasks.loop(minutes=5)
    async def rpc_update(self):
        if config.get("debug"):
            return
        await self.client.change_presence(activity=discord.Game(name=f"on {len(self.client.guilds)} Servers, Version: {__version__}"))

    @rpc_update.before_loop
    async def before_rpc_update(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(rpc_update(client))
    pass
