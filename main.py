import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

# Create an instance of Intents
intents = discord.Intents.default()
intents.all()
intents.message_content = True
load_dotenv()

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to print a message when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    # Change bot username
    await bot.user.edit(username='JEJ')

@bot.event
async def on_message(message): 
    username = str(message.author).split("#")[0] 
    channel = str(message.channel.name) 
    user_message = str(message.content) 

    print(f'Message {user_message} by {username} on {channel}') 

    if message.author == bot.user: 
        return

    if channel == "random": 
        if user_message.lower() == "hello" or user_message.lower() == "hi": 
            await message.channel.send(f'Hello {username}') 
            return
        elif user_message.lower() == "bye": 
            await message.channel.send(f'Bye {username}') 
            return
        elif user_message.lower() == "tell me a joke": 
            jokes = ["1", "2", "3", "4"] 
            await message.channel.send(random.choice(jokes))
            return
        elif "spadaj" in user_message.lower():
            await message.channel.send(f'Ty tez spadaj, {username}!')
            return
        elif user_message.lower().startswith('!changeservername'):
            await bot.process_commands(message)
            return

    await bot.process_commands(message)

# Command to greet the user
@bot.command(name='changeservername', help='Change the server name')
async def change_server_name(ctx, new_name):
    print('Command received!')
    try:
        print(f'Attempting to change server name to {new_name}')
        if ctx.guild.me.guild_permissions.manage_guild:
            await ctx.guild.edit(name=new_name)
            print(f'Success! Server name changed to {new_name}')
            await ctx.send(f'Server name changed to {new_name}')
        else:
            print('Bot does not have the "Manage Server" permission.')
            await ctx.send('Bot does not have the "Manage Server" permission.')
    except discord.errors.Forbidden:
        print('Changing server name forbidden. Make sure the bot has "Manage Server" permission.')
        await ctx.send('Changing server name forbidden. Make sure the bot has "Manage Server" permission.')
    except discord.errors.HTTPException as e:
        print(f'An error occurred: {e}')
        await ctx.send(f'An error occurred while changing the server name: {e}. Please check the bot\'s permissions.')

# Run the bot with your bot token
token = os.getenv('TOKEN')
bot.run(token)
