owner = 668957085882384398

special_peoples = [700949769224454186]
special_indices = ["Gy"]

cool_peoples = [531487237842665483, 285356466905415680, 668957085882384398]
cool_indices = ["Myth",             "CJ",               "Chris"]

bois = {"chris chriso chriso345": 668957085882384398,
        "dan dantheman daniel danman danthe danny": 656944638267228170,
        "logan yogi yogy donald": 683830932708655178,
        "jerry yigga": 346183365868781568,
        "james unrealistic jam": 259547691258740737}


def is_owner(ctx):
    global owner
    return ctx.author.id == owner


def is_mod(ctx):  # Checks if message author is mod
    if is_owner(ctx):
        return True
    return ctx.author.guild_permissions.administrator


def is_member(ctx, peoples):  # Checks is member matches that in people array
    if ctx.author.id in peoples:
        return True
    return False


def has_role(ctx, role):
    if any(r.name == role for r in ctx.author.roles):
        return True
    return False


def cool_person(ctx):
    if is_mod(ctx):
        return True
    if is_member(ctx, cool_peoples):
        return True


def is_bois(ctx, name):
    for names in bois.keys():
        if name in names.split():
            return bois.get(names)
    return False
