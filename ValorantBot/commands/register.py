from discord.utils import get
from ValorantBot.util import methods, sql


async def register(ctx, name, rank, vclient, bot):
    try:
        valUser = vclient.get_user(name, "name")
        valTag = valUser.__getattribute__("tagLine")
        valName = valUser.__getattribute__("gameName")
        valPUUID = valUser.__getattribute__("puuid")
    except:
        await ctx.send("There was an error with the Riot API (Check your Name and Tag)")
        return

    dcUser = ctx.author

    if any(ext in rank for ext in methods.valid_roles):
        role = get(dcUser.guild.roles, name=rank)

        reg = sql.insert_userdata(dcUser.id, valPUUID, valName, valTag, role)
        if reg:
            try:
                await dcUser.edit(nick=valName + "#" + valTag)
            except:
                await ctx.send("There was an error setting your Username.")
            await methods.set_rank(ctx, dcUser, role)
            await ctx.send("Your Nickname was set to your Valorant Name and your Rank has been updated.")
        else:
            await ctx.send("You are already registered.")
    else:
        await ctx.send("You can't give yourself this role.")
