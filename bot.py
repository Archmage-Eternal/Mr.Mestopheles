# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import signal

from db_manage import close_all_db_connections, open_db_connection, open_all_db_connections, guild_dbs

### Setup
# Load environment variables.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Set prefix for bot commands.
bot = commands.Bot(command_prefix='!')

# To close all sqlite3 connections on ctrl+c and also exit
def signal_handler():
    close_all_db_connections()
    exit(0)

# Create the database/ folder to store all .db files
os.makedirs('databases', exist_ok=True)

### For setting up databases
@bot.event
async def on_ready():
    open_all_db_connections(bot.guilds)
    print(guild_dbs)
    bot.loop.add_signal_handler(signal.SIGINT, signal_handler)

@bot.event
async def on_guild_join(guild):
    # create a new .db file on joining a new guild (should we delete if bot is rejoining?)
    open_db_connection(guild.id)


### Managerial Functions.
@bot.command(name='silence', help='Mutes everyone in the current voice channel.')
async def vcmute(ctx):
    '''
    A function to mute all users present in the current voice channel.
    Args:
        ctx (Discord): Gives the current context of the channel from which the function is called.
    '''
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)


@bot.command(name='break-silence', help='Unmutes everyone in the current voice channel.')
async def vcunmute(ctx):
    '''
    A function to unmute all server muted users in a voice channel.
    Args:
        ctx (Discord): Gives the current context of the channel from which the function is called.
    '''
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)


# Simple Fun/Utility Functions.

@bot.command(name='flip-coin', help='Simulates flipping a coin.')
async def flip_coin(ctx):
    '''
    A function to simulate the tossing of a coin.
    Args:
        ctx (Discord): Gives the current context of the channel from which the function is called.
    '''
    await ctx.send(random.choice(('Head\'s', 'Tail\'s')))


@bot.command(name='roll-dice', help='Simulates rolling dice, for a given number of dice and sides.')
async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
    '''
    A function to simulate the rolling of dice give the number of sides and the number of dice.
    Args:
        ctx (Discord): Gives the current context of the channel from which the function is called.
        number_of_dice (Integer): Gives the number of dice to be rolled.
        number_of_sides (Inreger): Gives the number of sides for the dice to be rolled.
    '''
    dice = [str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)]
    await ctx.send(', '.join(dice))


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99.')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    await ctx.send(random.choice(brooklyn_99_quotes))


@bot.command(name='8ball', help='A magic 8 ball.')
async def eight_ball(ctx, question = ''):
    '''
    A function to simulate a Magic 8 ball. It has 10 positive, 5 negative and 5 neutral.

    Args:
        ctx (Discord): Gives the current context of the channel from which the function is called.
    '''
    if question == '':
        await ctx.send('Enter a question dumbass.')
        return None

    eight_ball_responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.',
                            'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
                            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                            'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                            'Cannot predict now.', 'Concentrate and ask again.', 'Don\'t count on it.',
                            'My reply is no.', 'My sources say no.', 'Outlook not so good.',
                            'Very doubtful.']
    await ctx.send(random.choice(eight_ball_responses))
    if question[-1] != '?':
        await ctx.send('Also, you forgot the question mark, genius.')
bot.run(TOKEN)
