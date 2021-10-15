from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import cooldown, BucketType
import support
import random
import asyncpraw

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.topics =  ["dankmemes",
                  "memes",
                  "me_irl",
                  "ComedyCemetery",
                  "terriblefacebookmemes",
                  "shitposting"]
        self.reddit = asyncpraw.Reddit(client_id=support.config.get("Client_Id"),
                     client_secret=support.config.get("Client_Secret"),
                     user_agent=support.config.get("User_Agent"), 
                     check_for_async=False
                     )

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Sends random meme")
    async def meme(self, ctx, *, subredd=None):
        msg = await ctx.send("Please wait.. It may take a while. Because reddit api shit.")
        async with ctx.typing():
            topic = random.choice(self.topics) if subredd is None else subredd
            subreddit = await self.reddit.subreddit(topic)
            await subreddit.load()
            meme = await subreddit.random()
            if subreddit.over18:
                await ctx.send(embed=nextcord.Embed(description=f"🔞 Subreddit is 18+", color=support.colours.default), delete_after=10)
                return
            await ctx.send(embed=nextcord.Embed(
                title=f"{meme.title}",
                url=meme.shortlink,
                description=f"""
                u/{meme.author.name}""",
                color=support.colours.default
            ).set_image(url=meme.url).set_footer(text=f"Requested by: {ctx.message.author} • ⬆️ {meme.ups} | r/{topic}"))
            await msg.delete()
            
def setup(bot):
    bot.add_cog(meme(bot))