"""
Black Jack Command
~~~~~~~~~~~~~~~~~
Bruh moment

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands
import discord
from discord.ext.commands.core import is_owner
import support
from discord.ext.commands import cooldown, BucketType
import random
from math import ceil

cards = list({
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}.items())


class createButtons(discord.ui.View):
    def __init__(self, client, author, bet):
        super().__init__(timeout=30)
        self.client = client
        self.author = author
        self.message = None
        self.bet = bet

        self.dealerValue = 0
        self.dealerDeck = None
        self.dealerCards = []

        self.userValue = 0
        self.userDeck = None
        self.userCards = []

    async def on_timeout(self) -> None:
        self.hit.disabled = True
        self.stand.disabled = True
        self.resign.disabled = True
        await self.message.edit(view=self)
        return await super().on_timeout()

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.grey)
    async def hit(self, button: discord.ui.Button, interaction: discord.Interaction):
        card = random.choice(cards)
        self.userCards.append(card)
        await self.updateCards(interaction)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.grey)
    async def stand(self, button: discord.ui.Button, interaction: discord.Interaction):
        while self.dealerValue <= 16:
            self.dealerCards.append(random.choice(cards))
            self.dealerDeck, self.dealerValue = await self.renderCards(self.dealerCards)

        if self.dealerValue > 21:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
You won `{ceil(self.bet/2)}`$

Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerDeck}
`(Value: {self.dealerValue})`""", colour=support.colours.green))
            await support.globalData.addBalance(self.author, self.bet+ceil(self.bet/2))
        elif self.dealerValue == self.userValue:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
Tie. Your money was pushed back

Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerDeck}
`(Value: {self.dealerValue})`""", colour=support.colours.default))
            await support.globalData.addBalance(self.author, self.bet)
        elif self.dealerValue > self.userValue:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
You lost `{self.bet}`$

Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerDeck}
`(Value: {self.dealerValue})`""", colour=support.colours.red))
        elif self.dealerValue < self.userValue:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
You won `{ceil(self.bet/2)}`$

Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerDeck}
`(Value: {self.dealerValue})`""", colour=support.colours.green))
            await support.globalData.addBalance(self.author, self.bet+ceil(self.bet/2))
        await self.on_timeout()
        self.stop()

    @discord.ui.button(label="Resign", style=discord.ButtonStyle.red)
    async def resign(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.on_timeout()
        self.stop()

    async def updateCards(self, interaction):
        self.userDeck, self.userValue = await self.renderCards(self.userCards)
        if self.userValue > 21:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
You lost `{self.bet}`$

Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerDeck}
`(Value: {self.dealerValue})`""", colour=support.colours.red))
            await self.on_timeout()
            self.stop()
        else:
            await interaction.response.edit_message(embed=discord.Embed(
                description=f"""Black Jack
Your Deck: {self.userDeck}
`(Value: {self.userValue})`

Dealers Deck: {self.dealerCards[0][0]}, ?.
`(Value: {self.dealerCards[0][1]})`""", colour=support.colours.default))

    async def renderCards(self, cards):
        return ''.join(f"{card[0]}, " for card in cards)[:-2] + '.', sum([int(card[1]) for card in cards])


class blackjack(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="blackjack", aliases=["bj"])
    async def blackjack(self, ctx, bet):
        current = await support.globalData.getBalance(ctx.message.author)
        if bet.lower() == "max" or bet.lower() == "all":
            bet = current
        else:
            bet = float(bet)

        if current < bet:
            raise ValueError("You don't have enough money")
        elif bet <= 0:
            raise ValueError("Minimum bet value is `1`$.")

        await support.globalData.removebalance(ctx.message.author, bet)
        view = createButtons(self.client, ctx.message.author, bet)

        dealerCards = random.choices(cards, k=2)
        userCards = random.choices(cards, k=2)

        view.dealerCards = dealerCards
        view.userCards = userCards

        view.userDeck, view.userValue = await view.renderCards(userCards)
        view.dealerDeck, view.dealerValue = await view.renderCards(dealerCards)

        message = await ctx.send(embed=discord.Embed(
            description=f"""Black Jack
Your Deck: {view.userDeck}
`(Value: {view.userValue})`

Dealers Deck: {dealerCards[0][0]}, ?.
`(Value: {dealerCards[0][1]})`""",
            colour=support.colours.default
        ), view=view)
        view.message = message


def setup(bot):
    bot.add_cog(blackjack(bot))
