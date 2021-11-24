from discord.ext import commands
import discord
from datetime import datetime
from colorama import *
import support

def default():
    async def checks(ctx):
        user = list(await support.globalData.getUser(ctx.author))
        if user[3] != 0:
            await ctx.send(embed=discord.Embed(description="🚷 You're banned.",color=support.colours.yellow), delete_after=10)
            return False
        return True
    return commands.check(checks)

def admin():
    async def checks(ctx):
        user = list(await support.globalData.getUser(ctx.message.author))
        if user[4] != 1 or ctx.message.author.id != 846298981797724161:
            await ctx.send(embed=discord.Embed(description="🗝️ You've no permission.",color=support.colours.yellow), delete_after=10)
            return False
        return True
    return commands.check(checks)
