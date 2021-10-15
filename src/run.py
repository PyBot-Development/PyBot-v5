# -*- coding: utf-8 -*-
"""
Discord Pybot
~~~~~~~~~~~~~~~~~

Discord Bot

:copyright: (c) 2021-2021 mariyt10
:license: MIT, see LICENSE for more details.

I had to commit something to test shit
"""

__title__ = 'Pybot V5'
__author__ = 'mariyt10'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2021 mariyt10'
__version__ = '1.0.0'

from nextcord.ext import commands
import os
from colorama import *
import support
from datetime import datetime
from colorama import *

prefix=support.config.get("prefix")
client=commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True)
client.remove_command('help')

def loadCog(path, folder=True):
    if folder:
        for filename in os.listdir(f'{support.path}/cogs/{path}'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{path}.{filename[:-3]}')
                support.log(datetime.utcnow(), "INFO", "Cog loaded", f"{filename[:-3]}")
    else:
        client.load_extension(f'cogs.{path}')

if __name__ == "__main__":

    @client.before_invoke
    async def common(ctx):
        support.log(datetime.utcnow(), "COMMAND", f"{ctx.author}", ctx.command)

    loadCog("events")
    loadCog("commands")
    loadCog("loops")
    print("")
    client.run(support.config.get("token"))
