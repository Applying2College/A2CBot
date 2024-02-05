import os
import discord
from discord.ui import Button, View
from dotenv import load_dotenv
import aiohttp
import json
from config import *

load_dotenv()


"""
Query the NCES database for information about colleges. Search for a college with the "search" command, which
will return a list of colleges. Each college is assigned a CollegeButton that when pressed give info about that
college. 
Information includes: 
    Name, 
    Alias, 
    Icon, 
    Location, 
    Undergraduate Enrollment,
    Graduation Rate,
    Tuition Cost,
    Average Net Price,
    Application Price(TBA),
    Application Deadline(TBA),
    SAT Scores w/Percentiles,
    Net Price Calculator Link
"""


def url_corrector(url: str):  # the urlparser() from urllib.parse doesn't work and is replaced with this functions
    url = url.replace(' ', '%20')
    scheme = ''
    if len(url.split('://')) > 1:
        scheme, url = url.split('://')
    if scheme != 'https' and scheme != 'http':
        scheme = 'https'
    return '://'.join([scheme, url])


# Check to make sure queried data exists
def score_check(bottom, mid, top):
    if bottom and mid and top:
        return f"{bottom}/{mid}/{top}"
    return 'N/A'


# Check to make sure queried data exists
def add_score_check(bottom_math, mid_math, top_math, bottom_reading, mid_reading, top_reading):
    if bottom_math and mid_math and top_math and bottom_reading and mid_reading and top_reading:
        return f"{bottom_reading + bottom_math}/{mid_reading + mid_math}/{top_reading + top_math}"
    return 'N/A'


# Check to make sure queried data exists
def cost_check(cost):
    if cost:
        return f"${cost}"
    return 'N/A'


class CollegeButton(Button):
    def __init__(self, label, college_id):
        super().__init__(label=label)
        self.college_id = college_id
        self.label = label

    # Called when button is pressed
    async def callback(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:  # Get college specific data
            async with session.get(f'https://api.data.gov/ed/collegescorecard/v1/schools/?'
                                   f'api_key={os.getenv("COLLEGE_LOOKUP_KEY")}&'
                                   f'id={self.college_id}') as response:
                data = await response.json()

        # Title
        embed = discord.Embed(title=data['results'][0]['latest']['school']['name'],
                              description=f"Other names: {str(data['results'][0]['latest']['school']['alias']).replace('|', ', ')}")

        # Thumbnail
        embed.set_thumbnail(url=f"https://t1.gstatic.com/faviconV2?"
                                f"client=SOCIAL&"
                                f"type=FAVICON&"
                                f"fallback_opts=TYPE,SIZE,URL&"
                                f"url={url_corrector(data['results'][0]['latest']['school']['school_url'])}&"
                                f"size=128")

        # Location
        embed.add_field(name="Location",
                        value=f"{data['results'][0]['latest']['school']['city']}, "
                              f"{data['results'][0]['latest']['school']['state']}",
                        inline=False)

        # Undergraduate Enrollment
        embed.add_field(name="Undergraduate Enrollment",
                        value=data['results'][0]['latest']['student']['size'],
                        inline=False)

        # Graduation Rate
        embed.add_field(name="Graduation Rate",
                        value=f"{str(round(data['results'][0]['latest']['completion']['completion_rate_4yr_100nt'] * 100, 2)) + '%' if data['results'][0]['latest']['completion']['completion_rate_4yr_100nt'] else 'N/A'}",
                        inline=False)

        # Tuition Cost
        embed.add_field(name="Tuition Cost",
                        value=f"Tuition (In State): {cost_check(data['results'][0]['latest']['cost']['tuition']['in_state'])} \n"
                              f"Tuition (Out of State): {cost_check(data['results'][0]['latest']['cost']['tuition']['out_of_state'])} \n"
                              f"Room & Board: {cost_check(data['results'][0]['latest']['cost']['roomboard']['oncampus'])} \n"
                              f"Cost of Books and Supplies: {cost_check(data['results'][0]['latest']['cost']['booksupply'])} \n",
                        inline=False)

        # Average Net Price
        embed.add_field(name="Average Net Cost",
                        value=f"Tuition (In State): {cost_check(data['results'][0]['latest']['cost']['avg_net_price']['overall'])}",
                        inline=False)

        # Application Fee
        embed.add_field(name="Application Fee",
                        value=f"-",
                        inline=False)

        # Application Deadline
        embed.add_field(name="Application Deadline",
                        value=f"-",
                        inline=False)

        # Cleaning/Clarifying data
        math_score = [
            data['results'][0]['latest']['admissions']['sat_scores']['25th_percentile']['math'],
            data['results'][0]['latest']['admissions']['sat_scores']['midpoint']['math'],
            data['results'][0]['latest']['admissions']['sat_scores']['75th_percentile']['math']
        ]
        reading_score = [
            data['results'][0]['latest']['admissions']['sat_scores']['25th_percentile']['critical_reading'],
            data['results'][0]['latest']['admissions']['sat_scores']['midpoint']['critical_reading'],
            data['results'][0]['latest']['admissions']['sat_scores']['75th_percentile']['critical_reading']
        ]

        # SAT Range
        embed.add_field(name="SAT Scores 25th/50th/75th",
                        value=f"Math Range: {score_check(math_score[0], math_score[1], math_score[2])}\n"
                              f"Reading Range: {score_check(reading_score[0], reading_score[1], reading_score[2])}\n"
                              f"Total Range: {add_score_check(math_score[0], math_score[1], math_score[2], reading_score[0], reading_score[1], reading_score[2])}",
                        inline=False)

        print(url_corrector(data['results'][0]['latest']['school']['price_calculator_url']))

        # Net Price Calculator Link Button
        view = View()
        button = Button(label="Net Price Calculator",
                        url=url_corrector(data['results'][0]['latest']['school']['price_calculator_url']))
        view.add_item(button)

        await interaction.channel.send(embed=embed, view=view)


async def search(ctx: discord.ApplicationContext, college: str) -> None:
    await ctx.respond("Searching for colleges. This may take a moment...")

    async with aiohttp.ClientSession() as session:  # Search for colleges with NCES api
        async with session.get(f'https://api.data.gov/ed/collegescorecard/v1/schools?'
                               f'api_key={os.getenv("COLLEGE_LOOKUP_KEY")}&'
                               f'fields=id,school.name,school.alias,school.search&per_page=10&'
                               f'sort=school.alias:asc&'
                               f'school.search=${college}&'
                               f'school.operating=1&'
                               f'latest.student.size__range=1..&'
                               f'latest.academics.program_available.assoc_or_bachelors_or_certificate=true&'
                               f'school.degrees_awarded.predominant__range=1..3') as response:
            data = await response.json()

    view = View()
    for i, school in enumerate(data['results']):  # Add buttons to view from search results
        view.add_item(CollegeButton(school['school.name'][:77] + '...', school['id']) if len(school['school.name']) > 80 else CollegeButton(school['school.name'], school['id']))

    embed = discord.Embed(title="Search Results",
                          description=f"{len(data['results'])} result{'s' if len(data['results']) > 1 else ''} found")
    await ctx.respond(embed=embed, view=view)
