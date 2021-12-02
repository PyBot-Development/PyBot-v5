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
import json
import os

class on_message(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.censorshit = {
            'free taiwan': -30,
            'something happened on 1989': -100,
            'super idol': 15,
            'nothing happened on 1989': 100,
            'only one child': 30,
            'social credit hack!11!1!1!!!!111!1!!!!!!1!!!!11!1!': 1500
        }
        
    @commands.Cog.listener()
    async def on_message(self, message):
        for cs in self.censorshit:
            if cs in message.content.lower():
                await support.globalData.addSocialCredit(message.author, self.censorshit[cs])
                file = await support.processing.generate_social_credit(self.censorshit[cs], message.author.id) 
                await message.reply(
                    embed=discord.Embed(
                        description=f"{self.censorshit[cs]} Social Credit. Your Social Credit is now `{await support.globalData.getSocialCredit(message.author)}`",
                        colour=support.colours.red)
                         .set_image(url=f"attachment://{message.author.id}.png"),
                    file=discord.File(file),
                    delete_after=30)
                os.remove(file)
                
def setup(client):
    client.add_cog(on_message(client))
