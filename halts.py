async def not_moderator(ctx):
    await ctx.channel.send("Must be moderator to use this command.")


async def oopsies(ctx):
    await ctx.channel.send("Chris did an oopsies.")


async def bad_math(ctx):
    await ctx.channel.send("Please enter a valid equation")
