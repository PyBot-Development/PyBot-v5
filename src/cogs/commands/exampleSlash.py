"""
Say Command
~~~~~~~~~~~~~~~~~
Says something using bot

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
from discord.commands import Option
from cogs import checks

class hello(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @commands.slash_command(guild_ids=[885976189049651200])
    async def hello(
        self,
        ctx,
        name: Option(str, "Enter your name"),
        gender: Option(str, "Choose your gender", choices=["Male", "Female", "Other"]),
        age: Option(int, "Enter your age", required=False, default=18),
    ):
        await ctx.respond(f"Hello {name}")


def setup(bot):
    # bot.add_cog(hello(bot))
    pass
