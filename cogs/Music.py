import discord
import lavalink
import re

from discord import utils
from discord.ext import commands

from .utils import utils as ut


url_rx = re.compile(r'https?://(?:www\.)?.+')


class MusicTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(630743566960033802)
        self.bot.music.add_node('127.0.0.1', 7000, 'testing', 'ru', 'music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(name='join')
    async def join(self, ctx):
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        try:

            query = query.strip('<>')

            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            results = await player.node.get_tracks(query)

            if not results or not results['tracks']:
                return await ctx.send('Ничего не найдено...')

            embed = discord.Embed(color=ut.randomColor())

            if results['loadType'] == 'PLAYLIST_LOADED':
                tracks = results['tracks']

                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)

                embed.title = 'Плейлист ...'
                embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} трек'
            else:
                track = results['tracks'][0]
                embed.title = 'Трек...'
                embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

                track = lavalink.models.AudioTrack(track, ctx.author.id)
                player.add(requester=ctx.author.id, track=track)

            await ctx.send(embed=embed)

            # def check(m):
            #     return m.author.id == ctx.author.id
            #
            # response = await self.bot.wait_for('message', check=check)

        except Exception as error:
            print(error)

        if not player.is_playing:
            await player.play()

    @commands.command(name='skip')
    async def skip(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        await player.skip()
        await ctx.send('Скипнул')


def setup(bot):
  bot.add_cog(MusicTest(bot))