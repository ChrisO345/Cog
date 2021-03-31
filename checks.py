def is_mod(ctx):  # Checks if message author is mod
    return ctx.author.guild_permissions.administrator


def is_member(ctx, peoples):  # Checks is member matches that in people array
    if ctx.author.id in peoples:
        return True
    return False


def has_role(ctx, role):
    if any(r.name == role for r in ctx.author.roles):
        return True
    return False
