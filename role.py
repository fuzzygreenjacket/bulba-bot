# Contains code for the role command(s), which allow users to manipulate roles

import discord
from discord.ext import commands

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # give a role to a user (admin only)
    @commands.command(name='give-role')
    @commands.has_permissions(administrator=True)
    async def give_role(self, ctx, user: commands.MemberConverter, role: commands.RoleConverter):       # converts arguments to correct type
        if role.position >= ctx.guild.me.top_role.position:
                await ctx.send("I do not have the permissions to grant that role.")
                return
        await user.add_roles(role)
        await ctx.send(f"{role.name} has been granted to {user.mention}")

    @give_role.error
    async def give_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions necessary to use this command.")
        else:
            await ctx.send("Error! Make sure you're specifying the user and the role you want to grant to them!")

    # remove a role from a user
    @commands.command(name='remove-role')
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx, user: commands.MemberConverter, role: commands.RoleConverter):     
        if role.position >= ctx.guild.me.top_role.position:
            await ctx.send("I do not have the permissions to grant that role.")
            return
        if role not in user.roles:
            await ctx.send(f"{user.mention} does not have the role {role.name}")
            return
        await user.remove_roles(role)
        await ctx.send(f"{role.name} has been removed from {user.mention}")

    @remove_role.error
    async def remove_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions necessary to use this command.")
        else:
            await ctx.send("Error! Make sure you're specifying the user and the role you want to remove from them!")

async def setup(bot):
    await bot.add_cog(Role(bot))