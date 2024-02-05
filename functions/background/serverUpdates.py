from discord.ext import tasks
import asyncio
from config import Config
import helper
from datetime import datetime, timezone, timedelta, date

# Setting it to 3/4 of a day and then waiting to not go off-sync
# probably not necessary to do this step

'''spence fix this stuff the datetime isn't working right now'''
'''for the time being i put in a stopgap solution to the datetime issue'''
# @tasks.loop(next_iteration=datetime.time(hour=0, minute=0, second=0, tzinfo=timezone(offset=-timedelta(hours=4.0),
# name='ET')))


@tasks.loop(seconds=64800)
async def updateDateCount():
    # now = datetime.now()
    # seconds = (23-now.hour)*3600 + (59-now.minute)*60 + (60-now.second)
    # await asyncio.sleep(seconds)
    dec192020 = datetime(2020, 12, 19)
    today = datetime.now()
    days = (today - dec192020).days
    await Config.ChannelIDs.days_old_channel.edit(name=f"{days} days old")


async def launchTasks():
    while not helper.bot_ready:
        await asyncio.sleep(2)
    updateDateCount.start()

helper.loop.create_task(launchTasks())
