"""
Loop Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a template for loops

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.
"""

from discord.ext import commands, tasks


class loop_test(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop_test.start()

    @tasks.loop(seconds=10.0)
    async def loop_test(self):
        # Do Stuff Here
        pass

    @loop_test.before_loop
    async def before_loop_test(self):
        await self.client.wait_until_ready()


def setup(client):
    # client.add_cog(loop_test(client))
    pass
