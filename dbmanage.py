import sqlite3
from pathlib import Path

init_statements = [ 
    '''CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            pass TEXT NOT NULL 
        );''',

    '''CREATE TABLE IF NOT EXISTS reqVals (
            id INTEGER PRIMARY KEY, 
            salt BINARY(16) NOT NULL, 
            hash BINARY(32) NOT NULL
        );'''
]

def init_database():
    
    file_path = Path("secure.db")
    file_path.touch(exist_ok=False) #if the DB exists this should not be called.

    #create place to store passwords and associated account reasons
    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            for obj in init_statements:
                cursor.execute(obj)
            
            conn.commit()
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()

    #create a place to store the salt and key hash

    return True

def get_salt():

    salt = ""

    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            
            cursor.execute('''SELECT * FROM reqVals''')

            row = cursor.fetchone()
            salt = row[1]
            

            
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()

    return salt

def get_passhash():
    hash = ""

    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            
            cursor.execute('''SELECT * FROM reqVals''')

            row = cursor.fetchone()
            hash = row[2]

            
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()

    return hash

def get_passwordtable():
    table = []

    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            
            cursor.execute('''SELECT * FROM passwords''')

            rows = cursor.fetchall()
            table = rows

            conn.commit()
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()

    return table

def set_salt_hash(salt: bytes, hash: bytes):
    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            
            sql = '''INSERT INTO reqVals(salt, hash)
                     VALUES(?, ?) '''

            cursor.execute(sql, (salt, hash))

            conn.commit()
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()
    
    return


def add_password(name, password):
    try:
        with sqlite3.connect("secure.db") as conn:
            # interact with database
            cursor = conn.cursor()
            
            sql = '''INSERT INTO passwords(name, pass)
                     VALUES(?, ?) '''
            
            cursor.execute(sql, (name, password))

            conn.commit()
            
            pass
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
    finally:
        conn.close()

    return
