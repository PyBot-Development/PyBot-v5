"""
Music Command
~~~~~~~~~~~~~~~~~
Plays Music

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

import asyncio
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
import support
from discord.ext.commands import cooldown, BucketType
youtube_dl.utils.bug_reports_message = lambda: ''
from run import client
from discord.commands import Option
from cogs import checks

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        lang = support.getLanguageFileG(ctx.guild)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["play"]["returnSuccess"]
            .format(title=data["title"]),
            color=support.colours.default
        ), delete_after=10)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        ctx.bot.loop.create_task(self.player_loop(ctx))

    async def player_loop(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(
                        embed=discord.Embed(
                            description=lang["errors"]["songProcessing"],
                            color=support.colours.default,
                        )
                    )

                    continue

            source.volume = self.volume
            self.current = source
            self._guild.voice_client.play(
                source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(embed=discord.Embed(
                description=lang["commands"]["now_playing"]["returnSuccess"].format(title=source.title), color=support.colours.default
            ))
            await self.next.wait()
            source.cleanup()
            self.current = None
            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass
        try:
            del self.players[guild.id]
        except KeyError:
            pass

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.play.description", name="play")
    async def play_music(self, ctx, *, url):
        async with ctx.typing():
            vc = ctx.voice_client
            if not vc:
                await ctx.invoke(self.connect)
            player = self.get_player(ctx)
            try:
                async with timeout(10):
                    source = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)
                    await player.queue.put(source)
            except asyncio.TimeoutError:
                raise commands.TimeoutError("Command timed out.")

    # @cooldown(1, support.cooldown, BucketType.user)
    # @commands.command(description="Plays Music in current Voice Channel")
    # async def queue(self, ctx):
    #     async with ctx.typing():
    #         player = self.get_player(ctx)
    #         queue = await player.queue.get()
    #         print(queue)
    #         await ctx.send(queue)
    @checks.default()
    @client.slash_command(description="commands.play.description")
    async def play(
        self,
        ctx,
        name: Option(str, "Url/Name"),
    ):
        lang = support.getLanguageFileG(ctx.guild)
        await ctx.response.send_message(embed=discord.Embed(description="Playing...", color=support.colours.default), ephemeral=True)
        async with ctx.typing():
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                vc = await voice_channel.connect()
            player = self.get_player(ctx)
            try:
                async with timeout(10):
                    source = await YTDLSource.from_url(ctx, name, loop=self.bot.loop, stream=True)
                    await player.queue.put(source)
            except asyncio.TimeoutError:
                raise commands.TimeoutError("Command timed out.")
            source = await YTDLSource.from_url(ctx, name, loop=self.bot.loop, stream=True)
            await player.queue.put(source)
            
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['np', 'current', 'currentsong', 'playing'], description="commands.now_playing.description")
    async def now_playing(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["now_playing"]["notPlayingAnything"], color=support.colours.default
                ), delete_after=10, )

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["now_playing"]["notPlayingAnything"], color=support.colours.default
                ), delete_after=10, )

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["now_playing"]["returnSuccess"].format(title=vc.source.title),
            color=support.colours.default
        ))
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.skip.description")
    async def skip(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["now_playing"]["notPlayingAnything"], color=support.colours.default
                ), delete_after=10, )
        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        vc.stop()
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["skip"]["returnSuccess"].format(user=ctx.author), color=support.colours.default
        ))
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['vol'], description="commands.volume.description")
    async def volume(self, ctx, *, vol: float):
        lang = support.getLanguageFileG(ctx.guild)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["now_playing"]["notPlayingAnything"], color=support.colours.default
                ), delete_after=10, )

        if not 0 <= vol < 101:
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["volume"]["badValue"],
                    color=support.colours.default,
                ), delete_after=10, )

        player = self.get_player(ctx)
        if vc.source:
            vc.source.volume = vol / 100
        player.volume = vol / 100
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["volume"]["returnSuccess"].format(user=ctx.author, vol=vol), color=support.colours.default
        ))
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.stop.description")
    async def stop(self, ctx):
        lang = support.getLanguageFileG(ctx.guild)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply(mention_author=False, 
                embed=discord.Embed(
                    description=lang["commands"]["now_playing"]["notPlayingAnything"], color=support.colours.default
                ), delete_after=10, )
        await self.cleanup(ctx.guild)

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['join'], description="commands.connect.description")
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        lang = support.getLanguageFileG(ctx.guild)
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(
                    lang["errors"]["InvalidVoiceChannel"])
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    lang["commands"]["connect"]["timedout"].format(channel=channel.mention))
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    lang["commands"]["connect"]["timedout"].format(channel=channel.mention))
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["connect"]["returnSuccess"].format(channel=channel.mention), color=support.colours.default
        ), delete_after=10)


def setup(bot):
    bot.add_cog(Music(bot))
