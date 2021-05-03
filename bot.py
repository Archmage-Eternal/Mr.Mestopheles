import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import signal
from game import win_check

from db_manage import (
        open_db_connection,
        open_all_db_connections,
        create_and_populate_default_table,
        create_table_trigger,
        create_trigger,
        close_all_db_connections,
        db_add_member,
        db_remove_member,
        delete_db, get_wallet_money, update_wallet_money, get_bank_money, deposit_bank_money, withdraw_bank_money, get_leaderboard,
        guild_dbs,
        TABLE,
    )

### Setup
# Load environment variables.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set intent and prefix for bot commands.
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# To close all sqlite3 connections on ctrl+c and also exit
# works only for linux platform
def signal_handler():
    close_all_db_connections()
    exit(0)

# Create the database/ folder to store all .db files
os.makedirs('databases', exist_ok=True)

### For setting up databases and managing them on events
@bot.event
async def on_ready():
    print('Ready')
    open_all_db_connections(bot.guilds)
    if sys.platform == 'linux':
        bot.loop.add_signal_handler(signal.SIGINT, signal_handler)

@bot.event
async def on_guild_join(guild):
    # create a new .db file on joining a new guild (should we delete if bot is rejoining?)
    open_db_connection(guild)
    create_and_populate_default_table(guild)
    create_table_trigger(guild)
    create_trigger(guild)

@bot.event
async def on_member_join(member):
    db_add_member(member)

@bot.event
async def on_member_remove(member):
    print(member.id, bot.user.id)
    # if removed member is the bot itself, then delete guild
    # database
    if member.id == bot.user.id:
        delete_db(member.guild)
    else:
        db_remove_member(member)


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



@bot.command(name='roulette', help='Allows you to bet on roulette. Takes 2 arguments, bet amount and type')
async def roulette(ctx, bet_amount = -1, bet_type = ''):
    bets_payout = {'dozen':2,'color':1,'even_odd':1,'column':2,'high_low':1,'single_num':35}

    if bet_type == '':
        print('You forgot to give the type of bet, genius.')
        return 
        
    # todo: check current wallet balance. 
    current_wallet_balance = get_wallet_money(ctx.author)
    if current_wallet_balance < bet_amount:
        await ctx.send('You don\'t have that much money right now.')
        return
    
    result, payout_type, win_flag =  win_check(bet_amount, bet_type) 
    if win_flag:
        # todo: add amount to wallet database entry.
        update_wallet_money(ctx.author, bet_amount * bets_payout[payout_type])
        await ctx.send(f'The result is {result}.\nCongratulations, you have won. The payout is 1:{bets_payout[payout_type] + 1}.')
    else:
        # todo: remove amount from wallet database entry.
        print(ctx.author, ctx.guild)
        update_wallet_money(ctx.author, -bet_amount)
        await ctx.send(f'The result is {result}.\nSorry you lost.')


@bot.command(name='deposit', help='Allows you to deposit money into the bank.')
async def deposit(ctx,amount = -1):
    if amount == -1:
        await ctx.send('Please enter the amount you want to deposit, or type all to deposit all the money.')
    deposit_bank_money(ctx.author, amount)
    wallet_balance = get_wallet_money(ctx.author)
    bank_balance = get_bank_money(ctx.author)
    await ctx.send(f'The transfer has been completed.\nWallet Balance: {wallet_balance}\nBank Balance: {bank_balance}')

    


@bot.command(name='withdraw', help='Allows you to withdraw money from the bank.')
async def withdraw(ctx, amount = -1):
    if amount == -1:
        await ctx.send('Please enter the amount you want to withdraw, or type all to withdraw all the money.')
    withdraw_bank_money(ctx.author, amount)
    wallet_balance = get_wallet_money(ctx.author)
    bank_balance = get_bank_money(ctx.author)
    await ctx.send(f'The transfer has been completed.\nWallet Balance: {wallet_balance}\nBank Balance: {bank_balance}')
    

@bot.command(name='leaderboard', help='Displays the leaderboard for the server.')
async def print_leaderboard(ctx):
    members = get_leaderboard(ctx.guild)
    output = 'Leaderboard\n'
    for index, row in enumerate(members):
        member = bot.get_user(row[0])
        output += f'{index+1}. {member.name}\t{row[1] + row[2]}\n'
    await ctx.send('```\n' + output + '\n```')


@bot.command(name='money', help='Displays the wallet and bank money for the user.')
async def print_money(ctx):
    bank = str(get_bank_money(ctx.author))
    wallet = str(get_wallet_money(ctx.author))
    await ctx.send('```\nBank : ' + bank + '\nWallet : ' + wallet + '\n```')


bot.run(TOKEN)
