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
__copyright__ = 'Copyright 2021-2022 M2rsho'
__version__ = '1.8.0'

from discord.ext import commands
import discord
import os
from colorama import *
import support
from datetime import datetime
from colorama import *
from cogs.checks import *

prefix = support.config.get("prefix")

client = commands.Bot(command_prefix=support.getPrefix, case_insensitive=True, owner_ids=[471269649296916481, 846298981797724161, 760602301790158868, 484170415720235009, 459554887316013067])
if not support.config.get("debug"):
    client.activity = discord.Game(name=f"on [LOADING] Servers, Version: {__version__}")

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
        return "Loaded extension"

if __name__ == "__main__":

    @client.before_invoke
    async def common(ctx):
        try:
            support.log(datetime.utcnow(), "COMMAND", f"{str(ctx.author)}", ctx.message.content)
        except:
            support.log(datetime.utcnow(), "SLASH COMMAND", f"{str(ctx.author)}", ctx.command)
        
    loadCog("events")
    loadCog("commands")
    loadCog("loops")
    print("")
    client.run(support.config.get("token"))
