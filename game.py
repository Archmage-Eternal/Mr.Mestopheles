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

    bet_types = {'first_dozen':range(1,13),'second_dozen':range(13,25),'third_dozen':range(25,37),
        'red':'r','black':'b','even':'even','odd':'odd',
        'first_column':[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
        'second_column':[2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
        'third_column':[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        'high':range(19,37),'low':range(1,19),
        'single_num':list(roulette_table.keys())}

    bets_payout = {'dozen':2,'color':1,'even_odd':1,'column':2,'high_low':1,'single_num':36}
    #dbms operations
    # ! Not implemented.

    result = random.randint(1, 36)

    # ! Incomplete.
    if result == space:
        pass
    elif space == :
        pass
    elif space == :
        pass
    elif space == :
        pass
    elif result % 2 != 0 and space.lower() == 'odd':
        pass
    elif result % 2 == 0 and space.lower() == 'even':
        pass
    elif result in color_red and space.lower() == 'red':
        pass
    elif result in color_black and space.lower() == 'black':
        pass