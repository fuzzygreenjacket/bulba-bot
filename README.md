# Bulba Bot

Bulba Bot is a discord bot developed by Matt (Discord Username Bulbasaur2023) for various purposes, including general server upkeep, game playing, and other miscallaneous tasks. Bulba Bot uses the "-" prefix and all commands are case sensitive. If you have any questions or would like to add the bot to your server, feel free to DM me for inquiries!

## Current Commands

Channel Commands:  
```-create-channel [NAME] [CATEGORY]```: Create a channel. You have the option to specify the channel name and channel category respectively, using quotes to separate them. Channels created with this command are defaulted to private.  
```-num-channels```: Retrieve the total number of channels in the server  

Dice Roll Commands:  
```-roll [NUM_DICE] [NUM_SIDES]```: Roll NUM_DICE dice with NUM_SIDES each and sum the result  

Role Commands:  
```-give-role [USER] [ROLE]```: Give a role to a user. You must specify the user and the role in that order.  
```-remove-role [USER] [ROLE]```: Remove a role from a user. You must specify the user and the role in that order. 

Wordle Commands  
```-wordle```: Begin a game of wordle. Words are guessed by enclosing them in brackets, like ```[apple]```.  

## Admin-Only Commands
The following commands are admin-only:  
```-create-channel```  
```-give-role```  
```-remove-role```  

Credits:  
[RealPython](https://realpython.com/how-to-make-a-discord-bot-python/) for the skeleton code and setup instructions  
[Scholtes](https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d) for the Wordle dictionary  