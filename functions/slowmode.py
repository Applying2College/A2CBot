import asyncio
import configparser
import sysconfig
import time
import math
import discord.types.channel
from discord import Embed

from config import *


async def edit_slowmode(
        ctx: discord.ApplicationContext,
        increment: int,
        cap: int,
        message_rate: float,
        channel: discord.TextChannel
) -> None:
    # Handle divide by zero issues
    if message_rate == 0:
        await ctx.respond("⚠️ Cannot set message_rate to 0! To disable slowmode for a specific channel, "
                          "set increment or cap to 0 and set message_rate to 1.")
        return

    # Initialize slowmode for a channel by giving it a ChannelConfig
    Config.Slowmode.channels[f"{channel.id}"] = Config.Slowmode.ChannelConfig(
        increment, cap, message_rate)

    # Create and respond with embed on the edited slowmode config of this channel
    res = Embed()
    res.add_field(name=f"Edited Channel:",
                  value=f"<#{channel.id}>\n"
                        f"Increment: {Config.Slowmode.channels[f'{channel.id}'].increment} | "
                        f"Cap: {Config.Slowmode.channels[f'{channel.id}'].cap} | "
                        f"Message Rate: {Config.Slowmode.channels[f'{channel.id}'].message_rate} ")
    await ctx.respond(embed=res)


async def current_slow(ctx: discord.ApplicationContext) -> None:
    # Create and respond with embed of all slowmode configs
    res = Embed()
    for key in Config.Slowmode.channels:
        res.add_field(name=f"Channel:",
                      value=f"<#{key}>\n"
                            f"Increment: {Config.Slowmode.channels[key].increment} | "
                            f"Cap: {Config.Slowmode.channels[key].cap} | "
                            f"Message Rate: {Config.Slowmode.channels[key].message_rate} ")
    res.add_field(
        name="Note: ", value="To disable slowmode for a specific channel, set increment or cap to 0")
    await ctx.respond(embed=res)



async def slowmode(channel: discord.TextChannel) -> None:
    if Config.Slowmode.channels[f"{channel.id}"].cap == 0 or Config.Slowmode.channels[f"{channel.id}"].increment == 0:
        return

    # Increments count of messages sent in `channel`
    Config.Slowmode.channels[f"{channel.id}"].last_messages += 1

    # Calculate a slow amount that is `last_messages // message_rate * increment` or the
    # slow_amount cap, whichever is smaller
    slow_amount = min(
        (Config.Slowmode.channels[f"{channel.id}"].last_messages
         // Config.Slowmode.channels[f"{channel.id}"].message_rate)
        * Config.Slowmode.channels[f"{channel.id}"].increment,
        Config.Slowmode.channels[f"{channel.id}"].cap
    )
    await channel.edit(slowmode_delay=slow_amount)


# Decrement count of messages sent in all slowmode channels once per second
async def loop():
    while True:
        await asyncio.sleep(1)
        for config in list(Config.Slowmode.channels.values()):
            if config.last_messages > 0:
                config.last_messages -= 1
