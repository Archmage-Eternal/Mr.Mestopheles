import discord
from discord.ext import commands
import random

@bot.command(name='roulette', help='Allows you to bet on roulette.')
async def roulette(ctx, bet_amount: int, bet_type:str):
    roulette_table = {'00':'g',0:'g',1:'r',2:'b',3:'r',4:'b',5:'r',6:'b',7:'r',
            8:'b',9:'r',10:'b',11:'b',12:'r',13:'b',14:'r',15:'b',16:'r',
            17:'b',18:'r',19:'r',20:'b',21:'r',22:'b',23:'r',24:'b',25:'r',
            26:'b',27:'r',28:'b',29:'b',30:'r',31:'b',32:'r',33:'b',34:'r',
            35:'b',36:'r'}

    bet_types = {'first dozen':range(1,13),'second dozen':range(13,25),'third dozen':range(25,37),
        'red':'r','black':'b','even':'even','odd':'odd',
        'first column':[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        'second column':[2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        'third column':[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        'high':range(19,37),'low':range(1,19),
        'single_num':list(roulette_table.keys())}

    bets_payout = {'dozen':2,'color':1,'even_odd':1,'column':2,'high_low':1,'single_num':36}
    #dbms operations
    # ! Not implemented.

    result = random.choice(list(roulette_table.keys()))
    colour = roulette_table[result]

    # ! Incomplete.
    if bet_type.isnumeric():
        if int(bet_type) == result:
            print(f"payout is {bets_payout['single_num']} for a single number.")
        else:
            print(f'The result is {result}. Sorry you lose.')
    elif 'column' in bet_type:
        if result in bet_types[bet_type]:
            print(f"payout is {bets_payout['column']} for {bet_type}.")
    elif 'dozen' in bet_type:
        if result in bet_types[bet_type]:
            print(f"payout is {bets_payout['dozen']} for {bet_type}.")
    elif bet_type in 'high low':
        if result in bet_types[bet_type]:
            print(f"payout is {bets_payout['high_low']} for {bet_type}.")
    elif bet_type in 'red black':
        if bet_types[bet_type] == roulette_table[result]:
            print(f"payout is {bets_payout['color']} for {bet_type}.")
    elif result % 2 == 0 and bet_type == 'even':
        print(f"payout is {bets_payout['even_odd']} for {bet_type}.")
    elif result % 2 != 0 and bet_type == 'odd':
        print(f"payout is {bets_payout['even_odd']} for {bet_type}.")
    else:
        print(f'The result is {result}. Sorry you lose.')
    
    
    print(str(result), bet_type)