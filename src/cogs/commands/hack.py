"""
Idea Command
~~~~~~~~~~~~~~~~~
Allows users to send ideas for bot

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType
from cogs import checks
from faker import Faker
from faker.providers import internet, address, credit_card, geo, automotive, job
import asyncio
from random import randint



class hack(commands.Cog):
    def __init__(self, client):
        self.client = client

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description=support.getDescription("en.json", "hack"))
    async def hack(self, ctx, *, user: discord.Member):
        fake = Faker(['en_US', 'en_GB'])
        
        newline = '\n'
        message = await ctx.send(embed=discord.Embed(description=f"Hacking {user}.. Please wait", colour=support.colours.yellow))

        await asyncio.sleep(randint(2,5))

        embed = discord.Embed(description=f"Hacked {user}", color=support.colours.green)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="IRL Name", value=fake.name(), inline=True)
        embed.add_field(name="Credit Card Info", value=fake.credit_card_full(), inline=True)
        embed.add_field(name="Job", value=fake.job(), inline=True)
        embed.add_field(name="Public IP", value=fake.ipv4_public(), inline=True)
        embed.add_field(name="Private IP", value=fake.ipv4_private(), inline=True)
        embed.add_field(name="Address", value=fake.address(), inline=True)
        embed.add_field(name="Current Location", value=''.join(i + newline for i in fake.local_latlng()), inline=True)
        embed.add_field(name="Car License Plate", value=fake.license_plate(), inline=True)

        await message.edit(content="", embed=embed)

def setup(bot):
    bot.add_cog(hack(bot))
