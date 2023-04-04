import sqlite3

sql = sqlite3.connect('users.db')
cursor = sql.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                    (username TEXT, password TEXT, confirm TEXT)""")

def get_to_users(data_list):
    data = ','.join(data_list)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (data_list[0], data_list[1]))
    sql.commit()

def check_db():
    values = cursor.execute("SELECT * FROM users")
    for value in values:
        print(value)

