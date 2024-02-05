import discord
from discord.ext import commands
from config import Config


"""
Check to see if user can use command in context of their roles and the channel they are sending the message in
Roles:
- Dev
- Mod
- Event Coordinator

Channels:
- #emoji_suggestions
- #suggestion_decisions
- #bot_commands

Will tell the user if they can't use the command in certain channels

"""


def is_dev():
    async def predicate(ctx: discord.ApplicationContext):
        # Check if user has role
        return any([role.id == Config.RoleIDs.dev for role in ctx.author.roles])

    return commands.check(predicate)


def is_mod():
    async def predicate(ctx: discord.ApplicationContext):
        # Check if user has role
        return any([role.id == Config.RoleIDs.mod
                    or role.id == Config.RoleIDs.mod_in_training
                    or role.id == Config.RoleIDs.server_moderator
                    or role.id == Config.RoleIDs.admin
                    for role in ctx.author.roles])

    return commands.check(predicate)


def in_emoji_suggestions():
    async def predicate(ctx: discord.ApplicationContext):
        if ctx.channel.id == Config.ChannelIDs.emoji_suggestions.id:
            return True
        interaction = await ctx.respond(f"This command can only be used in <#{Config.ChannelIDs.emoji_suggestions.id}>")
        await interaction.delete_original_message(delay=Config.BotSettings.delete_delay)
        return False

    return commands.check(predicate)


def in_suggestion_decisions():
    async def predicate(ctx: discord.ApplicationContext):
        if ctx.channel.id == Config.ChannelIDs.suggestion_decisions.id:
            return True
        interaction = await ctx.respond(f"This command can only be used in <#{Config.ChannelIDs.suggestion_decisions}>")
        await interaction.delete_original_message(delay=Config.BotSettings.delete_delay)
        return False

    return commands.check(predicate)


def in_bot_commands():
    async def predicate(ctx: discord.ApplicationContext):
        if ctx.channel.id == Config.ChannelIDs.bot_commands.id:
            return True
        interaction = await ctx.respond(f"This command can only be used in <#{Config.ChannelIDs.bot_commands}>")
        await interaction.delete_original_message(delay=Config.BotSettings.delete_delay)
        return False

    return commands.check(predicate)
