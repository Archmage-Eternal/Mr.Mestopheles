import sqlite3
import os

# This dictionary store all the sqlite3 connections for each
# guild the bot joins
guild_dbs = {}

TABLE = "server_economy"

# creates .db file for a single guild. If a .db file already exists, then that
# file is used, else new one is created.  The new connection is then added to
# the guild_dbs dictionary
def open_db_connection(guild): 
    guild_id = guild.id
    conn = sqlite3.connect('databases/' + str(guild_id) + '.db')
    guild_dbs[guild_id] = conn  # Add the connection to the dictionary

def open_all_db_connections(guilds):
    for guild in guilds:
        open_db_connection(guild)

def close_all_db_connections():
    for id, guild_conn in guild_dbs.items():
        guild_conn.close()
        print("sqlite3 connection closed for guild id", id)

# creates a new table and populates the default value of each field for every
# member in guild
def create_and_populate_default_table(guild):
    guild_id = guild.id
    conn = guild_dbs[guild_id]
    conn.execute(f'''create table {TABLE} (id int primary key not null,
    wallet real,
    bank_balance real);''')

    for member in guild.members:
        if member.bot == True:  #skip bots
            continue

        member_id = member.id
        values = (member_id, 0, 100)
        conn.execute(f"insert into {TABLE} values(?,?,?)", values)

    conn.commit()

# adds a single member to table with default values
def db_add_member(member):
    if member.bot == True:
        return

    guild_id = member.guild.id
    conn = guild_dbs[guild_id]

    values = (member.id, 0, 100)
    conn.execute(f"insert into {TABLE} values(?,?,?)", values)
    conn.commit()

def db_remove_member(member):
    if member.bot == True:
        return

    guild_id = member.guild.id
    conn = guild_dbs[guild_id]

    conn.execute(f"delete from {TABLE} where id = {member.id}")
    conn.commit()

def delete_db(guild):
    guild_id = guild.id
    conn = guild_dbs[guild_id]
    conn.close()
    os.remove("databases/"+str(guild_id)+".db")
    guild_dbs.pop(guild_id)

# returns the wallet money of the member
def get_wallet_money(member):
    guild_id = member.guild.id
    conn = guild_dbs[guild_id]

    row = conn.execute(f"select wallet from {TABLE} where id = {member.id}").fetchone()
    return row[0]

# returns the bank money of the member
def get_bank_money(member):
    guild_id = member.guild.id
    conn = guild_dbs[guild_id]

    row = conn.execute(f"select bank_balance from {TABLE} where id = {member.id}").fetchone()
    return row[0]

# returns a list of tuples. Each tuple being one record/row.
def get_leaderboard(guild):
    guild_id = guild.id
    conn = guild_dbs[guild_id]

    cur = conn.execute(f'''select * from {TABLE}
    order by (wallet + bank_balance) desc;''');
    rows =  cur.fetchall()
    return rows

def update_wallet_money(member, amount):
    guild_id = member.guild.id
    conn = guild_dbs[guild_id]

    conn.execute(f'''update {TABLE} set wallet = wallet + {amount}
    where id = {member.id};''')
    conn.commit()

def deposit_bank_money(member, amount):
    guild_id = member.guild.id
    conn = guild_dbs[guild_id]
    
    # deduct the money from wallet first
    conn.execute(f'''update {TABLE}
    set wallet = wallet - {amount},
    bank_balance = bank_balance + {amount}
    where id = {member.id};''')

    conn.commit()
    
def withdraw_bank_money(member, amount):
    guild_id = member.guild.id
    conn = guild_dbs[guild_id]
    
    # deduct the money from wallet first
    conn.execute(f'''update {TABLE}
    set wallet = wallet + {amount},
    bank_balance = bank_balance - {amount}
    where id = {member.id};''')

    conn.commit()
