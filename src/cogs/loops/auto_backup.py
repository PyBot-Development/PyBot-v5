"""
Database Auto Backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because people are gay

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.
"""

from discord.ext import commands, tasks
from shutil import copyfile
import support
from datetime import datetime

class auto_backup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.auto_backup.start()

    @tasks.loop(minutes=30)
    async def auto_backup(self):
        copyfile(f"{support.path}/data/database.db", f"{support.path}/data/DataBackups/{datetime.utcnow()}.db") 

    @auto_backup.before_loop
    async def before_loop_auto_backup(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(auto_backup(client))
    pass
