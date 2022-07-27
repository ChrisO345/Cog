import discord
from discord.ext import commands
from discord.utils import get

from time import sleep, perf_counter
from random import choice, randrange

import pi
import halts
import checks
import info
import black_jack

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="|", intents=intents)


# Client Events.
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
        if not checks.has_role(ctx, "cog"):
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


# Useful Commands
@client.command(aliases=["clear"])
@commands.check(checks.is_mod)
async def purge(ctx: discord.Message, amount=5):
    amount += 1
    await ctx.channel.purge(limit=amount)


@client.command()
async def timer(ctx, sec=5):
    start = perf_counter()
    channel = ctx.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    voice.play(discord.FFmpegPCMAudio('Alarm.mp3'))
    voice.pause()

    try:
        sec = int(sec)
    except ValueError:
        await ctx.channel.send("Type Error Received. Please make sure the following information is a integer")
        return
    end = perf_counter()
    duration = float(f"{end - start:0.1f}")
    print(duration)
    sec_ = sec - duration
    print(sec)
    print(sec_)
    sleep(sec_)
    await ctx.channel.send(f"The {sec} second timer has finished!")
    voice.resume()

    while voice.is_playing():
        sleep(1)
    voice.stop()
    await voice.disconnect()


@client.command()
async def poll(ctx, *, terms):
    if checks.cool_person(ctx):
        print("yes")
        terms = terms.split("/")
        author = ctx.author
        poll_embed = discord.Embed(
            title=terms[0].title()
        )
        poll_embed.set_author(name=author.display_name, icon_url=author.avatar_url)

        if len(terms) < 3:
            pass
        else:
            poll_embed.add_field(name=terms[1].capitalize(), value="Select :one: to choose", inline=True)
            poll_embed.add_field(name=terms[2].capitalize(), value="Select :two: to choose", inline=True)

            await ctx.channel.send(embed=poll_embed)
            sleep(1)
            await ctx.channel.last_message.add_reaction("1️⃣")
            await ctx.channel.last_message.add_reaction("2️⃣")


@client.command(aliases=[])
async def evaluate(ctx, *, equation=""):
    if equation != "":
        if {"+", "-", "*", "/", "^"}.intersection(list(equation)):
            for item in list(equation):
                if item.isalpha():
                    await halts.bad_math(ctx)
                    return
            equation = equation.replace("=", "")
            eq = equation
            equation = equation.replace(" ", "")
            equation = equation.replace("^", "**")
            x = eval(equation)
            await ctx.channel.send(f"{eq}={x}")
        else:
            await halts.bad_math(ctx)
    else:
        await halts.bad_math(ctx)


# Fun Stuff
@client.command()
async def ghost(ctx, member: discord.Member, *, amount=3):
    if checks.is_owner(ctx):
        await ctx.channel.last_message.delete()
        for i in range(amount):
            await ctx.channel.send(f"<@!{member.id}>")
            await ctx.channel.last_message.delete()
    else:
        await halts.not_moderator(ctx)


@client.command()
async def dm(ctx, user="", *, message=""):
    await ctx.channel.last_message.delete()
    if user != "":
        for person in ctx.channel.members:
            person: discord.User = person
            if user.lower() == person.name.lower() or user.lower() == person.display_name.lower():
                await person.send(message)


@client.command(aliases=["bj"])
async def blackjack(ctx):
    black_jack.main(ctx)
    pass


@client.command(aliases=["flip", "coin"])
async def coinflip(ctx):
    await ctx.channel.send(choice(["Heads", "Tails"]))


@client.command()
async def slots(ctx):
    icons = "A B C D E F G".split()
    i1, i2, i3 = icons[randrange(0, len(icons))], icons[randrange(0, len(icons))], icons[randrange(0, len(icons))]
    if i1 == i2 and i1 == i3:
        await ctx.channel.send(f"| {i1} | {i2} | {i3} | WON 100")
    elif i1 == i2 or i2 == i3:
        await ctx.channel.send(f"| {i1} | {i2} | {i3} | WON 50")
    else:
        await ctx.channel.send(f"| {i1} | {i2} | {i3} | LOST")


# Game Util
@client.command()
async def shut(ctx, user="", *, p="True"):
    if p.lower() in ["no", "n", "0", "nope", "false"]:
        p = False
    else:
        p = True
    if user != "":
        for person in ctx.channel.members:
            person: discord.Member = person
            if user.lower() == person.name.lower() or user.lower() == person.display_name.lower():
                await person.edit(deafen=p, mute=p)
                break
            else:
                x = checks.is_bois(ctx, user.lower())
                if person.id == x:
                    await person.edit(deafen=p, mute=p)
                    break


# About
@client.command()
async def chris(ctx, other_stuff=""):
    if other_stuff == "github":
        await ctx.channel.send(r"https://github.com/chriso345")
    else:
        await ctx.channel.send("My Daddy is the bestest person ever")


@client.command()
async def about(ctx, person=None):
    if person is None:
        await ctx.channel.send(info.bot_info())
    else:
        try:
            func = getattr(info, person.lower())
        except AttributeError:
            func = info.handler(person)
        if func is not None:
            await ctx.channel.send(func())


# Management and tools stuff.
@client.command()
async def embed_test(ctx):
    if checks.is_owner(ctx):
        embed = discord.Embed(
            title="Title",
            description="Description",
            colour=discord.Colour.blue()
        )

        embed.set_footer(text='This is a footer')
        embed.set_image(url="https://github.com/chrisoliver345/Cog/blob/main/cog.png?raw=true")
        embed.set_thumbnail(url="https://github.com/chrisoliver345/Cog/blob/main/cog.png?raw=true")
        embed.set_author(name="Author", icon_url="https://github.com/chrisoliver345/Cog/blob/main/cog.png?raw=true")
        embed.add_field(name="Field Name 1", value="Field Value 1", inline=False)
        embed.add_field(name="Field Name 2", value="Field Value 2", inline=True)
        embed.add_field(name="Field Name 3", value="Field Value 3", inline=True)

        await ctx.channel.send(embed=embed)


client.run(open(r"../cog_token.txt", "r").read())
