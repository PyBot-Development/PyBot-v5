"""
Loop Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a template for loops

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.
"""

from discord.ext import commands, tasks


class auto_backup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop_test.start()

    @tasks.loop(hours=10)
    async def auto_backup(self):
        # Do Stuff Here
        pass

    @auto_backup.before_loop
    async def auto_backup(self):
        await self.client.wait_until_ready()


def setup(client):
    #client.add_cog(auto_backup(client))
    pass
