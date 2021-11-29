# -*- coding: utf-8 -*-
"""
Discord Pybot
~~~~~~~~~~~~~~~~~

Discord Bot 

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

__title__ = 'Pybot V5'
__author__ = 'M2rsho'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2021 M2rsho'
__version__ = '1.6.1'

from discord.ext import commands
import discord
import os
from colorama import *
import support
from datetime import datetime
from colorama import *
from cogs.checks import *

prefix = support.config.get("prefix")
activity = discord.Game(name=f"{prefix}help, Version: {__version__}")

client = commands.Bot(command_prefix=support.getPrefix, case_insensitive=True, activity=activity)
#    support.GetPrefix), case_insensitive=True, activity=activity)


client.remove_command('help')


def loadCog(path, folder=True):
    if folder:
        for filename in os.listdir(f'{support.path}/cogs/{path}'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{path}.{filename[:-3]}')
                support.log(datetime.utcnow(), "INFO",
                            "Cog loaded", f"{filename[:-3]}")
    else:
        client.load_extension(f'cogs.{path}')

if __name__ == "__main__":

    @client.before_invoke
    async def common(ctx):
        support.log(datetime.utcnow(), "COMMAND", f"{ctx.author}", ctx.message.content)
        
    loadCog("events")
    loadCog("commands")
    loadCog("loops")
    
    print("")
    client.run(support.config.get("token"))
