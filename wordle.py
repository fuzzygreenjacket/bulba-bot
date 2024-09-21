import discord
import random
from discord.ext import commands

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot