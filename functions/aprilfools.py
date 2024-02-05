import random
import shelve
import discord
from config import Config
import aiofiles


async def get_colleges():
    print("in get_college")
    async with aiofiles.open("college.txt") as f:
        print('Opened file')
        return await f.readlines()


async def name_bomb(ctx: discord.ApplicationContext):
    db = shelve.open('usernames.db')

    progress = await ctx.send("Changing names")
    print("setup db")

    colleges = await get_colleges()
    print(colleges)

    members: list[discord.Member] = Config.guild.members
    print(members)
    for count, member in enumerate(members):
        new_name = f"{random.choice(colleges)} - {random.randint(0, 101)}%"
        old_name = member.display_name
        userID = member.id
        print(new_name, old_name, userID)
        if count % 100 == 0:
            try:
                await progress.edit(content=f"Changed {count} of {len(members)}")
            except Exception as e:
                await ctx.send(f"Failed to edit progress message: {e}")
                pass
        try:
            await member.edit(nick=new_name)
            db[f'{count}'] = {'userID': userID, 'old_name': old_name}
        except Exception as e:
            await ctx.send(f"Failed to rename {userID} to {new_name}")
            print(e)
    await progress.edit(content="Renamed users")
    await ctx.respond("Changed names")


async def change_back(ctx: discord.ApplicationContext):
    db = shelve.open('usernames.db')

    progress = await ctx.send("Changing names")

    db_list = list(db.items())
    print(db_list)

    for count, item in db_list:
        print(count)
        if int(count) % 100 == 0:
            await progress.edit(content=f"Changed {count} of {len(db)}")
        try:
            await Config.guild.get_member(int(item['userID'])).edit(nick=item['old_name'])
        except Exception as e:
            await ctx.send(f"Failed to rename {item['userID']} to {item['old_name']}")
            print(e)
    await ctx.respond("Changed names")
