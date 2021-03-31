import discord
from math import pi, tau


async def get_tau(ctx):
    digits = ctx.content[1::].split()
    while "" in digits:
        digits.remove("")
    if len(digits) > 0:
        digits = digits[0]
    else:
        digits = 5
    if not digits:
        return
    tau_: str = str(tau)
    try:
        digits = int(digits) + 1
    except ValueError:
        await ctx.channel.send("In order to round, arguments must be numbers.")
    else:
        if digits == 0:
            await ctx.channel.send("6")
        elif 0 < digits <= 15:
            await ctx.channel.send(f"{tau_[0:digits + 1]}")
        else:
            await ctx.channel.send(f"Rounding values must be between 0 and 14 inclusive.")


async def get_pi(ctx):
    digits = ctx.content[1::].split()
    while "" in digits:
        digits.remove("")
    if len(digits) > 0:
        digits = digits[0]
    else:
        digits = 5
    if not digits:
        return
    pi_: str = str(pi)
    try:
        digits = int(digits) + 1
    except ValueError:
        await ctx.channel.send("In order to round, arguments must be numbers.")
    else:
        if digits == 0:
            await ctx.channel.send("6")
        elif 0 < digits <= 15:
            await ctx.channel.send(f"{pi_[0:digits + 1]}")
        else:
            await ctx.channel.send(f"Rounding values must be between 0 and 14 inclusive.")