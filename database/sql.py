import sqlite3
import config

sql = sqlite3.connect(config.db_path, check_same_thread=False)
db = sql.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS users(
           id INTEGER PRIMARY KEY, 
           count INTEGER,
           status TEXT
)''')
sql.commit()

table_name = config.table_name

def add_to_db(id: int, count=0, status="user"):
    db.execute(f"INSERT OR IGNORE INTO {table_name} (id, count, status) VALUES (?, ?, ?)", (id, count, status))
    sql.commit()

def select_from_db(id: int, obj: str):
    add_to_db(id)
    
    db.execute(f"SELECT {obj} FROM {table_name} WHERE id = ?", (id,))   
    value = db.fetchone()[0]

    return value

def update_in_db(id: int, obj: str, value: str):
    add_to_db(id)

    db.execute(f"UPDATE {table_name} SET {obj} = ? WHERE id = ?", (value, id))
    sql.commit() 