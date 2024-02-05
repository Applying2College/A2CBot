import discord
from config import Config
from collections import defaultdict


async def start_database(ctx: discord.ApplicationContext) -> None:
    # Get list of members
    members: list[discord.Member] = Config.guild.members

    # Give feedback on current state of adding users to database
    await ctx.respond("Adding user data to database")

    for count, member in enumerate(members):
        profile = parse_roles(member.roles)  # Turn roles into dict that represents profile

        # If member has roles, add them to firebase
        if profile:
            Config.db.collection('profiles').document(f'{member.id}').set(profile, merge=True)

        # Print member and their profile
        print(member.name, profile)

        # Every 100 users added, send a message to update status of migration
        if count % 100 == 0:
            await ctx.send(f'Added {count} of {len(members)} to database')

    # Send done signal
    await ctx.send(f'Finished adding users to database')


def parse_roles(roles: list) -> dict:  # Turn discord role information into a profile for firebase
    # https://www.geeksforgeeks.org/defaultdict-in-python/
    data = defaultdict(list)

    # Segregate roles into different parts of the profile
    for role in roles:
        if role in Config.RoleIDs.Pronouns:
            data['pronouns'].append(role.name)
        elif role in Config.RoleIDs.DMStatus:
            data['dmstatus'].append(role.name)
        elif role in Config.RoleIDs.Region:
            data['region'].append(role.name)
        elif role in Config.RoleIDs.Interests:
            data['interests'].append(role.name)
        elif role in Config.RoleIDs.GradeLevel:
            data['grade_level'].append(role.name)
        elif role in Config.RoleIDs.ApplicationType:
            data['application_type'].append(role.name)
        elif role in Config.RoleIDs.EducationType:
            data['education_type'].append(role.name)

    # Add data about Rising and Verified Role
    data = dict(data)
    if 'Rising' in [role.name for role in roles]:
        data['rising'] = True
    elif 'Verified' in [role.name for role in roles]:
        data['verified'] = True

    return data
