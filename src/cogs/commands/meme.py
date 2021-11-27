"""
Meme Command
~~~~~~~~~~~~~~~~~
Sends meme

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands import cooldown, BucketType
import support
import random
import requests
import json
from cogs import checks

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

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.meme.description")
    async def meme(self, ctx, *, subredd=None):
        async with ctx.typing():
            lang = support.getLanguageFileG(ctx.guild)
            topic = random.choice(self.topics) if subredd is None else subredd
            meme = json.loads(requests.get(
                f"https://meme-api.herokuapp.com/gimme/{topic}").text)

            if meme["nsfw"]:
                await ctx.send(embed=discord.Embed(description="🔞 Subreddit is 18+", color=support.colours.red), delete_after=10)
                return

            await ctx.send(embed=discord.Embed(
                title=f'''{meme["title"]}''',
                url=meme["postLink"],
                description=f"""
                u/{meme["author"]}""",
                color=support.colours.default
            ).set_image(url=meme["url"]).set_footer(text=f"⬆️ {meme['ups']} • r/{topic}"))


def setup(bot):
    bot.add_cog(meme(bot))
