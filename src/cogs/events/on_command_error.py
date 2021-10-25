"""
Error Handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Does Stuff on Error

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
from datetime import datetime
import discord
import support
from discord.ext.commands import CommandNotFound
from colorama import *
import datetime

class on_command_error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = support.config.get("prefix")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.datetime.utcnow()
        time = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}.{time.microsecond:02d}"

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(
                description=f"🕰️ That command is ratelimited, try again in {datetime.timedelta(seconds=error.retry_after)}.",
                color=support.colours.red
            ),
                delete_after=10)

        elif isinstance(error, CommandNotFound):
            cmd = str(ctx.message.content).split(" ")[0]
            await ctx.send(embed=discord.Embed(
                description=f"<:QuestionMark:885978535670464533> Command `{cmd}` not found.",
                color=support.colours.red
            ),
                delete_after=10)

        elif isinstance(
            error, (commands.MissingRequiredArgument,
                    commands.MissingPermissions)
        ):
            await ctx.send(embed=discord.Embed(
                description=f"<:QuestionMark:885978535670464533> {error}".capitalize(
                ),
                color=support.colours.red
            ),
                delete_after=10)
        else:
            error_ = str(error)[29:] if str(error).lower().startswith(
                "command") else str(error)  # Removes: "Command Invoked Error"
            await ctx.send(embed=discord.Embed(
                description=f"<:QuestionMark:885978535670464533> {str(error_).capitalize()}",
                color=support.colours.red
            ),
                delete_after=10)
            
            if support.config.get("debug"):
                raise error
        support.log(datetime.datetime.utcnow(), "ERROR", ctx.message.author, error)
        return


def setup(bot):
    bot.add_cog(on_command_error(bot))
