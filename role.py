import discord
from discord.ext import commands

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='give-role')
    @commands.has_permissions(administrator=True)
    async def give_role(self, ctx, user: commands.MemberConverter, role: commands.RoleConverter):
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

async def setup(bot):
    await bot.add_cog(Role(bot))