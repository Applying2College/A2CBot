import discord
import asyncio
from discord import Permissions
from discord.ext import commands

# Python will only run this file once, regardless of
# however many times this is imported. This means
# we can use this file to globally store the bot,
# and get an instance of it whenever we need it,
# in any file, not just main.py

# Just make sure to import any modules that use
# this library *before* you call bot.run(), otherwise
# the commands won't be registered.

loop = asyncio.get_event_loop()
bot_ready = False
intents = discord.Intents.all()
permissions = Permissions.all()
bot = commands.Bot(command_prefix="$",
                   allowed_mentions=discord.AllowedMentions(
                       users=True,
                       everyone=False,
                       roles=True,
                       replied_user=True,
                   ),
                   intents=intents,
                   permissions=permissions)
