from discord.ext import commands
import discord
from datetime import datetime
from colorama import *
import support

class UserBanned(commands.CommandError):
    """Error class for banned user"""
    def __init__(self) -> None:
        super().__init__(f'🚷 You\'re banned.')

class NoPermissions(commands.CommandError):
    """Error class for no permissions"""
    def __init__(self) -> None:
        super().__init__(f'🗝️ You\'ve no permission.')

def default():
    async def checks(ctx):
        try:
            if support.config.get("debug") and ctx.guild.id != 885976189049651200:
                return
        except AttributeError:
            if support.config.get("debug"):
                return
        user = list(await support.globalData.getUser(ctx.author))
        if user[3] != 0:
            raise UserBanned
            #await ctx.send(embed=discord.Embed(description="🚷 You're banned.",color=support.colours.yellow), delete_after=10)
            #return False
        return True
    return commands.check(checks)

def admin():
    async def checks(ctx):
        user = list(await support.globalData.getUser(ctx.message.author))
        if user[4] != 1 and ctx.message.author.id not in [846298981797724161, 484170415720235009]:
            raise NoPermissions
            #await ctx.send(embed=discord.Embed(description="🗝️ You've no permission.",color=support.colours.yellow), delete_after=10)
            #return False
        return True
    return commands.check(checks)
