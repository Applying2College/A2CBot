import discord
from config import Config
from firebase_admin import firestore
import requests
import json

MINECRAFT_UUID_BASE = "https://api.mojang.com/users/profiles/minecraft/"

async def whitelist_user(ctx: discord.ApplicationContext, mc_username: str) -> None:
    user_id = requests.get(MINECRAFT_UUID_BASE+mc_username).content
    mc_username_exists =  Config.db.collection('minecraft').document(f'{ctx.author.id}').get()
    if not user_id:
        await ctx.respond("Sorry, that Minecraft username does not exist. Please try again", ephemeral=True)
        return
    elif mc_username_exists.exists and mc_username_exists.to_dict()['mc_username'] == mc_username:
         await ctx.respond("You may only whitelist one Minecraft username per Discord account. Please remove the other one using `/removeminecraft` first", ephemeral=True)
         return
    else:
        user_id = json.loads(user_id)
        user_id_final = {"name":user_id['name'],"uuid":user_id['id']}
        if Config.Minecraft_Server_Path.prod:
            with open(Config.Minecraft_Server_Path.prod_path, 'r') as f:
                whitelist = json.load(f)
                for k in whitelist:
                    if k['uuid'] == user_id['id']:
                        await ctx.respond("That user is already whitelisted", ephemeral=True)
                        return
            whitelist.append(user_id_final)
            with open(Config.Minecraft_Server_Path.prod_path, 'w') as f:
                json.dump(whitelist, f)
            Config.db.collection('minecraft').document(f'{ctx.author.id}').set({"mc_username":mc_username})
            await ctx.respond("Successfully whitelisted user", ephemeral=True)
        else:
            #print("Not in production, added "+user_id+" to whitelist")
            await ctx.respond("Successfully whitelisted user", ephemeral=True)
async def remove_minecraft_user(ctx: discord.ApplicationContext) -> None:
    mc_username_exists =  Config.db.collection('minecraft').document(f'{ctx.author.id}').get()
    if not mc_username_exists.exists :
        await ctx.respond("You are not whitelisted", ephemeral=True)
        return
    else:
        user_id = requests.get(MINECRAFT_UUID_BASE+mc_username_exists.to_dict()['mc_username']).content
        user_id = json.loads(user_id)
        user_id_final = {"name":user_id['name'],"uuid":user_id['id']}
        if Config.Minecraft_Server_Path.prod:
            with open(Config.Minecraft_Server_Path.prod_path, 'r') as f:
                whitelist = json.load(f)
                for k in whitelist:
                    if k['uuid'] == user_id['id']:
                        whitelist.remove(k)
                        with open(Config.Minecraft_Server_Path.prod_path, 'w') as f:
                            json.dump(whitelist, f)
                        Config.db.collection('minecraft').document(f'{ctx.author.id}').delete()
                        await ctx.respond("Successfully removed user", ephemeral=True)
                        return
        else:
            #print("Not in production, removed "+user_id+" from whitelist")
            await ctx.respond("Successfully removed user", ephemeral=True)
