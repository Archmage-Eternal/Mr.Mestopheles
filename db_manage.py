import sqlite3

# This dictionary store all the sqlite3 connections for each
# guild the bot joins
guild_dbs = {}

# creates .db file for a single guild. If a .db file already exists, then that
# file is used, else new one is created.  The new connection is then added to
# the guild_dbs dictionary
def open_db_connection(guild_id): 
    guild_id = str(guild_id)    # convert to string
    conn = sqlite3.connect('databases/' + guild_id + '.db')
    guild_dbs[guild_id] = conn  # Add the connection to the dictionary

def open_all_db_connections(guilds):
    for guild in guilds:
        open_db_connection(guild.id)

def close_all_db_connections():
    print("called")
    for id, guild_conn in guild_dbs.items():
        guild_conn.close()
        print("sqlite3 connection closed for guild id", id)
