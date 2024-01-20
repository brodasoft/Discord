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

# Command to greet the user
@bot.command(name='hello', help='Greet the user')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

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
        elif user_message.lower() == "tell me a joke": 
            jokes = ["1","2","3","4"] 
            await message.channel.send(random.choice(jokes)) 

# Run the bot with your bot token
token = os.getenv('TOKEN')
bot.run(token)
