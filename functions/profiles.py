from config import *

"""
Firestore setup tutorial: https://www.youtube.com/watch?v=UVzBQ0LkO28
"""


async def view_profiles(ctx: discord.ApplicationContext, user: discord.Member) -> None:
    profile = discord.Embed()
    profile.set_author(name=f"{user}", icon_url=user.avatar.url)
    profile.set_thumbnail(url=user.avatar.url)

    info = Config.db.collection('profiles').document(f'{user.id}').get()

    # Predefining defaults for profiles that haven't been filled out
    pronouns = 'Unspecified by user'
    grade_level = 'Unspecified by user'
    dmstatus = 'Ask to DM'
    region = 'Unspecified by user'
    interests = 'Unspecified by user'
    application_type = 'Unspecified by user'
    education_type = 'Unspecified by user'

    # Construct profile data from profile on database
    if info.exists:
        for key, value in info.to_dict().items():
            if key == 'pronouns':
                pronouns = ', '.join(value)
            elif key == 'grade_level':
                grade_level = ', '.join(value)
            elif key == 'dmstatus':
                dmstatus = ', '.join(value)
            elif key == 'region':
                region = ', '.join(value)
            elif key == 'interests':
                interests = ', '.join(value)
            elif key == 'application_type':
                application_type = ', '.join(value)
            elif key == 'education_type':
                education_type = ', '.join(value)
            elif key == 'rising' and value:
                grade_level = 'Rising, ' + grade_level

    profile.add_field(name='Education Level', value=grade_level, inline=False)
    profile.add_field(name='Pronouns', value=pronouns, inline=False)
    profile.add_field(name='DM Status', value=dmstatus, inline=False)
    profile.add_field(name='Region', value=region, inline=False)
    profile.add_field(name='Major/Interests', value=interests, inline=False)
    profile.add_field(name='Application Type', value=application_type, inline=False)
    profile.add_field(name='Education Type', value=education_type, inline=False)

    await ctx.respond(embed=profile, ephemeral=True)


class ProfileSetup(discord.ui.View):
    def __init__(self, profile):
        super().__init__()

        # Get profile from initialization so that profile settings save in the SelectMenu
        self.profile = profile

        # Grade Level

        # Get data for this SelectMenu from profile or default to []
        self.grade_level = []
        if 'grade_level' in self.profile:
            self.grade_level.extend(self.profile['grade_level'])

        self.add_item(discord.ui.Select(
            placeholder="Select your current grade level...",
            min_values=1,
            max_values=4,
            options=[
                discord.SelectOption(label="HS Freshman", description="High School Freshman",
                                     default='HS Freshman' in self.grade_level),
                discord.SelectOption(label="HS Sophomore", description="High School Sophomore",
                                     default='HS Sophomore' in self.grade_level),
                discord.SelectOption(label="HS Junior", description="High School Junior",
                                     default='HS Junior' in self.grade_level),
                discord.SelectOption(label="HS Senior", description="High School Senior",
                                     default='HS Senior' in self.grade_level),
                discord.SelectOption(label="Prefrosh", description="Highschool Senior who has committed to a college",
                                     default='Prefrosh' in self.grade_level),
                discord.SelectOption(label="HS Grad", description="High School Graduate",
                                     default='HS Grad' in self.grade_level),
                discord.SelectOption(label="Gap Year",
                                     description="Taking a year off from school to pursuit other things",
                                     default='Gap Year' in self.grade_level),
                discord.SelectOption(label="College Freshman", description="College Freshman",
                                     default='College Freshman' in self.grade_level),
                discord.SelectOption(label="College Sophomore", description="College Sophomore",
                                     default='College Sophomore' in self.grade_level),
                discord.SelectOption(label="College Junior", description="College Junior",
                                     default='College Junior' in self.grade_level),
                discord.SelectOption(label="College Senior", description="College Senior",
                                     default='College Senior' in self.grade_level),
                discord.SelectOption(label="Bachelor's Graduate", description="Received a bachelors degree",
                                     default='Bachelor\'s Graduate' in self.grade_level),
                discord.SelectOption(label="Graduate Student", description="Currently a Graduate Student",
                                     default='Graduate Student' in self.grade_level),
                discord.SelectOption(label="Master's Graduate", description="Received a Master's Degree or higher",
                                     default='Master\'s Graduate' in self.grade_level),
            ])
        )

        # Callback for when the SelectMenu is interacted with
        async def grade_level_callback(interaction: discord.Interaction) -> None:
            # Update profile info on firebase
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'grade_level': list(interaction.data.values())[0]}, merge=True)

            # Get user from interaction for editing roles
            user: discord.Member = interaction.user

            # Gather the grade level roles that need to be removed
            to_be_removed = []
            for role in user.roles:
                if role in Config.RoleIDs.GradeLevel:
                    to_be_removed.append(role)

            # Remove grade level roles
            await user.remove_roles(*to_be_removed)

            # Gather roles that need to be added
            new_roles = []
            for role in list(interaction.data.values())[0]:
                new_roles.append(discord.utils.get(Config.RoleIDs.roles, name=role))

            # Add roles
            await user.add_roles(*new_roles)

        # Set above function to be the callback of the last object added to the SelectMenu
        self.children[-1].callback = grade_level_callback

        # Pronouns

        self.pronouns = []
        if 'pronouns' in self.profile:
            self.pronouns.extend(self.profile['pronouns'])

        self.add_item(discord.ui.Select(
            placeholder="Select pronouns that apply to you...",
            min_values=1,
            max_values=4,
            options=[
                discord.SelectOption(label="she/her", default='she/her' in self.pronouns),
                discord.SelectOption(label="he/him", default='he/him' in self.pronouns),
                discord.SelectOption(label="they/them", default='they/them' in self.pronouns),
                discord.SelectOption(label="ask for pronouns",
                                     description="If you do not use traditional pronouns",
                                     default='ask for pronouns' in self.pronouns)
            ])
        )

        async def pronoun_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'pronouns': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = pronoun_callback

        # Rising Student

        self.rising = None
        if 'rising' in self.profile:
            self.rising = self.profile['rising']

        self.add_item(discord.ui.Select(
            placeholder="Are you a rising student...",
            min_values=0,
            max_values=1,
            options=[
                discord.SelectOption(label="Yes, I'm a rising student",
                                     description="I'm currently between grades (ex: if you've finished junior "
                                                 "year you'd be a rising senior)",
                                     default=self.rising is not None and self.rising),
                discord.SelectOption(label="No, I'm not a rising student",
                                     default=self.rising is not None and not self.rising),
            ])
        )

        async def rising_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'rising': 'Yes, I\'m a rising student' in list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = rising_callback

        # DM Status

        self.dmstatus = []
        if 'dmstatus' in self.profile:
            self.dmstatus.extend(self.profile['dmstatus'])

        self.add_item(discord.ui.Select(
            placeholder="Choose your preferred DM Status...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Open DMs", description="Anyone is allowed to DM you",
                                     default='Open DMs' in self.dmstatus),
                discord.SelectOption(label="Closed DMs",
                                     description="No one is allowed to DM (if someone violates this "
                                                 "please contact the mods)",
                                     default='Closed DMs' in self.dmstatus),
                discord.SelectOption(label="Ask to DM",
                                     description="Users must ask you before beginning direct messages",
                                     default='Ask to DM' in self.dmstatus),
            ])
        )

        async def dmstatus_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'dmstatus': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = dmstatus_callback

        # Region

        self.region = []
        if 'region' in self.profile:
            self.region.extend(self.profile['region'])

        self.add_item(discord.ui.Select(
            placeholder="Choose your region...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="North America", default='North America' in self.region),
                discord.SelectOption(label="South America", default='South America' in self.region),
                discord.SelectOption(label="Europe", default='Europe' in self.region),
                discord.SelectOption(label="Asia", default='Asia' in self.region),
                discord.SelectOption(label="Oceania", default='Oceania' in self.region),
                discord.SelectOption(label="Africa", default='Africa' in self.region),
                discord.SelectOption(label="Middle East", default='Middle East' in self.region),
            ])
        )

        async def region_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'region': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = region_callback


# Views are only allowed to have a max of 5 rows and thus this second profile SelectMenu is needed
class ProfileSetup2(discord.ui.View):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile

        # Interests

        self.interests = []
        if 'interests' in self.profile:
            self.interests.extend(self.profile['interests'])

        # TODO: Allow users to specify their own majors with a modal (remember to add swear filter regex to this)
        self.add_item(discord.ui.Select(
            placeholder="Choose a role that represents your major or interests...",
            min_values=1,
            max_values=11,
            options=[
                discord.SelectOption(label="Arts", default='Arts' in self.interests),
                discord.SelectOption(label="Business/Economics", default='Business/Economics' in self.interests),
                discord.SelectOption(label="Engineering", default='Engineering' in self.interests),
                discord.SelectOption(label="Humanities", default='Humanities' in self.interests),
                discord.SelectOption(label="Life Science", default='Life Science' in self.interests),
                discord.SelectOption(label="Math", default='Math' in self.interests),
                discord.SelectOption(label="Physical Science", default='Physical Science' in self.interests),
                discord.SelectOption(label="Pre-Professional", default='Pre-Professional' in self.interests),
                discord.SelectOption(label="Social Science", default='Social Science' in self.interests),
                discord.SelectOption(label="Technology", default='Technology' in self.interests),
                discord.SelectOption(label="Other Major", default='Other Major' in self.interests),
                discord.SelectOption(label="Undecided Major", default='Undecided Major' in self.interests),
            ]
        ))

        async def interest_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'interests': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = interest_callback

        # Applicant Type

        self.application_type = []
        if 'application_type' in self.profile:
            self.application_type.extend(self.profile['application_type'])

        self.add_item(discord.ui.Select(
            placeholder="Choose what type of applicant you are...",
            min_values=1,
            max_values=3,
            options=[
                discord.SelectOption(label="International", description="Applying to the US from an other country",
                                     default='International' in self.application_type),
                discord.SelectOption(label="Nontraditional", description="Applying to college in a nontraditional way",
                                     default='Nontraditional' in self.application_type),
                discord.SelectOption(label="Transfer", description="Transferring to a different college",
                                     default='Transfer' in self.application_type),
            ])
        )

        async def application_type_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'application_type': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = application_type_callback

        # Education Type

        self.education_type = []
        if 'education_type' in self.profile:
            self.education_type.extend(self.profile['education_type'])

        self.add_item(discord.ui.Select(
            placeholder="Choose what type of applicant you are...",
            min_values=1,
            max_values=3,
            options=[
                discord.SelectOption(label="Dual Enrollment",
                                     description="Enrolled in both high school and college courses",
                                     default='Dual Enrollment' in self.education_type),
                discord.SelectOption(label="AP", description="Advanced Placement courses from College Board",
                                     default='AP' in self.education_type),
                discord.SelectOption(label="IB", description="International Baccalaureate",
                                     default='IB' in self.education_type),
                discord.SelectOption(label="A Levels",
                                     description="General Certificate of Education (GCE) Advanced Level",
                                     default='A Levels' in self.education_type),
            ])
        )

        async def education_type_callback(interaction: discord.Interaction) -> None:
            Config.db.collection('profiles').document(f'{interaction.user.id}').set(
                {'education_type': list(interaction.data.values())[0]}, merge=True)

        self.children[-1].callback = education_type_callback


async def edit_profile(ctx: discord.ApplicationContext):
    # Check if they are restricted from changing roles
    if 'restrict' in [role.name for role in ctx.author.roles]:
        await ctx.respond(f'You are currently being restricted from changing your profile', ephemeral=True)
        return

    embed = discord.Embed(title='Your Profile', description='Setup/Edit your profile by using the dropdowns')

    # Get profile data from database or set default as dict()
    doc = Config.db.collection('profiles').document(f'{ctx.user.id}').get()
    if doc.exists:
        doc = doc.to_dict()
    else:
        doc = dict()

    await ctx.respond(embed=embed, view=ProfileSetup(doc), ephemeral=True)
    await ctx.respond(view=ProfileSetup2(doc), ephemeral=True)
