# from functions.background import serverUpdates
import os
from os.path import join, dirname
import asyncio

import discord

from config import Config
import helper
from discord.ext import commands
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore

# Command Modules
import functions.slowmode as slowmode
import functions.emojiSuggestions as emojiSuggestions
import functions.collegeLookup as collegeLookup
import functions.permissions as permissions
# import functions.roleSelect as roleSelect
import functions.aprilfools as aprilfools
import functions.dev_debug as dev_debug
import functions.profiles as profiles
import functions.database as database
import functions.moderation as moderation
import functions.fun as fun
import functions.minecraft as minecraft

dotenv_path = join(dirname(__file__), '.dev-env')
load_dotenv(dotenv_path)

"""
I kinda don't like the fact that this file is kinda like a header file for other
commands. :noooo: why does every programming language eventually have this structure.
Does god demand that we write every function header twice??
"""

bot = helper.bot


@bot.event
async def on_ready() -> None:
    # Get current guild
    print(bot.guilds)
    # guild = discord.utils.get(bot.guilds, name='A2C Testing 2')
    # guild = discord.utils.get(bot.guilds, name='A2C Dev Testing')
    # guild = discord.utils.get(bot.guilds, name='ApplyingToCollege LilBillTest')
    guild = discord.utils.get(bot.guilds, name='ApplyingToCollege')
    print("Guild", guild)
    print("Guild ID", guild.id)
    #await bot.tree.sync(guild = guild.id)
    Config.guild = guild
    helper.bot_ready = True  # global bot ready state
    #await bot.register_commands(guild = guild.id)
    # Get channel ids
    channels = guild.channels
    Config.ChannelIDs.general = discord.utils.get(channels, name='🚀-general-chat')
    Config.ChannelIDs.bot_commands = discord.utils.get(
        channels, name='🤖-bot-commands')
    Config.ChannelIDs.emoji_suggestions = discord.utils.get(
        channels, name='🥐-emoji-suggestions')
    Config.ChannelIDs.suggestion_decisions = discord.utils.get(
        channels, name='✅-suggestion-decisions')
    Config.ChannelIDs.suggestion_voting = discord.utils.get(
        channels, name='💬-suggestion-voting')
    Config.ChannelIDs.roles = discord.utils.get(channels, name="🎭-roles")
    Config.ChannelIDs.dev_chat = discord.utils.get(
        channels, name="🧃💭-dev-chat")
    # Config.ChannelIDs.college_talk = discord.utils.get(channels, name="🏫-college-talk")
    Config.ChannelIDs.app_discussion = discord.utils.get(
        channels, name="🌻-app-discussion")
    Config.ChannelIDs.extracurriculars = discord.utils.get(
        channels, name="🏹-extracurriculars")
    Config.ChannelIDs.reports = discord.utils.get(channels, name="🤬🚨-reports")
    Config.ChannelIDs.days_old_channel = bot.get_channel(
        916104906065207346)  # This channel ID is the main A2C one

    Config.Slowmode.channels[f"{Config.ChannelIDs.general.id}"] = Config.Slowmode.ChannelConfig(
        3, 9, 2.0)
    # Config.Slowmode.channels[f"{Config.ChannelIDs.college_talk.id}"] = Config.Slowmode.ChannelConfig(
    #     3, 9, 2.0)

    # Get role ids
    Config.RoleIDs.roles = guild.roles
    #Config.RoleIDs.dev = discord.utils.get(
    #    Config.RoleIDs.roles, name='Developer').id
    Config.RoleIDs.mod_in_training = discord.utils.get(
        Config.RoleIDs.roles, name='Moderator in Training').id
    Config.RoleIDs.server_moderator = discord.utils.get(
        Config.RoleIDs.roles, name='Server Moderator').id
    Config.RoleIDs.mod = discord.utils.get(Config.RoleIDs.roles, name='mod').id
    Config.RoleIDs.admin = discord.utils.get(
        Config.RoleIDs.roles, name='admin').id
    Config.UserIDs.admidral = 262424335032123394

    for role in Config.RoleIDs.roles:
        # str() call is needed to convert the value of the color into something more readable

        if str(role.color) == '#d0312d':  # Pronouns
            Config.RoleIDs.Pronouns.append(role)
        elif str(role.color) == '#e67e22':  # DM Status
            Config.RoleIDs.DMStatus.append(role)
        elif str(role.color) == '#1f8b4c':  # Region
            Config.RoleIDs.Region.append(role)
        elif str(role.color) == '#3498db':  # Major/Interests
            Config.RoleIDs.Interests.append(role)
        elif role.name in ['HS Freshman', 'HS Sophomore', 'HS Junior', 'HS Senior', 'Prefrosh', 'HS Grad', 'Gap Year',
                           'College Freshman', 'College Sophomore', 'College Junior', 'College Senior',
                           'Bachelor\'s Graduate', 'Graduate Student', 'Master\'s Graduate',
                           'College+']:  # Education Level
            Config.RoleIDs.GradeLevel.append(role)
        elif role.name in ['Transfer', 'Nontraditional', 'International']:  # Application Type
            Config.RoleIDs.ApplicationType.append(role)
        elif role.name in ['Dual Enrollment']:  # Education Type
            Config.RoleIDs.EducationType.append(role)

    cred = credentials.Certificate(join(dirname(__file__), 'firebase-cert.json'))
    # cred = credentials.Certificate("firebase-cert.json")
    firebase_admin.initialize_app(cred)

    if Config.db is None:
        Config.db = firestore.client()

    print(f"We have logged in as {bot.user}")
    #await Config.ChannelIDs.dev_chat.send("Bot ready")
    print("successfully finished startup")
    print(await bot.get_desynced_commands())
    #await bot.sync_commands(force=True,delete_existing=False,method="auto")
    #print(await bot.get_desynced_commands())
    asyncio.run(await slowmode.loop())


""" MOD BOT COMMANDS """


@bot.slash_command(name="echo")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def echo(ctx: discord.ApplicationContext, *, message: str) -> None:
    print(f"{message}")
    await ctx.respond(f'echoing: {message}', ephemeral=True)

    await ctx.respond(message)

@bot.slash_command(name="sync")
@commands.check_any(permissions.is_admidral())
async def sync(ctx: discord.ApplicationContext) -> None:
    print(await bot.get_desynced_commands(guild_id=Config.guild.id, prefetched=None))
    await bot.sync_commands(method="auto")
    print("done loading")

@bot.slash_command(name="ping")
# @commands.check_any(permissions.is_mod(), permissions.is_dev())
async def ping(ctx: discord.ApplicationContext) -> None:
    print("author id for pong:",ctx.author.id)
    await ctx.respond("pong")


@bot.slash_command(name="name_bomb")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def name_bomb(ctx: discord.ApplicationContext) -> None:
    await aprilfools.name_bomb(ctx)


@bot.slash_command(name="change_back")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def change_back(ctx: discord.ApplicationContext) -> None:
    await aprilfools.change_back(ctx)


@bot.slash_command(name="editslow")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def edit_slow(
    ctx: discord.ApplicationContext,
    rate_increment: int,
    slowmode_cap: int,
    message_rate: float,
    channel: discord.Option(discord.TextChannel)
) -> None:
    await slowmode.edit_slowmode(ctx, rate_increment, slowmode_cap, message_rate, channel)


@bot.slash_command(name="currentslow")
@commands.check_any(permissions.is_mod(), permissions.is_dev(),permissions.is_admidral())
async def current_slow(ctx: discord.ApplicationContext) -> None:
    await slowmode.current_slow(ctx)


@bot.slash_command(name="suggestemoji")
@commands.check_any(permissions.in_emoji_suggestions())
async def suggest_emoji(ctx: discord.ApplicationContext, url: str, name: str) -> None:
    await emojiSuggestions.suggest_emoji(ctx, url, name)


@bot.slash_command(name="suggeststicker")
@commands.check_any(permissions.in_emoji_suggestions())
async def suggest_sticker(ctx: discord.ApplicationContext, url: str, name: str) -> None:
    await emojiSuggestions.suggest_sticker(ctx, url, name)


@bot.slash_command(name="approve")
@commands.check_any(permissions.is_mod() and permissions.in_suggestion_decisions())
async def approve(ctx: discord.ApplicationContext, message_id: int, *, reason: str) -> None:
    await emojiSuggestions.approve(ctx, message_id, reason)


@bot.slash_command(name="deny")
@commands.check_any(permissions.is_mod() and permissions.in_suggestion_decisions())
async def deny(ctx: discord.ApplicationContext, message_id: int, *, reason: str) -> None:
    await emojiSuggestions.deny(ctx, message_id, reason)


@bot.slash_command(name="givebonk")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def give_bonk(ctx: discord.ApplicationContext, user: discord.Option(discord.Member), charges: int):
    await fun.give_bonk(ctx, user, charges)


@bot.slash_command(name="checkbonk")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def check_bonk(ctx: discord.ApplicationContext, user: discord.Option(discord.Member)):
    await fun.check_bonk(ctx, user)


@bot.slash_command(name="yoink")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.is_admidral())
async def yoink(ctx: discord.ApplicationContext, user: discord.Option(discord.Member)) -> None:
    await fun.yoink(ctx, user)


@bot.slash_command(name="info")
@commands.check_any(permissions.is_mod(), permissions.is_dev())
async def info(ctx: discord.ApplicationContext, user: discord.Option(discord.Member)) -> None:
    await moderation.info(ctx, user)


""" MEMBER BOT COMMANDS """


@bot.slash_command(name="search")
@commands.check_any(permissions.is_mod(), permissions.is_dev(), permissions.in_bot_commands())
async def college_search(ctx: discord.ApplicationContext, *, college: str) -> None:
    await collegeLookup.search(ctx, college)


@bot.slash_command(name="whois")
async def view_profile(ctx: discord.ApplicationContext, user: discord.Option(discord.Member)) -> None:
    await profiles.view_profiles(ctx, user)


@bot.slash_command(name="profile")
async def edit_profile(ctx: discord.ApplicationContext) -> None:
    await profiles.edit_profile(ctx)


@bot.slash_command(name="report")
async def report(ctx: discord.ApplicationContext, message: str) -> None:
    await moderation.report(ctx, message)


@bot.slash_command(name="bonk")
async def bonk(ctx: discord.ApplicationContext, user: discord.Option(discord.Member)) -> None:
    await fun.bonk(ctx, user)


@bot.slash_command(name="remindbonk")
async def remind_bonk(ctx: discord.ApplicationContext) -> None:
    print("author id for remind bonk:",ctx.author.id)
    await fun.remind_bonk(ctx)


@bot.slash_command(name="sendbonk")
async def send_bonk(ctx: discord.ApplicationContext, user: discord.Option(discord.Member), charges: int) -> None:
    await fun.send_bonk(ctx, user, charges)


# MINECRAFT COMMANDS

@bot.slash_command(name="whitelist")
async def whitelist(ctx: discord.ApplicationContext, mc_username: str) -> None:
    await minecraft.whitelist_user(ctx, mc_username)


@bot.slash_command(name="removeminecraft")
@commands.check_any(permissions.is_mod(), permissions.is_dev())
async def remove_whitelist(ctx: discord.ApplicationContext, member: discord.Option(discord.Member)) -> None:
    await minecraft.remove_minecraft_user(ctx)


""" DEV COMMANDS """


@bot.slash_command(name="dev_roles")
@commands.check_any(permissions.is_dev())
async def dev_roles(ctx: discord.ApplicationContext, member:  discord.Option(discord.Member)) -> None:
    await dev_debug.dev_roles(ctx, member)


@bot.slash_command(name="start_database")
@commands.check_any(permissions.is_dev(), permissions.is_mod())
async def start_database(ctx: discord.ApplicationContext) -> None:
    await database.start_database(ctx)


@bot.slash_command(name="dev_channels")
@commands.check_any(permissions.is_dev())
async def dev_channels(ctx: discord.ApplicationContext) -> None:
    await dev_debug.dev_channels(ctx)


@bot.slash_command(name="dev_embed")
@commands.check_any(permissions.is_dev())
async def dev_embed(ctx: discord.ApplicationContext, title: str, description: str) -> None:
    await dev_debug.dev_embed(ctx, title, description)


@bot.slash_command(name="dev_slashcom")
@commands.check_any(permissions.is_dev())
async def dev_embed(ctx: discord.ApplicationContext, message: str) -> None:
    await dev_debug.dev_slashcom(ctx, message)
    
@bot.listen()
async def on_connect():
    print('Bot has connected!')


@bot.listen('on_message')
async def logging(msg: discord.Message) -> None:
    if msg.author == bot.user:
        return

    print(msg.content)
    if str(msg.channel.id) in Config.Slowmode.channels:
        await slowmode.slowmode(msg.channel)


@bot.listen('on_application_command_error')
async def log_error(ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
    embed = discord.Embed(title="Oh No! I seem to have gotten a wittle stucky wucky!", color=discord.Color.red(),
                          description="Pwease could you tell the devs? I need some help...")
    embed.add_field(name="Error Details", value=f"{error}")
    await ctx.respond(embed=embed)
    raise error

bot.run("secret-here")
