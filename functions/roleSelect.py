import discord
from discord.ui import Select, View
from discord import Embed, Interaction
from config import *


class GradeLevelSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Select your current grade level...",
                         min_values=1,
                         max_values=1,
                         options=[
                             discord.SelectOption(label="HS Freshman", description="High School Freshman"),
                             discord.SelectOption(label="HS Sophomore", description="High School Sophomore"),
                             discord.SelectOption(label="HS Junior", description="High School Junior"),
                             discord.SelectOption(label="HS Senior", description="High School Senior"),
                             discord.SelectOption(label="Prefrosh",
                                                  description="Highschool Senior "
                                                              "committed who has committed to a college"),
                             discord.SelectOption(label="HS Grad", description="High School Graduate"),
                             discord.SelectOption(label="Gap Year",
                                                  description="Taking a year off from school to pursuit other things"),
                             discord.SelectOption(label="College Freshman", description="College Freshman"),
                             discord.SelectOption(label="College Sophomore", description="College Sophomore"),
                             discord.SelectOption(label="College Junior", description="College Junior"),
                             discord.SelectOption(label="College Senior", description="College Senior"),
                             discord.SelectOption(label="Bachelor's Graduate",
                                                  description="Received a bachelors degree"),
                             discord.SelectOption(label="Graduate Student", description="Currently a Graduate Student"),
                             discord.SelectOption(label="Master's Graduate",
                                                  description="Received a Master's Degree or higher"),
                         ])

    async def callback(self, interaction: Interaction) -> None:
        # interaction.data =
        # {'values': ['he/him'], 'custom_id': '8c40cc1e4dc83ca381eb13ca429cd805', 'component_type': 3}
        # interaction.user
        roles = interaction.user.roles
        grade_level = interaction.data['values'][0]

        await interaction.channel.send("Debug: Role selected")


class PronounSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Select pronouns that apply to you...",
                         min_values=1,
                         max_values=4,
                         options=[
                             discord.SelectOption(label="she/her", value='she_her'),
                             discord.SelectOption(label="he/him", value='he_him'),
                             discord.SelectOption(label="they/them", value='they_them'),
                             discord.SelectOption(label="ask for pronouns", value='ask_for_pronouns',
                                                  description="If you do not use traditional pronouns")
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Pronoun Select {interaction.data}")


class DMStatusSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose your preferred DM Status...",
                         min_values=1,
                         max_values=1,
                         options=[
                             discord.SelectOption(label="Open DMs", description="Anyone is allowed to DM you"),
                             discord.SelectOption(label="Closed DMs",
                                                  description="No one is allowed to DM (if someone violates this "
                                                              "please contact the mods)"),
                             discord.SelectOption(label="Ask to DM",
                                                  description="Users must ask you before beginning direct messages"),
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: DM Status Select")


class OtherBackgroundSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose an option that applies to you...",
                         min_values=0,
                         max_values=4,
                         options=[
                             discord.SelectOption(label="International", description="Not applying from the US"),
                             discord.SelectOption(label="Transfer",
                                                  description="Transfer from one institution to another"),
                             discord.SelectOption(label="Nontraditional",
                                                  description="Not a traditional student such as homeschooled or"
                                                              " online school"),
                             discord.SelectOption(label="Dual Enrollment",
                                                  description="Taking classes at college and highschool"),
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Other Background Select")


class RegionSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose your region...",
                         min_values=1,
                         max_values=1,
                         options=[
                             discord.SelectOption(label="North America"),
                             discord.SelectOption(label="South America"),
                             discord.SelectOption(label="Europe"),
                             discord.SelectOption(label="Asia"),
                             discord.SelectOption(label="Oceania"),
                             discord.SelectOption(label="Africa"),
                             discord.SelectOption(label="Middle East"),
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Region Select")


class MajorSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose a role that represents your major...",
                         min_values=1,
                         max_values=11,
                         options=[
                             discord.SelectOption(label="Arts"),
                             discord.SelectOption(label="Business/Economics"),
                             discord.SelectOption(label="Humanities"),
                             discord.SelectOption(label="Life Sciences"),
                             discord.SelectOption(label="Engineering"),
                             discord.SelectOption(label="Physical Sciences"),
                             discord.SelectOption(label="Pre-Professional"),
                             discord.SelectOption(label="Social Science"),
                             discord.SelectOption(label="Technology"),
                             discord.SelectOption(label="Other Major"),
                             discord.SelectOption(label="Undecided"),
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Major Select")


class ProductivityMuteSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose a role that represents your major...",
                         min_values=0,
                         max_values=1,
                         options=[
                             discord.SelectOption(label="Productivity Mute"),
                             discord.SelectOption(label="Remove Productivity Mute")
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Productivity Mute Select")


class OptInRoleSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Choose some opt-in roles...",
                         min_values=0,
                         max_values=7,
                         options=[
                             discord.SelectOption(label="Announcements",
                                                  description="Receive pings for server announcements"),
                             discord.SelectOption(label="Best of A2C",
                                                  description="Receive pings for weekly posts of the Best of A2C"),
                             discord.SelectOption(label="Positivity Prompts",
                                                  description="Receive pings for positivity in #💖-good-vibes"),
                             discord.SelectOption(label="Events",
                                                  description="Receive pings for events such as the A2C Bakeoff"),
                             discord.SelectOption(label="QOTD",
                                                  description="Receive pings for the Question Of The Day"),
                             discord.SelectOption(label="Archive", description="Receive access to archived channels"),
                             discord.SelectOption(label="Opportunities",
                                                  description="Receive pings for opportunities posted in"
                                                              " #🔭-opportunities"),
                         ])

    async def callback(self, interaction: Interaction):
        await interaction.channel.send(f"Debug: Opt-In Role Select")


async def role_select(ctx: discord.ApplicationContext):

    # Grade Level Select
    embed = Embed(title="Grade Level",
                  description="All roles are based on the American grade level system. Please assign yourself "
                              "based on the American equivalency to your current year in school. You may change"
                              " to the next grade level once your school year has officially ended.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(GradeLevelSelect())

    await ctx.send(embed=embed, view=view)  # TODO: Change send location to roles channel only

    # Pronoun Select
    embed = Embed(title="Pronoun Roles",
                  description="Your pronouns",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(PronounSelect())

    await ctx.send(embed=embed, view=view)

    # DM Status
    embed = Embed(title="DM Status",
                  description="This role reflects whether or not you’re open to receiving direct messages from members "
                              "in this server. It’s a reflection of your preference, not a reflection on if it’s "
                              "possible for a server member to DM you. If someone does not have one of these roles, "
                              "please ask before messaging.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(DMStatusSelect())

    await ctx.send(embed=embed, view=view)

    # Other Background Roles
    embed = Embed(title="Other Backgrounds",
                  description="If other roles did not fit your background.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(OtherBackgroundSelect())

    await ctx.send(embed=embed, view=view)

    # Region Roles
    embed = Embed(title="Region Roles",
                  description="Your Region.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(RegionSelect())

    await ctx.send(embed=embed, view=view)

    # Major Roles
    embed = Embed(title="Major Roles",
                  description="Your Major.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(MajorSelect())

    await ctx.send(embed=embed, view=view)

    # Productivity Mute
    embed = Embed(title="Productivity Mute",
                  description="Once you select the Productivity Mute role, your access will become limited to "
                              "helpful/productive channels such as the app talk channels. Select the “Remove Mute” box "
                              "to regain full access to the server.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(ProductivityMuteSelect())

    await ctx.send(embed=embed, view=view)

    # Opt-In Roles
    embed = Embed(title="Opt-In Roles",
                  description="If you’d like to be pinged when announcements are made for the following topics or have "
                              "access to opt-in channels, select the role in the dropdown with the corresponding name "
                              "receive a role. If you would like to opt-out, select the role in the dropdown again.",
                  color=discord.Color.from_rgb(67, 181, 129))
    view = View(OptInRoleSelect())

    await ctx.send(embed=embed, view=view)
