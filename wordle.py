import discord
import random
from discord.ext import commands

letter_to_emoji = {
    'a': ':regional_indicator_a:', 'b': ':regional_indicator_b:', 
    'c': ':regional_indicator_c:', 'd': ':regional_indicator_d:',
    'e': ':regional_indicator_e:', 'f': ':regional_indicator_f:', 
    'g': ':regional_indicator_g:', 'h': ':regional_indicator_h:',
    'i': ':regional_indicator_i:', 'j': ':regional_indicator_j:', 
    'k': ':regional_indicator_k:', 'l': ':regional_indicator_l:',
    'm': ':regional_indicator_m:', 'n': ':regional_indicator_n:', 
    'o': ':regional_indicator_o:', 'p': ':regional_indicator_p:',
    'q': ':regional_indicator_q:', 'r': ':regional_indicator_r:', 
    's': ':regional_indicator_s:', 't': ':regional_indicator_t:',
    'u': ':regional_indicator_u:', 'v': ':regional_indicator_v:', 
    'w': ':regional_indicator_w:', 'x': ':regional_indicator_x:',
    'y': ':regional_indicator_y:', 'z': ':regional_indicator_z:'
}

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    # check whether a guess is valid
    def valid_word(self, word):
        with open("wordle_files/wordle-Ta.txt", 'r') as f:
            content = f.read()
            if word in content:
                return True
            else:
                return False
            
    # given a letter instance tracker and a letter, either add 1 to the number of instances or set it to 1 if it's not
    # in the tracker already
    def update_tracker(self, letter, tracker):
        if letter not in tracker:
            tracker[letter] = 1
        else:
            tracker[letter] += 1
    
    # given a list of letters, remove all letters that are in a certain word
    def remove_letters(self, letters, word):
        for letter in word:
            if letter in letters:
                letters.remove(letter)
    
    @commands.command(name='wordle')
    async def wordle(self, ctx):
        if ctx.channel.id in self.active_games:  # Check if a game is already active in this channel
            await ctx.send("Game already in progress in this channel! Send `[cancel]` to reset.")
            return
        self.active_games[ctx.channel.id] = True  # Set the game as active

        with open('wordle_files/wordle-La.txt') as f:
            lines = f.read().splitlines()
        word = random.choice(lines)     # choose random word from database
        total_guesses = 0
        unguessed_letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
            'y', 'z'
        ]

        await ctx.send("Word selected! Send your guess enclosed in brackets and with no dash at the start, e.g. `[apple]`. Do `[cancel]` to end the game.")
        
        while True:
            def check(msg):
                return msg.channel == ctx.channel   # make sure message is sent in the same channel
            try:
                msg = await self.bot.wait_for("message", check=check, timeout = 120)
                if msg.content.lower() == "[cancel]":    # game is canceled
                    await ctx.send(f"Game cancelled! The word was {word}.")
                    del self.active_games[ctx.channel.id]
                    return
                if len(msg.content) < 2 or msg.content[0] != '[' or msg.content[-1] != "]":      # message is not a guess
                    pass
                elif len(msg.content[1:-1]) != 5:     # guess is wrong length
                    await ctx.send("Your guess must be five letters long!")
                elif not self.valid_word(msg.content[1:-1].lower()):
                    await ctx.send("That is not a valid word. Try again!")
                else:
                    total_guesses += 1
                    guess = msg.content[1:-1].lower()
                    squares = ["X", "X", "X", "X", "X"]
                    word_letter_instances = {}      # hash map of each letter in word and how often they show up
                    guess_letter_instances = {}     # hash map of each letter in guess and how often they show up
                    for i in range(5):
                        self.update_tracker(word[i], word_letter_instances)
                    print(word_letter_instances)
                    for i in range(5):
                        if guess[i] == word[i]:
                            squares[i] = "🟩"
                            self.update_tracker(guess[i], guess_letter_instances)
                    for i in range(5):
                        if guess[i] != word[i] and guess[i] in word:
                            self.update_tracker(guess[i], guess_letter_instances)
                            print(guess_letter_instances)
                            if guess_letter_instances[guess[i]] <= word_letter_instances[guess[i]]:
                                squares[i] = "🟨"
                    print(squares)
                    print(guess_letter_instances)
                    for i in range(5):
                        if squares[i] == "X":
                            squares[i] = "⬛"
                    result = ''.join(squares)
                    emoji_guess = ""
                    for i in range(5):
                        emoji_guess += letter_to_emoji[guess[i]]
                    self.remove_letters(unguessed_letters, guess)
                    unguessed_letters_str = ""
                    for letter in unguessed_letters:
                        unguessed_letters_str += letter_to_emoji[letter]
                    if result == "🟩🟩🟩🟩🟩":
                        await ctx.send(f"{result}")
                        await ctx.send(f"{emoji_guess}")
                        await ctx.send(f"Unguessed Letters: {unguessed_letters_str}")
                        await ctx.send(f"Congrats! You correctly guessed the word in {total_guesses} guesses")
                        del self.active_games[ctx.channel.id]
                        return
                    else:
                        await ctx.send(f"{result}")
                        await ctx.send(f"{emoji_guess}")
                        await ctx.send(f"Unguessed Letters: {unguessed_letters_str}")
                        await ctx.send(f"That was guess number {total_guesses}")
                        if total_guesses == 6:
                            await ctx.send(f"All guesses used! The word was {word}")
                            del self.active_games[ctx.channel.id]
                            return
            except TimeoutError:
                await ctx.send("You took too long to respond!")
                del self.active_games[ctx.channel.id]
                return

async def setup(bot):
    await bot.add_cog(Wordle(bot))