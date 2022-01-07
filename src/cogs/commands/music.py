"""
Music Command
~~~~~~~~~~~~~~~~~
Plays Music

:copyright: (c) 2021-2021 M2rsho
:license: MIT, see LICENSE for more details.

"""

from cogs import errors
import datetime
from cogs import checks
from discord.commands import Option
from run import client
import asyncio
from sqlite3.dbapi2 import Error
import discord
import yt_dlp as youtube_dl
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


class queueButtons(discord.ui.View):
    def __init__(self, client, author, guild, queue, playing):
        super().__init__(timeout=20)
        self.client = client
        self.page = 0
        self.author = author
        self.message = None

        self.lang = support.getLanguageFileG(guild)
        titles = [
            f"{queue.index(item)+1}. [{item.title}]({item.original_url})" for item in queue]
        titles.insert(
            0, f"Now Playing [{playing.title}]({playing.original_url})\n")

        self.queue = []
        n = 10
        for index in range(0, len(titles), n):
            page = ''.join(f"{item}\n" for item in titles[index: index + n])
            self.queue.append(page)

        self.maxPages = int(len(self.queue)) - 1

    async def on_timeout(self) -> None:
        self.back.disabled = True
        self.stop_button.disabled = True
        self.forward.disabled = True
        self.home.disabled = True
        self.end.disabled = True
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
            title="Queue",
            description=f"""
[{self.lang['website']}](https://py-bot.cf/) | [{self.lang['command']}](https://py-bot.cf/commands) | [{self.lang['discord']}](https://discord.gg/dfKMTx9Eea)

{self.queue[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"{self.lang['page']}: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label="<", style=discord.ButtonStyle.grey)
    async def back(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.page -= 1 if self.page > 0 else 0
        await interaction.response.edit_message(embed=discord.Embed(
            title="Queue",
            description=f"""
[{self.lang['website']}](https://py-bot.cf/) | [{self.lang['command']}](https://py-bot.cf/commands) | [{self.lang['discord']}](https://discord.gg/dfKMTx9Eea)

{self.queue[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"{self.lang['page']}: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label="⬜", style=discord.ButtonStyle.grey)
    async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.back.disabled = True
        self.stop_button.disabled = True
        self.forward.disabled = True
        self.home.disabled = True
        self.end.disabled = True
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
            title="Queue",
            description=f"""
[{self.lang['website']}](https://py-bot.cf/) | [{self.lang['command']}](https://py-bot.cf/commands) | [{self.lang['discord']}](https://discord.gg/dfKMTx9Eea)

{self.queue[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"{self.lang['page']}: {self.page+1}/{self.maxPages+1}"))

    @discord.ui.button(label=">>", style=discord.ButtonStyle.grey)
    async def end(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(self.lang["notYourMenu"], ephemeral=True)
            return
        self.page = self.maxPages
        await interaction.response.edit_message(embed=discord.Embed(
            title="Queue",
            description=f"""
[{self.lang['website']}](https://py-bot.cf/) | [{self.lang['command']}](https://py-bot.cf/commands) | [{self.lang['discord']}](https://discord.gg/dfKMTx9Eea)

{self.queue[self.page]}""",
            color=support.colours.default
        ).set_footer(text=f"{self.lang['page']}: {self.page+1}/{self.maxPages+1}"))


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.uploader = data.get('Uploader') or "Unknown"
        try:
            self.uploader_url = data.get('uploader_url')
            if self.uploader_url is None:
                raise
        except:
            self.uploader_url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
        try:
            self.thumbnail = data.get('thumbnail')
            if self.thumbnail is None:
                raise
        except:
            self.thumbnail = "https://i.ytimg.com/vi_webp/dQw4w9WgXcQ/maxresdefault.webp"
        self.duration = data.get('duration') or "Unknown"
        try:
            self.views = f"{data.get('view_count'):,}"
        except:
            self.views = "Unknown"
        try:
            self.likes = f"{data.get('like_count'):,}"
        except:
            self.likes = "Unknown"
        self.original_url = data.get('original_url') or "Unknown"
        self.date = data.get('upload_date') or "Unknown"
        self.date = datetime.datetime.strptime(
            self.date, "%Y%m%d") or "Unknown"
        try:
            self.timedelta = datetime.timedelta(seconds=data.get('duration'))
        except:
            self.timedelta = "Unknown"

    @classmethod
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        lang = support.getLanguageFileG(ctx.guild)
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        try:
            date = data.get('upload_date')
            date = datetime.datetime.strptime(date, "%Y%m%d")
            date = f'{date.year} {date.strftime("%B")} {date.day}'
            timedelta = datetime.timedelta(seconds=data.get('duration'))
        except:
            date = "Unknown"
            timedelta = "Unknown"
        try:
            views = f"{data.get('view_count'):,}"
        except:
            views = "Unknown"
        try:
            likes = f"{data.get('like_count'):,}"
        except:
            likes = "Unknown"
        try:
            uploader = data.get('uploader')
        except:
            uploader = "Unknown"
        try:
            uploader_url = data.get('uploader_url')
            if uploader_url is None:
                raise
        except:
            uploader_url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
        try:
            thumbnail = data.get('thumbnail')
            if thumbnail is None:
                raise
        except:
            thumbnail = "https://i.ytimg.com/vi_webp/dQw4w9WgXcQ/maxresdefault.webp"
        await ctx.send(mention_author=False, embed=discord.Embed(
            title=lang["commands"]["play"]["returnSuccess"].format(
                title=data.get('title')),
            url=data.get('original_url'),
            color=support.colours.default,
            description=f"""
Duration: {timedelta}
Views: {views}
Likes: {likes}
Upload Date: {date}
                """
        ).set_thumbnail(url=thumbnail).set_author(name=uploader, url=uploader_url), delete_after=30)
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
        self.volume = 1
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
            try:
                self._guild.voice_client.play(
                    source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except:
                self.destroy(self._guild)
                raise errors.UnknownError("Unknown Error Occured")
            self.np = await self._channel.send(embed=discord.Embed(
                title=lang["commands"]["now_playing"]["returnSuccess"].format(
                    title=source.title),
                url=source.original_url,
                color=support.colours.default,
                description=f"""
Duration: {source.timedelta}
Views: {source.views}
Likes: {source.likes}
Upload Date: {source.date.year} {source.date.strftime("%B")} {source.date.day}
                """
            ).set_thumbnail(url=source.thumbnail).set_author(name=source.uploader, url=source.uploader_url))
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
            if not ctx.author.voice:
                raise errors.NotInVoiceChannel()
            vc = ctx.voice_client
            if not vc:
                await ctx.invoke(self.connect)
            player = self.get_player(ctx)
            try:
                async with timeout(10):
                    source = await YTDLSource.from_url(ctx, url, loop=self.bot.loop, stream=True)
                    await player.queue.put(source)
            except asyncio.TimeoutError:
                raise TimeoutError("Command timed out.")

    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.next.description")
    async def queue(self, ctx):
        async with ctx.typing():
            player = self.get_player(ctx)
            source = player.queue
            if list(source._queue) == [] and player.current == None:
                raise errors.EmptyQueue("Queue is empty")
            view = queueButtons(self.bot, ctx.author,
                                ctx.guild, source._queue, player.current)
            lang = view.lang
            message = await ctx.reply(mention_author=False, embed=discord.Embed(
                title="Queue",
                description=f"""
[{lang["website"]}](https://py-bot.cf/) | [{lang["command"]}](https://py-bot.cf/commands) | [{lang["discord"]}](https://discord.gg/dfKMTx9Eea)

{view.queue[view.page]}""",
                color=support.colours.default
            ).set_footer(text=f'{lang["page"]}: {view.page+1}/{view.maxPages+1}'), view=view)
            view.message = message

    @checks.default()
    @client.slash_command(description="commands.play.description")
    async def play(
        self,
        ctx,
        name: Option(str, "Url/Name"),
    ):
        if not ctx.author.voice:
            raise errors.NotInVoiceChannel()
        lang = support.getLanguageFileG(ctx.guild)
        await ctx.response.send_message(embed=discord.Embed(description="Playing...", color=support.colours.default), ephemeral=True)
        async with ctx.typing():
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            player = self.get_player(ctx)
            try:
                async with timeout(10):
                    source = await YTDLSource.from_url(ctx, name, loop=self.bot.loop, stream=True)
                    await player.queue.put(source)
            except asyncio.TimeoutError:
                raise TimeoutError("Command timed out.")

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
            description=lang["commands"]["now_playing"]["returnSuccess"].format(
                title=vc.source.title),
            color=support.colours.default
        ))

    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(description="commands.skip.description")
    async def skip(self, ctx):
        if not ctx.author.voice:
            raise errors.NotInVoiceChannel()
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
        if not ctx.author.voice:
            raise errors.NotInVoiceChannel()

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
        if not ctx.author.voice:
            raise errors.NotInVoiceChannel()
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
                raise errors.InvalidVoiceChannel(
                    lang["errors"]["InvalidVoiceChannel"])
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise errors.VoiceConnectionError(
                    lang["commands"]["connect"]["timedout"].format(channel=channel.mention))
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise errors.VoiceConnectionError(
                    lang["commands"]["connect"]["timedout"].format(channel=channel.mention))
        await ctx.reply(mention_author=False, embed=discord.Embed(
            description=lang["commands"]["connect"]["returnSuccess"].format(channel=channel.mention), color=support.colours.default
        ), delete_after=10)


def setup(bot):
    bot.add_cog(Music(bot))
