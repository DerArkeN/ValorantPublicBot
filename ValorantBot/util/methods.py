import numpy
from discord.utils import get
from ValorantBot.util import sql

valid_roles = ["Iron 1", "Iron 2", "Iron 3",
               "Bronze 1", "Bronze 2", "Bronze 3",
               "Silver 1", "Silver 2", "Silver 3",
               "Gold 1", "Gold 2", "Gold 3",
               "Platinum 1", "Platinum 2", "Platinum 3",
               "Diamond 1", "Diamond 2", "Diamond 3",
               "Immortal",
               "Radiant",
               ]

unvalid_roles = ["Administrator",
                 "Moderator"]

lft_data = dict()


def get_executor(msg_or_channel):
    value = lft_data[msg_or_channel.id]
    return value[0]


def get_msg(executor_or_channel):
    value = lft_data[executor_or_channel.id]
    return value[1]


def get_channel(executor_or_msg):
    value = lft_data[executor_or_msg.id]
    return value[2]


async def set_lft(executor, bot):
    channel = executor.voice.channel
    lft_channel = bot.get_channel(806109172336689162)
    user_role = await get_rank(executor)

    await channel.set_permissions(get(executor.guild.roles, id=806081402407092295), connect=False)
    await channel.edit(name="Looking for mates", user_limit=5)
    print(channel.name)
    msg = await lft_channel.send(
        content=executor.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
            len(executor.voice.channel.members)) + "/5 player in the channel.",
        delete_after=900)
    await msg.add_reaction('✅')
    lft_data[executor.id] = ["placeholder", msg, channel]
    lft_data[msg.id] = [executor, "placeholder", channel]
    lft_data[channel.id] = [executor, msg, "placeholder"]


async def set_closed(channel):
    executor = get_executor(channel)
    msg = get_msg(channel)

    await channel.set_permissions(get(executor.guild.roles, id=806081402407092295), connect=False)
    await msg.delete()
    await channel.edit(name="Playing", user_limit=5)
    del lft_data[msg.id]
    del lft_data[channel.id]
    del lft_data[executor.id]


async def set_casual(channel):
    msg = get_msg(channel)
    executor = get_executor(channel)

    await msg.delete()
    if len(channel.members) != 0:
        await channel.set_permissions(get(executor.guild.roles, id=806081402407092295), connect=True)
        await channel.edit(name=channel.members[0].nick + "'s channel", limit=0)
    del lft_data[msg.id]
    del lft_data[channel.id]
    del lft_data[executor.id]


async def get_rank(dcUser):
    roles_ROLES = dcUser.roles
    roles_NAME = [roles_ROLE.name for roles_ROLE in roles_ROLES]
    roles_NAME_filtered = numpy.setdiff1d(roles_NAME, unvalid_roles)
    roles_NAME_filtered = roles_NAME_filtered.tolist()
    roles_NAME_filtered.remove("@everyone")

    if roles_NAME_filtered:
        role = get(dcUser.guild.roles, name=roles_NAME_filtered[0])
        return role
    return False


def get_valid_roles(guild):
    roles = [get(guild.roles, name=role_name) for role_name in valid_roles]
    return roles


async def set_rank(dcUser, rank):
    old_roles_ROLES = dcUser.roles
    old_roles_NAME = []
    for old_roles_ROLE in old_roles_ROLES:
        old_roles_NAME += [old_roles_ROLE.name]

    old_roles_NAME_filtered = numpy.setdiff1d(old_roles_NAME, valid_roles)
    old_roles_NAME_filtered = old_roles_NAME_filtered.tolist()
    old_roles_NAME_filtered.remove("@everyone")

    await dcUser.edit(roles=[])
    await dcUser.add_roles(rank)

    sql.update_rank(dcUser.id, rank)

    for i in old_roles_NAME_filtered:
        await dcUser.add_roles(get(dcUser.guild.roles, name=i))


async def check_profile(member, vclient):
    if await get_rank(member) is not False:
        if member.nick is not None:
            if not member.bot:
                if sql.user_exists(member.id):
                    valPUUID = sql.get_puuid(member.id)

                    valUser = vclient.get_user(valPUUID, "puuid")
                    valTag = valUser.__getattribute__("tagLine")
                    valName = valUser.__getattribute__("gameName")

                    nick = member.nick

                    x = nick.split('#')
                    dcName = x[0]
                    dcTag = x[1]

                    if dcTag != valTag:
                        sql.update_tag(member.id, valTag)
                        try:
                            await member.edit(nick=valName + "#" + valTag)
                            sql.update_tag(member.id, valTag)
                        except:
                            print("error updating user tag. it would've been set to " + valName + "#" + valTag)
                    elif dcName != valName:
                        sql.update_name(member.id, valName)
                        try:
                            await member.edit(nick=valName + "#" + valTag)
                            sql.update_name(member.id, valName)
                        except:
                            print("error updating username. it would've been set to " + valName + "#" + valTag)
