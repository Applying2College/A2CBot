import discord
from config import Config
import calendar
from datetime import datetime, timezone, timedelta
import re

new_line = '\n'


# https://towardsdatascience.com/how-to-add-new-line-in-python-f-strings-7b4ccc605f4a
# Yes I know. It sucks.


async def report(ctx: discord.ApplicationContext, message: str) -> None:
    # Setup embed
    embed = discord.Embed(title='New Report',
                          description=f'{message}', color=discord.Color.red())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

    # Where did this report come from, with link to location if applicable
    embed.add_field(name='Sent from:',
                    value=f'<#{ctx.channel.id}> {f"[Jump to Context]({ctx.channel.last_message.jump_url})" if ctx.channel.last_message is not None else ""}',
                    inline=False)

    # Who sent this report, info about account age and id
    embed.add_field(name='Who sent alert:',
                    value=f'**Name:** {ctx.author} <@!{ctx.author.id}> '
                          f'{f"**NEW USER**{new_line}" if datetime.now(timezone.utc) - ctx.author.joined_at < timedelta(days=7) else f"{new_line}"}'
                          f'**Joined:** <t:{calendar.timegm(ctx.author.joined_at.utctimetuple())}>\n'
                          f'**Created:** <t:{calendar.timegm(ctx.author.created_at.utctimetuple())}>\n'
                          f'**ID:** {ctx.author.id}',
                    inline=False)

    # Loop through all mentions in report (find mentions with that regex)
    for i, userid in enumerate([int(x) for x in re.findall(r'<@!?([0-9]{15,20})>', message)]):
        # Getting information about persons being mentioned in report, info about account age, id
        user: discord.Member = ctx.guild.get_member(userid)
        embed.add_field(name=f'User Mentioned #{i + 1}',
                        value=f'**Name:** {user} <@!{userid}> '
                              f'{f"**NEW JOINER**{new_line}" if datetime.now(timezone.utc) - user.joined_at < timedelta(days=7) else f"{new_line}"}'
                              f'**Joined:** <t:{calendar.timegm(user.joined_at.utctimetuple())}>\n'
                              f'**Created:** <t:{calendar.timegm(user.created_at.utctimetuple())}>\n'
                              f'**ID:** {user.id}',
                        inline=False)

    # Feedback to the reporter that their report is being handled
    await ctx.respond('Raising the alarm...', ephemeral=True)
    # Send finalized embed with all data to mods and pinging them (the <@&some_string_of_numbers> pings roles)
    await Config.ChannelIDs.reports.send(f'<@&{Config.RoleIDs.mod}>', embed=embed)


async def info(ctx: discord.ApplicationContext, user: discord.Member) -> None:
    embed = discord.Embed(title='User Info', color=discord.Color.blue())

    embed.set_author(name=user.name, icon_url=user.avatar.url)
    embed.add_field(name='Roles', value=f"<@&{'> <@&'.join([str(x.id) for x in user.roles if not x.name == '@everyone'])}>")
    embed.add_field(
        name='Created', value=f'<t:{calendar.timegm(user.created_at.utctimetuple())}>')
    embed.add_field(
        name='Joined', value=f'<t:{calendar.timegm(user.joined_at.utctimetuple())}>')
    
    await ctx.respond(embed=embed)
