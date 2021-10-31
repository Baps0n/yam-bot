import random
import discord
from discord.ext.commands import Bot
from discord.ext import commands


class YamBot(Bot):
    async def on_ready(self):
        print('Бот работает')


class YamCommands(commands.Cog):
    def __init__(self, bot, yam_client):
        self.bot = bot
        self.yam_client = yam_client

    @commands.command(aliases=['j'])
    async def join(self, ctx, *args):
        voice_channel = ctx.author.voice.channel

        if not ctx.voice_client:
            voice_client = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        await ctx.send(f'Подключен к каналу {voice_channel}')

    @commands.command(aliases=['l'])
    async def leave(self, ctx, *args):
        voice_channel = ctx.author.voice.channel

        await ctx.voice_client.disconnect()
        await ctx.send(f'Отключен от канала {voice_channel}')

    @commands.command(aliases=['p'])
    async def play(self, ctx, *track_input):
        voice_channel = ctx.author.voice.channel
        track_route = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))

        track_input = ' '.join(track_input)
        track_search = self.yam_client.search(track_input, type_='track')['tracks']['results'][0]
        track_search.download(f'music\\{track_route}.mp3', bitrate_in_kbps=192)

        if not ctx.voice_client:
            voice_client = await voice_channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f'music\\{track_route}.mp3'), after=lambda e: print('done', e))

        await ctx.send(f'Воспроизведение {track_search["title"]} от {track_search["artists"][0]["name"]}')