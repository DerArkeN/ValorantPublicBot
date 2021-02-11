from discord.utils import get
from ValorantBot.util import methods, sql


async def rank(ctx, rank, bot):
    dcUser = ctx.author

    if any(ext in rank for ext in methods.valid_roles):
        role = get(dcUser.guild.roles, name=rank)

        if sql.user_exists(dcUser.id):
            await methods.set_rank(ctx, dcUser, role)
            await ctx.send("Your Rank has been updated.")
        else:
            await ctx.send("You have to register first.")
    else:
        await ctx.send("You can't give yourself this role.")
