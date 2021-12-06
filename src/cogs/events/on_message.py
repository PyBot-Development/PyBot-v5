"""
On Ready
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs code when bot is ready

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import support
from datetime import datetime, timezone 
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
            'only have one child': 30,
            'superidol is good': 15,
            'superidol is shit': -50,
            'superidol is bad': -50,
            'superidol good': 15,
            'superidol shit': -50,
            'superidol bad': -50,
            'bing chilling': 5,
            'any dupes': -500,
            'give dupes': -500,
            'send dupes': -500,
            'send dupe': -500,
            'free taiwian': -30,
            'taiwan is a country': -50,
            'taiwan is not a country': 50,
            'winnie-the-pooh': -2000,
            'winnie the pooh': -2000,
            'john xina': 10,
            'the wok': 10,
            'nothing happened in tinanmen square': 100,
            'something happened in tinanmen square': -100,
            'someone died in tinanmen square': -100,
            'no one died in tiananmen square': -100,
            'social credit hack!11!1!1!!!!111!1!!!!!!1!!!!11!1!': 1500
        }
    
    @commands.Cog.listener()
    async def on_message(self, message):
        #def check(m):
        #    return (m.author == message.author
        #        and (cs in m.content for cs in self.censorshit)
        #        and (datetime.now(timezone.utc)-m.created_at).seconds <= 2)
        #
        #if not message.author.bot:
        #   if not len(list(filter(lambda m: check(m), self.client.cached_messages))) <= 2:
        #        return

            for cs in self.censorshit:
                if cs in message.content.lower():
                    await support.globalData.addSocialCredit(message.author, self.censorshit[cs])
                    support.log(datetime.utcnow(), "SOCIAL CREDIT", f"{message.author}", message.content)
                    file = await support.processing.generate_social_credit(self.censorshit[cs], message.author.id) 
                    channel = await message.author.create_dm()
                    await channel.send(
                        embed=discord.Embed(
                            description=f"[Jump To Message]({message.jump_url}).\n{self.censorshit[cs]} Social Credit. Your Social Credit is now `{await support.globalData.getSocialCredit(message.author)}`",
                            colour=support.colours.red)
                            .set_image(url=f"attachment://{message.author.id}.png"),
                        file=discord.File(file))
                    try:
                        os.remove(file)
                    except:
                        pass
                
def setup(client):
    client.add_cog(on_message(client))
