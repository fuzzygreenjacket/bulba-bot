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
    
@bot.command(name='create-channel')
@commands.has_permissions(administrator=True)
async def create_channel(ctx, channel_name = 'new-channel', channel_category = None):
    if channel_category:
        channel_category = channel_category.title()
    temp_channel_category = channel_category # store name of channel_category in case it is overwritten later
    existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True) # type: ignore
    }
    if channel_category:
        channel_category = discord.utils.get(ctx.guild.categories, name=channel_category)
        if not channel_category:
            await ctx.send(f"The category \"**{temp_channel_category}**\" does not exist! If the category is multiple words, use quotation marks to denote it!")
            return  
    await ctx.guild.create_text_channel(channel_name, overwrites=overwrites, category=channel_category)
    if not existing_channel:
        await ctx.send(f"Channel with name \"**{channel_name}**\" successfully created.")
    else:
        await ctx.send(f"Channel with name \"**{channel_name}**\" successfully created. Warning: a channel with this name already exists.")
    
@create_channel.error
async def create_channel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions necessary to use this command.")
    else:
        await ctx.send("An error has occurred!")

@bot.command(name='num-channels')
@commands.has_permissions(administrator=True)
async def num_channels(ctx):
    await ctx.send(f"{len(ctx.guild.text_channels)} text channels")
    await ctx.send(f"{len(ctx.guild.voice_channels)} voice channels")
    await ctx.send(f"{len(ctx.guild.channels)} channels including categories")

@num_channels.error
async def num_channels_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions necessary to use this command.")
    else:
        await ctx.send("An error has occurred!")  


bot.run(TOKEN)