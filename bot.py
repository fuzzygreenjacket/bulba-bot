# bot.py
import os
import random
import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='-')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='roll')
async def roll(ctx, num_dice: int, num_sides: int):
    response = 0
    for i in range(num_dice):
        response += random.randint(1, num_sides)
    await ctx.send(response)

@roll.error
async def roll_error(ctx, error):
    await ctx.send("Error! Make sure you are specifying both the number of dice and the number of sides (i.e. `-roll 2 6`).")

@bot.command(name='give-role')
@commands.has_permissions(administrator=True)
async def give_role(ctx, user: commands.MemberConverter, role: commands.RoleConverter):
    if role.position >= ctx.guild.me.top_role.position:
            await ctx.send("I do not have the permissions to grant that role.")
            return
    await user.add_roles(role)
    await ctx.send(f"{role.name} has been granted to {user.mention}")

@give_role.error
async def give_role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions necessary to use this command.")
    else:
        await ctx.send("Error! Make sure you're specifying the user and the role you want to grant to them!")
    

bot.run(TOKEN)