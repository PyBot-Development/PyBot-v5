"""
Help Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Help Command with menu

:copyright: (c) 2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
import support
from discord.ext.commands import cooldown, BucketType, CommandNotFound
from cogs import checks

class HelpButtons(discord.ui.View):
    def __init__(self, client, author, guild):
        super().__init__(timeout=20)
        self.client = client
        self.page = 0
        self.author = author
        self.message = None

        if guild is not None:
            language = support.getLanguage(guild)
        else:
            language = "en.json"

        self.lang = support.getLanguageFile(language)

        commands = ''.join(
            f"{support.prefix}{command}\n​   `{support.getDescription(language, str(command))}`\n" for command in client.commands).splitlines()
        self.commands = []
        n = 10
        for index in range(0, len(commands), n):
            page = ''.join(f"{item}\n" for item in commands[index: index + n])
            self.commands.append(page)

        self.maxPages = int(len(self.commands)) - 1

    async def on_timeout(self) -> None:
        self.back.disabled = True
        self.stop_button.disabled = True
        self.forward.disabled = True
        self.home.disabled=True
        self.end.disabled=True
        await self.message.edit(view=self)
        return await super().on_timeout()

    @discord.ui.button(label="<<", style=discord.ButtonStyle.grey)
    async def home(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return

        self.page = 0
        await interaction.response.edit_message(embed=discord.Embed(
            title=self.lang["help"],
            description=f"""
[{self.lang["website"]}](https://py-bot.cf/) | [{self.lang["command"]}](https://py-bot.cf/commands) | [{self.lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label="<", style=discord.ButtonStyle.grey)
    async def back(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.page -= 1 if self.page > 0 else 0
        await interaction.response.edit_message(embed=discord.Embed(
            title=self.lang["help"],
            description=f"""
[{self.lang["website"]}](https://py-bot.cf/) | [{self.lang["command"]}](https://py-bot.cf/commands) | [{self.lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label="⬜", style=discord.ButtonStyle.grey)
    async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.back.disabled = True
        self.stop_button.disabled = True
        self.forward.disabled = True
        self.home.disabled=True
        self.end.disabled=True
        await interaction.response.edit_message(view=self)

        self.stop()

    @discord.ui.button(label=">", style=discord.ButtonStyle.grey)
    async def forward(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        if self.page < self.maxPages:
            self.page += 1
        await interaction.response.edit_message(embed=discord.Embed(
            title=self.lang["help"],
            description=f"""
[{self.lang["website"]}](https://py-bot.cf/) | [{self.lang["command"]}](https://py-bot.cf/commands) | [{self.lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label=">>", style=discord.ButtonStyle.grey)
    async def end(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.page = self.maxPages
        await interaction.response.edit_message(embed=discord.Embed(
            title=self.lang["help"],
            description=f"""
[{self.lang["website"]}](https://py-bot.cf/) | [{self.lang["command"]}](https://py-bot.cf/commands) | [{self.lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{self.commands[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: {self.page+1}/{self.maxPages+1}"))



class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["?"], description="commands.help.description")
    async def help(self, ctx, *, command=None):
        view = HelpButtons(self.client, ctx.message.author, ctx.guild)

        lang = view.lang

        message = await ctx.reply(mention_author=False, embed=discord.Embed(
            title=lang["help"],
            description=f"""
[{lang["website"]}](https://py-bot.cf/) | [{lang["command"]}](https://py-bot.cf/commands) | [{lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{view.commands[0]}""",
            color=support.colours.default
        ).set_footer(text=f"Page: 1/{view.maxPages+1}"), view=view)
        view.message = message

def setup(client):
    client.add_cog(help(client))
