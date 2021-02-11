import os
import valorant
import discord

from discord.ext import commands
from dotenv import load_dotenv

from ValorantBot.commands import lft, register, rank
from ValorantBot.util import sql, methods

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.voice_states = True

vclient = valorant.Client(os.getenv("KEY"))
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Valorant Bot logged in")
    print(sql.mydb)
    sql.create_table()


@bot.event
async def on_member_join(member):
    channel_support = bot.get_channel(806112383693094942)
    channel_rules = bot.get_channel(806088311848435732)
    channel_commands = bot.get_channel(806084486869417984)
    await channel_support.send(content=
    'Welcome to the Public Valorant Server, ' + member.mention + '\n\nStart of by reading the rules in ' + channel_rules.mention +
    '\nWhen you are done give yourself your Valorant Rank by going to ' + channel_commands.mention + ' and do !register "Name+Tag" "Rank". As an example !register "arkeN#0711" "Platinum 1"' + '\n\nNow you have full acces on the Discord Server, if any questions come up feel free to tag an Moderator or an Administrator for important questions.\n'
    , delete_after=900)


@bot.event
async def on_member_remove(member):
    if member.nick is not None:
        if not member.bot:
            sql.delete_user(member.id)


@bot.event
async def on_member_ban(guild, user):
    if user.nick is not None:
        if not user.bot:
            sql.delete_user(user.id)


def is_bot(message):
    return message.author != bot.get_user(806461492450426900)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel == bot.get_channel(806109172336689162):
        try:
            await message.channel.purge(check=is_bot)
        except:
            return


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.get_user(806461492450426900):
        await lft.lft_event_add(reaction, user, bot)


@bot.event
async def on_reaction_remove(reaction, user):
    await lft.lft_event_remove(reaction, user, bot)


@bot.command(name="register", pass_context=True)
async def register_command(ctx, name=None, rank=None):
    if ctx.channel == bot.get_channel(806084486869417984):
        if name is not None:
            if rank is not None:
                await register.register(ctx, name, rank, vclient, bot)
            else:
                await ctx.send("You have to enter a rank.")
        else:
            await ctx.send("You have to enter a name.")
    else:
        await bot.get_channel(806112383693094942).send(content=ctx.author.mention + "you can't use this command here, got to " + bot.get_channel(806084486869417984).mention, delete_after=30)
        await ctx.channel.purge(limit=1)


@bot.command(name="rank", pass_context=True)
async def rank_command(ctx, role=None):
    if ctx.channel == bot.get_channel(806084486869417984):
      if role is not None:
          await rank.rank(ctx, role, bot)
      else:
        await ctx.send("You have to enter a rank.")
    else:
        await bot.get_channel(806112383693094942).send(content=ctx.author.mention + " you can't use this command here, got to " + bot.get_channel(806084486869417984).mention, delete_after=30)
        await ctx.channel.purge(limit=1)


@bot.command(name="lft", pass_context=True)
async def lft_command(ctx):
    if ctx.channel == bot.get_channel(806109172336689162):
        await lft.lft(ctx, bot)
    else:
        await bot.get_channel(806112383693094942).send(ctx.author.mention + " you can't use this command here, got to " + bot.get_channel(806109172336689162).mention, delete_after=30)
        await ctx.channel.purge(limit=1)


@bot.event
async def on_voice_state_update(member, before, after):
    join_to_create = bot.get_channel(806102585995296809)
    join_to_create_category = join_to_create.category

    if after.channel == join_to_create:
        new_voice = await member.guild.create_voice_channel(name=member.nick + "'s Channel", category=join_to_create_category)
        await member.move_to(new_voice)


@bot.event
async def on_disconnect():
    sql.mydb.close()
    print("Valorant Bot logged out")


bot.run(os.getenv("TOKEN"))