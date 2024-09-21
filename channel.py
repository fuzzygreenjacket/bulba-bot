# Contains code for the channel command(s), which allow users to manipulate channels

import discord
from discord.ext import commands

class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Create a channel. You can optionally specify the name of the channel and the category it should be under.
    # Permissions are set to private
    @commands.command(name='create-channel')
    @commands.has_permissions(administrator=True)
    async def create_channel(self, ctx, channel_name = 'new-channel', channel_category = None):
        if channel_category:
            channel_category = channel_category.title()     # set channel category to title case
        temp_channel_category = channel_category # store name of channel_category in case it is overwritten later
        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True) # type: ignore
        }
        if channel_category:
            channel_category = discord.utils.get(ctx.guild.categories, name=channel_category)
            if not channel_category:    # make sure the name of the channel_category actually exists
                await ctx.send(f"The category \"**{temp_channel_category}**\" does not exist! If the category is multiple words, use quotation marks to denote it!")
                return  
        await ctx.guild.create_text_channel(channel_name, overwrites=overwrites, category=channel_category)
        if not existing_channel:
            await ctx.send(f"Channel with name \"**{channel_name}**\" successfully created.")
        else:
            await ctx.send(f"Channel with name \"**{channel_name}**\" successfully created. Warning: a channel with this name already exists.")
        
    @create_channel.error
    async def create_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions necessary to use this command.")
        else:
            await ctx.send("An error has occurred!")

    # Get the number of channels in a server
    @commands.command(name='num-channels')
    @commands.has_permissions(administrator=True)
    async def num_channels(self, ctx):
        await ctx.send(f"{len(ctx.guild.text_channels)} text channels")
        await ctx.send(f"{len(ctx.guild.voice_channels)} voice channels")
        await ctx.send(f"{len(ctx.guild.channels)} channels including categories")

    @num_channels.error
    async def num_channels_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions necessary to use this command.")
        else:
            await ctx.send("An error has occurred!")  

async def setup(bot):
    await bot.add_cog(Channel(bot))