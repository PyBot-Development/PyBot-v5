"""
Help Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Help Command with menu

:copyright: (c) 2021 Novasky-Guy
:license: MIT, see LICENSE for more details.
"""

from nextcord.ext import commands
import nextcord
import support
from nextcord.ext.commands import cooldown, BucketType, CommandNotFound
from nextcord.ext import menus

class HelpMenu(menus.ButtonMenu):
    def __init__(self, client):
        super().__init__(disable_buttons_after=True)
        self.client = client
        commands = ''.join(f"{support.prefix}{command}\n​   `{command.description}`\n" for command in self.client.commands).splitlines()
        self.commands = []
        n = 10
        for index in range(0, len(commands), n):
            page = ''.join(f"{item}\n" for item in commands[index : index + n])
            self.commands.append(page)
        self.maxPages = int(len(self.commands)) - 1
        self.page = 0

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=nextcord.Embed(
            title="Help",
            description=f"""
[Website](https://py-bot.cf/)
[Commands](https://py-bot.cf/commands)
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"), view=self)

    @nextcord.ui.button(label="<")
    async def backwards(self, button, interaction):
        if self.page == 0:
            await self.message.edit(embed=nextcord.Embed(
            title="Help",
            description=f"""
[Website](https://py-bot.cf/)
[Commands](https://py-bot.cf/commands)
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1} **Page Limit Reached**"))
            return

        self.page -= 1
        await self.message.edit(embed=nextcord.Embed(
            title="Help",
            description=f"""
[Website](https://py-bot.cf/)
[Commands](https://py-bot.cf/commands)
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))

    @nextcord.ui.button(emoji="\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, button, interaction):
        self.stop()

    @nextcord.ui.button(label=">")
    async def forwards(self, button, interaction):
        if self.page == self.maxPages:
            await self.message.edit(embed=nextcord.Embed(
            title="Help",
            description=f"""
[Website](https://py-bot.cf/)
[Commands](https://py-bot.cf/commands)
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1} **Page Limit Reached**"))
            return

        self.page += 1
        await self.message.edit(embed=nextcord.Embed(
            title="Help",
            description=f"""
[Website](https://py-bot.cf/)
[Commands](https://py-bot.cf/commands)
[PyBot's Discord Server](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))
        
class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["?"], description="Help Command")
    async def help(self, ctx, *, command=None):
        await HelpMenu(self.client).start(ctx)
            
def setup(client):
    client.add_cog(help(client))