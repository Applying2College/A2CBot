import re
import discord
from config import Config
from firebase_admin import firestore

funny_phrase = ['{user} suddenly feels a _deep_ need to thwack people...',
                '{user} is gonna give y\'all a wack\'in',
                '{user} _will_ find and {user} _will_ bonk you']


async def bonk(ctx: discord.ApplicationContext, user: discord.Member) -> None:
    # Get command data from firebase
    doc = Config.db.collection('commands').document(f'{ctx.author.id}')
    info = doc.get()

    # Check if author has been given bonk charges
    if not info.exists or 'bonk' not in info.to_dict():
        await ctx.respond(f'You have not been bestowed with the powers of bonk. Only staff '
                          f'may judge you worthy of wielding this.', ephemeral=True)
        return

    # Check how many bonk charges the author has
    charges = info.to_dict()['bonk']
    if charges <= 0:
        await ctx.respond(f'You have run out of charges on your bonk command. Only staff '
                          f'may judge you as worthy of more.', ephemeral=True)
        return

    # Exhaust one (1) bonk
    doc.update({'bonk': firestore.firestore.Increment(-1)})

    # Fire away
    await ctx.send(f'Bonked **{user}**')

    # Give user info about remaining bonks
    await ctx.respond(f'You have **{charges - 1}** bonk remaining', ephemeral=True)


async def give_bonk(ctx: discord.ApplicationContext, user: discord.Member, charges: int) -> None:
    # Check if charges is a valid int
    try:
        charges = int(charges)
    except TypeError:
        await ctx.respond(f'Invalid amount of charges', ephemeral=True)
        return

    # Add bonk charges to firebase
    Config.db.collection('commands').document(f'{user.id}').set({'bonk': firestore.firestore.Increment(charges)},
                                                                merge=True)

    # Give feedback about given bonks
    await ctx.respond(f'Gave **{user}** a total of **{charges}** bonks', ephemeral=True)

    # Notify that the user that they've been given bonks
    await ctx.send(f'<@!{user.id}> suddenly feels a _deep_ need to thwack people...')


async def send_bonk(ctx: discord.ApplicationContext, user: discord.Member, charges: int) -> None:
    # Check if charges is a valid int
    try:
        charges = int(charges)
    except TypeError:
        await ctx.respond(f'Invalid amount of charges', ephemeral=True)
        return
    # Get bonk info from firebase
    doc = Config.db.collection('commands').document(f'{ctx.author.id}')
    info = doc.get()

    # Check if author has been given bonk charges
    if not info.exists or 'bonk' not in info.to_dict():
        await ctx.respond(f'You have not been bestowed with the powers of bonk. Only staff '
                          f'may judge you worthy of wielding this.', ephemeral=True)
        return

    # Check how many bonk charges the author has
    author_charges = info.to_dict()['bonk']
    # Baseline check for trolling. We cant have ppl stealing bonks
    if charges == 0:
        await ctx.respond(f'LMAO 0 bonks? Peasant.', ephemeral=True)
        return
    if charges < 0:
        await ctx.respond(f'You cannot give negative charges, Nice Try. :troll:', ephemeral=True)
        return
    # Checks to make sure they have enough
    if author_charges < charges:
        await ctx.respond(f'You do not have enough charges.', ephemeral=True)
        return

    # Move bonk charges to firebase
    Config.db.collection('commands').document(f'{user.id}').set({'bonk': firestore.firestore.Increment(charges)},
                                                                merge=True)
    Config.db.collection('commands').document(f'{ctx.author.id}').set({'bonk': firestore.firestore.Increment(-charges)},
                                                                      merge=True)
    # Give feedback about given bonks
    await ctx.respond(f'You gave **{user}** a total **{charges}** of your bonks', ephemeral=True)

    # Notify that the user that they've been given bonks
    await ctx.send(f'**{user}** has been given **{charges}** bonks from **{ctx.author}**')


async def yoink(ctx: discord.ApplicationContext, user: discord.Member) -> None:
    # Remove all bonks from author
    Config.db.collection('commands').document(f'{user.id}').set({'bonk': 0}, merge=True)

    # Give feedback to author about removing bonk perms
    await ctx.respond(f'Removed bonk permissions from **{user}**', ephemeral=True)

    # Notify the user that their bonks have been revoked
    await ctx.send(f'<@!{user.id}> your bonk permissions have been revoked')


async def check_bonk(ctx: discord.ApplicationContext, user: discord.Member) -> None:
    # Get bonk info from firebase
    doc = Config.db.collection('commands').document(f'{user.id}')
    info = doc.get()

    # Check if author has been given bonk charges
    if not info.exists or 'bonk' not in info.to_dict():
        await ctx.respond(f'**{user}** has not been given charges', ephemeral=True)
        return

    # Check how many bonk charges the author has
    charges = info.to_dict()['bonk']
    await ctx.respond(f'**{user}** has **{charges}** bonk remaining', ephemeral=True)


async def remind_bonk(ctx: discord.ApplicationContext) -> None:
    # Get bonk info from firebase
    doc = Config.db.collection('commands').document(f'{ctx.author.id}')
    info = doc.get()

    # Check if author has been given bonk charges
    if not info.exists or 'bonk' not in info.to_dict():
        await ctx.respond(f'You have not been bestowed with the powers of bonk. Only staff '
                          f'may judge you worthy of wielding this.', ephemeral=True)
        return

    # Check how many bonk charges the author has
    charges = info.to_dict()['bonk']

    await ctx.respond(f'You have **{charges}** bonk', ephemeral=True)
