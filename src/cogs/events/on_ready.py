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

class on_ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        support.log(datetime.utcnow(), "INFO", "Startup",
                    f"{self.client.user} is online!")


def setup(client):
    client.add_cog(on_ready(client))
