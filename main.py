import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

# Ustawia instancję Intents, aby umożliwić botowi reagowanie na określone zdarzenia Discorda
intents = discord.Intents.default()
intents.all()
intents.message_content = True

# Wczytuje zmienne środowiskowe z pliku .env
load_dotenv()

# Tworzy instancję bota z prefiksem komend '!' i przekazuje Intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Zdarzenie on_ready - wywołuje się, gdy bot jest gotowy do użycia
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    # Zmienia nazwę bota na 'JEJ'
    await bot.user.edit(username='JEJ')

# Zdarzenie on_message - wywołuje się, gdy jest odbierana nowa wiadomość na serwerze Discord
@bot.event
async def on_message(message):
    # Pobiera dane z wiadomości
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    # Wyświetla informacje o wiadomości w konsoli
    print(f'Message {user_message} by {username} on {channel}')

    # Sprawdza, czy wiadomość została wysłana przez bota, i wtedy kończy funkcję
    if message.author == bot.user:
        return

    # Obsługuje komendy na kanale o nazwie 'random'
    if channel == "random":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            jokes = ["1", "2", "3", "4"]
            await message.channel.send(random.choice(jokes))
        elif "spadaj" in user_message.lower():
            await message.channel.send(f'Ty też spadaj, {username}!')
        elif user_message.lower().startswith('!changeservername'):
            await bot.process_commands(message)
        elif user_message.lower() == '!join':
            # Komenda !join - dołącza do kanału głosowego o nazwie 'General'
            await join_general_channel(message)
        elif user_message.lower() == '!leave':
            # Komenda !leave - odłącza się od kanału głosowego
            await leave_general_channel(message)
        elif user_message.lower() == '!ma':
            # Komenda !ma - wycisza wszystkich na kanale głosowym
            await mute_all_users(message)
        elif user_message.lower() == '!uma':
            # Komenda !uma - odcisza wszystkich na kanale głosowym
            await unmute_all_users(message)

    # Przetwarza inne komendy
    await bot.process_commands(message)

# Komenda !changeservername - zmienia nazwę serwera
@bot.command(name='changeservername', help='Change the server name')
async def change_server_name(ctx, new_name):
    print('Command received!')
    try:
        print(f'Attempting to change server name to {new_name}')

        # Sprawdza, czy bot ma uprawnienia do zarządzania serwerem
        if ctx.guild.me.guild_permissions.manage_guild:
            await ctx.guild.edit(name=new_name)  # Zmienia nazwę serwera.
            print(f'Success! Server name changed to {new_name}')
            await ctx.send(f'Server name changed to {new_name}')  # Wysyła wiadomość potwierdzającą zmianę nazwy serwera.
        else:
            print('Bot does not have the "Manage Server" permission.')
            await ctx.send('Bot does not have the "Manage Server" permission.')  # Informuje o braku uprawnień do zarządzania serwerem.
    except discord.errors.Forbidden:
        print('Changing server name forbidden. Make sure the bot has "Manage Server" permission.')
        await ctx.send('Changing server name forbidden. Make sure the bot has "Manage Server" permission.')  # Informuje o zakazie zmiany nazwy serwera.
    except discord.errors.HTTPException as e:
        print(f'An error occurred: {e}')
        await ctx.send(f'An error occurred while changing the server name: {e}. Please check the bot\'s permissions.')  # Informuje o wystąpieniu błędu HTTP.

# Komenda !join - dołącza do kanału głosowego o nazwie 'General'
@bot.command(name='join', help='Join the voice channel')
async def join_voice_channel(ctx):
    await join_general_channel(ctx)

# Komenda !leave - odłącza się od kanału głosowego
@bot.command(name='leave', help='Leave the voice channel')
async def leave_voice_channel(ctx):
    await leave_general_channel(ctx)

# Komenda !ma - wycisza wszystkich na kanale głosowym
@bot.command(name='ma', help='Mute all users on the voice channel')
async def mute_all_users(ctx):
    await mute_all_users_on_channel(ctx)

# Komenda !uma - odcisza wszystkich na kanale głosowym
@bot.command(name='uma', help='Unmute all users on the voice channel')
async def unmute_all_users(ctx):
    await unmute_all_users_on_channel(ctx)

async def join_general_channel(ctx):
    channel_name = "General"
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)

    if channel:
        voice_channel = await channel.connect()
        await ctx.send(f'Joined the voice channel: {channel_name}')
    else:
        await ctx.send(f'Voice channel {channel_name} not found.')

async def leave_general_channel(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_channel:
        await voice_channel.disconnect()
        await ctx.send('Left the voice channel')
    else:
        await ctx.send('Not currently in a voice channel.')

async def mute_all_users_on_channel(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_channel:
        for member in voice_channel.channel.members:
            await member.edit(mute=True)
        await ctx.send('Muted all users on the voice channel')
    else:
        await ctx.send('Bot is not currently in a voice channel.')

async def unmute_all_users_on_channel(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_channel:
        for member in voice_channel.channel.members:
            await member.edit(mute=False)
        await ctx.send('Unmuted all users on the voice channel')
    else:
        await ctx.send('Bot is not currently in a voice channel.')

# Uruchamia bota przy użyciu przypisanego tokena
token = os.getenv('TOKEN')  # Pobiera token bota zmienną środowiskową.
bot.run(token)  # Uruchamia bota.
