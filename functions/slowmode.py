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
        channel: discord.TextChannel,
        apply_to_threads: bool,
) -> None:
    # Handle divide by zero issues
    if message_rate == 0:
        await ctx.respond("⚠️ Cannot set message_rate to 0! To disable slowmode for a specific channel, "
                          "set increment or cap to 0 and set message_rate to 1.")
        return

    # Initialize slowmode for a channel by giving it a ChannelConfig
    Config.Slowmode.channels[f"{channel.id}"] = Config.Slowmode.ChannelConfig(
        increment, cap, message_rate, apply_to_threads)

    # Create and respond with embed on the edited slowmode config of this channel
    res = Embed()
    res.add_field(name=f"Edited Channel:",
                  value=f"<#{channel.id}>\n"
                        f"Increment: {Config.Slowmode.channels[f'{channel.id}'].increment} | "
                        f"Cap: {Config.Slowmode.channels[f'{channel.id}'].cap} | "
                        f"Message Rate: {Config.Slowmode.channels[f'{channel.id}'].message_rate} |"
                        f"Apply to threads: {Config.Slowmode.channels[f'{channel.id}'].apply_to_threads}")
    await ctx.respond(embed=res)

async def edit_slowmode_thread(
        ctx: discord.ApplicationContext,
        increment: int,
        cap: int,
        message_rate: float,
        channel: discord.Thread,
) -> None:
    # Handle divide by zero issues
    if message_rate == 0:
        await ctx.respond("⚠️ Cannot set message_rate to 0! To disable slowmode for a specific channel, "
                          "set increment or cap to 0 and set message_rate to 1.")
        return

    # Initialize slowmode for a channel by giving it a ChannelConfig
    Config.Slowmode.threads[f"{channel.id}"] = Config.Slowmode.ChannelConfig(
        increment, cap, message_rate)

    # Create and respond with embed on the edited slowmode config of this channel
    res = Embed()
    res.add_field(name=f"Edited Thread:",
                  value=f"<#{channel.id}>\n"
                        f"Increment: {Config.Slowmode.threads[f'{channel.id}'].increment} | "
                        f"Cap: {Config.Slowmode.threads[f'{channel.id}'].cap} | "
                        f"Message Rate: {Config.Slowmode.threads[f'{channel.id}'].message_rate}")
    await ctx.respond(embed=res)


async def current_slow(ctx: discord.ApplicationContext) -> None:
    # Create and respond with embed of all slowmode configs
    res = Embed()
    for key in Config.Slowmode.channels:
        res.add_field(name=f"Channel:",
                      value=f"<#{key}>\n"
                            f"Increment: {Config.Slowmode.channels[key].increment} | "
                            f"Cap: {Config.Slowmode.channels[key].cap} | "
                            f"Message Rate: {Config.Slowmode.channels[key].message_rate} |"
                            f"Apply to threads: {Config.Slowmode.channels[key].apply_to_threads}")
    for key in Config.Slowmode.threads:
        res.add_field(name=f"Thread:",
                      value=f"<#{key}>\n"
                            f"Increment: {Config.Slowmode.threads[f'{key}'].increment} | "
                            f"Cap: {Config.Slowmode.threads[f'{key}'].cap} | "
                            f"Message Rate: {Config.Slowmode.threads[f'{key}'].message_rate}")
    res.add_field(
        name="Note: ", value="To disable slowmode for a specific channel, set increment or cap to 0")
    await ctx.respond(embed=res)



async def slowmode(channel: discord.TextChannel) -> None:

    slow_amount = 0

    if channel.type == discord.ChannelType.public_thread:

        if str(channel.id) in Config.Slowmode.threads:
            if Config.Slowmode.threads[f"{channel.id}"].cap == 0 or Config.Slowmode.threads[f"{channel.id}"].increment == 0:
                return
            Config.Slowmode.threads[f"{channel.id}"].last_messages += 1
            slow_amount = min(
                (Config.Slowmode.threads[f"{channel.id}"].last_messages
                 // Config.Slowmode.threads[f"{channel.id}"].message_rate)
                * Config.Slowmode.threads[f"{channel.id}"].increment,
                Config.Slowmode.threads[f"{channel.id}"].cap
            )
        else:
            parent_channel_id = str(channel.parent_id)
            if Config.Slowmode.channels[parent_channel_id].cap == 0 or Config.Slowmode.channels[parent_channel_id].increment == 0:
                return
            if parent_channel_id in Config.Slowmode.channels and Config.Slowmode.channels[parent_channel_id].apply_to_threads:
                Config.Slowmode.channels[parent_channel_id].threads_last_messages[f"{channel.id}"] = Config.Slowmode.channels[parent_channel_id].threads_last_messages.get(f"{channel.id}", 0) + 1
                slow_amount = min(
                    (Config.Slowmode.channels[parent_channel_id].threads_last_messages.get(f"{channel.id}", 0)
                     // Config.Slowmode.channels[parent_channel_id].message_rate)
                    * Config.Slowmode.channels[parent_channel_id].increment,
                    Config.Slowmode.channels[parent_channel_id].cap
                )
    else:
        if Config.Slowmode.channels[f"{channel.id}"].cap == 0 or Config.Slowmode.channels[f"{channel.id}"].increment == 0:
            return
        Config.Slowmode.channels[f"{channel.id}"].last_messages += 1
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
            for thread_id in list(config.threads_last_messages.keys()):
                if config.threads_last_messages[thread_id] > 0:
                    config.threads_last_messages[thread_id] -= 1
        for config in list(Config.Slowmode.threads.values()):
            if config.last_messages > 0:
                config.last_messages -= 1