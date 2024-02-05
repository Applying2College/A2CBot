import discord
from config import Config


async def dev_roles(ctx: discord.ApplicationContext, member: discord.Member):

    for role in member.roles:
        print(role, role.color)

    await ctx.respond(f'{member.roles!r}')


async def dev_channels(ctx: discord.ApplicationContext):

    for channel in Config.guild.channels:
        print(channel)

    await ctx.respond(f'Check console output')


async def dev_embed(ctx: discord.ApplicationContext, title, description):
    embed = discord.Embed(title=f'{title}', description=f'{description}')
    await ctx.respond(embed=embed)


async def dev_slashcom(ctx: discord.ApplicationContext, message):
    print(f'{type(message)} {message!r}')
    await ctx.respond(f'{type(message)} {message!r}')
