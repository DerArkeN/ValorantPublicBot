from ValorantBot.util import methods

reactionMap = {}
removeMap = {}


async def lft(ctx, bot):
    dcUser = ctx.author
    user_role = await methods.get_rank(dcUser)

    if dcUser.voice is not None:
        msg = await ctx.send(
            content=dcUser.mention + " is looking for Teammates, he is " + user_role.name + ". Join a Channel and react to join the channel.",
            delete_after=300)
        await msg.add_reaction('✅')

        reactionMap[msg] = dcUser


async def lft_event_add(reaction, user, bot):
    user_role = await methods.get_rank(user)
    member_position = user_role.position

    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            removeMap[reaction] = user.voice.channel
            lft_author = reactionMap[reaction.message]
            channel_to_move = lft_author.voice.channel
            channel_members = channel_to_move.members
            for member in channel_members:
                member_role = await methods.get_rank(member)
                move = 0
                if not abs(member_role.position - member_position) > 3:
                    move += 1
                else:
                    move -= 1
            if move >= len(channel_members):
                await user.move_to(channel_to_move)
            else:
                await bot.get_channel(806112383693094942).send(
                    content=user.mention + ", there are people with too high ranks for you in this Channel.",
                    delete_after=30)
                await reaction.remove(user)
        else:
            await bot.get_channel(806112383693094942).send(
                content=user.mention + ", you have to be in a Voice Channel to use this reaction", delete_after=30)
            await reaction.remove(user)


async def lft_event_remove(reaction, user, bot):
    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            await user.move_to(removeMap[reaction])
