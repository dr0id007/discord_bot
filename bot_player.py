import discord
from discord.ext.commands import Bot
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = Bot(command_prefix='#')
token = os.getenv('TOKEN')  # replace this with token
voice = None
song_list = []


@client.event
async def on_ready():
    print("-------Bot is ready -------")


@client.command()
async def greet(ctx):
    await ctx.channel.send('hello world..')


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    global voice
    voice = await channel.connect()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'ac12.mp3',
    'noplaylist': 'True',

}


playing = False


async def play_list(ctx, song_list):
    print(song_list)
    if ctx.voice_client.is_playing() == True:
        await play_list(ctx, song_list)
    elif(len(song_list) > 0):
        os.system('youtube-dl ytsearch:'+song_list.pop(-1) +
                  ' --max-downloads 1 --no-playlist --no-part -x -o "bbb.mp3"')
        source = FFmpegPCMAudio('bbb.opus')
        player = await ctx.voice_client.play(source)
        await player.start()


async def play_next(ctx, song_list, client):
    asyncio.run_coroutine_threadsafe(
        play_list(ctx, song_list), client.loop)


async def loop():
    while True:
        print()

        await asyncio.sleep(3)

client.loop.create_task(loop())


@client.command()
async def sound(ctx, *args):
    if args[0] is None:
        await ctx.channel.send("no song specified..")

    if ctx.voice_client is None:
        await ctx.channel.send("Connect to audio channel first")
    else:
        # if ctx.voice_client is not None:
        #     ctx.voice_client.stop()
        if os.path.exists('ac12.mp3'):
            os.remove('ac12.mp3')
        if len(args) > 1:
            search = args[0] + args[1]
        else:
            search = args[0]
        song_list.append(search)
        await ctx.channel.send(search + " added to list")
        some = ctx.voice_client.is_playing()
        await play_next(ctx, song_list, client)


@client.command()
async def pause(ctx):
    playing = False
    ctx.voice_client.pause()


@client.command()
async def resume(ctx):
    playing = True
    ctx.voice_client.resume()


@client.command()
async def stop(ctx):
    playing = False
    ctx.voice_client.stop()


@client.command()
async def check(ctx):
    some = ctx.voice_client.is_playing()
    print("some:-", some)
    await ctx.channel.send(some)


client.run(token)
