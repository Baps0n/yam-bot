import asyncio
import random
import discord
from discord.ext.commands import Bot
from discord.ext import commands


class YamBot(Bot):
    async def on_ready(self):
        print('Бот работает')

    async def todo(self):
        print('Бот работает')


class YamCommands(commands.Cog):
    def __init__(self, bot, yam_client):
        self.bot = bot
        self.yam_client = yam_client
        self.track_list = []

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
    async def play(self, ctx, *search_input):
        search_input = ' '.join(search_input)
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            voice_client = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        track_search = self.yam_client.search(search_input, type_='track')['tracks']['results']
        album_search = self.yam_client.search(search_input, type_='album')["albums"]["results"]

        if len(track_search) == 0 and len(album_search) == 0:
            track_num = 0
        if len(track_search) > 0:
            track_choose = f'Выберите трек, написав его номер в списке:\n'
            for i in range(min(4, len(track_search))):
                track_choose += f'{i + 1}. {track_search[i]["title"]} от {track_search[i]["artists"][0]["name"]}\n'
            await ctx.send(track_choose)

        if len(album_search) > 0:
            album_choose = f'Выберите альбом, написав его номер в списке:\n'
            for i in range(min(4, len(album_search))):
                print(i, search_input, album_search[i])
                if album_search[i]["artists"]:
                    album_choose += f'{min(4, len(track_search)) + i + 1}. {album_search[i]["title"]} от {album_search[i]["artists"][0]["name"]}, треков: {album_search[i]["track_count"]}\n'
                else:
                    album_choose += f'{min(4, len(track_search)) + i + 1}. {album_search[i]["title"]} от неизвестного исполнителя, треков: {album_search[i]["track_count"]}\n'
            await ctx.send(album_choose)

        msg = await self.bot.wait_for("message")
        track_num = int(msg.content) - 1
        print(msg.content, track_num)

        if track_num < min(4, len(track_search)):
            track_route = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10))
            track_search[track_num].download(f'music\\{track_route}.mp3', bitrate_in_kbps=192)
            track_data = {
                "route": track_route,
                "name": track_search[track_num]["title"],
                "author": track_search[track_num]["artists"][0]["name"]
            }
            self.track_list.append(track_data)
            if ctx.voice_client.is_playing():
                await ctx.send(f'{track_data["name"]} от {track_data["author"]} Добавлен в очередь')

        else:
            album_id = int(album_search[track_num - min(4, len(track_search))]["id"])
            album_tracks = self.yam_client.albums_with_tracks(album_id)["volumes"][0]
            print(album_tracks[0], album_tracks)
            for i in album_tracks:
                track_route = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10))
                i.download(f'music\\{track_route}.mp3', bitrate_in_kbps=192)
                track_data = {
                    "route": track_route,
                    "name": i["title"],
                    "author": i["artists"][0]["name"]
                }
                self.track_list.append(track_data)
            await ctx.send(f'Треков добавлено в очередь: {len(album_tracks)}')

        if not ctx.voice_client.is_playing():
            await self.start_player(ctx)

    async def start_player(self, ctx):
        is_in = 0
        while self.track_list:
            if not ctx.voice_client.is_playing():
                cur_track = self.track_list[0]
                await self.play_track(ctx, cur_track)
                if is_in:
                    self.track_list.pop(0)
            if not is_in:
                self.track_list.pop(0)
            is_in = 1
            await asyncio.sleep(1)

    async def play_track(self, ctx, track):
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f'music\\{track["route"]}.mp3'))
        await ctx.send(f'Воспроизведение {track["name"]} от {track["author"]}')

    @commands.command(aliases=['pl'])
    async def show_play_list(self, ctx):
        show_text = f'Треков в очереди {len(self.track_list)}:\n'
        for i in range(len(self.track_list)):
            show_text += f'{i + 1}. {self.track_list[i]["name"]} от {self.track_list[i]["author"]}\n'

    @commands.command(aliases=['s'])
    async def stop(self, ctx, *track_input):
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            voice_client = await voice_channel.connect()

        ctx.voice_client.stop()
        await ctx.send(f'Воспроизведение остановлено')
