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

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
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
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        await ctx.send(embed=discord.Embed(
            description=f'Added `{data["title"]}` to queue.', color=support.colours.default
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
        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
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
                            description='There was an error processing your song. Try Again',
                            color=support.colours.default,
                        )
                    )

                    continue

            source.volume = self.volume
            self.current = source
            self._guild.voice_client.play(
                source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(embed=discord.Embed(
                description=f'Now Playing: `{source.title}`', color=support.colours.default
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

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Plays Music in current Voice Channel")
    async def play(self, ctx, *, url):
        async with ctx.typing():
            vc = ctx.voice_client
            if not vc:
                await ctx.invoke(self.connect)
            player = self.get_player(ctx)
            source = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)
            await player.queue.put(source)

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['np', 'current', 'currentsong', 'playing'], description="Sends currently playing song")
    async def now_playing(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(
                    description='Im Not Playing Anything!.', color=support.colours.default
                ), delete_after=10, )

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(
                embed=discord.Embed(
                    description='Im Not Playing Anything!', color=support.colours.default
                ), delete_after=10, )

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(embed=discord.Embed(
            description=f"Now Playing: {vc.source.title}",
            color=support.colours.default
        ))

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Skips current song")
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(
                    description='Im Not Playing Anything!', color=support.colours.default
                ), delete_after=10, )
        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        vc.stop()
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author} Skipped Current Song!', color=support.colours.default
        ))

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['vol'], description="Sets Music volume")
    async def volume(self, ctx, *, vol: float):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(
                    description='Im Not Playing Anything!', color=support.colours.default
                ), delete_after=10, )

        if not 0 < vol < 101:
            return await ctx.send(
                embed=discord.Embed(
                    description='Choose Value between 0.00/100.00',
                    color=support.colours.default,
                ), delete_after=10, )

        player = self.get_player(ctx)
        if vc.source:
            vc.source.volume = vol / 100
        player.volume = vol / 100
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author} Changed Volume to `{vol}%`', color=support.colours.default
        ))

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="Stops playing music")
    async def stop(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(
                embed=discord.Embed(
                    description='Im Not Playing Anything!', color=support.colours.default
                ), delete_after=10, )
        await self.cleanup(ctx.guild)

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=['join'], description="Connects to current voice channel")
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(
                    'No channel to join. Please either specify a valid channel or join one.')
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(
                    f'Connecting to channel: <{channel}> timed out.')
        await ctx.send(embed=discord.Embed(
            description=f'Connected to `{channel}`.', color=support.colours.default
        ), delete_after=10)


def setup(bot):
    bot.add_cog(Music(bot))
