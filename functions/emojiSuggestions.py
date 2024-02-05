import discord
from config import *

"""
Suggest emojis using suggestemoji <url> <name>
Suggest stickers using the suggeststicker <url> <name>.
Approve suggestions by using approve <suggestion_message_id> <reason>
Deny suggestions by using deny <suggestion_message_id> <reason>
"""


async def suggest_emoji(ctx: discord.ApplicationContext, url, name):
    embed = discord.Embed(title=f"Suggested by {ctx.author}", color=discord.Color.from_rgb(67, 181, 129))
    embed.add_field(name="Type", value=f"emoji")
    embed.add_field(name="Name", value=f"{name}")
    embed.set_image(url=url)

    suggestion = await ctx.respond(embed=embed)
    message = await suggestion.original_message()
    await message.add_reaction(Config.Emojis.arrow_up)
    await message.add_reaction(Config.Emojis.arrow_down)


async def suggest_sticker(ctx: discord.ApplicationContext, url, name):
    embed = discord.Embed(title=f"Suggested by {ctx.author}", color=discord.Color.from_rgb(67, 181, 129))
    embed.add_field(name="Type", value=f"sticker")
    embed.add_field(name="Name", value=f"{name}")
    embed.set_image(url=url)

    suggestion = await ctx.respond(embed=embed)
    message = await suggestion.original_message()
    await message.add_reaction(Config.Emojis.arrow_up)
    await message.add_reaction(Config.Emojis.arrow_down)


async def approve(ctx: discord.ApplicationContext, message_id: int, reason: str) -> None:
    # Get the channel and message of the suggestion
    channel = Config.ChannelIDs.emoji_suggestions
    message: discord.Message = await channel.fetch_message(message_id)

    try:  # Check if messages has suggestion
        embed = message.embeds[0]
    except IndexError as e:
        await ctx.respond("Message does not contain embed")
        return

    # Reformat the embed to be an approval
    embed.title = f"Suggestion by {embed.title.split()[-1]} Approved"
    embed.colour = discord.Color.from_rgb(0, 255, 0)

    # Add reason
    embed.add_field(name="Reason", value=f"{reason}")

    # Respond with embed
    await ctx.respond(embed=embed)
    # Delete original suggestion
    await message.delete()


async def deny(ctx: discord.ApplicationContext, message_id: int, reason: str) -> None:
    # Get the channel and message of the suggestion
    channel = Config.ChannelIDs.emoji_suggestions
    message: discord.Message = await channel.fetch_message(message_id)

    try:  # Check if message has suggestion
        embed = message.embeds[0]
    except IndexError as e:
        await ctx.respond("Message does not contain embed")
        return

    # Reformat the suggestion to be a denial
    embed.title = f"Suggestion by {embed.title.split()[-1]} Denied"
    embed.colour = discord.Color.from_rgb(255, 0, 0)

    # Add reason
    embed.add_field(name="Reason", value=f"{reason}")

    # Respond with embed
    await ctx.respond(embed=embed)
    # Delete original suggestion
    await message.delete()
