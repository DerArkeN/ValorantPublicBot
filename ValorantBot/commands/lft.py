from ValorantBot.util import methods

reaction_map = {}
remove_map = {}
leave_map = {}


async def lft(ctx, bot):
    if ctx.channel == bot.get_channel(806109172336689162):
        dcUser = ctx.author
        user_role = await methods.get_rank(dcUser)
        if dcUser.voice is not None:
            msg = await ctx.send(
                content=dcUser.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                    len(dcUser.voice.channel.members)) + "/5 player in the channel.",
                delete_after=900)
            await msg.add_reaction('✅')
            await dcUser.voice.channel.set_permissions(*dcUser.guild.members, connect=False)
            reaction_map[msg] = dcUser
    else:
        await bot.get_channel(806112383693094942).send(
            ctx.author.mention + " you can't use this command here, got to " + bot.get_channel(
                806109172336689162).mention, delete_after=30)
        await ctx.channel.purge(limit=1)


async def lft_event_add(reaction, user, bot):
    user_role = await methods.get_rank(user)
    member_position = user_role.position
    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            remove_map[reaction] = user.voice.channel
            lft_author = reaction_map[reaction.message]
            channel_to_move = lft_author.voice.channel
            channel_members = channel_to_move.members
            if user is not lft_author:
                for member in channel_members:
                    member_role = await methods.get_rank(member)
                    move = 0
                    if not abs(member_role.position - member_position) > 3:
                        move += 1
                    else:
                        move -= 1
                if move >= len(channel_members):
                    await user.move_to(channel_to_move)
                    leave_map[user] = reaction
                    lft_author_role = await methods.get_rank(lft_author)
                    content = lft_author.mention + " is looking for teammates for ranked, he is " + lft_author_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                        len(lft_author.voice.channel.members)) + "/5 players in the channel."
                    await reaction.message.edit(content=content)
                    if len(lft_author.voice.channel.members) >= 5:
                        reaction.message.delete()
                else:
                    await bot.get_channel(806112383693094942).send(
                        content=user.mention + ", there are people with too high ranks for you in this channel.",
                        delete_after=30)
                    await reaction.remove(user)
            else:
                await reaction.remove(user)
        else:
            await bot.get_channel(806112383693094942).send(
                content=user.mention + ", you have to be in a voice channel to use this reaction", delete_after=30)
            await reaction.remove(user)


async def lft_event_remove(reaction, user, bot):
    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            lft_author = reaction_map[reaction.message]
            user_role = await methods.get_rank(lft_author)
            await user.move_to(remove_map[reaction])
            content = lft_author.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                len(lft_author.voice.channel.members)) + "/5 players in the channel."
            await reaction.message.edit(content=content)


async def lft_leave_channel(member):
    if member.nick is not None:
        if member in leave_map:
            member_reaction = leave_map[member]
            lft_author = reaction_map[member_reaction.message]
            if member != lft_author:
                user_role = await methods.get_rank(lft_author)
                content = lft_author.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                    len(lft_author.voice.channel.members)) + "/5 players in the channel."
                await member_reaction.message.edit(content=content)
                await member_reaction.remove(member)