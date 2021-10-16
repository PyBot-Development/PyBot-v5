"""
Meme Command
~~~~~~~~~~~~~~~~~
Sends meme

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import random
import requests
import json


class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.topics = ["dankmemes",
                       "memes",
                       "me_irl",
                       "ComedyCemetery",
                       "terriblefacebookmemes",
                       "shitposting",
                       "ProgrammerHumor"]

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends random meme")
    async def meme(self, ctx, *, subredd=None):
        async with ctx.typing():
            topic = random.choice(self.topics) if subredd is None else subredd
            meme = json.loads(requests.get(
                f"https://meme-api.herokuapp.com/gimme/{topic}").text)

            if meme["nsfw"]:
                await ctx.send(embed=nextcord.Embed(description="🔞 Subreddit is 18+", color=support.colours.red), delete_after=10)
                return

            await ctx.send(embed=nextcord.Embed(
                title=f'''{meme["title"]}''',
                url=meme["postLink"],
                description=f"""
                u/{meme["author"]}""",
                color=support.colours.default
            ).set_image(url=meme["url"]).set_footer(text=f"⬆️ {meme['ups']} • r/{topic}"))


def setup(bot):
    bot.add_cog(meme(bot))
