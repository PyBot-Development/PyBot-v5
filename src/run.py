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
__version__ = '1.7.1'

from discord.ext import commands
import discord
import os
from colorama import *
import support
from datetime import datetime
from colorama import *
from cogs.checks import *
import server

prefix = support.config.get("prefix")

client = commands.Bot(command_prefix=support.getPrefix, case_insensitive=True, owner_ids=[471269649296916481, 846298981797724161, 760602301790158868, 484170415720235009, 459554887316013067])
client.activity = discord.Game(name=f"on {len(client.guilds)} Servers, Version: {__version__}")

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
            support.log(datetime.utcnow(), "COMMAND", f"{ctx.author}", ctx.message.content)
        except:
            support.log(datetime.utcnow(), "SLASH COMMAND", f"{ctx.author}", ctx.command)
        
    loadCog("events")
    loadCog("commands")
    loadCog("loops")
    print("")
    if support.config.get("serverSettings")["run"]:
        server = server.server()
        server.app.run(debug=False, port=support.config.get("serverSettings")["port"], use_reloader=False, threaded=True)
    client.run(support.config.get("token"))
