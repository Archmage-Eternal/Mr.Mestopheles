import discord
from discord.ext import commands
import random
from db_manage import get_wallet_money, update_wallet_money, get_bank_money, deposit_bank_money, withdraw_bank_money, get_leaderboard
def win_check(bet_amount, bet_type):
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

    result = random.choice(list(roulette_table.keys()))
    print('Result is', result)

    if result == '00' and bet_type == '00':
        return result, 'single_num', True
    elif bet_type.isnumeric():
        if int(bet_type) == result:
            return result, 'single_num', True
    elif 'column' in bet_type:
        if result in bet_types[bet_type]:
            return result, 'column', True
    elif 'dozen' in bet_type:
        if result in bet_types[bet_type]:
            return result, 'dozen', True 
    elif bet_type in 'high low':
        if result in bet_types[bet_type]:
            return result, 'high_low', True
    elif bet_type in 'red black':
        if bet_types[bet_type] == roulette_table[result]:
            return result, 'color', True 
    elif result % 2 == 0 and bet_type == 'even':
        return result, 'even_odd', True 
    elif result % 2 != 0 and bet_type == 'odd':
        return result, 'even_odd', True 

    return result, '', False
