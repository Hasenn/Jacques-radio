#!/usr/bin/env python3
import discord
from discord.ext import commands
import youtube_dl
import os
import asyncio
#local imports
import urlparser



TOKEN = os.environ['JQ_TOKEN']

description = "Radio Jacques"
bot = commands.Bot(command_prefix="!", description=description)

voice_clients = {}

@bot.event
async def on_ready():
    print("Let's roll !")
    activity = discord.CustomActivity(name="Ma femme est un homme politique")
    await bot.change_presence(activity = activity)

""" @bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"```{str(error)}```")
 """
async def recover():
    """
    In case we crashed and still have voice clients,
    recover them and store them in our dictionnary
    """
    for client in bot.voice_clients:
        voice_clients[channel.guild.id] = client

@bot.command(pass_context=True)
async def join(ctx):
    await recover()
    channel = ctx.message.author.voice.channel
    guild = ctx.message.guild
    voice_clients[guild.id] = await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    guild = ctx.message.guild
    vc = voice_clients.pop(guild.id)
    vc.disconnect()

@bot.command(pass_context=True)
async def play(ctx,url=""):
    guild = ctx.message.guild
    if not(guild.id in voice_clients):
        await join(ctx)
    vc = voice_clients[guild.id]
    source = await urlparser.parse(url, bot)
    await ctx.send("Bernadette ?! Envoie la musique !")
    vc.play(source)

@bot.command(pass_context=True)
async def stop(ctx):
    guild = ctx.message.guild
    vc = voice_clients[guild.id]
@stop.error
@leave.error
async def stop_error(ctx, error):
    if isinstance(error, KeyError):
        await ext.send("Not in a voice channel")



@bot.command(pass_context=True)
async def push(ctx,url,playlist):
    pass

@bot.command(pass_context=True)
async def pop(ctx):
    pass


bot.run(TOKEN)