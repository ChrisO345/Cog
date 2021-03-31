import discord
from discord.ext import commands
from discord.utils import get

from time import sleep

import pi
import halts
import checks

client = commands.Bot(command_prefix="c.")
cool_peoples = [531487237842665483, 285356466905415680, 668957085882384398]
cool_indices = ["Myth",             "CJ",               "Chris"]


@client.event
async def on_ready():
    print("Bot is Ready")

    await client.change_presence(status=discord.Status.online)


@client.event
async def on_message(ctx: discord.Message):
    if str(ctx.content).startswith("τ"):
        await pi.get_tau(ctx)
    if str(ctx.content).startswith("π"):
        await pi.get_pi(ctx)
    if str(ctx.content).lower() in ["its", "it's"]:
        await ctx.channel.send("it's brittany bitch :hot_face:")
    if "brodie" in str(ctx.content).lower():
        if not checks.has_role(ctx, "Bots"):
            await ctx.channel.send("ew ugly bitch brodie :face_vomiting:")
    await client.process_commands(ctx)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await halts.not_moderator(ctx)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await halts.oopsies(ctx)


@client.command()
@commands.check(checks.is_mod)
async def clear(ctx: discord.Message, amount=5):
    amount += 1
    await ctx.channel.purge(limit=amount)


@client.command(aliases=["cj"])
async def luv(ctx):
    await ctx.channel.send(":heart: luv you Aerin :heart:")


@client.command()
async def secret_command(ctx, ping=False):
    if checks.is_mod(ctx) or checks.is_member(ctx, cool_peoples):
        if ping:
            await ctx.channel.send(f"All Hail <@!531487237842665483>")
        else:
            await ctx.channel.send(f"All Hail MrMythicorn")
    else:
        await ctx.channel.send(f"All Hail MrMythicorn")


@client.command()
async def timer(ctx, sec=5):
    channel = ctx.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    voice.play(discord.FFmpegPCMAudio('Alarm.mp3'), after=print("Done"))
    voice.pause()

    try:
        sec = int(sec)
    except ValueError:
        await ctx.channel.send("Type Error Received. Please make sure the following information is a string")
        return

    sleep(sec)
    await ctx.channel.send(f"The {sec} second timer has finished!")
    voice.resume()

    while voice.is_playing():
        sleep(1)

    voice.stop()
    await voice.disconnect()


@client.command()
async def ghost(ctx, member: discord.Member, *, amount=3):
    await ctx.channel.last_message.delete()
    for i in range(amount):
        await ctx.channel.send(f"<@!{member.id}>")
        await ctx.channel.last_message.delete()


@client.command(aliases=["jerry"])
async def yigga(ctx):
    await ctx.channel.send(":heart: jerry is the best :heart:")


@client.command()
async def chris(ctx, other_stuff=""):
    if other_stuff == "github":
        await ctx.channel.send(r"https://github.com/chrisoliver345")
    else:
        await ctx.channel.send("My Daddy is the bestest person ever")

client.run(open(r"../cog_token.txt", "r").read())
