import sqlite3
import config

sql = sqlite3.connect(config.db_path, check_same_thread=False)
db = sql.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS users(
           id INTEGER PRIMARY KEY, 
           count INTEGER,
           status TEXT,
           reason TEXT
)''')
db.execute('''CREATE TABLE IF NOT EXISTS roles(
           id INTEGER PRIMARY KEY,
           price INTEGER,
           name TEXT
)''')
sql.commit()

table_name = config.table_name

def add_to_db(id: int, count=0, status="user", reason=None):
    db.execute(f"INSERT OR IGNORE INTO {table_name} (id, count, status, reason) VALUES (?, ?, ?, ?)", (id, count, status, reason))
    sql.commit()

def select_from_db(id: int, obj: str):
    add_to_db(id)
    
    db.execute(f"SELECT {obj} FROM {table_name} WHERE id = ?", (id,))   
    value = db.fetchone()[0]

    return value


def select_ban_list():
    db.execute(f"SELECT id FROM users WHERE status = 'ban'")   
    value = db.fetchall()

    return value

def select_all_from_db(table: str):
    db.execute(f"SELECT * FROM {table}")   
    value = db.fetchall()

    return value

def update_in_db(id: int, obj: str, value: str):
    add_to_db(id)

    db.execute(f"UPDATE {table_name} SET {obj} = ? WHERE id = ?", (value, id))
    sql.commit() 