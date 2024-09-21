# Contains code for the dice command(s), which allow users to roll dice

import discord
import random
from discord.ext import commands

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Roll x dice, each with y sides
    @commands.command(name='roll')
    async def roll(self, ctx, num_dice: int, num_sides: int):
        response = 0
        for i in range(num_dice):
            response += random.randint(1, num_sides)
        await ctx.send(response)
    
    @roll.error
    async def roll_error(self, ctx, error):
        await ctx.send("Error! Make sure you are specifying both the number of dice and the number of sides (i.e. `-roll 2 6`).")

async def setup(bot):
    await bot.add_cog(Roll(bot))